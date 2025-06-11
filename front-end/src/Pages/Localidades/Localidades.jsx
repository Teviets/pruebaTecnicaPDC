import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import CustomTable from '../../Components/Table/CustomTable.jsx'
import CustomDialog from '../../Components/Dialog/CustomDialog.jsx';

import './Localidades.scss';

const paperHeaderStyle = { 
          padding: 2,
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
        }

export default function Localidades() {

  const [paises, setPaises] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [municipalidades, setMunicipalidades] = useState([]);

  useEffect(() => {
    fetch('http://localhost:4000/pais').then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(data => {
      console.log(data);
      setPaises(data);
    }
    ).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);

  useEffect(() => {
    fetch('http://localhost:4000/departamento').then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(data => {
      console.log(data);
      setDepartamentos(data);
    }
    ).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);

  useEffect(() => {
    fetch('http://localhost:4000/municipio').then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(data => {
      console.log(data);
      setMunicipalidades(data);
    }
    ).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);

  const handleDeleteCountry = (id) => {
    fetch(`http://localhost:4000/pais/${id}`, {
      method: 'DELETE',
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(() => {
      setPaises(paises.filter(pais => pais.id !== id));
    }).catch(error => {
      console.error('There was a problem with the delete operation:', error);
    });
  }

  const handleDeleteDepartment = (id) => {
    fetch(`http://localhost:4000/departamento/${id}`, {
      method: 'DELETE',
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(() => {
      setDepartamentos(departamentos.filter(departamento => departamento.id !== id));
    }).catch(error => {
      console.error('There was a problem with the delete operation:', error);
    });
  }

  const handleDeleteMunicipality = (id) => {
    fetch(`http://localhost:4000/municipio/${id}`, {
      method: 'DELETE',
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(() => {
      setMunicipalidades(municipalidades.filter(municipio => municipio.id !== id));
    }).catch(error => {
      console.error('There was a problem with the delete operation:', error);
    });
  }

  const handleAddCountry = (newCountry) => {
    fetch('http://localhost:4000/pais', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newCountry),
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(data => {
      setPaises([...paises, data]);
    }).catch(error => {
      console.error('There was a problem with the add operation:', error);
    });
  }

  const handleUpdateCountry = (updatedCountry) => {
    fetch(`http://localhost:4000/pais/${updatedCountry.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedCountry),
    }).then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }).then(data => {
      setPaises(paises.map(pais => pais.id === data.id ? data : pais));
    }).catch(error => {
      console.error('There was a problem with the update operation:', error);
    });
  };

  const handleAddDepartment = (newDepartment) => {
    const payload = {
      nombre: newDepartment.nombre,
      id_pais: newDepartment.id_pais
    };

    fetch('http://localhost:4000/departamento/', {
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
        setDepartamentos([...departamentos, data]);
      })
      .catch(error => {
        console.error('There was a problem with the add operation:', error);
      });
  };

  const handleUpdateDepartment = (updatedDepartment) => {
    const payload = {
      nombre: updatedDepartment.nombre,
      id_pais: updatedDepartment.id_pais
    };

    fetch(`http://localhost:4000/departamento/${updatedDepartment.id}`, {
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
        setDepartamentos(departamentos.map(departamento => departamento.id === data.id ? data : departamento));
      })
      .catch(error => {
        console.error('There was a problem with the update operation:', error);
      });
  };

  const handleAddMunicipality = (newMunicipality) => {
    const payload = {
      nombre: newMunicipality.nombre,
      id_departamento: newMunicipality.id_departamento,
    };

    fetch('http://localhost:4000/municipio/', {
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
        setMunicipalidades(prev => [...prev, data]);
      })
      .catch(error => {
        console.error('There was a problem with the add operation:', error);
      });
  };

  const handleUpdateMunicipality = (updatedMunicipality) => {
    const payload = {
      nombre: updatedMunicipality.nombre,
      id_departamento: updatedMunicipality.id_departamento,
    };

    fetch(`http://localhost:4000/municipio/${updatedMunicipality.id}`, {
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
        setMunicipalidades(municipalidades.map(municipio => municipio.id === data.id ? data : municipio));
      })
      .catch(error => {
        console.error('There was a problem with the update operation:', error);
      });
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 2,
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        height: '85vh',
        padding: 12,
      }}
      >
      <Paper className='PapersLocal' elevation={16} >
        <Box sx={paperHeaderStyle}>
          <h3>Países</h3>            
          <CustomDialog type="pais" mode="add" onSubmit={handleAddCountry}/>
        </Box>
        <CustomTable data={paises} remove={handleDeleteCountry} edit={handleUpdateCountry} type="pais"/>
      </Paper>
      <Paper className='PapersLocal' elevation={16}>
        <Box sx={paperHeaderStyle}>
          <h3>Departamentos</h3>
          <CustomDialog type="departamento" mode="add" onSubmit={handleAddDepartment}/>
        </Box>
        <CustomTable data={departamentos} remove={handleDeleteDepartment} edit={handleUpdateDepartment} type="departamento"/>
      </Paper>
      <Paper className='PapersLocal' elevation={16} >
        <Box sx={paperHeaderStyle}>
          <h3>Municipalidades</h3>
          <CustomDialog type="municipio" mode="add" onSubmit={handleAddMunicipality}/>
        </Box>
        <CustomTable data={municipalidades} remove={handleDeleteMunicipality} edit={handleUpdateMunicipality} type="municipio"/>
      </Paper>
    </Box>
  )
}
