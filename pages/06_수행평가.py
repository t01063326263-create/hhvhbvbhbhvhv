import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data(file_path):
    """CSV 파일을 로드하고 '연월일'을 datetime으로 변환합니다."""
    try:
        # 파일 인코딩 문제로 'cp949' 또는 'euc-kr' 시도
        df = pd.read_csv(file_path, encoding='euc-kr')
        
        # '연월일' 열을 datetime 객체로 변환
        df['연월일'] = pd.to_datetime(df['연월일'])
        
        return df
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

def preprocess_data(df):
    """대륙별 중량(톤) 데이터를 추출하고 합계를 계산합니다."""
    
    # '중량(톤)'으로 끝나는 열만 필터링 (총합 제외)
    weight_cols = [col for col in df.columns if col.endswith('_중량(톤)') and not col.endswith('합계_중량(톤)')]
    
    # 열 이름에서 '중량(톤)'을 제거하고 대륙 이름만 남깁니다.
    continent_cols = {col: col.split('_')[1] for col in weight_cols}
    
    # 중량 데이터프레임 생성 및 열 이름 변경
    df_weight = df[weight_cols].rename(columns=continent_cols)
    
    # 각 대륙별 총합 계산
    continent_sums = df_weight.sum().sort_values(ascending=False).reset_index()
    continent_sums.columns = ['대륙', '총 수입 중량(톤)']
    
    return continent_sums

def create_bar_chart(df):
    """Plotly를 사용하여 인터랙티브한 막대 그래프를 생성합니다."""
    
    # 1위 대륙 확인
    top_continent = df.iloc[0]['대륙']
    
    # 색상 맵 생성: 1위는 초록색, 나머지는 파란색 계열 그라데이션
    color_map = {continent: '#3cb371' if continent == top_continent else '#4682b4' for continent in df['대륙']}
    
    # Plotly 막대 그래프 생성
    fig = px.bar(
        df, 
        x='대륙', 
        y='총 수입 중량(톤)', 
        title='🇰🇷 한국의 대륙별 천연가스 총 수입 중량 (톤)',
        color='대륙', # 색상을 대륙별로 적용
        color_discrete_map=color_map,
        labels={'총 수입 중량(톤)': '총 수입 중량 (톤)', '대륙': '대륙'},
        template='plotly_white'
    )
    
    # y축 포맷 변경 (10억 단위로)
    fig.update_yaxes(tickformat=',.2s', title='총 수입 중량 (톤)')
    
    # 막대 위에 값 표시
    fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig

# Streamlit 앱 시작
def main():
    st.set_page_config(layout="wide", page_title="천연가스 수입 분석")
    st.title("🚢 한국 천연가스 대륙별 수입 현황 분석")
    st.write("---")
    
    # CSV 파일 경로 설정 (pages 폴더 기준 상위 폴더)
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '..', '한국가스공사_한국의 대륙별 천연가스 수입 현황_20240630.csv')
    
    df = load_data(csv_path)
    
    if df is not None:
        st.subheader("1. 전체 기간 대륙별 총 수입량")
        
        continent_sums_df = preprocess_data(df)
        
        # 데이터 테이블 출력
        st.dataframe(
            continent_sums_df, 
            hide_index=True,
            column_config={
                "총 수입 중량(톤)": st.column_config.NumberColumn(
                    "총 수입 중량 (톤)",
                    format="%d"
                )
            }
        )
        
        # 막대 그래프 시각화
        st.subheader("2. 수입량 시각화 (막대 그래프)")
        fig = create_bar_chart(continent_sums_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"데이터 기간: {df['연월일'].min().strftime('%Y년 %m월')} ~ {df['연월일'].max().strftime('%Y년 %m월')}")
        
if __name__ == '__main__':
    main()
