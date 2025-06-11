from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Models import schemas, models
from app import database

router = APIRouter()

@router.get("/colaborador/", response_model=list[schemas.EmpresaColaboradorOut])
def get_company_collaborators(
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaColaboradorOut]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).all()
    result = []
    for ec in empresa_colaboradores:
        colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == ec.id_colaborador).first()
        empresa = db.query(models.Empresa).filter(models.Empresa.id == ec.id_empresa).first()
        if colaborador and empresa:
            result.append(schemas.EmpresaColaboradorOut(
                id_colaborador=colaborador.id,
                id_empresa=empresa.id,
                nombre_empresa=empresa.nombre_comercial or empresa.razon_social,
                nombre_colaborador=colaborador.nombre_completo,
                edad=colaborador.edad,
                telefono=colaborador.telefono,
                correo=colaborador.correo
            ))
    return result

@router.post("/colaborador/", response_model=schemas.EmpresaColaboradorOut)
def post_colaborador_with_empresa(
    payload: schemas.ColaboradorConEmpresa,
    db: Session = Depends(database.get_db)
):
    # Crear colaborador
    db_colaborador = models.Colaborador(
        nombre_completo=payload.nombre_completo,
        edad=payload.edad,
        telefono=payload.telefono,
        correo=payload.correo
    )
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)

    # Crear relación con empresa
    db_empresa_colaborador = models.EmpresaColaborador(
        id_empresa=payload.id_empresa,
        id_colaborador=db_colaborador.id
    )
    db.add(db_empresa_colaborador)
    db.commit()

    # Obtener nombre de la empresa
    empresa = db.query(models.Empresa).filter(models.Empresa.id == payload.id_empresa).first()

    return schemas.EmpresaColaboradorOut(
        id_colaborador=db_colaborador.id,
        id_empresa=empresa.id,
        nombre_colaborador=db_colaborador.nombre_completo,
        nombre_empresa=empresa.nombre_comercial or empresa.razon_social,
        edad=db_colaborador.edad,
        telefono=db_colaborador.telefono,
        correo=db_colaborador.correo
    )


@router.put("/colaborador/{id_colaborador}", response_model=schemas.EmpresaColaboradorOut)
def put_colaborador_with_empresa(
    id_colaborador: int,
    payload: schemas.ColaboradorConEmpresa,
    db: Session = Depends(database.get_db)
):
    # Buscar colaborador
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    # Actualizar datos del colaborador
    db_colaborador.nombre_completo = payload.nombre_completo
    db_colaborador.edad = payload.edad
    db_colaborador.telefono = payload.telefono
    db_colaborador.correo = payload.correo
    db.commit()

    # Actualizar relación con empresa
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_colaborador == id_colaborador
    ).first()

    if db_empresa_colaborador:
        db_empresa_colaborador.id_empresa = payload.id_empresa
    else:
        db_empresa_colaborador = models.EmpresaColaborador(
            id_colaborador=id_colaborador,
            id_empresa=payload.id_empresa
        )
        db.add(db_empresa_colaborador)

    db.commit()

    empresa = db.query(models.Empresa).filter(models.Empresa.id == payload.id_empresa).first()

    return schemas.EmpresaColaboradorOut(
        id_colaborador=id_colaborador,
        id_empresa=empresa.id,
        nombre_colaborador=db_colaborador.nombre_completo,
        nombre_empresa=empresa.nombre_comercial or empresa.razon_social,
        edad=db_colaborador.edad,
        telefono=db_colaborador.telefono,
        correo=db_colaborador.correo
    )

@router.delete("/colaborador/{id_colaborador}")
def delete_colaborador_with_empresa(
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    
    
    db.delete(db_colaborador)
    db.commit()
    
    return {"message": "Colaborador deleted successfully"}
