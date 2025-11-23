# File: pages/osaka_food_map.py
# Streamlit + Folium map showing Osaka Top10 local-favorite restaurants
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Osaka Top10 Local Eats (Folium)", layout="wide")

st.title("🍜 Osaka — Locals' Top 10 Eats (Folium map)")
st.markdown(
    "이 지도는 여러 여행 가이드·리뷰(로컬/트립어드바이저 등)를 바탕으로 '오사카 현지/로컬에게 인기 있는' 맛집 후보 Top10을 표시합니다. "
    "좌표는 공개 정보를 바탕으로 근사값을 사용했습니다. 방문 전 최신 정보를 반드시 확인하세요."
)

# --- Top10 리스트 (이름, 위도, 경도, 설명, 출처) ---
# 좌표는 공개 출처(관광 가이드/업체 페이지 등)를 참고해 근사값으로 기입했습니다.
places = [
    {"name": "Mizuno (Okonomiyaki, Dotonbori)", "lat": 34.66909, "lon": 135.50104,
     "desc": "오사카 명물 오코노미야키(미즈노, 도톤보리)", "source":"https://insideosaka.com/mizuno/"},
    {"name": "Kushikatsu Daruma (Shinsekai)", "lat": 34.65250, "lon": 135.50630,
     "desc": "신세카이의 전통 쿠시카츠 명소(다루마)", "source":"https://www.gltjp.com/en/directory/item/11883/"},
    {"name": "Takoyaki Wanaka (Dotonbori / Namba)", "lat": 34.66885, "lon": 135.50130,
     "desc": "나니와 스타일의 인기 타코야키(와나카)", "source":"https://metronine.osaka/en/kiosk/spot-detail/?spot_id=16385150523118"},
    {"name": "Kani Doraku (Dotonbori, Crab specialty)", "lat": 34.66887, "lon": 135.50140,
     "desc": "도톤보리의 상징적 게 전문점(간이도라쿠)", "source":"https://douraku.co.jp/en/search/"},
    {"name": "Endo Sushi (Osaka Central Fish Market / Kyobashi branch)", "lat": 34.66590, "lon": 135.49400,
     "desc": "오사카 중앙 어시장의 전통 초밥집(엔도스시)", "source":"http://www.endo-sushi.com/english"},
    {"name": "Kuromon Ichiba Market (street stalls & local eats)", "lat": 34.66531, "lon": 135.50701,
     "desc": "쿠로몬 시장 — 현지식 포장·스낵 명소", "source":"https://matcha-jp.com/en/8236"},
    {"name": "Ichiran (Dotonbori ramen / popular ramen chain branch)", "lat": 34.66870, "lon": 135.50110,
     "desc": "개별 부스형 라멘 체인(잇쵸란 도톤보리 지점)", "source":"https://ichiran.com/"},
    {"name": "Izakaya Toyo (Toyo-san, Kyobashi area)", "lat": 34.69720, "lon": 135.53513,
     "desc": "지역에서 유명한 즉석 이자카야(토요)", "source":"https://en.tobacco.tokyo/osaka-fu/osaka-shi-miyakojima-ku/higashinodamachi-3/night/1u7t"},
    {"name": "Kawafuku Honten (Handmade udon, Shinsaibashi)", "lat": 34.67289, "lon": 135.50342,
     "desc": "수타 우동의 고향격 가게(카와후쿠 본점)", "source":"https://www.osaka-kawafuku.com/kawafuku/"},
    {"name": "ChaoChao Gyoza (popular gyoza shop)", "lat": 34.67180, "lon": 135.50210,
     "desc": "현지에서 사랑받는 작은 교자 가게(챠오챠오)", "source":"https://ilseonthego.com/best-cheap-eats-osaka/"}
]

# --- Map 기본 설정: 오사카 중심 좌표와 줌 레벨 ---
# 중심은 도톤보리/난바 근처로 설정
map_center = [34.6687, 135.5013]
m = folium.Map(location=map_center, zoom_start=13, tiles="OpenStreetMap")

# Add marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers with popups
for p in places:
    popup_html = f"""
    <b>{p['name']}</b><br/>
    {p['desc']}<br/>
    <a href="{p['source']}" target="_blank">출처 열기</a>
    """
    folium.Marker(
        location=[p['lat'], p['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=p['name'],
        icon=folium.Icon(color="green", icon="cutlery", prefix='fa')
    ).add_to(marker_cluster)

# 추가: 중심 마커(도톤보리)
folium.CircleMarker(location=map_center, radius=6, color="crimson", fill=True, fill_opacity=0.7,
                    popup="도톤보리 근처 (지도 중심)").add_to(m)

# Streamlit에 Folium 지도 표시 (streamlit_folium 사용)
st.subheader("오사카 Top10 음식 지도 (현지/인기 기반 후보)")
map_out = st_folium(m, width=1100, height=700)

st.markdown("**참고 및 주의**: 위 리스트는 여행/맛집 가이드·리뷰(로컬 추천 포함)를 바탕으로 선정한 후보입니다. 실제 영업상황·휴무·위치 변경 가능성이 있으니 방문 전 반드시 공식 사이트/지도/업체에 확인하세요.")
st.markdown("핵심 출처 예시: Mizuno(도톤보리), Kushikatsu Daruma(신세카이), Takoyaki Wanaka, Endo Sushi, Kuromon Ichiba 등. (앱 내 개별 마커에 출처 링크 포함).")
