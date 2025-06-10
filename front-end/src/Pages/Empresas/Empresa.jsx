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

export default function Empresa() {
  const [empresas, setEmpresas] = useState([]);

  const loadCompanies = () => {
    fetch('http://localhost:4000/empresa')
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => setEmpresas(data))
      .catch(error => console.error('Fetch error:', error));
  };

  useEffect(() => {
    loadCompanies();
  }
  , []);

  const handleAddCompany = (newCompany) => {
    const payload = {
      nit: newCompany.NIT,
      razon_social: newCompany.razon_social,
      nombre_comercial: newCompany.nombre_comercial,
      telefono: newCompany.telefono,
      correo: newCompany.correo,
      id_pais: newCompany.id_pais,
      id_departamento: newCompany.id_departamento,
      id_municipio: newCompany.id_municipio
    };

    fetch('http://localhost:4000/empresa/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        loadCompanies();
      })
      .catch(error => {
        console.error('Hubo un error al crear la empresa:', error);
      });
  };

  const handleUpdateCompany = (updatedCompany) => {
    const payload = {
      nit: updatedCompany.NIT,
      razon_social: updatedCompany.razon_social,
      nombre_comercial: updatedCompany.nombre_comercial,
      telefono: updatedCompany.telefono,
      correo: updatedCompany.correo,
      id_pais: updatedCompany.id_pais,
      id_departamento: updatedCompany.id_departamento,
      id_municipio: updatedCompany.id_municipio
    };

    fetch(`http://localhost:4000/empresa/${updatedCompany.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Aquí puedes actualizar la lista de empresas o mostrar mensaje de éxito
        console.log('Empresa actualizada:', data);
        loadCompanies();
      })
      .catch(error => {
        console.error('Hubo un error al actualizar la empresa:', error);
      });
  }

  const handleDeleteCompany = (companyId) => {
    fetch(`http://localhost:4000/empresa/${companyId}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Aquí puedes actualizar la lista de empresas o mostrar mensaje de éxito
        console.log('Empresa eliminada');
      })
      .catch(error => {
        console.error('Hubo un error al eliminar la empresa:', error);
      });
  }



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
            <h3>Países</h3>            
            <CustomDialog type="empresa" mode="add" onSubmit={handleAddCompany} />
          </Box>
          <CustomTable data={empresas} type="empresa" remove={handleDeleteCompany} edit={handleUpdateCompany}/>
        </Paper>
    </Box>
  )
}
