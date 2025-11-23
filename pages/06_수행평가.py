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
    "
