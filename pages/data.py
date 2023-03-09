import numpy as np
import plotly.figure_factory as ff
import datetime
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

sidebar_option = st.sidebar.selectbox("數據來源", ('住建部官方數據',
                                               '鏈家數據'))
if sidebar_option == '住建部官方數據':
    city_option = st.sidebar.selectbox("城市", ('深圳','武汉'))
    if city_option == '深圳':
        df = pd.read_csv('./SZOffical.csv')
        df['日期'] = pd.to_datetime(df['日期'])
        df_week = df.groupby([df['日期'].dt.year, df['weekofyear']]).sum()
        df_week.index.names = ['year', 'week']
        fig = go.Figure(data=[
            # go.Line(name='2019', x=df_week.iloc[:51].index.get_level_values(1), y=df_week.iloc[:51,1]),
            go.Line(name='2020', x=df_week.iloc[51:103].index.get_level_values(1), y=df_week.iloc[51:103,0],marker_color='darkcyan'), #, marker_color='darkcyan'),
            go.Line(name='2021', x=df_week.iloc[103:156].index.get_level_values(1), y=df_week.iloc[103:156,0], marker_color='lightslategray'),
            go.Line(name='2022', x=df_week.iloc[156:207].index.get_level_values(1), y=df_week.iloc[156:207,0], marker_color='blue'),
            go.Line(name='2023', x=df_week.iloc[207:].index.get_level_values(1), y=df_week.iloc[207:,0], marker_color='red', mode='lines+markers')
        ])

        fig.update_layout(title_text='深圳每周一手房成交面积2020-2023', title_x=0.3,
                         yaxis=dict(
                title='面积(平方米)',
                titlefont_size=16,
                tickfont_size=14),
                         xaxis=dict(
                title='周数',
                titlefont_size=16,
                tickfont_size=14,
                dtick = 5))

        fig2 = go.Figure(data=[
            # go.Line(name='2019', x=df_week.iloc[:51].index.get_level_values(1), y=df_week.iloc[:51,1]),
            go.Line(name='2020', x=df_week.iloc[51:103].index.get_level_values(1), y=df_week.iloc[51:103,2], marker_color='darkcyan'), #, marker_color='darkcyan'),
            go.Line(name='2021', x=df_week.iloc[103:156].index.get_level_values(1), y=df_week.iloc[103:156,2], marker_color='lightslategray'),
            go.Line(name='2022', x=df_week.iloc[156:207].index.get_level_values(1), y=df_week.iloc[156:207,2], marker_color='blue'),
            go.Line(name='2023', x=df_week.iloc[207:].index.get_level_values(1), y=df_week.iloc[207:,2], marker_color='red', mode='lines+markers')
        ])

        fig2.update_layout(title_text='深圳每周二手房成交面积 2020-2023',title_x=0.3,
                         yaxis=dict(
                title='面积(平方米)',
                titlefont_size=16,
                tickfont_size=14),
                         xaxis=dict(
                title='周数',
                titlefont_size=16,
                tickfont_size=14,
                dtick = 5))

        st.plotly_chart(fig)
        st.plotly_chart(fig2)
    elif city_option == '武汉':
        pd.options.display.float_format = '{:.2%}'.format
        df_wh = pd.read_csv('./WHOffical.csv')
        df_wh = df_wh[['date', 'area', 'volume']]
        df_wh = df_wh.sort_values('date', ascending=False)
        df_wh['date'] = pd.to_datetime(df_wh['date'])
        df_wh['weekofyear'] = df_wh['date'].dt.weekofyear

        df_wh['area'] = df_wh['area'].astype(float)
        df_wh_2020 = df_wh[df_wh['date'].dt.date >= datetime.date(2020, 1, 1)]
        df_wh_2020['year'] = df_wh_2020['date'].dt.year
        df_wh_2020.loc[(df_wh_2020['weekofyear'] > 51) & (df_wh_2020['date'].dt.month != 12), 'year'] -= 1
        df_wh_2020_week = df_wh_2020.groupby([df_wh_2020['year'], df_wh_2020['weekofyear']]).sum()

        df_wh_week_pivot = df_wh_2020_week[['area']].pivot_table(index='year', columns='weekofyear', values='area')

        df_wh_2020_week_mom = df_wh_2020_week.pct_change()
        df_wh_2020_week_mom_pivot = df_wh_2020_week_mom[['area']].pivot_table(index='year', columns='weekofyear',
                                                                              values='area')
        df_wh_2020_week_yoy_pivot = df_wh_week_pivot.pct_change()

        fig = go.Figure(data=[
            # go.Bar(name='2019', x=df_week.iloc[:51].index.get_level_values(1), y=df_week.iloc[:51,1]),
            go.Line(name='2020', x=df_wh_2020_week.iloc[:44].index.get_level_values(1),
                    y=df_wh_2020_week.iloc[:44]['area'], marker_color='darkcyan'),
            go.Line(name='2021', x=df_wh_2020_week.iloc[44:96].index.get_level_values(1),
                    y=df_wh_2020_week.iloc[44:96]['area'], marker_color='lightslategray'),
            go.Line(name='2022', x=df_wh_2020_week.iloc[96:148].index.get_level_values(1),
                    y=df_wh_2020_week.iloc[96:148]['area'], marker_color='blue'),
            go.Line(name='2023', x=df_wh_2020_week.iloc[148:].index.get_level_values(1),
                    y=df_wh_2020_week.iloc[148:]['area'], marker_color='red')
        ])
        fig.update_layout(title_text='武汉新建商品房网签备案统计情况2020-2023', title_x=0.3,
                          yaxis=dict(
                              title='网签面积(平方米)',
                              titlefont_size=16,
                              tickfont_size=14),
                          xaxis=dict(
                              title='周数',
                              titlefont_size=16,
                              tickfont_size=14,
                              dtick=5))
        st.plotly_chart(fig)
        st.header('數據')
        st.dataframe(df_wh_week_pivot)
        st.header('環比數據')
        st.dataframe(df_wh_2020_week_mom_pivot.style.format("{:.1%}"))
        st.header('同比數據')
        st.dataframe(df_wh_2020_week_yoy_pivot.style.format("{:.1%}"))

