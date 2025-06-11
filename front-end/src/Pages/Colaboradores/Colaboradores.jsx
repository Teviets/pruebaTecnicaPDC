import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import CustomDialog from '../../Components/Dialog/CustomDialog';
import CustomTable from '../../Components/Table/CustomTable';

const paperHeaderStyle = { 
          padding: 2,
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
        }

export default function Colaboradores() {
  const [colaboradores, setColaboradores] = useState([]);


  const loadColaboradores = () => {
    fetch('http://localhost:4000/colaborador',
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        setColaboradores(data)
        console.log(data);
      })
      .catch(error => console.error('Fetch error:', error));
  }

  const handleAddColaborador = (newColaborador) => {
    console.log(newColaborador);
    const payload = {
      nombre_completo: newColaborador.nombre_completo,
      edad: newColaborador.edad,
      telefono: newColaborador.telefono,
      correo: newColaborador.correo,
      id_empresa: newColaborador.id_empresa,
    };

    fetch('http://localhost:4000/colaborador/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        loadColaboradores();
      })
      .catch(error => console.error('Fetch error:', error));
  }

  const handleDeleteColaborador = (colaborID) => {
    console.log("Eliminando colaborador con ID:", colaborID);
    fetch(`http://localhost:4000/colaborador/${colaborID}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        loadColaboradores();
      })
      .catch(error => console.error('Fetch error:', error));
  }

  const handleUpdateColaborador = (colaborador) => {
    const payload = {
      nombre_completo: colaborador.nombre_completo,
      edad: colaborador.edad,
      telefono: colaborador.telefono,
      correo: colaborador.correo,
      id_empresa: colaborador.id_empresa
    };

    fetch(`http://localhost:4000/colaborador/${colaborador.id_colaborador}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => {
      if (!response.ok) throw new Error('Error al actualizar colaborador');
      return response.json();
    })
    .then(data => {
      console.log('Colaborador actualizado:', data);
      loadColaboradores();
    })
    .catch(error => {
      console.error('Error en la solicitud PUT:', error);
    });
  };


  useEffect(() => {
    loadColaboradores();
  }
  , []);
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'flex-start',
        justifyContent: 'center',
        height: '85vh',
        padding: 2,
      }}
      >
        <Paper className='PapersLocal' elevation={16} >
          <Box sx={paperHeaderStyle}>
            <h3>Colaboradores</h3>
            <CustomDialog type="colaborador" mode="add" onSubmit={handleAddColaborador} />
          </Box>
          <CustomTable data={colaboradores} type="colaborador" remove={handleDeleteColaborador} edit={handleUpdateColaborador}/>
        </Paper>
    </Box>
  )
}
