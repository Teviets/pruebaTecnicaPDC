import { Routes, Route } from 'react-router-dom';
import Config from "./assets/Constants/Constant.jsx";

import Dashboard from './Pages/Dashboard/Dashboard.jsx';
import Empresa from './Pages/Empresas/Empresa.jsx';
import Colaboradores from './Pages/Colaboradores/Colaboradores.jsx';
import Localidades from './Pages/Localidades/Localidades.jsx';

import Header from './Components/Header/Header.jsx';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="MainContent">
        <Routes>
          <Route path={Config.Dashboard.path} element={<Dashboard />} />
          <Route path={Config.Empresas.path} element={<Empresa />} />
          <Route path={Config.Colaboradores.path} element={<Colaboradores />} />
          <Route path={Config.Localidades.path} element={<Localidades />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
