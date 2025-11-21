# File: pages/gas_imports_dashboard.py
# Streamlit app — 한국의 수입(중량) by 국가/지역 (Plotly 그래프, 1등 초록, 나머지 그라데이션)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="한국의 가스(중량) 수입 - 국가/지역별", layout="wide")

@st.cache_data
def load_data(paths=None, encodings=None):
    if paths is None:
        paths = ["./vvs.csv", "/mnt/data/vvs.csv", "./csv.csv", "/mnt/data/csv.csv"]
    if encodings is None:
        encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin1"]
    for p in paths:
        for enc in encodings:
            try:
                df = pd.read_csv(p, encoding=enc, low_memory=False)
                st.session_state['__data_path_used'] = p
                st.session_state['__data_enc_used'] = enc
                return df
            except Exception:
                continue
    raise FileNotFoundError("프로젝트 루트 또는 /mnt/data에 vvs.csv를 업로드해 주세요.")

def make_green_gradient(n: int) -> list:
    """첫 번째 항목은 초록색(#008000), 나머지는 연한->진한 그라데이션"""
    if n <= 0:
        return []
    if n == 1:
        return ["#008000"]
    start = np.array([230, 255, 230])  # 연한 연두
    end = np.array([0, 128, 0])        # 진한 초록
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)
        rgb = np.round((1 - t) * start + t * end).astype(int)
        colors.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    colors[0] = "#008000"  # 1등은 고정 초록
    return colors

# Load data
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.title("🇰🇷 한국의 수입(중량) — 국가/지역별 비교")
st.caption(f"데이터 경로: {st.session_state.get('__data_path_used','unknown')}  |  인코딩: {st.session_state.get('__data_enc_used','unknown')}")

# Quick overview
with st.expander("데이터 기본 정보(미리보기)"):
    st.write("행/열:", df.shape)
    st.write("컬럼:", df.columns.tolist())
    st.dataframe(df.head(8))

# Identify weight columns (중량(톤)_*)
weight_cols = [c for c in df.columns if c.startswith('중량(톤)') or c.startswith('중량(톤)_')]

if not weight_cols:
    st.error("데이터에서 '중량(톤)_...' 형식의 컬럼을 찾을 수 없습니다. 파일 컬럼명을 확인해주세요.")
    st.stop()

# Map col -> label (suffix)
mapping = {}
for c in weight_cols:
    # typical format: '중량(톤)_아시아' or '중량(톤)_합계'
    if '_' in c:
        label = c.split('_', 1)[1]
    else:
        # fallback
        label = c.replace('중량(톤)', '').strip('_ ')
    mapping[c] = label if label else '전체'

# Compute totals (sum across time)
totals = []
for c, label in mapping.items():
    s = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce').fillna(0).sum()
    totals.append({'region_or_country': label, 'total_tons': int(s)})

tot_df = pd.DataFrame(totals).sort_values('total_tons', ascending=False).reset_index(drop=True)

# Option: exclude '합계' from bar chart by default
exclude_total = st.checkbox("전체 합계('합계')를 차트에서 제외", value=True)
plot_df = tot_df.copy()
if exclude_total and ('합계' in plot_df['region_or_country'].values):
    plot_df = plot_df[plot_df['region_or_country'] != '합계'].reset_index(drop=True)

# Controls
col1, col2 = st.columns([3,1])
with col1:
    top_n = st.slider("상위 몇 개 국가/지역을 표시할까요?", min_value=3, max_value=min(20, len(plot_df)), value=min(10, len(plot_df)))
with col2:
    normalize_percent = st.checkbox("백분율(%)로 표시", value=True)

plot_df = plot_df.head(top_n).copy()
if normalize_percent:
    total = plot_df['total_tons'].sum()
    plot_df['percent'] = (plot_df['total_tons'] / total * 100).round(2)
    y_col = 'percent'
    y_title = '비율 (%)'
    text_col = 'percent'
else:
    y_col = 'total_tons'
    y_title = '중량 (톤)'
    text_col = 'total_tons'

# Colors: 1등 초록, 나머지는 그라데이션
colors = make_green_gradient(len(plot_df))

fig = px.bar(
    plot_df,
    x='region_or_country',
    y=y_col,
    text=text_col,
    title=f"한국의 수입 중량 — 상위 {top_n} (총 {plot_df[y_col].sum():,.0f}{' %' if normalize_percent else ' 톤'})"
)
fig.update_traces(marker_color=colors, texttemplate="%{text}%", textposition='outside')
fig.update_layout(xaxis_title='국가/지역', yaxis_title=y_title, uniformtext_minsize=8)
# y축 범위 살짝 여유 주기
fig.update_yaxes(range=[0, max( (plot_df[y_col].max()*1.15), 10 )])

st.plotly_chart(fig, use_container_width=True)

# Show table and allow CSV download
with st.expander("원본 집계 테이블"):
    st.dataframe(plot_df)

csv_bytes = tot_df.to_csv(index=False).encode('utf-8-sig')
st.download_button("국가/지역별 중량 합계 CSV 다운로드", data=csv_bytes, file_name="korea_gas_imports_by_region.csv", mime="text/csv")

st.markdown("**참고**: 데이터셋에는 일부 개별 국가(예: '러시아')와 함께 '중동','아시아' 같은 지역 컬럼이 섞여있습니다. '국가별'을 엄밀히 원하시면 개별 국가 컬럼이 있는지 확인하거나 원자료(품목/수출입 항목별 세부표)가 필요할 수 있습니다.")


