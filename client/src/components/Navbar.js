import { useState } from "react"
import logo from './star.png';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import {
   Link,
   useLocation
} from "react-router-dom";


const logoStyle = {
    maxWidth: '50px', // sets the maximum width of the logo
    height: 'auto', // maintains the aspect ratio of the logo
    verticalAlign: 'middle', // vertically aligns the logo with the text
  };

  
const links = [
    {
        name: "HOME",
        link: "/",
        id: "home",
        priority: false,
        transparant: true,
    },
    {
        name: "CREATE",
        link: "/create",
        id: "create",
        priority: false,
        transparant: true,
    },
    {
        name: "RECORD",
        link: "/record",
        id: "record",
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
    <header className="flex flex-col justify-center z-[99999999] min-h-[7vh] py-2 lg:py-4" 
    style={{
        background: 'linear-gradient(to right, rgba(0, 0, 0, 0.85), rgba(32, 32, 32, 0.95))', // Dark and less vibrant gradient
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)' // Adjusted for darker design
    }}
        >
            <div className="container px-4 mx-auto lg:flex lg:items-center">
                <div className="flex justify-between items-center">
                    <Link className="flex flex-row items-center gap-4" to="/">
                        <img src={logo} alt="Logo" style={logoStyle} /> {/* Apply the style to the image */}
                        <h2 className="text-white hover:text-gray-200 text-xl lg:text-2xl font-bold">NOSTALG.AI</h2>


                    </Link>
    
                    <button
                        className="border border-solid border-gray-200 px-3 py-1 rounded text-gray-200 opacity-50 hover:opacity-75 lg:hidden cursor-pointer"
                        aria-label="Menu"
                        data-test-id="navbar-menu"
                        onClick={() => setShowDropdown(!showDropdown)}
                    >
                        <FontAwesomeIcon icon="fa-solid fa-bars" style={{ color: '#ffffff' }} />
                    </button>
                </div>
    
                <div className={`${showDropdown ? "flex" : "hidden"} lg:flex flex-col lg:flex-row lg:ml-auto mt-3 lg:mt-0`} data-test-id="navbar">
                    <div>
                        {links.map(({ name, link, priority, id }) => 
                            <Link key={name}
                            className={`${priority ? "text-purple-900 hover:bg-purple-900 hover:text-pink-200 text-center border border-solid border-purple-900 mt-1 lg:mt-0 lg:ml-1" : "text-white text-2xl hover:bg-gray-200/25 hover:text-pink-200"} p-2 lg:px-4 lg:mx-2 rounded duration-300 transition-colors ${
                                pathname === link ? "text-pink-200 font-bold" : ""
                            }`}
                            
                                to={link}>
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