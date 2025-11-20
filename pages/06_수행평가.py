import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="오사카 맛집 지도", layout="wide")

st.title("🍜 일본 오사카 현지인 추천 맛집 Top10 지도")
st.write("현지인들이 사랑하는 오사카의 주요 맛집 위치를 폴리움 지도 위에 표시했습니다.")

# 오사카 맛집 Top10 (예시)
restaurants = [
    {"name": "이치란 라멘 난바점", "lat": 34.6669, "lon": 135.5013},
    {"name": "쿠시카츠 다루마 신세카이", "lat": 34.6525, "lon": 135.5063},
    {"name": "마루카메 제면 우동", "lat": 34.6683, "lon": 135.5017},
    {"name": "야키니쿠 호르몬 본점", "lat": 34.6740, "lon": 135.5009},
    {"name": "하나마루 우동", "lat": 34.6698, "lon": 135.4979},
    {"name": "스시 잔마이 도톤보리점", "lat": 34.6691, "lon": 135.5010},
    {"name": "몬자야끼 우메다집", "lat": 34.7025, "lon": 135.4980},
    {"name": "타코야끼 쿠쿠루 본점", "lat": 34.6689, "lon": 135.5012},
    {"name": "규카츠 모토무라", "lat": 34.6685, "lon": 135.5005},
    {"name": "도톤보리 이마이 우동", "lat": 34.6684, "lon": 135.5009},
]

# 지도 생성
osaka_map = folium.Map(location=[34.6937, 135.5023], zoom_start=12)

# 마커 표시
for r in restaurants:
    folium.Marker(
        [r["lat"], r["lon"]],
        popup=r["name"],
        tooltip=r["name"]
    ).add_to(osaka_map)

# Streamlit에 표시
st_folium(osaka_map, width=800, height=600)
