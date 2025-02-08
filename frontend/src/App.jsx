import { Outlet } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import axiosInstance from "./utils/axiosInstance";
import { login, logout } from "./store/authSlice";

function App() {
  const dispatch = useDispatch();

  // verify token on refresh
  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        dispatch(logout());
      } else {
        try {
          const response = await axiosInstance.get("/verify-token", {
            headers: { "x-auth-token": token },
          });

          dispatch(
            login({
              token: response.data.token,
              user_id: response.data.user_id,
            })
          );
        } catch (error) {
          dispatch(logout());
          localStorage.removeItem("token");
        }
      }
    };

    verifyToken();
  }, []);

  return (
    <div className="container">
      <Navbar />
      <Outlet />
    </div>
  );
}

export default App;
