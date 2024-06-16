# Словари dict КПГЗ
from typing import Mapping

import pandas as pd

column_mapping_directory = {
    'название_сте': 'ste_name', 'наименование_характеристик': 'characteristics_name',
    'рефцена': 'reference_price', 'конечную_категорию_справочника': 'final_category_directory',
    'кпгз_код': 'kpgz_code', 'кпгз': 'kpgz', 'спгз_код': 'spgz_code',
    'спгз': 'spgz', 'реестровый_номер_в_рк': 'registry_number_rk'
}
# Контракты
column_mapping_contracts = {
    'id_спгз': 'id_spgz', 'наименование_спгз': 'name_spgz',
    'реестровый_номер_в_рк': 'registry_number_rk',
    'номер_лота_в_закупке': 'lot_number_procurement', 'икз': 'ikz', 'заказчик': 'customer',
    'наименование_предмет_гк': 'subject_gk_name',
    'способ_определения_поставщика': 'supplier_selection_method',
    'основание_заключения_контракта_с_ед__поставщиком': 'contract_basis_single_supplier',
    'статус_контракта': 'contract_status', '№_версии': 'version_number',
    'цена_гк_руб': 'gk_price_rub', 'цена_гк_при_заключении_руб': 'gk_price_at_signing_rub',
    'оплачено_руб': 'paid_rub', 'оплачено_%': 'paid_percent',
    'конечный_код_кпгз': 'final_kpgz_code',
    'конечное_наименование_кпгз': 'final_kpgz_name', 'дата_заключения': 'contract_date',
    'дата_регистрации': 'registration_date', 'дата_последнего_изменения': 'last_change_date',
    'срок_исполнения_с': 'execution_start_date', 'срок_исполнения_по': 'execution_end_date',
    'дата_окончания_срока_действия': 'contract_end_date',
    'принадлежность_поставщика_к_мсп_на_момент_заключения_гк': 'supplier_sme_status_at_contract_signing',
    'наименование_субъекта_рф_поставщика': 'supplier_region_name',
    'закон_основание_44_223': 'law_basis_44_223',
    'электронное_исполнение': 'electronic_execution',
    'исполнено_поставщиком': 'fulfilled_by_supplier'
}
# Оборотная ведомость
column_mapping_turnover = {
    'товар': 'product', 'код': 'code', 'единица_измерения': 'unit_of_measurement',
    'количество_начало_дебет': 'quantity_start_debit', 'сальдо_начало_дебет': 'balance_start_debit',
    'количество_обороты_дебет': 'quantity_turnover_debit', 'обороты_дебет': 'turnover_debit',
    'количество_обороты_кредит': 'quantity_turnover_credit', 'обороты_кредит': 'turnover_credit',
    'количество_конец_дебет': 'quantity_end_debit', 'сальдо_конец_дебет': 'balance_end_debit',
    'номер_счета': 'account_number', 'номер_квартала': 'quarter_number', 'год': 'year'
}


def make_turnover_df(rows: list[Mapping]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.rename(columns=column_mapping_turnover)


def make_contracts_df(rows: list[Mapping]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.rename(columns=column_mapping_contracts)


def make_directory_df(rows: list[Mapping]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.rename(columns=column_mapping_directory)
