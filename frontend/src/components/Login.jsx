import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import axiosInstance from "../utils/axiosInstance";
import { useDispatch } from "react-redux";
import { login } from "../store/authSlice";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";

const schema = z.object({
  email: z.string(),
  password: z.string(),
});

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data) => {
    try {
      const response = await axiosInstance.post("/auth/login", data);
      console.log(response.data);

      if (response.data) {
        localStorage.setItem("token", response.data.token);

        axiosInstance.defaults.headers.common["x-auth-token"] =
          response.data.token;

        dispatch(
          login({
            token: response.data.token,
            user_id: response.data.user_id,
          })
        );

        navigate("/");
      }
    } catch (error) {
      if (error.response) {
        setError(error.response.data.error);
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <>
      <h1>Login</h1>
      <div className="login_container">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="input_email">
            <label htmlFor="email">Email: </label>
            <input
              type="text"
              name="email"
              placeholder="example@example.com"
              {...register("email")}
            />
          </div>

          <div className="input_password">
            <label htmlFor="password">Password: </label>
            <input type="password" name="password" {...register("password")} />
          </div>

          <div className="submit_btn">
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Loading..." : "Login"}
            </button>
          </div>

          {error && (
            <div className="error_msg">
              <p>{error}</p>
            </div>
          )}
        </form>
        <div className="signup_link">
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </div>
      </div>
    </>
  );
};

export default Login;
