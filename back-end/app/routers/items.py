from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Models import schemas, models
from app import database


router = APIRouter()

@router.post("/pais/")
def post_countries(
    pais: schemas.PaisCreate,
    db: Session = Depends(database.get_db)
) -> schemas.PaisOut:
    db_pais = models.Pais(nombre=pais.nombre)
    db.add(db_pais)
    db.commit()
    db.refresh(db_pais)
    return schemas.PaisOut.from_orm(db_pais)

@router.get("/pais/", response_model=list[schemas.PaisOut])
def get_countries(
    db: Session = Depends(database.get_db)
) -> list[schemas.PaisOut]:
    paises = db.query(models.Pais).all()
    return [schemas.PaisOut.from_orm(pais) for pais in paises]

@router.get("/pais/{id_pais}", response_model=schemas.PaisOut)
def get_country(
    id_pais: int,
    db: Session = Depends(database.get_db)
) -> schemas.PaisOut:
    db_pais = db.query(models.Pais).filter(models.Pais.id == id_pais).first()
    if not db_pais:
        raise HTTPException(status_code=404, detail="Country not found")
    return schemas.PaisOut.from_orm(db_pais)

@router.put("/pais/{id_pais}")
def put_country(
    id_pais: int,
    pais: schemas.PaisBase,
    db: Session = Depends(database.get_db)
) -> schemas.PaisOut:
    db_pais = db.query(models.Pais).filter(models.Pais.id == id_pais).first()
    if not db_pais:
        raise HTTPException(status_code=404, detail="Country not found")
    
    db_pais.nombre = pais.nombre
    db.commit()
    db.refresh(db_pais)
    return schemas.PaisOut.from_orm(db_pais)

@router.delete("/pais/{id_pais}")
def delete_country(
    id_pais: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_pais = db.query(models.Pais).filter(models.Pais.id == id_pais).first()
    if not db_pais:
        raise HTTPException(status_code=404, detail="Country not found")
    
    db.delete(db_pais)
    db.commit()
    return {"message": "Country deleted successfully"}

@router.post("/departamento/")
def post_departments(
    departamento: schemas.DepartamentoBase,
    db: Session = Depends(database.get_db)
) -> schemas.DepartamentoOut:
    db_departamento = models.Departamento(
        nombre=departamento.nombre,
        id_pais=departamento.id_pais
    )
    db.add(db_departamento)
    db.commit()
    db.refresh(db_departamento)

    pais_nombre = db_departamento.pais.nombre

    return schemas.DepartamentoOut(
        id=db_departamento.id,
        departamento=db_departamento.nombre,
        pais=pais_nombre
    )


@router.get("/departamento/", response_model=list[schemas.DepartamentoOut])
def get_departments(db: Session = Depends(database.get_db)):
    departamentos = db.query(models.Departamento).all()
    return [
        schemas.DepartamentoOut(
            id=d.id,
            departamento=d.nombre,
            pais=d.pais.nombre
        ) for d in departamentos
    ]

@router.get("/departamento/{id_departamento}", response_model=schemas.DepartamentoOut)
def get_department(
    id_departamento: int,
    db: Session = Depends(database.get_db)
) -> schemas.DepartamentoOut:
    db_departamento = db.query(models.Departamento).filter(models.Departamento.id == id_departamento).first()
    if not db_departamento:
        raise HTTPException(status_code=404, detail="Department not found")
    return schemas.DepartamentoOut.from_orm(db_departamento)

@router.get("/departamento/{id_pais}/pais", response_model=list[schemas.DepartamentoOut])
def get_departments_by_country(
    id_pais: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.DepartamentoOut]:
    db_departamentos = db.query(models.Departamento).filter(models.Departamento.id_pais == id_pais).all()

    if not db_departamentos:
        raise HTTPException(status_code=404, detail="No departments found for this country")
    
    return [
        schemas.DepartamentoOut(
            id=d.id,
            departamento=d.nombre,
            pais=d.pais.nombre
        ) for d in db_departamentos
    ]


@router.put("/departamento/{id}", response_model=schemas.DepartamentoOut)
def put_department(
    id: int,
    departamento: schemas.DepartamentoBase,
    db: Session = Depends(database.get_db)
):
    db_departamento = db.query(models.Departamento).filter(models.Departamento.id == id).first()
    if not db_departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    db_departamento.nombre = departamento.nombre
    db_departamento.id_pais = departamento.id_pais

    db.commit()
    db.refresh(db_departamento)

    return schemas.DepartamentoOut(
        id=db_departamento.id,
        departamento=db_departamento.nombre,
        pais=db_departamento.pais.nombre
    )


@router.delete("/departamento/{id_departamento}")
def delete_department(
    id_departamento: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_departamento = db.query(models.Departamento).filter(models.Departamento.id == id_departamento).first()
    if not db_departamento:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_departamento)
    db.commit()
    return {"message": "Department deleted successfully"}

@router.post("/municipio/", response_model=schemas.MunicipioOut)
def post_municipalities(
    municipio: schemas.MunicipioBase,
    db: Session = Depends(database.get_db)
) -> schemas.MunicipioOut:
    db_municipio = models.Municipio(
        nombre=municipio.nombre,
        id_departamento=municipio.id_departamento
    )
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)

    # Obtener nombre del departamento
    departamento = db_municipio.departamento

    return schemas.MunicipioOut(
        id=db_municipio.id,
        municipio=db_municipio.nombre,
        departamento=departamento.nombre
    )

