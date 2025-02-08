import axios from "axios";
import store from "../store/store"; // Import Redux store
import { logout } from "../store/authSlice"; // Import logout action

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Global response interceptor to handle middleware errors
axiosInstance.interceptors.response.use(
  (response) => response, // If success, return response as it is
  (error) => {
    if (error.response) {
      if (error.response.error === 401 || error.response.error === 403) {
        // Middleware returned authentication error
        store.dispatch(logout()); // Logout user
        window.location.href = "/login"; // Redirect to login page
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
