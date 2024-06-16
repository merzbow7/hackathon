import { AppShell, Burger, NavLink, Text, Avatar, Group, Menu, rem } from '@mantine/core';
import { IconCircleLetterG, IconUsers, IconServer, IconDoorExit, IconHomeMove } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from 'react-router-dom';
import UserService from "../services/userService";
import styles from './BaseLayout.module.css';
import { useMemo } from 'react';

export default function BaseLayout({ children }: { children: JSX.Element }) {
  const [opened, { toggle }] = useDisclosure();
  const navigate = useNavigate();
  const openKK = () => window.open(import.meta.env.VITE_KK_HOST);

  const userName = useMemo(() => UserService.getUsername(), [])

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 250,
        breakpoint: 'sm',
        collapsed: { mobile: !opened },
      }}
      padding="lg"
    >
      <AppShell.Header className={styles.header}>
        <Burger
          opened={opened}
          onClick={toggle}
          hiddenFrom="sm"
          size="sm"
        />

        <Group gap="xs">
          <IconServer />
          <Text visibleFrom="sm" fw={700}>Admin Panel</Text>
        </Group>

        <Menu shadow="md" width={250}>
          <Menu.Target>
            <Group gap="xs" style={{cursor: 'pointer'}}>
              <Text fw={400}>{userName}</Text>
              <Avatar radius="xl" />
            </Group>
          </Menu.Target>

          <Menu.Dropdown>
            <Menu.Item
              leftSection={<IconHomeMove style={{ width: rem(14), height: rem(14) }} />}
              onClick={openKK}
            >
              Перейти в Keycloak
            </Menu.Item>

            <Menu.Divider />
            <Menu.Item
              color="red"
              leftSection={<IconDoorExit style={{ width: rem(14), height: rem(14) }} />}
              onClick={() => UserService.doLogout()}
            >
              Выйти
            </Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </AppShell.Header>

      <AppShell.Navbar p="sm" className={styles.sidebar}>
        <NavLink
          label="Пользователи"
          leftSection={<IconUsers size="1.2rem" stroke={1.5} />}
          onClick={() => navigate('/')}
        />

        <NavLink
          label="Учреждения"
          leftSection={<IconCircleLetterG size="1.2rem" stroke={1.5} />}
          onClick={() => navigate('/institutions')}
        />
      </AppShell.Navbar>

      <AppShell.Main><main>{children}</main></AppShell.Main>
    </AppShell>
  )
}