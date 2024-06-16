import { useEffect } from "react";
import { fetchInstitutions } from '../../../store/institutionsSlice';
import { Table } from '@mantine/core';
import { useAppDispatch, useAppSelector } from "../../../store";

export default function InstitutionsTable() {
  const dispatch = useAppDispatch();
  const institutions = useAppSelector((state) => state.institutions.items);

  useEffect(() => {
    dispatch(fetchInstitutions());
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const rows = institutions.map((institution) => (
    <Table.Tr key={institution.id}>
      <Table.Td>{institution.id}</Table.Td>
      <Table.Td>{institution.name}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Table.ScrollContainer minWidth={500}>
      <Table horizontalSpacing="lg" verticalSpacing="sm" highlightOnHover stickyHeader striped>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Id</Table.Th>
            <Table.Th>Имя</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </Table.ScrollContainer>
  )
}