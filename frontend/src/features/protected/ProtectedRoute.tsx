import { Outlet } from 'react-router-dom';
import { Center, Flex, Button } from '@mantine/core';
import UserService from "../../services/userService";

const ProtectedRoute = () => {
  const openTG = () => window.open(import.meta.env.VITE_TELEGRAM_URL);

  if (!UserService.isAdmin()) {
    return <Center h={300}>
    <Flex
      gap="sm"
      justify="center"
      align="center"
      direction="column"
      wrap="wrap"
    >
      <h1>Oops!</h1>
      <p>У вас не достаточно прав</p>
      <Button onClick={openTG}>Перейти в телеграм</Button>
    </Flex>
  </Center>;
  }

  return <Outlet />;
};

export default ProtectedRoute;