import pandas as pd
import numpy as np
import os.path
import math

def process_file(file, target_columns):
    try:

        # convert from raw csv data to final data used for ML training
        df = pd.read_csv(file, encoding="gb2312")
        df = df.T

        # step 1: get row[0] and pick the columns we are interested
        topics = list(df.iloc[0])
        found_topics = []
        found_columns = []
        column_rename_mapping = {}

        for i in range(0, len(list(df.columns))):
            topic = topics[i]
            if topic.strip() in target_columns:
                if not topic.strip() in found_topics:
                    found_topics.append(topic.strip())
                    found_columns.append(i)
                    column_rename_mapping[i] = topic.strip()

        # step 2: create new df with only columns we are interested
        # print(found_topics)
        df = df[found_columns]
        df.rename(columns=column_rename_mapping, inplace=True)

        # delete first row
        df.drop(list(df.index)[0], inplace=True)
        return df

    except Exception as ex:
        print("Failed to process: " + file + ' ' + str(ex))


def process_data(code):
    # empty values: '流动负债(万元)' '流动资产合计(万元)'  '非流动负债合计(万元)'
    target_columns = ['主营业务收入(万元)', '总资产(万元)', '营业利润(万元)', '流动负债合计(万元)', '总负债(万元)', '净利润(万元)', '资产减值损失(万元)',

                      '存货(万元)', '流动资产合计(万元)', '股东权益不含少数股东权益(万元)', '应收账款(万元)', '营业成本(万元)', '固定资产净值(万元)',
                      '经营活动现金流入小计(万元)',

                      '经营活动现金流出小计(万元)', '货币资金(万元)', '非流动负债合计(万元)', '基本每股收益(元)']

    path = "C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/" + 'zycwzb' + "_" + code + ".csv"
    if not os.path.exists(path):
        print('failed to process data for ' + code + ' due to file ' + path + ' not exist')
        return
    df1 = process_file(path, target_columns)
    if df1.empty:
        print('failed to process data for ' + code + ' due to data ' + path + ' not exist')
        return
    target_columns = list(set(target_columns).difference(set(df1.columns)))
    path = "C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/" + 'zcfzb' + "_" + code + ".csv"
    if not os.path.exists(path):
        print('failed to process data for ' + code + ' due to file ' + path + ' not exist')
        return
    df2 = process_file(path, target_columns)
    if df2.empty:
        print('failed to process data for ' + code + ' due to data ' + path + ' not exist')
        return
    target_columns = list(set(target_columns).difference(set(df2.columns)))
    path = "C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/" + 'lrb' + "_" + code + ".csv"
    if not os.path.exists(path):
        print('failed to process data for ' + code + ' due to file ' + path + ' not exist')
        return
    df3 = process_file(path, target_columns)
    if df3.empty:
        print('failed to process data for ' + code + ' due to data ' + path + ' not exist')
        return
    target_columns = list(set(target_columns).difference(set(df3.columns)))
    path = "C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/" + 'xjllb' + "_" + code + ".csv"
    if not os.path.exists(path):
        print('failed to process data for ' + code + ' due to file ' + path + ' not exist')
        return
    df4 = process_file(path, target_columns)
    if df4.empty:
        print('failed to process data for ' + code + ' due to data ' + path + ' not exist')
        return
    df = pd.concat([df1, df2, df3, df4], axis=1)

    # clean the data
    df = df.replace(['--'], np.nan)
    df = df.replace([' '], np.nan)
    # remove bad rows
    df = df.loc[(df.index > '1995-12-31') & (df.index < '2021-12-31')]

    df = df.sort_index()
    gProfitIn3Years = []
    gDic = {}
    for index, row in df.iterrows():
        if '12-31' in str(index):
            # remove first element
            if len(gProfitIn3Years) > 2:
                gProfitIn3Years.pop(0)
            # append to tail
            gProfitIn3Years.append(float(row['营业利润(万元)']))
            try:
                if row['总资产(万元)'] == '0':
                    gDic[index] = np.nan
                else:
                    gDic[index] = sum(gProfitIn3Years) / float(row['总资产(万元)'])
            except Exception as e:
                gDic[index] = np.nan
        else:
            gDic[index] = np.nan

    df['ebit'] = df['主营业务收入(万元)'].astype(float) - df['营业成本(万元)'].astype(float) - df['经营活动现金流出小计(万元)'].astype(float)
    df['ebitda'] = df['ebit'].astype(float) + df['资产减值损失(万元)'].astype(float)

    # save to csv
    df.to_csv('C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/output/' + code + '.csv', encoding="gb2312")

    df['X1'] = df['净利润(万元)'].astype(float) / df['总资产(万元)'].astype(float)
    df['X2'] = df['总负债(万元)'].astype(float) / df['总资产(万元)'].astype(float)
    df['X3'] = (df['流动资产合计(万元)'].astype(float) - df['流动负债合计(万元)'].astype(float)) / df['总资产(万元)'].astype(float)
    df['X4'] = df['流动资产合计(万元)'].astype(float) / df['流动负债合计(万元)'].astype(float)

    df['X7'] = df['ebit'].astype(float) / df['总资产(万元)'].astype(float)
    df['X8'] = df['基本每股收益(元)'].astype(float) / df['总负债(万元)'].astype(float)
    df['X9'] = df['主营业务收入(万元)'].astype(float) / df['总资产(万元)'].astype(float)
    df['X10'] = df['股东权益不含少数股东权益(万元)'].astype(float) / df['总资产(万元)'].astype(float)

    df['X12'] = df['营业利润(万元)'].astype(float) / df['流动负债合计(万元)'].astype(float)
    df['X13'] = (df['营业利润(万元)'].astype(float) + df['资产减值损失(万元)'].astype(float)) / df['主营业务收入(万元)'].astype(float)
    df['X15'] = (df['总负债(万元)'].astype(float) * 90) / (df['营业利润(万元)'].astype(float) + df['资产减值损失(万元)'].astype(float))
    df['X16'] = (df['营业利润(万元)'].astype(float) + df['资产减值损失(万元)'].astype(float)) / df['总负债(万元)'].astype(float)
    df['X17'] = df['总资产(万元)'].astype(float) / df['总负债(万元)'].astype(float)
    df['X18'] = df['营业利润(万元)'].astype(float) / df['总资产(万元)'].astype(float)

    df['X19'] = df['营业利润(万元)'].astype(float) / df['主营业务收入(万元)'].astype(float)
    df['X20'] = df['存货(万元)'].astype(float) * 90 / df['主营业务收入(万元)'].astype(float)
    df['X21'] = df['主营业务收入(万元)'].astype(float) / df['主营业务收入(万元)'].shift(periods=1).astype(float)

    df['X22'] = df['经营活动现金流入小计(万元)'].astype(float) / df['总资产(万元)'].astype(float)
    df['X23'] = df['净利润(万元)'].astype(float) / df['主营业务收入(万元)'].astype(float)
    df['X24'] = pd.Series(gDic)
    df['X26'] = (df['净利润(万元)'].astype(float) + df['资产减值损失(万元)'].astype(float))/df['总负债(万元)'].astype(float)
    df['X28'] = (df['流动资产合计(万元)'].astype(float) - df['流动负债合计(万元)'].astype(float)) / df['固定资产净值(万元)'].astype(float)
    df['X29'] = np.log(df['总资产(万元)'].astype(float))
    df['X30'] = (df['总负债(万元)'].astype(float) - df['货币资金(万元)'].astype(float)) / df['主营业务收入(万元)'].astype(float)

    df['X32'] = (df['流动负债合计(万元)'].astype(float) * 90) / df['营业成本(万元)'].astype(float)
    df['X33'] = df['经营活动现金流出小计(万元)'].astype(float) / df['流动负债合计(万元)'].astype(float)
    df['X34'] = df['经营活动现金流出小计(万元)'].astype(float) / df['总负债(万元)'].astype(float)
    df['X37'] = (df['流动资产合计(万元)'].astype(float) - df['存货(万元)'].astype(float)) / df['非流动负债合计(万元)'].astype(float)
    df['X40'] = (df['流动负债合计(万元)'].astype(float) - df['存货(万元)'].astype(float) - df['应收账款(万元)'].astype(float))/df['流动负债合计(万元)'].astype(float)
    df['X41'] = df['总负债(万元)'].astype(float) / (df['经营活动现金流入小计(万元)'].astype(float) + df['资产减值损失(万元)'].astype(float)) * (12/90)
    df['X42'] = df['经营活动现金流入小计(万元)'].astype(float) / df['主营业务收入(万元)'].astype(float)
    df['X44'] = df['应收账款(万元)'].astype(float) * 90 / df['主营业务收入(万元)'].astype(float)
    df['X45'] = df['净利润(万元)'].astype(float) / df['存货(万元)'].astype(float)
    df['X46'] = (df['流动资产合计(万元)'].astype(float) - df['存货(万元)'].astype(float))/df['流动负债合计(万元)'].astype(float)
    df['X47'] = df['存货(万元)'].astype(float) * 90 / df['营业成本(万元)'].astype(float)
    df['X48'] = df['ebitda'].astype(float) / df['总资产(万元)'].astype(float)
    df['X49'] = df['ebitda'].astype(float) / df['主营业务收入(万元)'].astype(float)
    df['X50'] = df['流动资产合计(万元)'].astype(float) / df['总负债(万元)'].astype(float)
    df['X51'] = df['流动负债合计(万元)'].astype(float) / df['总资产(万元)'].astype(float)
    df['X53'] = df['股东权益不含少数股东权益(万元)'].astype(float) / df['固定资产净值(万元)'].astype(float)
    df['X55'] = df['流动资产合计(万元)'].astype(float) - df['流动负债合计(万元)'].astype(float)
    df['X56'] = (df['主营业务收入(万元)'].astype(float)-df['营业成本(万元)'].astype(float))/df['主营业务收入(万元)'].astype(float)
    df['X57'] = (df['流动资产合计(万元)'].astype(float) - df['存货(万元)'].astype(float) - df['流动负债合计(万元)'].astype(float))\
                / (df['主营业务收入(万元)'].astype(float) - df['营业利润(万元)'].astype(float) - df['资产减值损失(万元)'].astype(float))
    df['X59'] = df['非流动负债合计(万元)'].astype(float) / df['股东权益不含少数股东权益(万元)'].astype(float)
    df['X60'] = df['主营业务收入(万元)'].astype(float) / df['存货(万元)'].astype(float)
    df['X61'] = df['主营业务收入(万元)'].astype(float) / df['应收账款(万元)'].astype(float)
    df['X62'] = df['流动负债合计(万元)'].astype(float) * 90 / df['主营业务收入(万元)'].astype(float)
    df['X63'] = df['主营业务收入(万元)'].astype(float) / df['流动负债合计(万元)'].astype(float)
    df['X64'] = df['主营业务收入(万元)'].astype(float) / df['固定资产净值(万元)'].astype(float)

    new_columns = ['X1', 'X2', 'X3', 'X4', 'X7', 'X8', 'X9', 'X10', 'X12', 'X13', 'X15', 'X16', 'X17', 'X18', 'X19',
                   'X20', 'X21', 'X22', 'X23', 'X24', 'X26', 'X28', 'X29', 'X30', 'X32', 'X33', 'X34', 'X37', 'X40', 'X41', 'X42', 'X44', 'X45', 'X46',
                   'X47', 'X48', 'X49', 'X50', 'X51', 'X53', 'X55', 'X56', 'X57', 'X59', 'X60', 'X61', 'X62', 'X63', 'X64']
    df = df[new_columns]
    df.to_csv('C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/output/' + code + '_extended.csv', encoding="gb2312")
    print('succeeded to generate files for ' + code)


def main():
    table_type_names = ['zycwzb','zcfzb', 'lrb', 'xjllb']
    # 600 601
    #  '603', '000', '001', '002', '300'
    code_prefixes = ['002', '300']

    # 退市代码列表
    '''
    600086,
    600175,
    600401,
    601558,
    600687
    600074,
    600069,
    600240,
    600747,
    600432,
    000662,
    300104,
    300431,
    000979,
    002680,
    600175,
    002477,
    600401,
    601558
    '''



    # process_data('300015')
    # process_data('300956')
    # process_data('300118')
    # process_data('300136')
    for prefix in code_prefixes:
        for i in range(0, 1000):
            code = str(i).zfill(3)
            print('start to process ' + prefix + code)
            process_data(str(prefix+code))


if __name__ == "__main__":
    main()