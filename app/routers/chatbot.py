import os
import json
import re
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError
from groq import Groq
from app.database import get_db, engine

# Initialize Router
router = APIRouter(
    prefix="/api/chatbot",
    tags=["Chatbot"]
)

# --- Configuration & Constants ---
# Using GROQ_API_KEY which exists in main .env project
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant" # Lighter model to avoid Rate Limits

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = [] # [{"role": "user", "content": "..."}, ...]

class ChatResponse(BaseModel):
    response_markdown: str
    sql_query: Optional[str] = None
    data_source: str = "BD" # BD or WEB
    suggested_questions: List[str] = []
    chart_data: Optional[Dict[str, Any]] = None

# --- Helper: Schema Loading ---
def get_schema_summary():
    """
    Returns a comprehensive string representation of the ENTIRE database schema.
    Automatically discovers ALL tables and columns.
    """
    try:
        inspector = inspect(engine)
        schema_text = "=== COMPLETE DATABASE SCHEMA ===\n\n"
        
        # Get all tables
        all_tables = inspector.get_table_names()
        
        # Categorize tables
        main_tables = [t for t in all_tables if 'licitacion' in t.lower() or 'contrato' in t.lower() or 'consorcio' in t.lower()]
        other_tables = [t for t in all_tables if t not in main_tables and not t.startswith('etl_') and not t.startswith('audit_') and not t.startswith('chat_')]
        
        # Document main tables in detail
        schema_text += "MAIN TABLES (most important):\n"
        for table_name in main_tables:
            columns = inspector.get_columns(table_name)
            col_strs = [f"{col['name']} ({col['type']})" for col in columns[:15]]  # Limit cols to prevent overflow
            schema_text += f"\n{table_name}:\n"
            schema_text += f"  Columns: {', '.join(col_strs)}\n"
            if len(columns) > 15:
                schema_text += f"  ... and {len(columns) - 15} more columns\n"
        
        # Add explicit relationship documentation
        schema_text += "\n\nTABLE RELATIONSHIPS (JOIN KEYS):\n"
        schema_text += "- licitaciones_cabecera ↔ licitaciones_adjudicaciones\n"
        schema_text += "  JOIN ON: id_convocatoria\n"
        schema_text += "  USE CASE: Get guarantees/retention with location/category info\n"
        schema_text += "  EXAMPLE: SELECT COUNT(*) FROM licitaciones_adjudicaciones a JOIN licitaciones_cabecera c ON a.id_convocatoria=c.id_convocatoria WHERE c.departamento='LIMA' AND a.tipo_garantia LIKE '%RETENCION%'\n\n"
        
        schema_text += "- contratos ↔ detalle_consorcios\n"
        schema_text += "  JOIN ON: id_contrato\n"
        schema_text += "  USE CASE: Get consortium details for contracts\n\n"
        
        # List other tables briefly
        if other_tables:
            schema_text += f"OTHER TABLES: {', '.join(other_tables)}\n"
        
        return schema_text
    except Exception as e:
        return f"Error loading schema: {e}"

# --- Core Service Logic ---

