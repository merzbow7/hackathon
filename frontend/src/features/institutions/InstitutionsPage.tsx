import { Button, Flex, Space, Title, Loader, Modal, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import InstitutionsTable from './components/InstitutionsTable';
import { useAppDispatch, useAppSelector } from "../../store";
import Layout from '../../layouts/BaseLayout';
import { useDisclosure } from '@mantine/hooks';
import { addInstitution } from '../../store/institutionsSlice';

export default function InstitutionPage() {
  const dispatch = useAppDispatch();
  const loading = useAppSelector((state) => state.institutions.loading);
  const [opened, { open, close }] = useDisclosure(false);

  const form = useForm({
    initialValues: {
      name: '',
    },
  });

  const add = () => {
    if (!form.values.name) return; /* @ts-expect-error: Unreachable code error */
    dispatch(addInstitution(form.values.name));
    close();
  }

  return (
    <Layout>
      <>
      <Flex direction="column">
        <Flex justify='space-between'>
            <Title order={2}>Учреждения  { loading && <Loader color="green" size="sm" />}</Title>
            <Button onClick={open}>Добавить</Button>
        </Flex>
        <Space h="md" />
        <InstitutionsTable/>
      </Flex>

      <Modal opened={opened} onClose={close} title="Создать учреждение">
        <TextInput
          key={form.key('name')}
          {...form.getInputProps('name')}
          label="Наименование учреждения"
          placeholder='Введите название'
        />
        <Space h="md" />
        <Flex justify='flex-end'>
          <Button color='green' onClick={add}>Добавить</Button>
        </Flex>
      </Modal>
      </>
    </Layout>
  )
}