@router.get("/municipio/", response_model=list[schemas.MunicipioOut])
def get_municipalities(
    db: Session = Depends(database.get_db)
) -> list[schemas.MunicipioOut]:
    municipios = db.query(models.Municipio).all()
    return [
        schemas.MunicipioOut(
            id=m.id,
            municipio=m.nombre,
            departamento=m.departamento.nombre
        )
        for m in municipios
    ]

@router.put("/municipio/{id_municipio}", response_model=schemas.MunicipioOut)
def put_municipality(
    id_municipio: int,
    municipio: schemas.MunicipioBase,
    db: Session = Depends(database.get_db)
):
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id == id_municipio).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    db_municipio.nombre = municipio.nombre
    db_municipio.id_departamento = municipio.id_departamento
    db.commit()
    db.refresh(db_municipio)

    return schemas.MunicipioOut(
        id=db_municipio.id,
        municipio=db_municipio.nombre,
        departamento=db_municipio.departamento.nombre
    )




@router.delete("/municipio/{id_municipio}")
def delete_municipality(
    id_municipio: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id == id_municipio).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    db.delete(db_municipio)
    db.commit()
    return {"message": "Municipality deleted successfully"}

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
    return schemas.EmpresaOut.from_orm(db_empresa)

@router.get("/empresa/", response_model=list[schemas.EmpresaOut])
def get_companies(
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaOut]:
    empresas = db.query(models.Empresa).all()
    return [schemas.EmpresaOut.from_orm(empresa) for empresa in empresas]

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
    return schemas.EmpresaOut.from_orm(db_empresa)

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

@router.post("/colaborador/")
def post_collaborators(
    colaborador: schemas.ColaboradorBase,
    db: Session = Depends(database.get_db)
) -> schemas.ColaboradorOut:
    db_colaborador = models.Colaborador(
        nombre_completo=colaborador.nombre_completo,
        edad=colaborador.edad,
        telefono=colaborador.telefono,
        correo=colaborador.correo
    )
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    return schemas.ColaboradorOut.from_orm(db_colaborador)

@router.get("/colaborador/", response_model=list[schemas.ColaboradorOut])
def get_collaborators(
    db: Session = Depends(database.get_db)
) -> list[schemas.ColaboradorOut]:
    colaboradores = db.query(models.Colaborador).all()
    return [schemas.ColaboradorOut.from_orm(colaborador) for colaborador in colaboradores]

@router.put("/colaborador/{id_colaborador}")
def put_collaborator(
    id_colaborador: int,
    colaborador: schemas.ColaboradorBase,
    db: Session = Depends(database.get_db)
) -> schemas.ColaboradorOut:
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    db_colaborador.nombre_completo = colaborador.nombre_completo
    db_colaborador.edad = colaborador.edad
    db_colaborador.telefono = colaborador.telefono
    db_colaborador.correo = colaborador.correo
    db.commit()
    db.refresh(db_colaborador)
    return schemas.ColaboradorOut.from_orm(db_colaborador)

@router.delete("/colaborador/{id_colaborador}")
def delete_collaborator(
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    db.delete(db_colaborador)
    db.commit()
    return {"message": "Collaborator deleted successfully"}

@router.post("/empresa_colaborador/")
def post_company_collaborator(
    empresa_colaborador: schemas.EmpresaColaboradorBase,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = models.EmpresaColaborador(
        id_empresa=empresa_colaborador.id_empresa,
        id_colaborador=empresa_colaborador.id_colaborador
    )
    db.add(db_empresa_colaborador)
    db.commit()
    db.refresh(db_empresa_colaborador)
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/", response_model=list[schemas.EmpresaColaboradorBase])
def get_company_collaborators(
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaColaboradorBase]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).all()
    return [schemas.EmpresaColaboradorBase.from_orm(ec) for ec in empresa_colaboradores]

@router.put("/empresa_colaborador/{id_empresa_colaborador}")
def put_company_collaborator(
    id_empresa_colaborador: int,
    empresa_colaborador: schemas.EmpresaColaboradorBase,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id == id_empresa_colaborador).first()
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Company Collaborator not found")
    
    db_empresa_colaborador.id_empresa = empresa_colaborador.id_empresa
    db_empresa_colaborador.id_colaborador = empresa_colaborador.id_colaborador
    db.commit()
    db.refresh(db_empresa_colaborador)
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.delete("/empresa_colaborador/{id_empresa_colaborador}")
def delete_company_collaborator(
    id_empresa_colaborador: int,
    db: Session = Depends(database.get_db)
) -> dict:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id == id_empresa_colaborador).first()
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Company Collaborator not found")
    
    db.delete(db_empresa_colaborador)
    db.commit()
    return {"message": "Company Collaborator deleted successfully"}

