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

  const handleClickOpen = () => {
  setOpen(true);
  if (mode === 'edit' && data) {
    // Normaliza los datos según el tipo
    const normalized = { ...data };

    if (type === 'municipio') {
      normalized.nombre = data.municipio; // el campo de texto
      normalized.id_departamento = data.id_departamento || data.departamento_id || ''; // ajusta si es necesario
    }

    if (type === 'departamento') {
      normalized.nombre = data.departamento;
      normalized.id_pais = data.id_pais || ''; // puede que debas ajustar esto también
    }

    setForm(normalized);
  } else {
    setForm({});
  }
};


  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (field) => (event) => {
        const value = event.target.value;
        setForm((prevForm) => ({
            ...prevForm,
            [field]: value,
            ...(field === 'id_pais' ? { id_departamento: '' } : {}) // limpia el departamento si se cambia país
        }));

        if (field === 'id_pais') {
            fetch(`http://localhost:4000/departamento/${value}/pais`)
            .then(res => {
                if (!res.ok) throw new Error('Error al obtener departamentos');
                return res.json();
            })
            .then(data => setDepartamentos(data))
            .catch(err => {
                console.error('Error fetching departamentos por país:', err);
                setDepartamentos([]);
            });
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
    }, [type]);


  const fieldsByType = {
    pais: ['nombre'],
    departamento: ['id_pais', 'nombre'],
    municipio: ['id_pais','id_departamento','nombre' ],
    empresa: ['razon_social', 'nombre_comercial', 'telefono', 'correo', 'id_pais', 'id_departamento', 'id_municipio'],
    colaborador: ['nombre_completo', 'edad', 'telefono', 'correo'],
  };

  const labels = {
    nombre: 'Nombre',
    nombre_completo: 'Nombre Completo',
    razon_social: 'Razón Social',
    nombre_comercial: 'Nombre Comercial',
    telefono: 'Teléfono',
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
          {fieldsByType[type]?.map((field) => {
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
          })}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancelar</Button>
          <Button onClick={handleSave}>Guardar</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
