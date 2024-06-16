import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

reverse_column_mapping_directory = {
    'ste_name': 'название_сте',
    'characteristics_name': 'наименование_характеристик',
    'reference_price': 'рефцена',
    'final_category_directory': 'конечную_категорию_справочника',
    'kpgz_code': 'кпгз_код',
    'kpgz': 'кпгз',
    'spgz_code': 'спгз_код',
    'spgz': 'спгз',
    'registry_number_rk': 'реестровый_номер_в_рк'
}

reverse_column_mapping_contracts = {
    'id_spgz': 'id_спгз',
    'name_spgz': 'наименование_спгз',
    'registry_number_rk': 'реестровый_номер_в_рк',
    'lot_number_procurement': 'номер_лота_в_закупке',
    'ikz': 'икз',
    'customer': 'заказчик',
    'subject_gk_name': 'наименование_предмет_гк',
    'supplier_selection_method': 'способ_определения_поставщика',
    'contract_basis_single_supplier': 'основание_заключения_контракта_с_ед__поставщиком',
    'contract_status': 'статус_контракта',
    'version_number': '№_версии',
    'gk_price_rub': 'цена_гк_руб',
    'gk_price_at_signing_rub': 'цена_гк_при_заключении_руб',
    'paid_rub': 'оплачено_руб',
    'paid_percent': 'оплачено_%',
    'final_kpgz_code': 'конечный_код_кпгз',
    'final_kpgz_name': 'конечное_наименование_кпгз',
    'contract_date': 'дата_заключения',
    'registration_date': 'дата_регистрации',
    'last_change_date': 'дата_последнего_изменения',
    'execution_start_date': 'срок_исполнения_с',
    'execution_end_date': 'срок_исполнения_по',
    'contract_end_date': 'дата_окончания_срока_действия',
    'supplier_sme_status_at_contract_signing': 'принадлежность_поставщика_к_мсп_на_момент_заключения_гк',
    'supplier_region_name': 'наименование_субъекта_рф_поставщика',
    'law_basis_44_223': 'закон_основание_44_223',
    'electronic_execution': 'электронное_исполнение',
    'fulfilled_by_supplier': 'исполнено_поставщиком'
}

reverse_column_mapping_turnover = {
    'product': 'товар',
    'code': 'код',
    'unit_of_measurement': 'единица_измерения',
    'quantity_start_debit': 'количество_начало_дебет',
    'balance_start_debit': 'сальдо_начало_дебет',
    'quantity_turnover_debit': 'количество_обороты_дебет',
    'turnover_debit': 'обороты_дебет',
    'quantity_turnover_credit': 'количество_обороты_кредит',
    'turnover_credit': 'обороты_кредит',
    'quantity_end_debit': 'количество_конец_дебет',
    'balance_end_debit': 'сальдо_конец_дебет',
    'account_number': 'номер_счета',
    'quarter_number': 'номер_квартала',
    'year': 'год',
}


def sentence_similarity(sentence1, sentence2):
    # Создаем объект TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Преобразуем предложения в TF-IDF матрицу
    tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])

    # Вычисляем косинусное сходство между двумя векторами
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity


def prepare_regular_items_dataframe(df_contracts):
    spgz_unique_list = []
    for spgz_name in df_contracts['наименование_спгз'].unique():
        df_tmp = df_contracts[df_contracts['наименование_спгз'] == spgz_name]
        if df_tmp['дата_заключения'].dt.year.nunique() > 1 or (
            df_tmp['дата_заключения'].dt.year.astype('str') + df_tmp['дата_заключения'].dt.month.astype(
            'str')).nunique() >= 4:
            spgz_unique_list.append(spgz_name)

    df_contracts_regular = df_contracts[df_contracts['наименование_спгз'].isin(spgz_unique_list)]

    return df_contracts_regular


def prepare_final_remainders_dataframe(df_turnover_total):
    df_turnover_last_year = df_turnover_total[df_turnover_total['год'] == df_turnover_total['год'].max()]
    df_remainders_final = df_turnover_last_year[
        df_turnover_last_year['номер_квартала'] == df_turnover_last_year['номер_квартала'].max()]
    df_remainders_final = df_remainders_final[df_remainders_final['количество_конец_дебет'] > 0]

    return df_remainders_final


def item_parts_in_true_item_name(user_item_name, table_item_name):
    item_parts_list = user_item_name.lower().split(' ')
    res = True
    for part in item_parts_list:
        res = res and (part in table_item_name.lower())

    return res


