import { Loader, Text, Space, Button } from '@mantine/core';
import styles from './SyncPage.module.css';
import { useParams } from 'react-router-dom';
import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from "../../store";
import { bindUser } from '../../store/accountSlice';
import {
  IconMoodSad
} from '@tabler/icons-react';
export default function SyncPage() {
  const { code } = useParams();
  const openTG = () => window.open(import.meta.env.VITE_TELEGRAM_URL);

  const dispatch = useAppDispatch();
  const account = useAppSelector((state) => state.account);

  useEffect(() => {/* @ts-expect-error: Unreachable code error */
    if (code) dispatch(bindUser(code));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  console.log('account: ', account);

  return (
    <div className={styles.container}>
      { account.loading && <><Text
          size="xl"
          fw={900}
          variant="gradient"
          gradient={{ from: 'blue', to: 'blue', deg: 360 }}
        >
          Инизиализация
        </Text><Space h="lg" /><Loader color="blue" size={50} /></>}

      { account.isBind && <>
        <Text
          size="xl"
          fw={900}
          variant="gradient"
          gradient={{ from: 'indigo', to: 'teal', deg: 360 }}
        >
          Пользователь авторизован
        </Text>
        <Text fw={200}>вернуться к чат-боту</Text>
        <Space h="lg" />
        <Button onClick={openTG}>Перейти в телеграм</Button>
      </>}

      { account.error && <>
        <IconMoodSad color='red' size="4.2rem" />
        <Space h="lg" />
        <Text
          size="xl"
          fw={900}
          variant="gradient"
          gradient={{ from: 'red', to: 'red', deg: 360 }}
        >
          { account.error }
        </Text>
      </> }
    </div>
  )
}