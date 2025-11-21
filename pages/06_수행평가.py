# File: pages/seogwipo_rescue_dashboard.py
# Streamlit app — 서귀포시 인명구조함 비율 대시보드
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="서귀포시 인명구조함 비율", layout="wide")

# 유틸: 파일 로드 (여러 경로/인코딩 시도)
@st.cache_data
def load_data() -> pd.DataFrame:
    candidates = ["./csvvvvvvv.csv", "/mnt/data/csvvvvvvv.csv", "./csv.csv", "/mnt/data/csv.csv"]
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin1"]
    for p in candidates:
        for enc in encodings:
            try:
                df = pd.read_csv(p, encoding=enc, low_memory=False)
                st.session_state['__data_path_used'] = p
                st.session_state['__data_enc_used'] = enc
                return df
            except Exception:
                continue
    raise FileNotFoundError("프로젝트 루트 또는 /mnt/data에 csvvvvvvv.csv 파일을 올려 주세요.")

def make_gradient_colors(n: int) -> list:
    # 첫번째(1등)는 강렬한 빨간색, 나머지는 그라데이션으로 반환
    if n <= 0:
        return []
    if n == 1:
        return ["#ff0000"]
    start_rgb = np.array([255, 210, 210])  # 연한 빨강
    end_rgb = np.array([255, 0, 0])        # 진한 빨강
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)
        rgb = np.round((1 - t) * start_rgb + t * end_rgb).astype(int)
        colors.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    colors[0] = "#ff0000"  # 1등은 진한 빨강으로 고정
    return colors

# Load
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.title("📊 서귀포시 인명구조함 비율 대시보드")
st.caption(f"데이터 경로(시도): {st.session_state.get('__data_path_used','unknown')}  |  인코딩: {st.session_state.get('__data_enc_used','unknown')}")

# 기본 요약
with st.expander("데이터 기본 요약 (클릭해서 보기)", expanded=False):
    st.write("행/열:", df.shape)
    st.write("컬럼:", df.columns.tolist())
    st.write("결측치 합계:", int(df.isna().sum().sum()))
    st.dataframe(df.head(10))

# 컬럼 존재 확인 (필수 컬럼들)
expected_cols = ['읍면동', '설치장소(위치)', '수량']
for c in expected_cols:
    if c not in df.columns:
        st.error(f"데이터에 필수 컬럼 '{c}'가 없습니다. 컬럼 이름을 확인해주세요.")
        st.stop()

# 정리: 문자열 정규화 & 수량 숫자 변환
df['설치장소(위치)'] = df['설치장소(위치)'].astype(str).str.strip()
df['읍면동'] = df['읍면동'].astype(str).str.strip()
# 수량을 숫자로 안전 변환
df['수량'] = pd.to_numeric(df['수량'].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0).astype(int)

# "서귀포"가 포함된 행 필터 (설치장소 기준)
mask_seogwipo = df['설치장소(위치)'].str.contains("서귀포", na=False)
seogwipo_df = df[mask_seogwipo].copy()

st.markdown(f"**서귀포시 관련 행 수:** {len(seogwipo_df)}  (전체 {len(df)} 행 중)")
st.markdown(f"**서귀포시 내 인명구조함 총 수량 합계:** {seogwipo_df['수량'].sum()}")

if seogwipo_df.empty:
    st.info("데이터 내에 '서귀포' 관련 항목이 없습니다.")
    st.stop()

# 읍면동별 집계 (수량 합계 -> 비율)
agg = seogwipo_df.groupby('읍면동', dropna=False)['수량'].sum().reset_index().sort_values('수량', ascending=False)
agg['percent'] = (agg['수량'] / agg['수량'].sum() * 100).round(2)

# 선택: 전체/상위N 보기
col1, col2 = st.columns([2,1])
with col1:
    top_n = st.selectbox("상위 몇 개 읍면동 보일까요?", options=[5, 10, 20, len(agg)], index=0)
with col2:
    show_table = st.checkbox("테이블 함께 보기", value=True)

plot_df = agg.head(top_n).reset_index(drop=True)

if show_table:
    st.subheader("읍면동별 수량 및 비율")
    st.dataframe(plot_df)

# 색 지정: 1등 빨강, 나머지는 그라데이션
colors = make_gradient_colors(len(plot_df))

fig = px.bar(
    plot_df,
    x='읍면동',
    y='percent',
    text='percent',
    title=f"서귀포시 — 읍면동별 인명구조함 비율 (상위 {top_n})",
)
fig.update_traces(marker_color=colors, texttemplate='%{text}%', textposition='outside')
fig.update_layout(yaxis_title='비율 (%)', xaxis_title='읍면동', uniformtext_minsize=8)
fig.update_yaxes(range=[0, max(10, plot_df['percent'].max() * 1.15)])

st.plotly_chart(fig, use_container_width=True)

# 다운로드(옵션): 집계 CSV
csv_bytes = agg.to_csv(index=False).encode('utf-8-sig')
st.download_button("읍면동 집계 CSV 다운로드", data=csv_bytes, file_name="seogwipo_agg.csv", mime="text/csv")

# 추가 정보 / 제안
with st.expander("추가 분석 아이디어"):
    st.write("""
    - 설치 위치(좌표가 있다면)로 지도 시각화(위치 컬럼을 좌표로 변환 필요).  
    - 시간 변화 분석 (데이터기준일자 컬럼을 사용).  
    - 동일 포맷의 다른 시/군 데이터와 비교.
    """)