def is_item_regular(df_contracts, df_directory, user_item_name):
    df_contracts_regular = prepare_regular_items_dataframe(df_contracts)

    df_directory['реестровый_номер_в_рк'] = df_directory['реестровый_номер_в_рк'].astype(int)
    df_contracts_regular['реестровый_номер_в_рк'] = df_contracts_regular['реестровый_номер_в_рк'].astype(int)

    df_merged = pd.merge(df_contracts_regular, df_directory, left_on=['реестровый_номер_в_рк', 'конечный_код_кпгз'],
                         right_on=['реестровый_номер_в_рк', 'кпгз_код'])

    is_in_detailed_names = np.any(
        df_merged.apply(lambda x: item_parts_in_true_item_name(user_item_name, x['название_сте']), axis=1).values)
    is_in_common_names = np.any(
        df_contracts_regular.apply(lambda x: item_parts_in_true_item_name(user_item_name, x['наименование_спгз']),
                                   axis=1).values)
    is_regular = is_in_detailed_names or is_in_common_names

    return is_regular


def find_remainders_by_item_name(df_remainders_total, item_name):
    cols_to_leave = ['товар', 'единица_измерения', 'количество_конец_дебет']

    df_remainders = df_remainders_total[
        df_remainders_total.apply(lambda x: item_parts_in_true_item_name(item_name, x['товар']), axis=1)][cols_to_leave]
    df_remainders = df_remainders.sort_values('количество_конец_дебет', ascending=False)
    df_remainders = df_remainders.rename(columns={'количество_конец_дебет': 'количество'})
    return df_remainders


def processing_user_request_remainders(df_turnover_total, user_item_name):
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

    df_remainders_total = prepare_final_remainders_dataframe(df_turnover_total)

    df_remainders = find_remainders_by_item_name(df_remainders_total, user_item_name)

    if df_remainders.shape[0] == 0:
        output_str = 'На складе не обнаружено товаров, подходящих под описание "{}" (состояние на конец {} квартала {} года)'. \
            format(user_item_name, df_remainders_total['номер_квартала'].unique()[0],
                   df_remainders_total['год'].unique()[0])
        res = (1, output_str)
        return res

    else:
        output_str = 'Остатки по всем товарам, подходящим под описание "{}", приведены в таблице на рисунке выше (состояние на конец {} квартала {} года)'. \
            format(user_item_name, df_remainders_total['номер_квартала'].unique()[0],
                   df_remainders_total['год'].unique()[0])

        # # Render the table
        # fig, ax = plt.subplots(figsize=(15, 7))
        # ax.axis('tight')
        # ax.axis('off')
        # ax.table(cellText=df_remainders.values, colLabels=df_remainders.columns, loc='center')
        # Save the table as an image file
        # plt.savefig('df_remainders.png')
        # plt.close(fig)

        res = (0, output_str, df_remainders)
        return res


def processing_user_request_time_to_finish_check(df_contracts, df_directory, df_turnover_total, user_item_name):
    df_contracts = df_contracts.copy().rename(columns=reverse_column_mapping_contracts)
    df_directory = df_directory.copy().rename(columns=reverse_column_mapping_directory)
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

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
        output_str = 'Этот товар закупается регулярно, но у меня недостаточно данных в оборотных ведомостях за {} год(ы)'.format(
            df_turnover_total['год'].unique())
        res = (1, output_str)
        return res

    output_str = 'По Вашему запросу в оборотной ведомости за {} год(ы) были найдены следующие товары, подходящие под описание (для оценки скорости расходования товаров):\n'.format(
        df_turnover_total['год'].unique())
    output_str += '\n'.join(items_list)
    # output_str += '\n\nПодходят ли эти товары под Ваш запрос? Или Вы хотели бы его скорректировать?'

    # на выбор две кнопки - "товары подходят, продолжаем" или "скорректировать запрос"

    res = (0, output_str, items_list)
    return res


