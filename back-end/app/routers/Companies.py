from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Models import schemas, models
from app import database

router = APIRouter()

@router.post("/empresa/")
def post_companies(
    empresa: schemas.EmpresaBase,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaOut:
    db_empresa = models.Empresa(
        nit=empresa.nit,
        razon_social=empresa.razon_social,
        nombre_comercial=empresa.nombre_comercial,
        telefono=empresa.telefono,
        correo=empresa.correo,
        id_pais=empresa.id_pais,
        id_departamento=empresa.id_departamento,
        id_municipio=empresa.id_municipio
    )
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return schemas.EmpresaOut(
        id=db_empresa.id,
        nit=db_empresa.nit,
        razon_social=db_empresa.razon_social,
        nombre_comercial=db_empresa.nombre_comercial,
        telefono=db_empresa.telefono,
        correo=db_empresa.correo,
        id_pais=db_empresa.id_pais,
        id_departamento=db_empresa.id_departamento,
        id_municipio=db_empresa.id_municipio,
        pais=db_empresa.pais.nombre if db_empresa.pais else None,
        departamento=db_empresa.departamento.nombre if db_empresa.departamento else None,
        municipio=db_empresa.municipio.nombre if db_empresa.municipio else None
    )


@router.get("/empresa/", response_model=list[schemas.EmpresaOut])
def get_companies(
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaOut]:
    empresas = db.query(models.Empresa).all()
    return [
        schemas.EmpresaOut(
            id=e.id,
            pais=e.pais.nombre if e.pais else None,
            departamento=e.departamento.nombre if e.departamento else None,
            municipio=e.municipio.nombre if e.municipio else None,
            nit=e.nit,
            razon_social=e.razon_social,
            nombre_comercial=e.nombre_comercial,
            telefono=e.telefono,
            correo=e.correo,
            id_pais=e.id_pais,
            id_departamento=e.id_departamento,
            id_municipio=e.id_municipio,
            
        )
        for e in empresas
    ]


@router.get("/empresa/{id_empresa}", response_model=schemas.EmpresaOut)
def get_company(
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaOut:
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == id_empresa).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    return schemas.EmpresaOut.from_orm(db_empresa)

@router.get("/empresa/{id_empresa}/colaboradores", response_model=list[schemas.ColaboradorOut])
def get_company_collaborators(
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.ColaboradorOut]:
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == id_empresa).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    
    empresa_colaboradores = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id_empresa == id_empresa).all()
    colaboradores = [db.query(models.Colaborador).filter(models.Colaborador.id == ec.id_colaborador).first() for ec in empresa_colaboradores]
    return [schemas.ColaboradorOut.from_orm(colaborador) for colaborador in colaboradores if colaborador]

@router.put("/empresa/{id_empresa}")
def put_company(
    id_empresa: int,
    empresa: schemas.EmpresaBase,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaOut:
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == id_empresa).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_empresa.nit = empresa.nit
    db_empresa.razon_social = empresa.razon_social
    db_empresa.nombre_comercial = empresa.nombre_comercial
    db_empresa.telefono = empresa.telefono
    db_empresa.correo = empresa.correo
    db_empresa.id_pais = empresa.id_pais
    db_empresa.id_departamento = empresa.id_departamento
    db_empresa.id_municipio = empresa.id_municipio
    db.commit()
    db.refresh(db_empresa)
    
    return schemas.EmpresaOut(
        id=db_empresa.id,
        nit=db_empresa.nit,
        razon_social=db_empresa.razon_social,
        nombre_comercial=db_empresa.nombre_comercial,
        telefono=db_empresa.telefono,
        correo=db_empresa.correo,
        id_pais=db_empresa.id_pais,
        id_departamento=db_empresa.id_departamento,
        id_municipio=db_empresa.id_municipio,
        pais=db_empresa.pais.nombre if db_empresa.pais else None,
        departamento=db_empresa.departamento.nombre if db_empresa.departamento else None,
        municipio=db_empresa.municipio.nombre if db_empresa.municipio else None
    )

@router.delete("/empresa/{id_empresa}")
def delete_company(
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == id_empresa).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_empresa)
    db.commit()
    return {"message": "Company deleted successfully"}