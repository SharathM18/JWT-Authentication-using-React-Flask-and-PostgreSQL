import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import axiosInstance from "../utils/axiosInstance";
import { useDispatch } from "react-redux";
import { useState } from "react";
import { signup } from "../store/authSlice";

const schema = z.object({
  username: z.string(),
  email: z.string(),
  password: z.string(),
});

const Signup = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [error, setError] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data) => {
    try {
      const response = axiosInstance.post("/auth/signup", data);

      if (response.data) {
        localStorage.setItem("token", response.data.token);

        axiosInstance.defaults.headers.common["x-auth-token"] =
          response.data.token;

        dispatch(
          signup({ token: response.data.token, user_id: response.data.user_id })
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
      <h1>Signup</h1>
      <div className="signup_container">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="input_username">
            <label htmlFor="email">Username: </label>
            <input type="text" name="username" {...register("username")} />
          </div>

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
              {isSubmitting ? "Loading..." : "Signup"}
            </button>
          </div>

          {error && (
            <div className="error_msg">
              <p>{error}</p>
            </div>
          )}
        </form>

        <div className="login_link">
          Already have an account? <Link to="/login">Log In</Link>
        </div>
      </div>
    </>
  );
};

export default Signup;
