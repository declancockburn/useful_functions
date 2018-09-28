# -*- coding: utf-8 -*-
"""
Created by dcockbur on 19/09/2018
"""
import pandas as pd

from variables import path, filename, tools

def parse_data():

    # This is just so the dataframes can be viewed while coding
    # pd.set_option('display.width', 200)
    # pd.set_option("display.max_columns", 10)

    drive_list = list()
    time_list = list()

    for tool in tools:
        try:
            filepath = "{}/{}/Source/{}".format(path, tool, filename)
            df1 = pd.read_table(filepath, dtype=str, delim_whitespace=True, skiprows=1, lineterminator='\n').dropna(
                how='all')
            if len(df1) < 45:
                df2 = df1.iloc[:].dropna(how='all')
                mask_lastentry = df2.index[0]
                df2 = df2.loc[mask_lastentry:].iloc[1:]
            else:
                df2 = df1.iloc[-40:].dropna(how='all')  # $$$$$
                mask_lastentry = df2[df2['Use%'].isin(['PDT', 'PST'])].index[-1]
                df2 = df2.loc[mask_lastentry:].iloc[1:]  # $$$$
                time = ' '.join([str(x) for x in df1.loc[mask_lastentry][:4]])[:4]
            mask_fix_cols = df2['Available'].str.contains("%").fillna(value=False)
            c = list(df2.columns.values)
            df2.loc[mask_fix_cols, c] = df2.loc[mask_fix_cols, c].shift(1, axis=1)

            # Slice out the separate MSC and DAS parts
            slice1 = df2.loc[df2.iloc[:, 0] == 'MSC'].index[0]
            slice2 = df2.loc[df2.iloc[:, 0] == 'DAS'].index[0]

            df_msc = df2.loc[slice1:slice2 - 1]
            df_das = df2.loc[slice2:]

            rename_dic = {"Mounted": "Drives", "Use%": tool}

            drives = "/home|/public"
            df_msc = df_msc.iloc[:, 1:-1].dropna(how='all')
            df_msc = df_msc.loc[df_msc['Mounted'].str.contains(drives)]
            df_msc.rename(columns=rename_dic, inplace=True)
            df_msc['Drives'] = ["MSC/{}".format(x.split('/')[-1]) for x in df_msc['Drives']]
            df_msc.set_index('Drives', inplace=True)
            df_msc = df_msc[tool]

            drives = "/home"
            df_das = df_das.iloc[:, 1:-1].dropna(how='all')
            df_das = df_das.loc[df_das['Mounted'].str.contains(drives)]
            df_das.rename(columns=rename_dic, inplace=True)
            df_das['Drives'] = ["DAS/{}".format(x.split('/')[-1]) for x in df_das['Drives']]
            df_das.set_index('Drives', inplace=True)
            df_das = df_das[tool]

            # Recombine the new parsed MSC and DAS dataframes
            df2 = pd.concat([df_msc, df_das])

            df_time2 = pd.Series(index=[tool], data=[time])
            time_list.append(df_time2)
            drive_list.append(df2)

        except:
            print('{} not readable!'.format(tool))

    df3 = pd.concat(time_list, axis=0).to_frame().T
    df3.index = ['Date']
    df4 = pd.concat([pd.concat(drive_list, axis=1)], axis=0)
    df5 = pd.concat([df3, df4], axis=0)
    return df5


# parse_data()