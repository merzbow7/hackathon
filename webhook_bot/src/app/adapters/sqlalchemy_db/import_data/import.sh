#!/bin/bash

# Установим переменные окружения для подключения к базе данных
DB_HOST=${POSTGRES_HOST}
DB_PORT=${POSTGRES_PORT}
DB_USER=${POSTGRES_USER}
DB_PASSWORD=${POSTGRES_PASSWORD}
DB_NAME=${POSTGRES_DB}

# Команда для проверки, пуста ли таблица
CHECK_DICT_TABLE_EMPTY="SELECT CASE WHEN EXISTS (SELECT 1 FROM public.dict) THEN 0 ELSE 1 END;"

# Проверка, пуста ли таблица
DICT_TABLE_EMPTY=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "$CHECK_DICT_TABLE_EMPTY")

# Если таблица пуста, выполните загрузку данных
if [ "$DICT_TABLE_EMPTY" -eq 1 ]; then
  echo "Таблица пуста. Загружаем данные..."
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "\\copy public.dict (ste_name, characteristics_name, reference_price, final_category_directory, kpgz_code, kpgz, spgz_code, spgz, registry_number_rk) FROM '/scripts/dict.txt' DELIMITER E'\\t' ;"
  echo "Данные успешно загружены."
else
  echo "Таблица уже содержит данные. Пропускаем загрузку."
fi
