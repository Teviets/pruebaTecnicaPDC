import React, { useState, useEffect } from 'react';
import {
  Button, TextField, Dialog, DialogActions, DialogContent,
  DialogTitle, MenuItem
} from '@mui/material';
import { IoMdAddCircle } from "react-icons/io";
import { MdModeEditOutline } from "react-icons/md";

export default function CustomDialog({ type, mode, data, onSubmit }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({});
  const [paises, setPaises] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [municipalidades, setMunicipalidades] = useState([]);

  const [empresas, setEmpresas] = useState([]);

  const handleClickOpen = () => {
    setOpen(true);
    if (mode === 'edit' && data) {
      // Normaliza los datos según el tipo
      const normalized = { ...data };

      if (type === 'municipio') {
        normalized.id_pais = data.pais || ''; // puede que debas ajustar esto también
        normalized.nombre = data.municipio; // el campo de texto
        normalized.id_departamento = data.departamento || data.departamento || ''; // ajusta si es necesario
      }

      if (type === 'departamento') {
        normalized.nombre = data.departamento;
        normalized.id_pais = data.id_pais || ''; // puede que debas ajustar esto también
      }

      if (type === 'empresa') {
        console.log(data);
        normalized.NIT = data.nit; // Ajustar NIT
        handleGetDepartmentsByCountry(data.id_pais); // Cargar departamentos del país
        handleGetMunicipalitiesByDepartment(data.id_departamento); // Cargar municipios del departamento
        normalized.id_pais = data.id_pais || '';
        normalized.departamento = data.departamento || '';
        normalized.municipio = data.municipio || '';
      }

      if (type === 'colaborador') {
        normalized.nombre_completo = data.nombre_colaborador || '';
        normalized.id_empresa = data.id_empresa || '';
      }


      setForm(normalized);
    } else {
      setForm({});
    }
  };


  const handleClose = () => {
    setOpen(false);
  };

  const handleGetCompanies = () => {
    fetch('http://localhost:4000/empresa')
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => setEmpresas(data))
      .catch(error => console.error('Fetch error:', error));
  };

  const handleGetDepartmentsByCountry = (countryId) => {
    fetch(`http://localhost:4000/departamento/${countryId}/pais`)
      .then(res => {
        if (!res.ok) throw new Error('Error al obtener departamentos');
        return res.json();
      })
      .then(data => setDepartamentos(data))
      .catch(err => {
        console.error('Error fetching departamentos por país:', err);
        setDepartamentos([]);
      });
  };

  const handleGetMunicipalitiesByDepartment = (departmentId) => {
    fetch(`http://localhost:4000/municipio/${departmentId}/departamento`)
      .then(res => {
        if (!res.ok) throw new Error('Error al obtener municipios');
        return res.json();
      })
      .then(data => setMunicipalidades(data))
      .catch(err => {
        console.error('Error fetching municipios por departamento:', err);
        setMunicipalidades([]);
      });
  };

  const handleChange = (field) => (event) => {
        const value = event.target.value;
        setForm((prevForm) => ({
            ...prevForm,
            [field]: value,
            ...(field === 'id_pais' ? { id_departamento: '' } : {}) // limpia el departamento si se cambia país
        }));

        if (field === 'id_pais') {
          handleGetDepartmentsByCountry(value);
        }

        if (field === 'id_departamento') {
          handleGetMunicipalitiesByDepartment(value);
        }

    };

    const handleSave = () => {
        onSubmit(form);
        handleClose();
    };

    useEffect(() => {
        if (['departamento', 'empresa', 'municipio'].includes(type)) {
            fetch('http://localhost:4000/pais')
            .then(res => res.json())
            .then(data => setPaises(data))
            .catch(err => console.error('Error fetching países:', err));
        }
        if (type === 'colaborador') {
            handleGetCompanies();
        }
    }, [type]);


  const fieldsByType = {
    pais: ['nombre'],
    departamento: ['id_pais', 'nombre'],
    municipio: ['id_pais','id_departamento','nombre' ],
    empresa: [ 'id_pais', 'id_departamento', 'id_municipio', 'nombre_comercial', 'razon_social', 'NIT','telefono','correo'],
    colaborador: ['id_empresa','nombre_completo', 'edad', 'telefono', 'correo'],
  };

  const labels = {
    nombre: 'Nombre',
    id_empresa: 'Empresa',
    nombre_completo: 'Nombre Completo',
    razon_social: 'Razón Social',
    nombre_comercial: 'Nombre Comercial',
    telefono: 'Teléfono',
    NIT: 'NIT',
    correo: 'Correo',
    edad: 'Edad',
    id_pais: 'País',
    id_departamento: 'Departamento',
    id_municipio: 'Municipio',
  };

  return (
    <>
      {mode === 'edit' ? (
        <button onClick={handleClickOpen}>
          <MdModeEditOutline size={15} />
        </button>
      ) : (
        <Button onClick={handleClickOpen}>
          <IoMdAddCircle size={24} />
        </Button>
      )}

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{mode === 'edit' ? `Editar ${type}` : `Agregar ${type}`}</DialogTitle>
        <DialogContent>
          {type === 'empresa' ? (
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div style={{ flex: 1 }}>
                <TextField
                  select
                  margin="dense"
                  id="id_pais"
                  name="id_pais"
                  label={labels['id_pais']}
                  fullWidth
                  variant="standard"
                  value={form['id_pais'] || ''}
                  onChange={handleChange('id_pais')}
                >
                  {paises.map((pais) => (
                    <MenuItem key={pais.id} value={pais.id}>
                      {pais.nombre}
                    </MenuItem>
                  ))}
                </TextField>

                <TextField
                  select
                  margin="dense"
                  id="id_departamento"
                  name="id_departamento"
                  label={labels['id_departamento']}
                  fullWidth
                  variant="standard"
                  value={form['id_departamento'] || ''}
                  onChange={handleChange('id_departamento')}
                >
                  {departamentos.map((dep) => (
                    <MenuItem key={dep.id} value={dep.id}>
                      {dep.departamento}
                    </MenuItem>
                  ))}
                </TextField>

                <TextField
                  select
                  margin="dense"
                  id="id_municipio"
                  name="id_municipio"
                  label={labels['id_municipio']}
                  fullWidth
                  variant="standard"
                  value={form['id_municipio'] || ''}
                  onChange={handleChange('id_municipio')}
                >
                  {municipalidades.map((mun) => (
                    <MenuItem key={mun.id} value={mun.id}>
                      {mun.municipio}
                    </MenuItem>
                  ))}
                </TextField>

              </div>

              <div style={{ flex: 1 }}>
                {['nombre_comercial', 'razon_social', 'NIT', 'telefono', 'correo'].map((field) => (
                  <TextField
                    key={field}
                    margin="dense"
                    id={field}
                    name={field}
                    label={labels[field]}
                    fullWidth
                    variant="standard"
                    value={form[field] || ''}
                    onChange={handleChange(field)}
                  />
                ))}
              </div>
            </div>
          ) : (
            // comportamiento anterior para otros types
            fieldsByType[type]?.map((field) => {
              if (field === 'id_pais') {
                return (
                  <TextField
                    key={field}
                    select
                    margin="dense"
                    id={field}
                    name={field}
                    label={labels[field]}
                    fullWidth
                    variant="standard"
                    value={form[field] || ''}
                    onChange={handleChange(field)}
                  >
                    {paises.map((pais) => (
                      <MenuItem key={pais.id} value={pais.id}>
                        {pais.nombre}
                      </MenuItem>
                    ))}
                  </TextField>
                );
              }
              if (field === 'id_departamento') {
                return (
                  <TextField
                    key={field}
                    select
                    margin="dense"
                    id={field}
                    name={field}
                    label={labels[field]}
                    fullWidth
                    variant="standard"
                    value={form[field] || ''}
                    onChange={handleChange(field)}
                  >
                    {departamentos.map((dep) => (
                      <MenuItem key={dep.id} value={dep.id}>
                        {dep.departamento}
                      </MenuItem>
                    ))}
                  </TextField>
                );
              }
              if (field === 'id_empresa') {
                return (
                  <TextField
                    key={field}
                    select
                    margin="dense"
                    id={field}
                    name={field}
                    label={labels[field]}
                    fullWidth
                    variant="standard"
                    value={form[field] || ''}
                    onChange={handleChange(field)}
                  >
                    {empresas.map((empresa) => (
                      <MenuItem key={empresa.id} value={empresa.id}>
                        {empresa.nombre_comercial || empresa.razon_social}
                      </MenuItem>
                    ))}
                  </TextField>
                );
              }

              return (
                <TextField
                  key={field}
                  margin="dense"
                  id={field}
                  name={field}
                  label={labels[field] || field}
                  type={field.includes('id') || field === 'edad' ? 'number' : 'text'}
                  fullWidth
                  variant="standard"
                  value={form[field] || ''}
                  onChange={handleChange(field)}
                />
              );
            })
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={handleClose}>Cancelar</Button>
          <Button onClick={handleSave}>Guardar</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
