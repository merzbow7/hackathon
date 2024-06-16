import pandas as pd
import numpy as np
import re
import os

def replace_spgz(x):
    try:
        x = x.replace('Система пропускная автоматизированная', 'Система СКУД')
        x = x.replace('Система охранного телевидения', 'Система СОТ')
    except:
        pass
    return x

def rename_columns(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace(',', '')
    df.columns = df.columns.str.replace('.', '')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('(', '')
    df.columns = df.columns.str.replace(')', '')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace('^ +', '_')
    df.columns = df.columns.str.replace(' +$', '_')
    df.columns = df.columns.str.replace('^ +| +$', '_')
    df.columns = map(str.lower, df.columns)

    return df

def parse_turnover_21_101(f_path):

    df = pd.ExcelFile(f_path).parse(skiprows=[0,1,2,3,4,5,6], header=[0])
    last_idx = df[df['Счет'] == 'Итого'].index[0]
    df = df.iloc[:last_idx]

    cols_to_drop = []
    for col_name in df.columns:
        if sum(df[col_name].isna()) == df.shape[0]:
            cols_to_drop.append(col_name)

    df = df.drop(columns=cols_to_drop)

    df.columns = ['товар', 'код', 'показатели', 'сальдо_начало_дебет', 'сальдо_начало_кредит', 'обороты_дебет', 'обороты_кредит', 'сальдо_конец_дебет', 'сальдо_конец_кредит']
    df = df.drop(index=0)

    df['код'] = df['код'].to_list()[2:]+[np.NaN]*2
    df['количество_начало_дебет'] = df['сальдо_начало_дебет'].to_list()[1:]+[np.NaN]
    df['количество_начало_кредит'] = df['сальдо_начало_кредит'].to_list()[1:]+[np.NaN]
    df['количество_обороты_дебет'] = df['обороты_дебет'].to_list()[1:]+[np.NaN]
    df['количество_обороты_кредит'] = df['обороты_кредит'].to_list()[1:]+[np.NaN]
    df['количество_конец_дебет'] = df['сальдо_конец_дебет'].to_list()[1:]+[np.NaN]
    df['количество_конец_кредит'] = df['сальдо_конец_кредит'].to_list()[1:]+[np.NaN]

    df = df.dropna(subset=['код'])
    df = df.drop(columns=['показатели', 'сальдо_начало_кредит', 'количество_начало_кредит', 'сальдо_конец_кредит', 'количество_конец_кредит'])
    df['единица_измерения'] = '-'

    df = df.fillna(0)

    df = df.groupby(['товар', 'код', 'единица_измерения']).sum().reset_index()

    # заполняем информацию о номере квартала, года, счете
    filename = os.path.split(f_path)[1]
    pattern = r'сч\. (\d+) за (\d) кв\. (\d{4})г'
    match = re.search(pattern, filename)

    if match:
        # Извлекаем данные
        account = match.group(1)
        quarter = match.group(2)
        year = match.group(3)
    else:
        print('Не удалось извлечь информацию')

    df['номер_счета'] = int(account)
    df['номер_квартала'] = int(quarter)
    df['год'] = int(year)

    return df

def parse_turnover_105(f_path):
    df = pd.ExcelFile(f_path).parse().iloc[:,2:]
    df.columns = ['код', 'товар', 'единица_измерения', 'количество_начало_дебет', 'сальдо_начало_дебет', \
                'количество_обороты_дебет', 'обороты_дебет', 'количество_обороты_кредит', 'обороты_кредит', 'количество_конец_дебет', 'сальдо_конец_дебет']
    df = df.dropna(subset=['товар']).fillna(0)

    df = df.groupby(['товар', 'код', 'единица_измерения']).sum().reset_index()

    # заполняем информацию о номере квартала, года, счете
    filename = os.path.split(f_path)[1]
    pattern = r'сч\. (\d+) за (\d) кв\. (\d{4})г'
    match = re.search(pattern, filename)

    if match:
        # Извлекаем данные
        account = match.group(1)
        quarter = match.group(2)
        year = match.group(3)
    else:
        print('Не удалось извлечь информацию')

    df['номер_счета'] = int(account)
    df['номер_квартала'] = int(quarter)
    df['год'] = int(year)

    return df

def processing_contracts(df_contracts):
    df_contracts = rename_columns(df_contracts)

    df_contracts['дата_заключения'] = pd.to_datetime(df_contracts['дата_заключения'], format='%d.%m.%Y')
    df_contracts['дата_регистрации'] = pd.to_datetime(df_contracts['дата_регистрации'], format='%d.%m.%Y')
    df_contracts['дата_последнего_изменения'] = pd.to_datetime(df_contracts['дата_последнего_изменения'], format='%d.%m.%Y')
    df_contracts['срок_исполнения_с'] = pd.to_datetime(df_contracts['срок_исполнения_с'], format='%d.%m.%Y')
    df_contracts['срок_исполнения_по'] = pd.to_datetime(df_contracts['срок_исполнения_по'], format='%d.%m.%Y')
    df_contracts['дата_окончания_срока_действия'] = pd.to_datetime(df_contracts['дата_окончания_срока_действия'], format='%d.%m.%Y')

    df_contracts['наименование_спгз'] = df_contracts['наименование_спгз'].apply(replace_spgz)

    df_contracts = df_contracts[(df_contracts['статус_контракта'] != 'Исполнение') & (df_contracts['статус_контракта'] != 'Расторгнут') & (df_contracts['статус_контракта'] != 'Согласование')]
    df_contracts = df_contracts.dropna(subset = ['реестровый_номер_в_рк'])

    return df_contracts


def processing_directory(df_directory):
    df_directory = rename_columns(df_directory)
    df_directory = df_directory.dropna(subset = ['название_сте'])

    return df_directory


