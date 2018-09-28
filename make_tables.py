# -*- coding: utf-8 -*-
"""
Created by dcockbur on 24/09/2018	
"""
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
from matplotlib import colors

def make_table_image(df, coldate=False, yellowcell=50, redcell=80, darkredcell=90,
                     col_width=3.0, row_height=0.625, font_size=18,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0, header_rows=0,
                     ax=None, **kwargs):
    overthresh = False
    df2 = df.copy()
    df2.loc['Date'] = "1%"
    df3 = pd.concat([df2[x].str.rstrip("%") for x in df2.columns.values], axis=1).astype(float)
    if np.max(df3.values) > redcell:
        overthresh = True
    colors = df3.applymap(lambda x: (1, 0, 0, 0.7) if x > darkredcell else
    (1, 0, 0, 0.3) if x > redcell else
    (1, 1, 0, 0.3) if x > yellowcell else '#f1f1f2').reset_index().drop(['index'], axis=1)
    if ax is None:
        size = (np.array(df.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=df.values, bbox=bbox,
                         rowLabels=df.index.values,
                         colLabels=df.columns,
                         **kwargs,
                         loc='right',
                         cellLoc='right',
                         cellColours=colors.values,
                         )
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):

        cell.set_edgecolor(edge_color)
        if k[0] <= header_rows:  # Set header colour for first row/header
            cell.set_text_props(weight='normal', color='w')
            cell.set_facecolor(header_color)
        elif k[1] < header_columns:  # Set header colour for column labels
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)

    plt.title('Drive Fullness', backgroundcolor='#40466e', color='w', fontsize=18, weight='bold')

    plt.gcf().subplots_adjust(left=0.2, right=0.99, top=0.8)  # Adjust the placement of the table!
    #plt.show()
    plt.savefig('machine_drive_fullness.png')
    return ax, overthresh

def make_table_html(df):
    def background_gradient(s, m, M, cmap='PuBu', low=0, high=0):
        s = s.str.rstrip("%").astype(int)
        rng = M - m
        norm = colors.Normalize(m - (rng * low),
                                M + (rng * high))
        normed = norm(s.values)
        c = [colors.rgb2hex(x) for x in plt.cm.get_cmap(cmap)(normed)]
        return ['background-color: {}'.format(color) for color in c]
    def non_highlighted(x):
        if x:
            return 'background-color: #f1f1f2'
    df2 = df.copy()
    df2.loc['Date'] = "1%"
    df2 = pd.concat([df2[x].str.rstrip("%") for x in df2.columns.values], axis=1).astype(float)
    return df.style.apply(background_gradient,
                   cmap='YlOrRd',
                   m = 60,# m=df3.min().min(),
                   M = 100,# M=df3.max().max(),
                   low=0,
                   high=0.2,
                   subset=pd.IndexSlice[df2.iloc[1].name:]).applymap(non_highlighted, subset=pd.IndexSlice['Date':'Date']).set_table_attributes("border=1").render()

def make_email_content(file, top, middle, bottom):
    with open(file, 'w') as f:
        f.write(top)
    with open(file, 'a') as f:
        f.write(middle)
        f.write(bottom)

