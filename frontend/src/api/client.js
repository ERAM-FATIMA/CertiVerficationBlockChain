import axios from "axios";

// very important, refer to read me file....
const api = axios.create({
  baseURL: "http://10.105.55.148:10000",    //very important... dont just blindly change..  trailing symbols like / very important
});

// Attach token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;