import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="서울 관광지 지도", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울의 주요 관광지 TOP 10")

st.markdown("""
서울은 전통과 현대가 공존하는 매력적인 도시입니다.  
아래 지도에는 외국인들이 가장 많이 방문하고 좋아하는 서울의 대표 관광지 10곳이 표시되어 있습니다.
""")

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# 관광지 데이터 (예시)
tourist_spots = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "조선 왕조의 법궁"},
    {"name": "명동거리", "lat": 37.5636, "lon": 126.9827, "desc": "쇼핑과 길거리 음식의 중심"},
    {"name": "남산타워(N서울타워)", "lat": 37.5512, "lon": 126.9882, "desc": "서울 전경을 한눈에 볼 수 있는 명소"},
    {"name": "북촌한옥마을", "lat": 37.5826, "lon": 126.9830, "desc": "전통 한옥이 모여 있는 마을"},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.5665, "lon": 127.0090, "desc": "현대적인 디자인의 랜드마크"},
    {"name": "홍대거리", "lat": 37.5563, "lon": 126.9220, "desc": "젊음과 예술의 거리"},
    {"name": "이태원", "lat": 37.5349, "lon": 126.9944, "desc": "다국적 문화와 음식의 거리"},
    {"name": "청계천", "lat": 37.5694, "lon": 126.9780, "desc": "도심 속 휴식 공간"},
    {"name": "롯데월드", "lat": 37.5110, "lon": 127.0980, "desc": "대형 놀이공원"},
    {"name": "잠실 롯데타워", "lat": 37.5130, "lon": 127.1026, "desc": "대한민국 최고층 빌딩"},
]

# Folium 지도 생성
m = folium.Map(location=seoul_center, zoom_start=12)

# 마커 추가
for spot in tourist_spots:
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=f"<b>{spot['name']}</b><br>{spot['desc']}",
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=800, height=600)
