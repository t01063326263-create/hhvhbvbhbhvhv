# mbti_recs_app.py
import streamlit as st

st.set_page_config(page_title="MBTI 책·영화 추천 🌟", page_icon="📚🎬", layout="centered")

st.title("MBTI별 책·영화 추천 ✨")
st.caption("MBTI 하나 골라봐 — 그 유형에 어울리는 책 2권과 영화 2편을 추천해줄게!")

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 추천 데이터 구조: {MBTI: {"books": [(title, short)], "movies":[(title, short)]}}
RECS = {
    "ISTJ": {
        "books": [
            ("To Kill a Mockingbird", "책임감 있고 규칙을 중시하는 ISTJ에게, 정의와 성찰을 다룬 고전."),
            ("The Hobbit", "계획적이고 실용적인 성향에 맞는 탄탄한 모험 서사.")
        ],
        "movies": [
            ("Hidden Figures", "성실함과 실력이 드러나는 실화 기반 영화."),
            ("The Shawshank Redemption", "인내와 원칙이 중심이 되는 서사.")
        ]
    },
    "ISFJ": {
        "books": [
            ("Little Women", "돌보는 성향과 공감 능력에 잘 맞는 따뜻한 성장 이야기."),
            ("Anne of Green Gables", "사려 깊고 헌신적인 성격에 어울리는 감성 소설.")
        ],
        "movies": [
            ("Wonder", "타인을 배려하는 마음을 다루는 감동 드라마."),
            ("The Secret Life of Walter Mitty", "안정적이지만 가끔 모험을 꿈꾸는 이에게.")
        ]
    },
    "INFJ": {
        "books": [
            ("The Little Prince", "내면의 의미를 찾는 INFJ에게 잘 맞는 철학적 동화."),
            ("Man's Search for Meaning", "의미 추구와 공감 능력을 자극하는 책.")
        ],
        "movies": [
            ("Dead Poets Society", "가치와 이상을 깊게 고민하는 사람에게 추천."),
            ("Her", "감정과 관계의 미묘함을 섬세하게 그린 작품.")
        ]
    },
    "INTJ": {
        "books": [
            ("1984", "전략적 · 분석적 사고를 하는 INTJ에게 도전적인 고전."),
            ("The Martian", "문제 해결 능력과 자기주도성이 돋보이는 소설.")
        ],
        "movies": [
            ("Inception", "복잡한 구조와 전략적 사고를 즐기는 이에게."),
            ("Interstellar", "큰 비전과 논리를 좋아하는 성향에 어울림.")
        ]
    },
    "ISTP": {
        "books": [
            ("The Old Man and the Sea", "실천적이고 직관적인 ISTP에게 맞는 간결한 서사."),
            ("Ender's Game", "실전적 문제 해결과 전략 요소가 많은 작품.")
        ],
        "movies": [
            ("The Karate Kid", "실용적 훈련과 성장 서사가 잘 맞음."),
            ("Baby Driver", "빠른 템포와 능동적 행동을 즐기는 이에게.")
        ]
    },
    "ISFP": {
        "books": [
            ("Norwegian Wood", "감성적이고 예술적 감각이 강한 ISFP에게 맞는 문학."),
            ("The Fault in Our Stars", "섬세한 감정 묘사를 좋아하는 사람에게.")
        ],
        "movies": [
            ("Spirited Away", "시각적·감정적 경험을 중시하는 이에게 추천."),
            ("Call Me by Your Name", "감성적 교감과 섬세함을 느낄 수 있는 작품.")
        ]
    },
    "INFP": {
        "books": [
            ("The Alchemist", "이상과 꿈을 좇는 INFP에게 영감을 주는 이야기."),
            ("The Little Prince", "내면의 상상력과 가치관을 자극하는 동화.")
        ],
        "movies": [
            ("Amélie", "낭만적 상상력과 따뜻함을 좋아하는 이에게."),
            ("The Perks of Being a Wallflower", "감정의 깊이를 탐구하는 성장 영화.")
        ]
    },
    "INTP": {
        "books": [
            ("The Curious Incident of the Dog in the Night-Time", "지적인 호기심과 독특한 시각을 즐기는 사람에게."),
            ("Flatland", "논리적 사고와 개념적 상상을 자극하는 고전.")
        ],
        "movies": [
            ("The Imitation Game", "지적 도전과 분석을 좋아하는 이에게."),
            ("Good Will Hunting", "문제 해결과 자기성찰을 그린 작품.")
        ]
    },
    "ESTP": {
        "books": [
            ("The Outsiders", "실제적이고 행동지향적인 ESTP에게 공감 가는 이야기."),
            ("Delivering Happiness", "즉각적인 실행과 경험 가치를 중시하는 이에게.")
        ],
        "movies": [
            ("Ferris Bueller's Day Off", "자유롭고 즉흥적인 스타일을 즐기는 이에게."),
            ("Ocean's Eleven", "스릴과 재치, 액션을 좋아하는 사람에게.")
        ]
    },
    "ESFP": {
        "books": [
            ("Eat Pray Love", "경험 중심적이고 감각을 즐기는 ESFP에게."),
            ("The Sun Is Also a Star", "감정과 만남의 순간을 중요하게 여기는 이에게.")
        ],
        "movies": [
            ("La La Land", "음악과 감각적인 경험을 좋아하는 사람에게."),
            ("The Greatest Showman", "공연과 활기를 즐기는 이에게 어울림.")
        ]
    },
    "ENFP": {
        "books": [
            ("The Alchemist", "아이디어와 가능성에 열려 있는 ENFP에게 영감 제공."),
            ("Big Magic", "창의적 모험과 용기를 북돋아 주는 책.")
        ],
        "movies": [
            ("Inside Out", "감정과 상상력을 중요시하는 사람에게."),
            ("Into the Wild", "자유와 탐험을 동경하는 이에게.")
        ]
    },
    "ENTP": {
        "books": [
            ("Surely You're Joking, Mr. Feynman!", "호기심 많고 토론을 즐기는 ENTP에게 즐거운 읽을거리."),
            ("The Art of Strategy (basic intro)", "토론과 전략적 사고를 즐기는 이에게.")
        ],
        "movies": [
            ("The Social Network", "아이디어와 토론, 기발함을 다룬 영화."),
            ("The Big Short", "유머 섞인 논쟁과 사고 전개를 좋아하는 이에게.")
        ]
    },
    "ESTJ": {
        "books": [
            ("How to Win Friends and Influence People", "조직적·실용적 리더십을 지향하는 ESTJ에게."),
            ("The 7 Habits of Highly Effective People", "체계적 자기관리와 목표지향적 사고에 도움됨.")
        ],
        "movies": [
            ("Remember the Titans", "리더십과 팀워크를 다룬 감동 실화."),
            ("The Devil Wears Prada", "실무 중심적이고 목표지향적인 분위기 이해에 도움됨.")
        ]
    },
    "ESFJ": {
        "books": [
            ("Pride and Prejudice", "관계와 사회적 조화를 중시하는 ESFJ에게."),
            ("Little Women", "돌봄과 유대감을 다루는 따뜻한 소설.")
        ],
        "movies": [
            ("Chef", "사람들과의 연결과 즐거운 분위기를 좋아하는 이에게."),
            ("The Help", "공감과 연대를 다룬 작품.")
        ]
    },
    "ENFJ": {
        "books": [
            ("Man's Search for Meaning", "타인을 이끄는 데서 오는 책임과 의미를 고민하는 이에게."),
            ("To Kill a Mockingbird", "공감과 정의에 민감한 ENFJ에게 잘 맞음.")
        ],
        "movies": [
            ("Dead Poets Society", "영향력과 리더십의 의미를 생각하게 함."),
            ("The King's Speech", "소통과 용기를 다룬 실화 기반 영화.")
        ]
    },
    "ENTJ": {
        "books": [
            ("The Prince", "전략과 리더십에 관심 많은 ENTJ가 읽어볼 만한 고전."),
            ("Good to Great", "조직과 성과에 관심있는 사람에게 실용적 인사이트 제공.")
        ],
        "movies": [
            ("The Godfather", "권력과 전략, 리더십 테마를 다루는 고전."),
            ("Scent of a Woman", "결단력과 영향력을 보여주는 드라마.")
        ]
    }
}

# --- UI ---
st.write("👉 MBTI를 골라볼래?")

col1, col2 = st.columns([2,3])
with col1:
    mbti_choice = st.selectbox("MBTI 선택", MBTI_LIST, index=0)

with col2:
    st.markdown("**한줄 TIP**: MBTI는 성향 참고용이야. 꼭 맞아야 할 필요는 없어!")

st.markdown("---")

if mbti_choice:
    rec = RECS.get(mbti_choice, {})
    st.header(f"{mbti_choice} 추천 목록 🎯")
    st.subheader("책 📚")
    for title, desc in rec.get("books", []):
        st.markdown(f"- **{title}** — {desc}")
    st.subheader("영화 🎬")
    for title, desc in rec.get("movies", []):
        st.markdown(f"- **{title}** — {desc}")

    st.markdown("---")
    st.info("추가로 원하면 해당 책/영화의 '읽기 포인트'나 '감상 포인트'도 간단히 정리해줄게. 원하면 그냥 '요약해줘'라고 말해줘! 😊")

st.caption("만든 사람: 옥경 스타일 추천기 — 학생분들 취향에 맞게 골라봤어요.")
