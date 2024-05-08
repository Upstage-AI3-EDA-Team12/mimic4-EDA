#streamlit run app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

tab1, tab2, tab3, tab4 = st.tabs(['나이별', '연도별', '성별 및 나이별', '성별 및 연도별'])

with tab1:
    grouped = df.groupby(['age'])[col].mean()
    fig, ax = plt.subplots()
    grouped.plot(kind='line', marker='o', ax=ax)
    ax.set_title(f'Average {col_p} by Age')
    ax.set_xlabel('Age')
    ax.set_ylabel(f'Average {col_p}')
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    grouped = df.groupby(['year'])[col].mean()
    fig, ax = plt.subplots()
    grouped.plot(kind='line', marker='o', ax=ax)
    ax.set_title(f'Average {col_p} by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'Average {col_p}')
    ax.set_xticks(grouped.index)
    ax.grid(True)
    st.pyplot(fig)

with tab3:
    grouped = df.groupby(['sex', 'age'])[col].mean().unstack(0)
    fig, ax = plt.subplots()
    grouped.plot(kind='line', marker='o', ax=ax)
    ax.set_title(f'Average {col_p} by Age for Each Sex')
    ax.set_xlabel('Age')
    ax.set_ylabel(f'Average {col_p}')
    ax.legend(title='Sex', labels=['Male', 'Female'])
    ax.grid(True)
    st.pyplot(fig)

with tab4:
    grouped = df.groupby(['sex', 'year'])[col].mean().unstack(0)
    fig, ax = plt.subplots()
    grouped.plot(kind='line', marker='o', ax=ax)
    ax.set_title(f'Average {col_p} by Year for Each Sex')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'Average {col_p}')
    ax.set_xticks(grouped.index)
    ax.legend(title='Sex', labels=['Male', 'Female'])
    ax.grid(True)
    st.pyplot(fig)
