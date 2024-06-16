#!/bin/bash

# Установим переменные окружения для подключения к базе данных
DB_HOST=${POSTGRES_HOST}
DB_PORT=${POSTGRES_PORT}
DB_USER=${POSTGRES_USER}
DB_PASSWORD=${POSTGRES_PASSWORD}
DB_NAME=${POSTGRES_DB}

# Команда для проверки, пуста ли таблица
CHECK_DICT_TABLE_EMPTY="SELECT CASE WHEN EXISTS (SELECT 1 FROM public.dict) THEN 0 ELSE 1 END;"
CHECK_TURNOVER_TABLE_EMPTY="SELECT CASE WHEN EXISTS (SELECT 1 FROM public.turnover) THEN 0 ELSE 1 END;"
CHECK_CONTRACTS_TABLE_EMPTY="SELECT CASE WHEN EXISTS (SELECT 1 FROM public.contracts) THEN 0 ELSE 1 END;"

# Проверка, пуста ли таблица
DICT_TABLE_EMPTY=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "$CHECK_DICT_TABLE_EMPTY")
TURNOVER_TABLE_EMPTY=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "$CHECK_TURNOVER_TABLE_EMPTY")
CONTRACTS_TABLE_EMPTY=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "$CHECK_CONTRACTS_TABLE_EMPTY")

# Если таблица пуста, выполните загрузку данных
if [ "$DICT_TABLE_EMPTY" -eq 1 ]; then
  echo "Таблица dict пуста. Загружаем данные..."
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "\\copy public.dict (ste_name, characteristics_name, reference_price, final_category_directory, kpgz_code, kpgz, spgz_code, spgz, registry_number_rk) FROM '/scripts/dict.txt' DELIMITER E'\\t' ;"
  echo "Данные успешно загружены."
else
  echo "Таблица dict  уже содержит данные. Пропускаем загрузку."
fi


if [ "$TURNOVER_TABLE_EMPTY" -eq 1 ]; then
  echo "Таблица turnover пуста. Загружаем данные..."
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "\\copy public.turnover (product, code, unit_of_measurement, quantity_start_debit, balance_start_debit, quantity_turnover_debit, turnover_debit, quantity_turnover_credit, turnover_credit, quantity_end_debit, balance_end_debit, account_number, quarter_number, year) FROM '/scripts/turnover.txt' DELIMITER E'\\t' ;"
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "update public.turnover set institution_id=(select i.id from public.institution i order by i.id limit 1);"
  echo "Данные успешно загружены."
else
  echo "Таблица turnover уже содержит данные. Пропускаем загрузку."
fi

if [ "$CONTRACTS_TABLE_EMPTY" -eq 1 ]; then
  echo "Таблица contracts пуста. Загружаем данные..."
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "\\copy public.contracts (id_spgz, name_spgz, registry_number_rk, lot_number_procurement, ikz, customer, subject_gk_name, supplier_selection_method, contract_basis_single_supplier, contract_status, version_number, gk_price_rub, gk_price_at_signing_rub, paid_rub, paid_percent, final_kpgz_code, final_kpgz_name, contract_date, registration_date, last_change_date, execution_start_date, execution_end_date, contract_end_date, supplier_sme_status_at_contract_signing, supplier_region_name, law_basis_44_223, electronic_execution, fulfilled_by_supplier) FROM '/scripts/contracts.txt' DELIMITER E'\\t' ;"
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME --command "update public.contracts set institution_id=(select i.id from public.institution i order by i.id limit 1);"
  echo "Данные успешно загружены."
else
  echo "Таблица contracts уже содержит данные. Пропускаем загрузку."
fi