from sqlalchemy import Column, String, Date, DateTime, func
from app.database import Base

class Contrato(Base):
    __tablename__ = "contratos"

    id_contrato = Column(String(100), primary_key=True)
    id_adjudicacion = Column(String(100), nullable=False, index=True)
    id_convocatoria = Column(String(100), nullable=False, index=True)
    ocid = Column(String(100), index=True)
    fecha_firma = Column(Date)
    estado_contrato = Column(String(50))
    fecha_registro = Column(DateTime, server_default=func.now())