class ChatService:
    def __init__(self, db_session):
        self.db = db_session
        self.schema_context = get_schema_summary()

    def _sanitize_sql(self, sql: str) -> str:
        """
        Ensures strict READ-ONLY policy.
        """
        sql = sql.strip().strip(';').replace("```sql", "").replace("```", "").strip()
        
        forbidden_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", 
            "CREATE", "GRANT", "REVOKE", "EXECUTE"
        ]
        
        upper_sql = sql.upper()
        for kw in forbidden_keywords:
            if kw in upper_sql:
                raise ValueError(f"Security Alert: Operation {kw} is not allowed. Read-only access.")
        
        return sql

    def _execute_sql(self, sql: str) -> List[Dict[str, Any]]:
        """
        Executes the SQL query and returns results as a list of dicts.
        """
        try:
            result = self.db.execute(text(sql))
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]
        except SQLAlchemyError as e:
            raise ValueError(f"SQL Execution Failed: {str(e)}")

    def _truncate_history(self, history: List[Dict], max_chars: int = 1000) -> List[Dict]:
        """
        Truncates long message content in history to prevent context overflow.
        """
        truncated = []
        for msg in history:
            content = msg.get("content", "")
            if len(content) > max_chars:
                content = content[:max_chars] + "...[truncated]"
            truncated.append({"role": msg["role"], "content": content})
        return truncated

    def _generate_chart_data(self, query_results: List[Dict], sql_query: str) -> Optional[Dict[str, Any]]:
        """
        Detects if query results are suitable for charting and generates chart data.
        """
        if not query_results or len(query_results) < 2:
            return None
        
        # Check if query has GROUP BY or aggregation (simple heuristic)
        sql_upper = sql_query.upper()
        has_grouping = 'GROUP BY' in sql_upper or 'COUNT(' in sql_upper
        
        if not has_grouping:
            return None
        
        # Extract first two columns (label + value)
        first_row = query_results[0]
        keys = list(first_row.keys())
        
        if len(keys) < 2:
            return None
        
        label_key = keys[0]  # First column (e.g., departamento, categoria)
        value_key = keys[1]  # Second column (e.g., COUNT)
        
        # Extract labels and values
        labels = []
        values = []
        
        for row in query_results[:10]:  # Limit to top 10 for readability
            label = str(row[label_key]) if row[label_key] else 'N/A'
            value = row[value_key]
            
            # Try to convert to number
            try:
                value = float(value) if value else 0
            except:
                continue
            
            labels.append(label)
            values.append(value)
        
        if not labels or not values:
            return None
        
        # Determine chart type
        chart_type = "bar"  # Default
        if len(labels) <= 6:
            chart_type = "pie"  # Pie for small datasets
        
        return {
            "type": chart_type,
            "labels": labels,
            "datasets": [{
                "label": value_key,
                "data": values
            }]
        }


    def _generate_sql(self, user_message: str, history: List[Dict]) -> str:
        """
        Generates SQL using the LLM with strict security and accuracy rules.
        """
        # Define allowed and sensitive tables
        allowed_tables = [
            "licitaciones_cabecera",
            "licitaciones_adjudicaciones", 
            "detalle_consorcios",
            "contratos"
        ]
        
        sensitive_tables = [
            "chat_history",
            "chatbot_analytics",
            "audit_logs",
            "control_cargas",
            "etl_consorcios_log",
            "etl_execution_log"
        ]
        
        allowed_tables_str = ", ".join(allowed_tables)
        sensitive_tables_str = ", ".join(sensitive_tables)
        
        system_prompt = f"""You are AURA, an expert MySQL Database Assistant.
Goal: Generate ONE safe, READ-ONLY MySQL query that answers the user using ONLY the provided schema.

OUTPUT (STRICT):
- Return ONLY the raw SQL query. No markdown, no explanations, no backticks.
- If not related to DB, return exactly: NO_SQL
- If the question needs a missing required filter/identifier, return exactly:
  CLARIFY: <one short question in Spanish>

SECURITY (STRICT):
1) Only SELECT or WITH are allowed.
2) Single statement only. Do NOT include ';' anywhere.
3) No SQL comments ('--', '/*', '*/').
4) You MUST use only tables from this allowlist:
{allowed_tables_str}
5) Sensitive tables exist and should NOT be used unless the user explicitly asks and it is necessary:
{sensitive_tables_str}
(If the user asks for sensitive data, return CLARIFY asking for authorization scope.)

DATABASE SCHEMA (authoritative):
{self.schema_context}

JOIN RULES (CRITICAL FOR ACCURACY):
- Only join tables if you can see matching key columns in the schema above.
- Prefer joins on identifiers:
  - id_convocatoria (between licitaciones_cabecera and licitaciones_adjudicaciones)
  - id_contrato (between contratos and detalle_consorcios)
  - ocid
- Only use equality joins: t1.key = t2.key
- Never guess join keys or columns not shown in the schema.
- If a join is needed but the join key is not clear from schema, return:
  CLARIFY: ¿Con qué campo se relacionan estas tablas? (por ejemplo id_convocatoria, ocid, id_contrato)

LOCATION HINTS:
- Major cities (Lima, Arequipa, Cusco, Trujillo, etc.) → check departamento first
- Smaller cities/districts (Tarapoto, Chiclayo, Iquitos, etc.) → check distrito or provincia
- If user says a city name, try: departamento LIKE '%NAME%' OR provincia LIKE '%NAME%' OR distrito LIKE '%NAME%'
- Examples:
  - "Tarapoto" → distrito = 'TARAPOTO' (41 records)
  - "Lima" → departamento = 'LIMA' (most common)

QUERY QUALITY:
- Prefer explicit column list; avoid SELECT *.
- COUNT queries: use COUNT(*) AS total and DO NOT add LIMIT.
- For listing/detail queries: add ORDER BY (date column if available) and LIMIT 10.
- If user has typos in filters, use LIKE '%...%' on text columns.

MULTI-TURN CONTEXT:
- If the user refines previous question (e.g. "y en Huánuco?"), keep previous filters and add the new one.

Now generate the SQL for the user request."""

        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Context: Add truncated history (last 3 messages)
        safe_history = self._truncate_history(history)[-3:]
        messages.extend(safe_history)
        messages.append({"role": "user", "content": f"Generate SQL for: {user_message}"})

        response = client.chat.completions.create(
            messages=messages,
            model=MODEL_NAME,
            temperature=0.1, 
        )
        
        return response.choices[0].message.content.strip()

    def _generate_final_response(self, user_message: str, sql_query: str, query_results: List[Dict], error: str = None) -> Any: # Returns Tuple[str, List[str]]
        """
        Generates the friendly Markdown response AND 3 context-aware follow-up questions.
        """
        data_summary = json.dumps(query_results, default=str) if query_results else "No results found."
        
        # DEBUG: Log data passed to LLM
        print(f"[DEBUG] Passing {len(query_results)} results to LLM (JSON length: {len(data_summary)} chars)")

        # Dynamic Prompting based on data complexity
        is_single_value = False
        if len(query_results) == 1 and len(query_results[0]) == 1:
            is_single_value = True

        if is_single_value:
            # ULTRA-STRICT PROMPT FOR SIMPLE ANSWERS
            actual_value = str(list(query_results[0].values())[0]) if query_results else "0"
            
            system_prompt = f"""You are AURA.
The user asked: "{user_message}"
Database returned EXACTLY this value: {actual_value}

CRITICAL INSTRUCTION:
1. Output ONLY ONE sentence using THE EXACT NUMBER: {actual_value}
2. Example: "Hay {actual_value} licitaciones en estado contratado."
3. DO NOT change the number. DO NOT invent data. USE: {actual_value}
4. Add "///Suggested///" at the end with 3 follow-up questions."""
        else:
            # PROMPT FOR LISTS/RECORDS - STRICT ANTI-HALLUCINATION
            system_prompt = f"""You are AURA, a database assistant.

User Question: "{user_message}"

Database Query Results (JSON):
{data_summary}

CRITICAL RULES - READ CAREFULLY:
1. **USE ONLY THE DATA PROVIDED ABOVE**. DO NOT invent, imagine, or add ANY data from your training.
2. **FORBIDDEN**: Do NOT use country names, department names, or ANY data not in the JSON results.
3. **IF** the JSON shows data, create a Markdown table with EXACTLY those values.
4. **Start** with a brief intro sentence (e.g. "Aquí tienes la distribución...").
5. **Table Format**: 2 columns - First column = category/name, Second column = count/value
6. **Ensure** Spanish grammar correctness.
7. **Suggestions**: End with "///Suggested///" followed by 3 follow-up questions.

EXAMPLE (if JSON has dept data):
"Aquí tienes el conteo de licitaciones por departamento:

| Departamento | Número de Licitaciones |
|--------------|------------------------|
| LIMA | 3168 |
| ... | ... |

///Suggested///
- Ver detalle de Lima
- Comparar con otros años
- Filtrar por estado"

REMEMBER: Use ONLY the JSON data above. No hallucinations.
"""
        messages = [{"role": "system", "content": system_prompt}]
        
        response = client.chat.completions.create(
            messages=messages,
            model=MODEL_NAME,
            temperature=0.3, 
        )
        
        full_content = response.choices[0].message.content.strip()
        
        # Split response and suggestions
        parts = full_content.split("///Suggested///")
        main_response = parts[0].strip()
        suggestions = []
        if len(parts) > 1:
            raw_suggestions = parts[1].strip().split('\n')
            suggestions = [s.strip().replace('- ', '').replace('* ', '') for s in raw_suggestions if s.strip()]
            
        return main_response, suggestions[:3]

    def _generate_general_response(self, user_message: str, history: List[Dict]) -> str:
        """
        Handles general conversation without SQL.
        """
        system_prompt = """You are AURA, an intelligent, helpful, and professional Assistant and Co-pilot.
The user asked something that does not require a database query.
Answer helpfuly. If you need external information, mention that you assume it based on general knowledge "(Fuente: Web/General)".
"""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history[-4:])
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            messages=messages,
            model=MODEL_NAME,
            temperature=0.7,
        )
        return response.choices[0].message.content


    def process_message(self, request: ChatRequest) -> ChatResponse:
        try:
            # 1. Analyze intent & Generate SQL
            generated_sql_or_flag = self._generate_sql(request.message, request.history)
            
            # 2a. If CLARIFY, ask user for more info
            if generated_sql_or_flag.startswith("CLARIFY:"):
                clarification_question = generated_sql_or_flag.replace("CLARIFY:", "").strip()
                return ChatResponse(
                    response_markdown=clarification_question,
                    data_source="BD",
                    suggested_questions=[]
                )
            
            # 2b. If NO_SQL, act as general chatbot
            if "NO_SQL" in generated_sql_or_flag:
                response_text = self._generate_general_response(request.message, request.history)
                return ChatResponse(response_markdown=response_text, data_source="WEB")

            # 3. If valid SQL, Execute Strict
            sql_query = generated_sql_or_flag
            query_results = []
            error_msg = None
            
            # DEBUG: Log SQL
            print(f"\n[DEBUG] Generated SQL: {sql_query}\n")
            
            try:
                cleaned_sql = self._sanitize_sql(sql_query)
                query_results = self._execute_sql(cleaned_sql)
                
                # DEBUG: Log result count
                print(f"[DEBUG] Query returned {len(query_results)} rows")
                if query_results:
                    print(f"[DEBUG] First row: {query_results[0]}")
                    if len(query_results) > 1:
                        print(f"[DEBUG] Last row: {query_results[-1]}")
                    
                    # Special logging for single value results (COUNT etc.)
                    if len(query_results) == 1 and len(query_results[0]) == 1:
                        actual_value = list(query_results[0].values())[0]
                        print(f"[DEBUG] ⚠️ SINGLE VALUE RESULT: {actual_value}")
                
            except Exception as e:
                error_msg = str(e)
                print(f"[DEBUG] SQL Error: {error_msg}")
            
            # 4. Generate Final Answer
            final_answer, suggestions = self._generate_final_response(request.message, sql_query, query_results, error_msg)
            
            # 5. Generate Chart Data (if applicable)
            chart_data = self._generate_chart_data(query_results, sql_query) if query_results else None
            
            return ChatResponse(
                response_markdown=final_answer,
                sql_query=sql_query,
                data_source="BD",
                suggested_questions=suggestions,
                chart_data=chart_data
            )
        except Exception as e:
            # Fallback for critical errors (API failures, etc)
            print(f"CRITICAL ERROR: {e}")
            return ChatResponse(
                response_markdown=f"⚠️ **Error del Sistema**: {str(e)}\n\nPor favor intenta de nuevo más tarde.",
                data_source="ERROR"
            )

# --- Routes ---

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db=Depends(get_db)):
    """
    Main Chat Endpoint.
    Analyzes message -> Generates SQL (if needed) -> Executes -> Returns Answer.
    """
    service = ChatService(db)
    return service.process_message(request)
