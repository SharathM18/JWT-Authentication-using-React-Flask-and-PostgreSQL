import { NavLink } from "react-router-dom";
import "../style/navbar.css";
import { useSelector } from "react-redux";

const Navbar = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  const navbarItem = [
    {
      name: "Home",
      path: "/",
      visible: true,
    },
    {
      name: "Profile",
      path: "/profile",
      visible: isAuthenticated,
    },
    {
      name: "Login",
      path: "/login",
      visible: !isAuthenticated,
    },
    {
      name: "Signup",
      path: "/signup",
      visible: !isAuthenticated,
    },
  ];

  return (
    <header className="navbar_container">
      <nav className="nav_links">
        {navbarItem.map((item, idx) =>
          item.visible ? (
            <NavLink to={item.path} key={idx}>
              {item.name}
            </NavLink>
          ) : null
        )}
      </nav>
    </header>
  );
};

export default Navbar;