elif sidebar_option == '鏈家數據':
    city_option = st.sidebar.selectbox("城市", ('深圳', '武汉'))
    cols = ['date', 'title', 'region', 'house', 'price', 'size', 'link']
    if city_option == '深圳':
        df_old = pd.read_csv('20230308lianjiaSZ.csv')
        df_new = pd.read_csv('20230309lianjiaSZ.csv')
    elif city_option == '武汉':
        df_old = pd.read_csv('20230308lianjiaWH.csv')
        df_new = pd.read_csv('20230309lianjiaWH.csv')

    df_merge = df_old.merge(df_new, on=['housecode'], suffixes=('_old', '_new'), how='outer')

    # new_list
    new_list_number = df_merge.loc[df_merge['date_old'].isnull(), 'size_new'].count()
    new_list_size = df_merge.loc[df_merge['date_old'].isnull(), 'size_new'].sum()
    # miss_list
    miss_list_number = df_merge.loc[df_merge['date_new'].isnull(), 'size_old'].count()
    miss_list_size = df_merge.loc[df_merge['date_new'].isnull(), 'size_old'].sum()
    # df_summary = pd.DataFrame({'Count': [new_list_number, miss_list_number], 'Size (平方米)': [new_list_size, miss_list_size]},
    #                           index=['new listing', 'delisting'])
    df_summary = pd.DataFrame(
        {'Count': [miss_list_number], 'Size (平方米)': [miss_list_size]},
        index=['delisting']
    )
    df_summary = df_summary.transpose()
    # df_summary['difference'] = df_summary['new listing'] - df_summary['delisting']

    df_new = df_new[cols]
    df_old = df_old[cols]
    df_new.rename(columns={'price': 'price (万)', 'size': 'size(平方米)'}, inplace=True)
    df_old.rename(columns={'price': 'price (万)', 'size': 'size(平方米)'}, inplace=True)

    st.header('Summary')
    st.dataframe(df_summary)
    text = "If today's data does not have a record of yesterday's data, assume that the missing part ({}unit, {}平方米) has been sold"
    st.markdown(text.format(df_summary.iloc[0,0], round(df_summary.iloc[1,0])))

    st.header('2023-03-09')
    st.dataframe(df_new)

    st.header('2023-03-08')
    st.dataframe(df_old)