"""
Create chatbot_analytics table
"""
import sys
sys.path.insert(0, 'c:/laragon/www/proyecto_garantias')

from app.database import engine, SessionLocal
from app.models.chatbot_analytics import Base, ChatbotAnalytics

print("Creating chatbot_analytics table...")

# Create table
Base.metadata.create_all(bind=engine, tables=[ChatbotAnalytics.__table__])

print("✅ Table created successfully!")

# Verify
db = SessionLocal()
try:
    count = db.query(ChatbotAnalytics).count()
    print(f"Current analytics records: {count}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
