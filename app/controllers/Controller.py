from genericpath import exists
import pandas as pd
import os
from datetime import datetime
import calendar

from utils.branches import get_branch_code

data_dir = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data"))

today = datetime.today()
filename = 'mock_revenue_{}_{}-{}.csv'.format("HN", today.month, today.year)

# if os.path.exists(os.path.join(data_dir, filename)):
#     print("exists")
# else:
# no_week = len(calendar.monthcalendar(today.year, today.month))
# column_names = ['revenue_target', 'revenue_source',
#                 'revenue_category', 'revenue_subcategory', 'revenue_detail']
# column_names.extend(['week{}'.format(x) for x in range(no_week)])

# revenue_data = [(156730, 'Trong Mobifone', 'Doanh thu ổn định, chuyển tiếp',
#                 'Tổng cuộc gọi được ĐTV trả lời', '', 28417, 0, 0, 0, 0),
#                 (70, 'Trong Mobifone', 'Doanh thu dịch vụ mới',
#                 'Cung cấp các sản phẩm, dịch vụ của MobiFone', 'Doanh thu dịch vụ MobiFone E-office', 0, 0, 0, 0, 0)]

# df_revenue = pd.DataFrame(revenue_data, columns=column_names)

# df_revenue.to_csv(os.path.join(data_dir, filename), index=False)


def insert(revenue_target):
    branch_filename = os.path.join(data_dir, 'mock_revenue_{}_{}-{}.csv'.format(
        get_branch_code(revenue_target["branch"]), today.month, today.year))
    df_revenue = pd.read_csv(os.path.join(data_dir, branch_filename))

    df_is_duplicated = df_revenue.loc[(df_revenue["revenue_target"] == revenue_target["value"]) & (df_revenue["revenue_source"] == revenue_target["revenue_source"]) &
                                      (df_revenue["revenue_category"] == revenue_target["revenue_category"]) & (df_revenue["revenue_subcategory"] == revenue_target["revenue_subcategory"]) & (df_revenue["revenue_detail"] == revenue_target["revenue_detail"])]
    if len(df_is_duplicated.index) == 0:
        data = {
            "revenue_source": revenue_target["revenue_source"],
            "revenue_category": revenue_target["revenue_category"],
            "revenue_subcategory": revenue_target["revenue_subcategory"] if revenue_target["revenue_subcategory"] != None else "",
            "revenue_detail": revenue_target["revenue_detail"] if revenue_target["revenue_detail"] != None else "",
            "revenue_target": revenue_target["value"],
        }
        df_insert_data = pd.DataFrame([data])
        df_revenue = pd.concat([df_revenue, df_insert_data], ignore_index=True)

        column_names = get_column_names()
        df_insert_data = df_revenue.reindex(columns=column_names)
        df_insert_data = df_insert_data.fillna(0)
    else:
        raise Exception('duplicated')
    try:
        df_revenue.to_csv(os.path.join(data_dir, branch_filename), index=False)
        return True
    except Exception:
        return False


def update(revenue_target):
    df_revenue = pd.read_csv(os.path.join(data_dir, 'mock_revenue_{}_{}-{}.csv'.format(
        get_branch_code(revenue_target['branch']), today.month, today.year)))
    df_revenue = df_revenue.fillna("")
    data = {
        "revenue_source": revenue_target["revenue_source"],
        "revenue_category": revenue_target["revenue_category"],
        "revenue_subcategory": revenue_target["revenue_subcategory"] if revenue_target["revenue_subcategory"] != None else "",
        "revenue_detail": revenue_target["revenue_detail"] if revenue_target["revenue_detail"] != '0' else "",
        "revenue_target": float(revenue_target["revenue_target"]),
    }
    for key in revenue_target.keys():
        if 'week' in key:
            data[key] = revenue_target[key]
    df_revenue.loc[(df_revenue["revenue_target"] == float(revenue_target["revenue_target"])) &
                   (df_revenue["revenue_source"] == revenue_target["revenue_source"]) &
                   (df_revenue["revenue_category"] == revenue_target["revenue_category"]) &
                   (df_revenue["revenue_subcategory"] == revenue_target["revenue_subcategory"]) &
                   (df_revenue["revenue_detail"] == revenue_target["revenue_detail"])] = data.values()
    column_names = get_column_names()
    df_insert_data = df_revenue.reindex(columns=column_names)
    df_insert_data = df_insert_data.fillna(0)
    df_revenue.to_csv(os.path.join(data_dir, filename), index=False)
    return True


