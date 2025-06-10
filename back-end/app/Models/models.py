from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    departamentos = relationship('Departamento', back_populates='pais')

class Departamento(Base):
    __tablename__ = "departamento"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"), nullable=False)

    pais = relationship("Pais", back_populates="departamentos")
    municipios = relationship("Municipio", back_populates="departamento")

class Municipio(Base):
    __tablename__ = "municipio"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    id_departamento = Column(Integer, ForeignKey("departamento.id"), nullable=False)

    departamento = relationship("Departamento", back_populates="municipios")

class Empresa(Base):
    __tablename__ = "empresa"
    id = Column(Integer, primary_key=True, index=True)
    id_pais = Column(Integer, ForeignKey("pais.id"), nullable=False)
    id_departamento = Column(Integer, ForeignKey("departamento.id"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("municipio.id"), nullable=False)
    nit = Column(String(50), nullable=False, unique=True)
    razon_social = Column(String(100))
    nombre_comercial = Column(String(100))
    telefono = Column(String(50))
    correo = Column(String(100))

    pais = relationship("Pais")
    departamento = relationship("Departamento")
    municipio = relationship("Municipio")

    colaboradores = relationship("EmpresaColaborador", back_populates="empresa")


class Colaborador(Base):
    __tablename__ = "colaborador"
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    edad = Column(Integer)
    telefono = Column(String(50))
    correo = Column(String(100))

    empresas = relationship("EmpresaColaborador", back_populates="colaborador")

class EmpresaColaborador(Base):
    __tablename__ = "empresa_colaborador"
    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey("empresa.id"), nullable=False)
    id_colaborador = Column(Integer, ForeignKey("colaborador.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="colaboradores")
    colaborador = relationship("Colaborador", back_populates="empresas")

    __table_args__ = (
        UniqueConstraint('id_empresa', 'id_colaborador', name='uix_empresa_colaborador'),
    )
