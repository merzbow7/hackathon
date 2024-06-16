import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def prepare_regular_items_dataframe(df_contracts):

    spgz_unique_list = []
    for spgz_name in df_contracts['наименование_спгз'].unique():
        df_tmp = df_contracts[df_contracts['наименование_спгз'] == spgz_name]
        if df_tmp['дата_заключения'].dt.year.nunique() > 1 or (df_tmp['дата_заключения'].dt.year.astype('str')+df_tmp['дата_заключения'].dt.month.astype('str')).nunique() >= 4:
            spgz_unique_list.append(spgz_name)

    df_contracts_regular = df_contracts[df_contracts['наименование_спгз'].isin(spgz_unique_list)]

    return df_contracts_regular


def prepare_final_remainders_dataframe(df_turnover_total):

    df_turnover_last_year = df_turnover_total[df_turnover_total['год'] == df_turnover_total['год'].max()]
    df_remainders_final = df_turnover_last_year[df_turnover_last_year['номер_квартала'] == df_turnover_last_year['номер_квартала'].max()]
    return df_remainders_final


def item_parts_in_true_item_name(user_item_name, table_item_name):
    item_parts_list = user_item_name.lower().split(' ')
    res = True
    for part in item_parts_list:
        res = res and (part in table_item_name.lower())
    
    return res

def is_item_regular(df_contracts, df_directory, user_item_name):

    df_contracts_regular = prepare_regular_items_dataframe(df_contracts)
    df_merged = pd.merge(df_contracts_regular, df_directory, left_on=['реестровый_номер_в_рк', 'конечный_код_кпгз'], right_on=['реестровый_номер_в_рк', 'кпгз_код'])

    is_in_detailed_names = np.any(df_merged.apply(lambda x: item_parts_in_true_item_name(user_item_name, x['название_сте']), axis=1).values)
    is_in_common_names = np.any(df_contracts_regular.apply(lambda x: item_parts_in_true_item_name(user_item_name, x['наименование_спгз']), axis=1).values)
    is_regular = is_in_detailed_names or is_in_common_names

    return is_regular

def find_remainders_by_item_name(df_remainders_total, item_name):

    cols_to_leave = ['товар', 'единица_измерения', 'количество_конец_дебет']

    df_remainders = df_remainders_total[df_remainders_total.apply(lambda x: item_parts_in_true_item_name(item_name, x['товар']), axis=1)][cols_to_leave]
    df_remainders = df_remainders.sort_values('количество_конец_дебет', ascending=False)
    df_remainders = df_remainders.rename(columns={'количество_конец_дебет':'количество'})
    return df_remainders


def processing_user_request_remainders(df_turnover_total, user_item_name):

    df_remainders_total = prepare_final_remainders_dataframe(df_turnover_total)

    df_remainders = find_remainders_by_item_name(df_remainders_total, user_item_name)

    if df_remainders.shape[0] == 0:
        output_str = 'На складе не обнаружено товаров, подходящих под описание "{}" (состояние на конец {} квартала {} года)'.\
            format(user_item_name, df_remainders_total['номер_квартала'].unique()[0], df_remainders_total['год'].unique()[0])
        res = (1, output_str)
        return res
        
    else:
        output_str = 'Остатки по всем товарам, подходящим под описание "{}", приведены в таблице на рисунке ниже (состояние на конец {} квартала {} года)'.\
            format(user_item_name, df_remainders_total['номер_квартала'].unique()[0], df_remainders_total['год'].unique()[0])

        # Render the table
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=df_remainders.values, colLabels=df_remainders.columns, loc='center')
        # Save the table as an image file
        # plt.savefig('df_remainders.png')
        plt.close(fig)

        res = (0, output_str, fig)
        return res
    
def processing_user_request_time_to_finish_check(df_contracts, df_directory, df_turnover_total, user_item_name):

    is_regular = is_item_regular(df_contracts, df_directory, user_item_name)

    if not is_regular:
        output_str = 'Этот товар не закупается регулярно, поэтому я не могу сделать выводы относительно него'
        res = (1, output_str)
        return res

    items_list = []
    for item in df_turnover_total['товар'].unique():
        if item_parts_in_true_item_name(user_item_name.lower(), item):
            items_list.append(item)

    if len(items_list) == 0:
        output_str = 'Этот товар закупается регулярно, но у меня недостаточно данных в оборотных ведомостях за {} год(ы)'.format(df_turnover_total['год'].unique())
        res = (1, output_str)
        return res

    output_str = 'По Вашему запросу в оборотной ведомости за {} год(ы) были найдены следующие товары, подходящие под описание (для оценки скорости расходования товаров):\n'.format(df_turnover_total['год'].unique())
    output_str += '\n'.join(items_list)
    output_str += '\n\nПодходят ли эти товары под Ваш запрос? Или Вы хотели бы его скорректировать?'

    # на выбор две кнопки - "товары подходят, продолжаем" или "скорректировать запрос"

    res = (0, output_str, items_list)
    return res