def processing_user_request_time_to_finish(df_turnover_total, user_item_name, items_list):
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

    df_remainders_total = prepare_final_remainders_dataframe(df_turnover_total)

    df_tmp = df_turnover_total[df_turnover_total['товар'].isin(items_list)][
        ['товар', 'единица_измерения', 'количество_обороты_кредит', 'номер_квартала', 'год']]

    df_tmp['товар'] = user_item_name

    df_tmp = df_tmp.groupby(['товар', 'номер_квартала', 'год']).sum().reset_index()

    df_tmp['товар'] = df_tmp['товар'] + '\n' + 'квартал: ' + df_tmp['номер_квартала'].astype(str) + '\n' + 'год: ' + \
                      df_tmp['год'].astype(str)

    df_tmp = df_tmp[['товар', 'количество_обороты_кредит']].rename(columns={'количество_обороты_кредит': 'количество'})

    df_remainders = find_remainders_by_item_name(df_remainders_total, user_item_name)

    V = df_tmp['количество'].mean()

    if V == 0:
        output_str = 'Данные по расходам для этих товаров в оборотных ведомостях за {} год(ы) не найдены'.format(
            df_turnover_total['год'].unique())
        res = (1, output_str)
        return res

    T = df_remainders['количество'].sum() / V * 3

    output_str = 'Данные по расходам для этих товаров приведены на диаграмме\n'

    # fig, ax = plt.subplots()
    # sns.barplot(df_tmp, x="количество", y="товар", ax=ax)
    # plt.grid()
    # plt.close(fig)

    output_str += '\nСредняя скорость расхода товара "{}" составляет {} единиц в квартал.\nИсходя из этого, оставшегося на складе товара хватит на {:0.2f} месяцев'.format(
        user_item_name, V, T)

    res = (0, output_str, df_tmp)
    return res


def processing_user_request_how_many(time_period, df_turnover_total, user_item_name, items_list):
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

    output_str = 'По Вашему запросу в оборотной ведомости за {} год(ы) были найдены следующие товары, подходящие под описание:\n'.format(
        df_turnover_total['год'].unique())
    output_str += '\n'.join(items_list)

    output_str += '\n\nДанные по закупкам и расходам для этих товаров приведены на диаграмме\n'

    df_tmp = df_turnover_total[df_turnover_total['товар'].isin(items_list)][
        ['товар', 'единица_измерения', 'обороты_дебет', 'количество_обороты_дебет', 'количество_обороты_кредит',
         'номер_квартала', 'год']]

    df_tmp['товар'] = user_item_name
    df_tmp = df_tmp.sort_values(['год', 'номер_квартала'])

    df_tmp = df_tmp.groupby(['товар', 'номер_квартала', 'год']).sum().reset_index()

    df_tmp['товар'] = df_tmp['товар'] + '\n' + 'квартал: ' + df_tmp['номер_квартала'].astype(str) + '\n' + 'год: ' + \
                      df_tmp['год'].astype(str)

    df_tmp1 = df_tmp[['товар', 'количество_обороты_дебет']].rename(columns={'количество_обороты_дебет': 'количество'})
    df_tmp1['type'] = 'закуплено'
    df_tmp2 = df_tmp[['товар', 'количество_обороты_кредит']].rename(columns={'количество_обороты_кредит': 'количество'})
    df_tmp2['type'] = 'израсходовано'
    df_tmp_res = pd.concat([df_tmp1, df_tmp2])

    years_list = list(df_turnover_total[df_turnover_total['количество_обороты_дебет'] != 0]['год'].unique())
    count_year = df_tmp['количество_обороты_дебет'].sum() / len(years_list)

    df_tmp_cut = df_tmp[df_tmp['количество_обороты_дебет'] != 0]
    start_point = 1  # min(3, df_tmp_cut.shape[0])
    price_for_item = (df_tmp_cut.iloc[-start_point:]['обороты_дебет'] / df_tmp_cut.iloc[-start_point:][
        'количество_обороты_дебет']).mean()

    total_volume = time_period * count_year
    total_price = time_period * count_year * price_for_item

    output_str += '\nПо данным за {} год(ы) товар "{}" закупался в количестве {} единиц в год.'.format(years_list,
                                                                                                       user_item_name,
                                                                                                       count_year)
    # output_str += '\nПо данным последних кварталов средняя стоимость одной единицы товара составила {:0.2f} рублей'.format(price_for_item)
    output_str += '\nПо данным последней закупки средняя стоимость одной единицы товара составила {:0.2f} рублей'.format(
        price_for_item)
    output_str += '\nЕсли количество сотрудников не изменится, то на {} лет необходимо закупить {:0.1f} единиц товара общей стоимостью порядка {:0.2f} рублей'.format(
        time_period, total_volume, total_price)

    # fig, ax = plt.subplots()
    # sns.barplot(df_tmp_res, x="количество", y="товар", hue='type', ax=ax)
    # plt.grid()
    # plt.close(fig)

    res = (0, output_str, df_tmp_res, total_volume, total_price)
    return res


