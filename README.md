# Sistema Administrativo - Proyecto Técnico

Este sistema permite la gestión de empresas y colaboradores asociados, incluyendo ubicación por país, departamento y municipio.

## 🧱 Tecnologías

- Backend: [FastAPI](https://fastapi.tiangolo.com/)
- Base de Datos: PostgreSQL (v15)
- Frontend: React + Material UI
- Contenedores: Docker + Docker Compose

---

## 🚀 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## ⚙️ Cómo iniciar el proyecto

1. Clona el repositorio:

```bash
git clone https://github.com/Teviets/pruebaTecnicaPDC
cd pruebaTecnicaPDC
````

2. Levanta los servicios con Docker:

```bash
docker-compose up --build
```

3. Accede al sistema:

* 📡 **Backend (FastAPI)**: [http://localhost:4000/docs](http://localhost:4000/docs)
* 🌐 **Frontend (React)**: [http://172.20.0.4:5173/](http://172.20.0.4:5173/)

---

## 🗂️ Estructura del proyecto

```
.
├── back-end/              # Código backend con FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   └── models/
│   └── requirements.txt
├── front-end/             # Código frontend con React
│   └── src/
├── db-init/               # Scripts SQL de inicialización
│   └── init.sql
├── docker-compose.yml
```

---

## 🧪 Endpoints útiles

* `GET /empresa/`
* `POST /empresa/`
* `PUT /empresa/{id}`
* `GET /colaborador/`
* `POST /colaborador/`
* `PUT /colaborador/{id}`
* `DELETE /colaborador/{id}`

Todos los endpoints están documentados en:
📚 [http://localhost:4000/docs](http://localhost:4000/docs)

---

## 📝 Notas

* Asegúrate que el puerto `5173` no esté ocupado por otro proceso en tu máquina local.
* La base de datos se inicializa automáticamente al primer arranque con los scripts de `db-init/`.

---

## 🧑‍💻 Autor

Desarrollado por Sebastian Estrada.


