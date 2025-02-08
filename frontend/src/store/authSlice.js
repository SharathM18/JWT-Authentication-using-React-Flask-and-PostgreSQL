import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  isAuthenticated: false,
  user_id: null,
  token: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login: (state, action) => {
      state.isAuthenticated = true;
      state.token = action.payload.token;
      state.user_id = action.payload.user_id;
    },

    signup: (state, action) => {
      state.isAuthenticated = true;
      state.token = action.payload.token;
      state.user_id = action.payload.user_id;
    },

    logout: (state) => {
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      localStorage.removeItem("token");
    },
  },
});

export const { login, signup, logout } = authSlice.actions;
export default authSlice.reducer;
