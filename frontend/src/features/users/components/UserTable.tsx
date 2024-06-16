import { useEffect } from "react";
import { fetchUsers } from '../../../store/usersSlice';
import {Table, Pill } from '@mantine/core';
import { useAppDispatch, useAppSelector } from "../../../store";
import UserMenu from './UserMenu';

export default function UserTable() {
  const dispatch = useAppDispatch();
  const items = useAppSelector((state) => state.users.items);

  useEffect(() => {
    dispatch(fetchUsers());
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const rows = items.map((user) => (
    <Table.Tr key={user.id}>
      <Table.Td>{user.first_name + ' ' + user.last_name}</Table.Td>
      <Table.Td>{user.telegram_id}</Table.Td>
      <Table.Td><Pill size="md">{user.institution?.name}</Pill></Table.Td>
      <Table.Td>
        <UserMenu userId={user.id}/>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Table.ScrollContainer minWidth={500}>
      <Table horizontalSpacing="lg" verticalSpacing="sm" highlightOnHover stickyHeader striped>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Имя</Table.Th>
            <Table.Th>Telegram Id</Table.Th>
            <Table.Th>Учреждение</Table.Th>
            <Table.Th style={{width: '60px'}}></Table.Th>
          </Table.Tr>
        </Table.Thead><Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Table.ScrollContainer>
  )
}