def processing_json_calc_volume(time_period, df_contracts, df_directory, df_turnover_total, user_item_name):
    df_contracts = df_contracts.copy().rename(columns=reverse_column_mapping_contracts)
    df_directory = df_directory.copy().rename(columns=reverse_column_mapping_directory)
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

    is_regular = is_item_regular(df_contracts, df_directory, user_item_name)

    if not is_regular:
        items_list = []
        for item in df_turnover_total['товар'].unique():
            if item_parts_in_true_item_name(user_item_name.lower(), item):
                items_list.append(item)

        items_list_contracts_spgz = []
        for item in df_contracts['наименование_спгз'].unique():
            if item_parts_in_true_item_name(user_item_name.lower(), item):
                items_list_contracts_spgz.append(item)

        if len(items_list) == 0 and len(items_list_contracts_spgz) == 0:
            df_merged = pd.merge(df_contracts, df_directory, left_on=['реестровый_номер_в_рк', 'конечный_код_кпгз'],
                                 right_on=['реестровый_номер_в_рк', 'кпгз_код'])
            items_list_contracts_ste = []
            for item in df_merged['название_сте'].unique():
                if item_parts_in_true_item_name(user_item_name.lower(), item):
                    items_list_contracts_ste.append(item)

    if is_regular:
        res = processing_user_request_time_to_finish_check(df_contracts, df_directory, df_turnover_total,
                                                           user_item_name)
        if res[0] == 1:
            output_str = res[1]
            output_str += '\nУ меня недостаточно данных для формирования прогноза на закупку. Тем не менее, я могу помочь с составлением json, если Вы укажете объем закупки и общую стоимость товаров'
            res = (2, output_str)
            return res

        else:
            output_str1 = res[1]
            items_list = res[2]

            # здесь должна быть возможность скорректировать запрос на товары
            res = processing_user_request_how_many(time_period, df_turnover_total, user_item_name, items_list)
            return res

    # если вообще нигде не нашли этот товар
    elif len(items_list) == 0 and len(items_list_contracts_spgz) == 0 and len(items_list_contracts_ste) == 0:
        output_str = 'К сожалению, я не смог найти информацию по товару для формирования json. Вы можете ввести все данные самостоятельно'
        res = (1, output_str)
        return res

    else:
        output_str = 'У меня недостаточно данных для формирования прогноза на закупку. Тем не менее, я могу помочь с составлением json, если Вы укажете объем закупки и общую стоимость товаров'
        res = (2, output_str)
        return res


def prepare_json(df_turnover_total, df_contracts, df_directory, user_item_name, total_volume, total_price):
    df_contracts = df_contracts.copy().rename(columns=reverse_column_mapping_contracts)
    df_directory = df_directory.copy().rename(columns=reverse_column_mapping_directory)
    df_turnover_total = df_turnover_total.copy().rename(columns=reverse_column_mapping_turnover)

    json_dict = {}

    items_list = []
    for item in df_turnover_total['товар'].unique():
        if item_parts_in_true_item_name(user_item_name.lower(), item):
            items_list.append(item)

    df_contracts_cut = df_contracts[
        df_contracts['реестровый_номер_в_рк'].isin(df_directory['реестровый_номер_в_рк'].unique())]
    df_contracts_other = df_contracts[
        ~df_contracts['реестровый_номер_в_рк'].isin(df_directory['реестровый_номер_в_рк'].unique())]
    df_contracts_other['название_сте'] = df_contracts_other['наименование_спгз']
    df_merged = pd.merge(df_contracts_cut, df_directory, left_on=['реестровый_номер_в_рк', 'конечный_код_кпгз'],
                         right_on=['реестровый_номер_в_рк', 'кпгз_код'])

    df_merged['detailed'] = 1
    df_contracts_other['detailed'] = 0

    df_contracts_total = pd.concat([df_merged, df_contracts_other])
    df_contracts_total = df_contracts_total.sort_values('дата_заключения')
    df_contracts_total.index = range(df_contracts_total.shape[0])

    series_res = df_contracts_total['название_сте'].apply(
        lambda x: sentence_similarity(x.lower(), user_item_name.lower())) + df_contracts_total[
                     'наименование_предмет_гк'].apply(lambda x: sentence_similarity(x.lower(), user_item_name.lower()))
    idxmax = series_res.idxmax()
    json_dict['delivery_time'] = \
        (df_contracts_total['срок_исполнения_по'] - df_contracts_total['срок_исполнения_с']).dt.days[idxmax]
    json_dict['deliveryAmount'] = total_volume
    json_dict['entityId'] = df_contracts_total.loc[idxmax, 'id_спгз']
    json_dict['id'] = df_contracts_total.loc[idxmax, 'id_спгз']
    json_dict['nmc'] = total_price
    json_dict['purchaseAmount'] = total_volume
    json_dict['spgzCharacteristics_kpgzCharacteristicId'] = df_contracts_total.loc[idxmax, 'конечный_код_кпгз']

    return json_dict
