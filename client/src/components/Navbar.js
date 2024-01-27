import { useState } from "react"
 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import {
   Link,
   useLocation
} from "react-router-dom";


const links = [
    {
        name: "Home",
        link: "/",
        id: "home",
        priority: false,
        transparant: true,
    },
    {
        name: "Create",
        link: "/create",
        id: "create",
        priority: false,
        transparant: true,
    },
]

   /*
   {
       name: "Sign Up",
       link: "/sign-up",
       id: "call-to-action",
       priority: true
   },
   */

 
const Navbar = () => {
   const [showDropdown, setShowDropdown] = useState(false);
   const { pathname } = useLocation();

   const [loggedIn, setLoggedIn] = useState(false)

   const handleClick = () => {
       setLoggedIn(!loggedIn)
   }

   return (
       <header className="border-[#130611] border-transparent border-solid border-2 flex flex-col justify-center bg-slate-800 z-[99999999] min-h-[7vh] py-2 lg:py-4">
           <div className="container px-4 mx-auto lg:flex lg:items-center m-30">
               <div className="flex justify-between items-center">
                   <Link className="flex flex-row items-center gap-4 font-bold text-2xl text-teal" to="/">
                       <h2 className="text-4xl text-white font-mono hover:text-gray-200">Name </h2>
                   </Link>
 
                   <button
                       className="border border-solid border-gray-200 px-3 py-1 rounded text-gray-200 opacity-50 hover:opacity-75 lg:hidden cursor-pointer"
                       aria-label="Menu"
                       data-test-id="navbar-menu"
                       onClick={
                           () => {
                               setShowDropdown(!showDropdown);
                           }}
                   >
                        <FontAwesomeIcon icon="fa-solid fa-bars" />
                   </button>
               </div>
 
               <div className={`${showDropdown ? "flex" : "hidden"} lg:flex flex-col lg:flex-row lg:ml-auto mt-3 lg:mt-0`} data-test-id="navbar">
                    <div>
                        {links.map(({ name, link, priority, id }) => 
                            <Link key={name} className={`${priority ? "text-purple-900 hover:bg-purple-900 hover:text-white text-center border border-solid border-purple-900 mt-1 lg:mt-0 lg:ml-1" : "text-white text-2xl hover:bg-gray-200/25 hover:text-gray-200"} p-2 lg:px-4 lg:mx-2 rounded duration-300 transition-colors ${pathname === name && "font-bold"}`} to={link}>
                                {name}
                            </Link>
                        )}

                    </div>
               </div>             
           </div>
       </header>
   )
}
 
export default Navbar;