import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import { ModalsProvider } from '@mantine/modals';
import { theme } from './theme';
import ErrorPage from './features/errors/ErrorPage'
import UsersPage from './features/users/UserPage';
import SyncPage from './features/sync/SyncPage';
import ProtectedRoute from './features/protected/ProtectedRoute';
import InstitutionsPage from './features/institutions/InstitutionsPage';
import '@mantine/core/styles.css';

const router = createBrowserRouter([{
  element: <ProtectedRoute />,
  errorElement: <ErrorPage />,
  children: [
    {
      path: '/',
      element: <UsersPage/>,
      errorElement: <ErrorPage />,
    },
    {
      path: '/institutions',
      element: <InstitutionsPage/>,
      errorElement: <ErrorPage />,
    }
  ]
} ,{
  path: '/sync/:code',
  element: <SyncPage/>,
  errorElement: <ErrorPage />,
}]);

const App = () => (
  <MantineProvider theme={theme}>
    <ModalsProvider>
      <RouterProvider router={router} />
    </ModalsProvider>
  </MantineProvider>
);

export default App;