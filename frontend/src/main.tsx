import React from 'react'
import { Provider } from 'react-redux';
import { createRoot } from "react-dom/client";
import App from './App.tsx'
import UserService from "./services/userService";
import store from './store';
import './index.css'

const renderApp = () => createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App/>
    </Provider>
  </React.StrictMode>,
);

UserService.initKeycloak(renderApp);