import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 앱 제목
st.title("🌍 국가별 MBTI 유형 비율 시각화")
st.write("국가를 선택하면 해당 국가의 MBTI 유형 비율이 막대그래프로 표시됩니다.")

# 국가 선택
country = st.selectbox("국가를 선택하세요:", df["Country"].unique())

# 선택한 국가의 데이터 추출
country_data = df[df["Country"] == country].iloc[0, 1:]  # Country 열 제외
country_df = pd.DataFrame({
    "MBTI": country_data.index,
    "비율": country_data.values
}).sort_values(by="비율", ascending=False)

# 색상 지정 (1등은 빨강, 나머지는 그라데이션)
colors = ["#FF4C4C" if i == 0 else f"rgba(255, {(200 + i*2)%255}, {(150 + i*3)%255}, 0.8)" 
          for i in range(len(country_df))]

# Plotly 막대 그래프
fig = px.bar(
    country_df,
    x="MBTI",
    y="비율",
    text="비율",
    color=country_df["MBTI"],
    color_discrete_sequence=colors,
    title=f"🇨🇭 {country}의 MBTI 분포",
)

fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
fig.update_layout(
    showlegend=False,
    yaxis_title="비율(%)",
    xaxis_title="MBTI 유형",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor="lightgray")
)

st.plotly_chart(fig, use_container_width=True)
