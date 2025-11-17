import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("써브웨이.csv", encoding="cp949")
    return df

df = load_data()

st.title("🚇 2025년 10월 지하철 승하차 분석")

# 날짜 선택
dates = sorted(df["사용일자"].unique())
selected_date = st.selectbox("날짜 선택", dates)

# 호선 선택
lines = sorted(df["노선명"].unique())
selected_line = st.selectbox("호선 선택", lines)

# 필터링
filtered = df[(df["사용일자"] == selected_date) & (df["노선명"] == selected_line)].copy()

# 승하차 총합 계산
filtered["총승객수"] = filtered["승차총승객수"] + filtered["하차총승객수"]

# 상위 10개 역 추출
top10 = filtered.sort_values("총승객수", ascending=False).head(10)

# 색상 설정: 1등 빨강 + 나머지 파랑 → 옅어지는 그라데이션
colors = ["red"] + [f"rgba(0,0,255,{alpha})" for alpha in list(
    pd.np.linspace(1, 0.2, 9)
)]

# Plotly 그래프 생성
fig = px.bar(
    top10,
    x="역명",
    y="총승객수",
    title=f"{selected_date} - {selected_line} 상위 10개 역 승하차 총합",
)

# 색 적용
fig.update_traces(marker_color=colors)

# y축·레이아웃 정리
fig.update_layout(
    xaxis_title="역명",
    yaxis_title="승하차 총합",
    template="plotly_white"
)

# 출력
st.plotly_chart(fig, use_container_width=True)
