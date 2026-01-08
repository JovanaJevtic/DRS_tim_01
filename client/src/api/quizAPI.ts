import axios from "axios";

const quizApi = axios.create({
  baseURL: import.meta.env.VITE_QUIZ_API || "http://localhost:5001/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});


quizApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default quizApi;