def get_revenue_from_source(branch: str, source_value: str):
    branch_filename = 'mock_revenue_{}_{}-{}.csv'.format(
        get_branch_code(branch), today.month, today.year)
    df_revenue = pd.read_csv(os.path.join(data_dir, branch_filename))
    df_source = df_revenue.loc[df_revenue["revenue_source"]
                               == source_value].fillna('')
    columns = df_source.columns.to_list()
    ret = []
    for index, row in df_source.sort_values(by=['revenue_category', 'revenue_subcategory', 'revenue_detail'], ascending=False).iterrows():
        revenue_record = {}
        sum = 0
        for column in columns:
            if column == 'revenue_source':
                continue
            if 'week' in column:
                sum += row[column] if type(row[column]) != str else 0
            revenue_record[column] = row[column]
        revenue_record['complete_rate'] = "{}%".format(round(100 * sum /
                                                             revenue_record["revenue_target"], 2))
        ret.append(revenue_record)
    return ret


def get_category_suggestion(source_value: str):
    df_revenue = pd.read_csv(os.path.join(data_dir, filename))
    category = list(df_revenue.loc[df_revenue["revenue_source"]
                                   == source_value]["revenue_category"].dropna().unique())
    return category


def get_subcategory_suggestion(source_value: str, category_value: str):
    df_revenue = pd.read_csv(os.path.join(data_dir, filename))
    subcategory = list(df_revenue.loc[(df_revenue["revenue_source"]
                                       == source_value) & (df_revenue["revenue_category"]
                                                           == category_value)]["revenue_subcategory"].dropna().unique())
    return subcategory


def get_detail_suggestion(source_value: str, category_value: str, subcategory_value: str):
    df_revenue = pd.read_csv(os.path.join(data_dir, filename))
    detail = list(df_revenue.loc[(df_revenue["revenue_source"]
                                  == source_value) & (df_revenue["revenue_category"]
                                                      == category_value) & (df_revenue["revenue_subcategory"]
                                                                            == subcategory_value)]["revenue_detail"].dropna().unique())
    return detail


def insert_excel(revenue_targets, target):
    df_revenue = check_existence(target)
    data = []
    for revenue_target in revenue_targets:
        revenue_target = revenue_target.__dict__
        data.append({
            "revenue_source": revenue_target["revenue_source"],
            "revenue_category": revenue_target["revenue_category"],
            "revenue_subcategory": revenue_target["revenue_subcategory"] if revenue_target["revenue_subcategory"] != None else "",
            "revenue_detail": revenue_target["revenue_detail"] if revenue_target["revenue_detail"] != None else "",
            "revenue_target": revenue_target["value"],

        })
    df_insert_data = pd.DataFrame(data)
    df_revenue = pd.concat([df_revenue, df_insert_data], ignore_index=True)

    try:
        column_names = get_column_names()
        df_insert_data = df_insert_data.reindex(columns=column_names)
        df_insert_data = df_insert_data.fillna(0)
        df_insert_data.to_csv(os.path.join(
            data_dir, 'mock_revenue_{}_{}-{}.csv'.format(get_branch_code(target), today.month, today.year)), columns=column_names, index=False)
        return True
    except Exception as e:
        print(e)
        return False


def get_column_names():
    no_week = len(calendar.monthcalendar(today.year, today.month))
    column_names = ['revenue_source',
                    'revenue_category', 'revenue_subcategory', 'revenue_detail', 'revenue_target', ]
    column_names.extend(['week{}'.format(x) for x in range(no_week)])
    return column_names


def check_existence(target):
    file_path = os.path.join(data_dir, 'mock_revenue_{}_{}-{}.csv'.format(
        get_branch_code(target), today.month, today.year))
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        columns = get_column_names()
        df_revenue = pd.DataFrame(columns=columns)
        return df_revenue