@router.get("/empresa_colaborador/{id_empresa}")
def get_collaborators_by_company(
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.ColaboradorOut]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id_empresa == id_empresa).all()
    colaboradores = [db.query(models.Colaborador).filter(models.Colaborador.id == ec.id_colaborador).first() for ec in empresa_colaboradores]
    return [schemas.ColaboradorOut.from_orm(colaborador) for colaborador in colaboradores if colaborador]

@router.get("/empresa_colaborador/colaborador/{id_colaborador}")
def get_companies_by_collaborator(
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaOut]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id_colaborador == id_colaborador).all()
    empresas = [db.query(models.Empresa).filter(models.Empresa.id == ec.id_empresa).first() for ec in empresa_colaboradores]
    return [schemas.EmpresaOut.from_orm(empresa) for empresa in empresas if empresa]

@router.get("/empresa_colaborador/colaborador/{id_colaborador}/empresa/{id_empresa}")
def get_collaborator_in_company(
    id_colaborador: int,
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_colaborador == id_colaborador,
        models.EmpresaColaborador.id_empresa == id_empresa
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Collaborator not found in the specified company")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/empresa/{id_empresa}/colaborador/{id_colaborador}")
def get_company_collaborator(
    id_empresa: int,
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_empresa == id_empresa,
        models.EmpresaColaborador.id_colaborador == id_colaborador
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Company Collaborator not found")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/empresa/{id_empresa}/colaborador")
def get_company_collaborators(
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.ColaboradorOut]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id_empresa == id_empresa).all()
    colaboradores = [db.query(models.Colaborador).filter(models.Colaborador.id == ec.id_colaborador).first() for ec in empresa_colaboradores]
    return [schemas.ColaboradorOut.from_orm(colaborador) for colaborador in colaboradores if colaborador]

@router.get("/empresa_colaborador/colaborador/{id_colaborador}/empresa")
def get_collaborator_companies(
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.EmpresaOut]:
    empresa_colaboradores = db.query(models.EmpresaColaborador).filter(models.EmpresaColaborador.id_colaborador == id_colaborador).all()
    empresas = [db.query(models.Empresa).filter(models.Empresa.id == ec.id_empresa).first() for ec in empresa_colaboradores]
    return [schemas.EmpresaOut.from_orm(empresa) for empresa in empresas if empresa]

@router.get("/empresa_colaborador/empresa/{id_empresa}/colaborador/{id_colaborador}")
def get_company_collaborator_details(
    id_empresa: int,
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_empresa == id_empresa,
        models.EmpresaColaborador.id_colaborador == id_colaborador
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Company Collaborator not found")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/colaborador/{id_colaborador}/empresa/{id_empresa}")
def get_collaborator_company_details(
    id_colaborador: int,
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_colaborador == id_colaborador,
        models.EmpresaColaborador.id_empresa == id_empresa
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Collaborator not found in the specified company")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/empresa/{id_empresa}/colaborador/{id_colaborador}/details")
def get_company_collaborator_details_full(
    id_empresa: int,
    id_colaborador: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_empresa == id_empresa,
        models.EmpresaColaborador.id_colaborador == id_colaborador
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Company Collaborator not found")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

@router.get("/empresa_colaborador/colaborador/{id_colaborador}/empresa/{id_empresa}/details")
def get_collaborator_company_details_full(
    id_colaborador: int,
    id_empresa: int,
    db: Session = Depends(database.get_db)
) -> schemas.EmpresaColaboradorBase:
    db_empresa_colaborador = db.query(models.EmpresaColaborador).filter(
        models.EmpresaColaborador.id_colaborador == id_colaborador,
        models.EmpresaColaborador.id_empresa == id_empresa
    ).first()
    
    if not db_empresa_colaborador:
        raise HTTPException(status_code=404, detail="Collaborator not found in the specified company")
    
    return schemas.EmpresaColaboradorBase.from_orm(db_empresa_colaborador)

