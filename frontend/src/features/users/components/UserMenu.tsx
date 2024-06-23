import { useDisclosure } from '@mantine/hooks';
import { useForm } from '@mantine/form';
import { Menu, ActionIcon, rem, Modal, Text, Select, Button, Flex, Space } from '@mantine/core';
import {
  IconDots,
  IconSettings,
  IconTrash,
} from '@tabler/icons-react';
import { modals } from '@mantine/modals';
import { useAppDispatch, useAppSelector } from "../../../store";
import { updateInstitution, deleteUser } from '../../../store/usersSlice';

export default function UserMenu({ userId }: { userId: string | number}) {
  const [institutionOpened, institutionCallbacks] = useDisclosure(false);
  const dispatch = useAppDispatch();
  const institutions = useAppSelector((state) => state.institutions.items.map((item) => ({
    value: item.id.toString(),
    label: item.name,
  })));

  const form = useForm({
    initialValues: {
      institutionId: '',
    },
  });

  const openDeleteModal = () => modals.openConfirmModal({
    title: 'Подтверждение удаления',
    children: (
      <Text size="sm">
        Вы действительно хотите удалить пользователя?
      </Text>
    ),
    labels: { confirm: 'Удалить', cancel: 'Отменить' },
    confirmProps: { color: 'red' },
    onCancel: () => console.log('Cancel'),
    onConfirm: () => dispatch(deleteUser(userId)),
  });

  const updateUserInstitution = () => {
    dispatch(updateInstitution({
      userId, institutionId: form.values.institutionId
    }));
    institutionCallbacks.close();
  };

  return (
    <>
      <Modal opened={institutionOpened} onClose={institutionCallbacks.close} title="Выберите учреждение">
        <Select
          label="Учреждение"
          placeholder='Введите наименование'
          data={institutions}
          clearable
          key={form.key('institutionId')}
          {...form.getInputProps('institutionId')}
        />
        <Space h="md" />
        <Flex justify='flex-end'>
          <Button color='green' onClick={updateUserInstitution}>Применить</Button>
        </Flex>
      </Modal>

      <Menu shadow="md" width={250}>
        <Menu.Target>
          <ActionIcon size="sm" variant="outline" aria-label="Settings">
            <IconDots size="1rem" />
          </ActionIcon>
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Операции</Menu.Label>
          <Menu.Item
            leftSection={<IconSettings style={{ width: rem(14), height: rem(14) }} />}
            onClick={institutionCallbacks.open}
          >
            Установить учреждение
          </Menu.Item>

          <Menu.Divider />
          <Menu.Item
            color="red"
            leftSection={<IconTrash style={{ width: rem(14), height: rem(14) }} />}
            onClick={openDeleteModal}
          >
            Удалить
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
    </>
  )
}