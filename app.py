#streamlit run app.py
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/data2.csv", encoding='cp949')

st.sidebar.title('Korean Health Analysis')
st.write("2018년부터 2022년까지의 국민건강보험공단 건강검진정보 데이터를 바탕으로 분석한 결과입니다")

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

col_info = {'height': '', 'weight': '', 'waist': '', 'sight': '· 정상 시력: 1.0-1.2',
            'hearing': '', 'SBP': '· 정상: 120 미만', 'DBP': '· 정상: 80 미만', 'FBG': '· 정상: 70-100 mg/dL',
            'TC': '· 정상: 180 mg/dL 미만', 'LDL': '· 정상 남성: 40 mg/dL 이상  \n· 정상 여성: 50 mg/dL 이상',
            'NF': '· 정상: 150 mg/dL 미만', 'Hgb': '· 정상 남성: 13.0-17.0 g/dL 이상  \n· 정상 여성: 12.0-16.0 g/dL 이상',
            'urine protein': '', 'serum creatinine': '· 정상: 0.7-1.4 mg/dL', 'AST': '· 정상 40 이하',
            'ALT': '· 정상 35 이하', 'GTP': '· 정상 남성: 63 이하  \n· 정상 여성: 35 이하'}
st.sidebar.write(col_info[col])

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

def map_sex(sex):
    sex_dict = {
        1: 'male', 2: 'female'
    }
    return sex_dict.get(sex)

df['age_group'] = df['age'].apply(map_age_group)
df['sex'] = df['sex'].apply(map_sex)

tab_age, tab_year = st.tabs(['나이별', '연도별'])

with tab_age:
    df_grouped = df.groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title='나이별 평균', color_discrete_sequence=['dimgray'])
    st.plotly_chart(fig)
    
    df_grouped = df.groupby(['sex', 'age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, color='sex', markers=True, title='나이별(남여)', color_discrete_sequence=['palevioletred', 'steelblue'])
    st.plotly_chart(fig)

    df_grouped = df[df.sex == 'male'].groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title='나이별(남)', color_discrete_sequence=['steelblue'])
    st.plotly_chart(fig)

    df_grouped = df[df.sex == 'female'].groupby(['age_group']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='age_group', y=col, markers=True, title='나이별(여)', color_discrete_sequence=['palevioletred'])
    st.plotly_chart(fig)

with tab_year:
    df_grouped = df.groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title='연도별 평균', color_discrete_sequence=['dimgray'])
    st.plotly_chart(fig)

    df_grouped = df.groupby(['sex', 'year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, color='sex', markers=True, title='연도별(남여)', color_discrete_sequence=['palevioletred', 'steelblue'])
    st.plotly_chart(fig)

    df_grouped = df[df.sex == 'male'].groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title=f'연도별(남)', color_discrete_sequence=['steelblue'])
    st.plotly_chart(fig)

    df_grouped = df[df.sex == 'female'].groupby(['year']).agg({col: 'mean'}).reset_index()
    fig = px.line(df_grouped, x='year', y=col, markers=True, title=f'연도별(여)', color_discrete_sequence=['palevioletred'])
    st.plotly_chart(fig)