from pydantic import BaseModel
from typing import Optional

class PaisBase(BaseModel):
    nombre: str

class PaisCreate(PaisBase):
    pass

class PaisOut(PaisBase):
    id: int
    class Config:
        from_attributes = True

class DepartamentoBase(BaseModel):
    nombre: str
    id_pais: int

class DepartamentoOut(BaseModel):
    id: int
    pais: Optional[str]
    departamento: str
    class Config:
        from_attributes = True

class MunicipioBase(BaseModel):
    nombre: str
    id_departamento: int

class MunicipioOut(BaseModel):
    id: int
    departamento: Optional[str]
    municipio: str

    class Config:
        from_attributes = True


class EmpresaBase(BaseModel):
    nit: str
    razon_social: Optional[str] = None
    nombre_comercial: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    id_pais: int
    id_departamento: int
    id_municipio: int

class EmpresaOut(BaseModel):
    id: int
    pais: Optional[str]
    departamento: Optional[str]
    municipio: Optional[str]
    nombre_comercial: Optional[str]
    razon_social: Optional[str]
    nit: str
    telefono: Optional[str]
    correo: Optional[str]
    id_pais: int
    id_departamento: int
    id_municipio: int
    

    class Config:
        from_attributes = True


class ColaboradorBase(BaseModel):
    nombre_completo: str
    edad: Optional[int] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class ColaboradorOut(ColaboradorBase):
    id: int
    class Config:
        from_attributes = True

class EmpresaColaboradorBase(BaseModel):
    id_empresa: int
    id_colaborador: int

class EmpresaColaboradorOut(EmpresaColaboradorBase):
    id: int
    class Config:
        from_attributes = True
