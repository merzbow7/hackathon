import { Flex, Space, Title, Loader, ScrollArea } from '@mantine/core';
import Layout from '../../layouts/BaseLayout';
import UserTable from './components/UserTable';
import { useAppSelector, useAppDispatch } from "../../store";
import { fetchInstitutions } from '../../store/institutionsSlice';
import { useEffect } from 'react';

export default function UsersPage() {
  const dispatch = useAppDispatch();
  const mounted = useAppSelector((state) => state.institutions.mounted);
  const loading = useAppSelector((state) => state.users.loading);
  useEffect(() => {
    if (!mounted) dispatch(fetchInstitutions());
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <Layout>
      <Flex direction="column" style={{height: 'calc(100vh - 100px)'}}>
        <Flex align="center"><Title order={2}>Пользователи { loading && <Loader color="green" size="sm" />}</Title></Flex>
        <Space h="md" />
        <UserTable />
      </Flex>
    </Layout>
  )
}