def processing_user_request_time_to_finish(df_turnover_total, user_item_name, items_list):

    df_remainders_total = prepare_final_remainders_dataframe(df_turnover_total)

    df_tmp = df_turnover_total[df_turnover_total['товар'].isin(items_list)][['товар','единица_измерения', 'количество_обороты_кредит', 'номер_квартала', 'год']]

    df_tmp['товар'] = user_item_name

    df_tmp = df_tmp.groupby(['товар', 'номер_квартала', 'год']).sum().reset_index()

    df_tmp['товар'] = df_tmp['товар'] + '\n' + 'квартал: ' + df_tmp['номер_квартала'].astype(str) + '\n' + 'год: ' + df_tmp['год'].astype(str)

    df_tmp = df_tmp[['товар','количество_обороты_кредит']].rename(columns={'количество_обороты_кредит':'количество'})

    df_remainders = find_remainders_by_item_name(df_remainders_total, user_item_name)

    V = df_tmp['количество'].mean()

    if V == 0:
        output_str = 'Данные по расходам для этих товаров в оборотных ведомостях за {} год(ы) не найдены'.format(df_turnover_total['год'].unique())
        res = (1, output_str)
        return res

    T = df_remainders['количество'].sum()/V*3

    output_str = 'Данные по расходам для этих товаров приведены на диаграмме\n'

    fig, ax = plt.subplots()
    sns.barplot(df_tmp, x="количество", y="товар", ax=ax)
    plt.grid()
    plt.close(fig)

    output_str += '\nСредняя скорость расхода товара "{}" составляет {} единиц в квартал.\nИсходя из этого, оставшегося на складе товара хватит на {:0.2f} месяцев'.format(user_item_name,V,T)

    res = (0, output_str, fig)
    return res


def processing_user_request_how_many(time_period, df_turnover_total, user_item_name, items_list):

    output_str = 'По Вашему запросу в оборотной ведомости за {} год(ы) были найдены следующие товары, подходящие под описание:\n'.format(df_turnover_total['год'].unique())
    output_str += '\n'.join(items_list)

    output_str += '\n\nДанные по закупкам и расходам для этих товаров приведены на диаграмме\n'


    df_tmp = df_turnover_total[df_turnover_total['товар'].isin(items_list)][['товар','единица_измерения','количество_обороты_дебет', 'количество_обороты_кредит', 'номер_квартала']]

    df_tmp['товар'] = user_item_name

    df_tmp = df_tmp.groupby(['товар', 'номер_квартала']).sum().reset_index()

    df_tmp['товар'] = df_tmp['товар'] + '\n' + 'квартал: ' + df_tmp['номер_квартала'].astype(str)

    df_tmp1 = df_tmp[['товар','количество_обороты_дебет']].rename(columns={'количество_обороты_дебет':'количество'})
    df_tmp1['type'] = 'закуплено'
    df_tmp2 = df_tmp[['товар','количество_обороты_кредит']].rename(columns={'количество_обороты_кредит':'количество'})
    df_tmp2['type'] = 'израсходовано'
    df_tmp_res = pd.concat([df_tmp1, df_tmp2])

    years_list = list(df_turnover_total['год'].unique())
    count_year = df_tmp['количество_обороты_дебет'].sum()/len(years_list)
    output_str += '\nПо данным за {} год(ы) товар "{}" закупался в количестве {} единиц в год.'.format(years_list,user_item_name, count_year)
    output_str += '\nЕсли количество сотрудников не изменится, то на {} лет необходимо закупить {:0.1f} единиц товара'.format(time_period,time_period*count_year)

    fig, ax = plt.subplots()
    sns.barplot(df_tmp_res, x="количество", y="товар", hue='type', ax=ax)
    plt.grid()
    plt.close(fig)

    res = (0, output_str, fig)
    return res
    