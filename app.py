#streamlit run app.py
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/data2.csv", encoding='cp949')

st.sidebar.title('Korean Health Analysis')
st.write("2018년부터 2022년까지의 국민건강보험공단 건강검진정보 데이터를 바탕으로 분석한 결과입니다.")

select_variables = st.sidebar.selectbox(
    '확인하고 싶은 항목을 선택하세요',
    ['신장', '체중', '허리둘레', '시력', '청력', 
        '수축기혈압', '이완기혈압', '식전혈당(공복혈당)', '총콜레스테롤', 
        '트리글리세라이드', 'HDL콜레스테롤', 'LDL콜레스테롤', '혈색소', 
        '요단백', '혈청크레아티닌', '혈청지오티(AST)', '혈청지피티(ALT)', 
        '감마지티피']
)
col_dict = {'기준년도': 'year', '가입자일련번호': 'id', '시도코드': 
            'region', '성별': 'sex', '연령대코드(5세단위)': 'age', 
            '신장': 'height', '체중': 'weight', '허리둘레': 'waist', 
            '시력': 'sight', '청력': 'hearing', 
            '수축기혈압': 'SBP', '이완기혈압': 'DBP', '식전혈당(공복혈당)': 'FBG', 
            '총콜레스테롤': 'TC', '트리글리세라이드': 'NF', 'HDL콜레스테롤': 'HDL', 'LDL콜레스테롤': 'LDL', 
            '혈색소': 'Hgb', '요단백': 'urine protein', '혈청크레아티닌': 'serum creatinine', 
            '혈청지오티(AST)': 'AST', '혈청지피티(ALT)': 'ALT', '감마지티피': 'GTP'}
col = col_dict[select_variables]
col_p = col[0].upper() + col[1:]

def map_age_group(age):
    age_group = {
        1: '0~4', 2: '5~9', 3: '10~14', 4: '15~19', 5: '20~24', 6: '25~29', 7: '30~34',
        8: '35~39', 9: '40~44', 10: '45~49', 11: '50~54', 12: '55~59', 13: '60~64',
        14: '65~69', 15: '70~74', 16: '75~79', 17: '80~84', 18: '85~'
    }
    age_group = {
        1: '0~', 2: '5~', 3: '10~', 4: '15~', 5: '20~', 6: '25~', 7: '30~',
        8: '35~', 9: '40~', 10: '45~', 11: '50~', 12: '55~', 13: '60~',
        14: '65~', 15: '70~', 16: '75~', 17: '80~', 18: '85~'
    }
    return age_group.get(age)

df['age_group'] = df['age'].apply(map_age_group)

tab_age, tab_age_both, tab_age_male, tab_age_female, tab_year, tab_year_both, tab_year_male, tab_year_female = st.tabs(
    ['나이별', '나이별(남여)', '나이별(남)', '나이별(여)', '연도별', '연도별(남여)', '연도별(남)', '연도별(여)']
)

with tab_age:
    df_grouped = df.groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title=f'Average {col_p} by Age')
    st.plotly_chart(fig)

with tab_age_both:
    df_grouped = df.groupby(['sex', 'age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, color='sex', markers=True, title=f'Average {col_p} by Age for Each Sex')
    st.plotly_chart(fig)

with tab_age_male:
    df_grouped = df[df.sex == 1].groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title=f'Average {col_p} by Age for Male')
    st.plotly_chart(fig)

with tab_age_female:
    df_grouped = df[df.sex == 2].groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title=f'Average {col_p} by Age for Female')
    st.plotly_chart(fig)

with tab_year:
    df_grouped = df.groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title=f'Average {col_p} by Year')
    st.plotly_chart(fig)

with tab_year_both:
    df_grouped = df.groupby(['sex', 'year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, color='sex', markers=True, title=f'Average {col_p} by Year for Each Sex')
    st.plotly_chart(fig)

with tab_year_male:
    df_grouped = df[df.sex == 1].groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title=f'Average {col_p} by Year for Male')
    st.plotly_chart(fig)

with tab_year_female:
    df_grouped = df[df.sex == 2].groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title=f'Average {col_p} by Year for Female')
    st.plotly_chart(fig)

    # matplotlib ver.
    # grouped = df.groupby(['
    # sex', 'year'])[col].mean().unstack(0)
    # fig, ax = plt.subplots()
    # grouped.plot(kind='line', marker='o', ax=ax)
    # ax.set_title(f'Average {col_p} by Year for Each Sex')
    # ax.set_xlabel('Year')
    # ax.set_ylabel(f'Average {col_p}')
    # ax.set_xticks(grouped.index)
    # ax.legend(title='Sex', labels=['Male', 'Female'])
    # ax.grid(True)
    # st.pyplot(fig)
