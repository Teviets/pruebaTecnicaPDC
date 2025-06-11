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

@router.get("/municipio/{id_departamento}/departamento", response_model=list[schemas.MunicipioOut])
def get_municipalities_by_department(
    id_departamento: int,
    db: Session = Depends(database.get_db)
) -> list[schemas.MunicipioOut]:
    db_municipios = db.query(models.Municipio).filter(models.Municipio.id_departamento == id_departamento).all()
    
    if not db_municipios:
        raise HTTPException(status_code=404, detail="No municipalities found for this department")
    
    return [
        schemas.MunicipioOut(
            id=m.id,
            municipio=m.nombre,
            departamento=m.departamento.nombre
        )
        for m in db_municipios
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