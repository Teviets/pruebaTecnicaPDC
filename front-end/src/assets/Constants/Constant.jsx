import { MdDashboard } from "react-icons/md";
import { FaUserFriends } from "react-icons/fa";
import { IoBagSharp } from "react-icons/io5";
import { FaGlobeAmericas } from "react-icons/fa";
import { MdApartment } from "react-icons/md";
import { FaCity } from "react-icons/fa";
import Localidades from "../../Pages/Localidades/Localidades";

const Config = {
    Dashboard:{
        title: "Dashboard",
        path: "/",
        icon: <MdDashboard size={24} color="FFFFFF"/>
    },
    Colaboradores:{
        title: "Colaboradores",
        path: "/colaboradores",
        icon: <FaUserFriends size={24} color="FFFFFF"/>
    },
    Empresas:{
        title: "Empresas",
        path: "/empresas",
        icon: <IoBagSharp size={24} color="FFFFFF"/>
    },
    Localidades:{
        title: "Localidades",
        path: "/localidades",
        icon: <FaGlobeAmericas size={24} color="FFFFFF"/>,
    }
    
}

export default Config;