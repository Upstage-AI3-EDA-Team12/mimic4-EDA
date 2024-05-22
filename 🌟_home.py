import streamlit as st

st.set_page_config(
    page_title="Multi-page App",
    page_icon="🌟"
)

st.title("국민건강보험 자료 분석 메인페이지")
st.caption("nhis: National Health Insurance Service")

st.sidebar.success("select a page above.")

st.write("국민건강보험 자료를 바탕으로")
st.write("분석한 자료를 보기 편하게 한 대쉬보드 페이지와")
st.write("데이터를 활용해 bmi체크가 가능하도록 해보았습니다. ")

with st.container(border=1):
    st.image('./1.png')
    st.caption("EDA dashboard")
with st.container(border=1):
    st.image('./3.png')
    st.caption("BMI check activity")
