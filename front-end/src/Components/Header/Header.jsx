import React, { useState } from 'react'
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

import SideBar from '../SideBar/SideBar.jsx';

import Config from '../../assets/Constants/Constant.jsx';

export default function Header() {
    const [title, setTitle] = useState(Config.Dashboard.title);



    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    
                    <SideBar setTitle={setTitle} />
                    
                    <Typography
                        variant="h6"
                        noWrap
                        component="div"
                        sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
                    >
                        {title}
                    </Typography>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
