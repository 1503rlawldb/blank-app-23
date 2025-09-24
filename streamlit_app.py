import streamlit as st
import time
import base64
import os

# --- 페이지 설정 ---
st.set_page_config(page_title="도티 키우기", page_icon="👑")

# --- 오디오 재생 함수 (HTML/JS 트릭) ---
def get_audio_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def play_sound(file_path):
    audio_base64 = get_audio_base64(file_path)
    if audio_base64:
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            </audio>
            """, unsafe_allow_html=True)

# --- 게임 상태 초기화 ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.age = 0.0
    st.session_state.subscribers = 0
    st.session_state.subscribers_per_click = 1
    st.session_state.subscribers_per_second = 0
    st.session_state.quality_upgrade_cost = 10
    st.session_state.equipment_upgrade_cost = 50
    st.session_state.last_update_time = time.time()
    
    # 사운드 재생을 위한 플래그
    st.session_state.play_sound_flag = "hoitjja.wav"


# --- 도티 상태 정보 ---
DOTTY_STAGES = {
    0: {"desc": "변기에서 태어난 아기 도티", "color": "#FFD1DC"},
    10: {"desc": "샌드박스에 놀러 간 학생 도티", "color": "#A2D2FF"},
    20: {"desc": "열정 넘치는 신인 크리에이터 도티", "color": "#BDE0FE"},
    30: {"desc": "어엿한 베테랑 크리에이터 도티", "color": "#FFC8DD"},
}

# --- 시간 및 자동 성장 처리 ---
SECONDS_PER_YEAR = 5.0
current_time = time.time()
elapsed_time = current_time - st.session_state.last_update_time

if st.session_state.age < 40:
    # 자동 구독자 증가
    st.session_state.subscribers += st.session_state.subscribers_per_second * elapsed_time
    # 나이 증가
    st.session_state.age += elapsed_time / SECONDS_PER_YEAR

st.session_state.last_update_time = current_time


# --- UI 그리기 ---
st.title("👑 도티 키우기")
st.write("---")

# 게임 클리어 화면
if st.session_state.age >= 40:
    st.header("🎉 살아있는 전설, 40살의 도티!")
    st.balloons()
    final_subs = int(st.session_state.subscribers)
    st.metric("최종 구독자 수", f"{final_subs:,}명")
    st.success("축하합니다! 도티를 40살까지 성공적으로 키웠습니다!")
    
    if st.button("다시 시작하기"):
        st.session_state.clear()
        st.rerun()

# 게임 진행 화면
else:
    # 사운드 플래그가 있으면 재생하고 초기화
    if st.session_state.play_sound_flag:
        play_sound(f"assets/{st.session_state.play_sound_flag}")
        st.session_state.play_sound_flag = None
        
    # 상단 정보 (나이, 구독자)
    col1, col2 = st.columns(2)
    age_display = int(st.session_state.age)
    sub_display = int(st.session_state.subscribers)
    col1.metric("나이", f"{age_display}살")
    col2.metric("구독자", f"{sub_display:,}명")

    # 도티 상태 표시
    current_stage_age = max([k for k in DOTTY_STAGES if k <= st.session_state.age])
    stage_info = DOTTY_STAGES[current_stage_age]
    st.markdown(f"""
    <div style="background-color:{stage_info['color']}; padding: 20px; border-radius: 10px; text-align: center;">
        <h2 style="color: black;">{stage_info['desc']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 여백

    # 콘텐츠 제작 버튼
    if st.button("콘텐츠 제작!", use_container_width=True, type="primary"):
        st.session_state.subscribers += st.session_state.subscribers_per_click
        st.session_state.play_sound_flag = "click.wav"
        st.rerun()

    st.write("---")
    st.subheader("업그레이드")

    # 업그레이드 버튼
    col3, col4 = st.columns(2)
    with col3:
        if st.button(f"영상 퀄리티 (+{st.session_state.subscribers_per_click} / 클릭)", use_container_width=True):
            if st.session_state.subscribers >= st.session_state.quality_upgrade_cost:
                st.session_state.subscribers -= st.session_state.quality_upgrade_cost
                st.session_state.subscribers_per_click += 1
                st.session_state.quality_upgrade_cost = int(st.session_state.quality_upgrade_cost * 1.5)
                st.rerun()
        st.caption(f"비용: {int(st.session_state.quality_upgrade_cost):,}명")

    with col4:
        if st.button(f"장비 업그레이드 (+{st.session_state.subscribers_per_second} / 초)", use_container_width=True):
            if st.session_state.subscribers >= st.session_state.equipment_upgrade_cost:
                st.session_state.subscribers -= st.session_state.equipment_upgrade_cost
                st.session_state.subscribers_per_second += 1
                st.session_state.equipment_upgrade_cost = int(st.session_state.equipment_upgrade_cost * 1.8)
                st.rerun()
        st.caption(f"비용: {int(st.session_state.equipment_upgrade_cost):,}명")