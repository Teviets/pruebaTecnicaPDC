import React, { useState } from 'react'
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import CustomDialog from '../Dialog/CustomDialog.jsx';

import { MdModeEditOutline } from "react-icons/md";
import { MdDelete } from "react-icons/md";

const excludedColumns = ['id', 'id_pais', 'id_departamento', 'id_municipio', 'id_empresa', 'id_colaborador'];

export default function CustomTable({ data = [], remove, edit, type }) {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  if (!data.length) return <p>No hay datos para mostrar.</p>

  const columns = Object.keys(data[0]).map((key) => ({
    id: key,
    label: key
      .replace(/_/g, ' ')               // reemplaza '_' por espacio
      .replace(/\b\w/g, l => l.toUpperCase()), // mayúscula en cada palabra
    minWidth: 100,
    align: 'left',
  }));


  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="tabla dinámica">
          <TableHead>
            <TableRow>
              {columns
                .filter((column) => !excludedColumns.includes(column.id))
                .map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    {column.label}
                  </TableCell>
              ))}
              <TableCell align="right" style={{ minWidth: 100 }}>Editar</TableCell>
              <TableCell align="right" style={{ minWidth: 100 }}>Eliminar</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data
            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
            .map((row, rowIndex) => (
              <TableRow hover tabIndex={-1} key={rowIndex}>
                {columns
                  .filter((column) => !excludedColumns.includes(column.id))
                  .map((column) => (
                    <TableCell key={column.id} align={column.align}>
                      {String(row[column.id])}
                    </TableCell>
                  ))}
                <TableCell align="right">
                  <CustomDialog
                    type={type}
                    mode="edit"
                    data={row}
                    onSubmit={edit}/>
                </TableCell>
                <TableCell align="right">
                  <button onClick={() => {
                      if (type === 'colaborador') {
                        remove(row.id_colaborador)
                      }else{
                        remove(row.id)
                      }
                    }}><MdDelete/></button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  )
}
