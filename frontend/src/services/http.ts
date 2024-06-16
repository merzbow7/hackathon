import axios from "axios";
import UserService from "./userService";

const baseURL = import.meta.env.VITE_API_URL;

const http = axios.create({ baseURL });

/* @ts-expect-error: Unreachable code error */
http.interceptors.request.use((config) => {
  if (UserService.isLoggedIn()) {
    const cb = () => {
      config.headers.Authorization = `Bearer ${UserService.getToken()}`;
      return Promise.resolve(config);
    };
    return UserService.updateToken(cb);
  }
});

export default http;