import tkinter as tk
from tkinter import messagebox

# --- 게임 설정 ---
WIDTH = 500
HEIGHT = 600
SECONDS_PER_YEAR = 5 # 1살 먹는 데 걸리는 실제 시간(초)

# --- 효과음 (Windows 전용) ---
try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("알림: 현재 운영체제에서는 효과음을 재생할 수 없습니다. (Windows 전용)")

def play_sound(sound_file):
    if SOUND_ENABLED:
        try:
            winsound.PlaySound(f"assets/{sound_file}", winsound.SND_ASYNC | winsound.SND_FILENAME)
        except Exception as e:
            print(f"사운드 파일 재생 오류: {e}")
            print(f"'{sound_file}' 파일이 'assets' 폴더에 있는지 확인하세요.")

# --- 게임 상태 변수 ---
age = 0
subscribers = 0
subscribers_per_click = 1
subscribers_per_second = 0

# 업그레이드 비용
quality_upgrade_cost = 10
equipment_upgrade_cost = 50

# 시간 흐름 관리
age_timer = 0

# --- 게임 창 설정 ---
root = tk.Tk()
root.title("도티 키우기")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# --- 도티 상태에 따른 텍스트 ---
# 나이에 따라 캐릭터 설명과 이미지가 바뀝니다.
DOTTY_STAGES = {
    0: {"desc": "변기에서 태어난 아기 도티", "color": "#FFD1DC"},
    10: {"desc": "샌드박스에 놀러 간 학생 도티", "color": "#A2D2FF"},
    20: {"desc": "열정 넘치는 신인 크리에이터 도티", "color": "#BDE0FE"},
    30: {"desc": "어엿한 베테랑 크리에이터 도티", "color": "#FFC8DD"},
    40: {"desc": "살아있는 전설, 40살의 도티!", "color": "#FFAFCC"}
}

# --- UI 함수 ---
def update_display():
    """화면의 모든 텍스트를 현재 상태에 맞게 업데이트합니다."""
    # 구독자 수 표시 (단위 추가)
    if subscribers >= 10000:
        sub_text = f"{subscribers/10000:.2f}만 명"
    else:
        sub_text = f"{subscribers}명"
    
    sub_label.config(text=f"구독자: {sub_text}")
    age_label.config(text=f"나이: {age}살")
    
    # 업그레이드 버튼 텍스트 업데이트
    quality_button.config(text=f"영상 퀄리티 ({quality_upgrade_cost}명)")
    equipment_button.config(text=f"장비 업그레이드 ({equipment_upgrade_cost}명)")
    
    # 나이에 맞는 도티 상태 업데이트
    current_stage_age = max([k for k in DOTTY_STAGES if k <= age])
    stage_info = DOTTY_STAGES[current_stage_age]
    dotty_status_label.config(text=stage_info["desc"])
    dotty_display_frame.config(bg=stage_info["color"])


# --- 게임 로직 함수 ---
def create_content():
    """'콘텐츠 제작' 버튼 클릭 시 호출됩니다."""
    global subscribers
    subscribers += subscribers_per_click
    play_sound("click.wav")
    update_display()

def upgrade_quality():
    """영상 퀄리티 업그레이드"""
    global subscribers, subscribers_per_click, quality_upgrade_cost
    if subscribers >= quality_upgrade_cost:
        subscribers -= quality_upgrade_cost
        subscribers_per_click += 1
        quality_upgrade_cost = int(quality_upgrade_cost * 1.5)
        update_display()

def upgrade_equipment():
    """장비 업그레이드 (자동 성장)"""
    global subscribers, subscribers_per_second, equipment_upgrade_cost
    if subscribers >= equipment_upgrade_cost:
        subscribers -= equipment_upgrade_cost
        subscribers_per_second += 1
        equipment_upgrade_cost = int(equipment_upgrade_cost * 1.8)
        update_display()

def game_loop():
    """게임의 메인 루프. 1초마다 실행됩니다."""
    global age, age_timer, subscribers
    
    # 자동 구독자 증가
    subscribers += subscribers_per_second
    
    # 나이 증가
    age_timer += 1
    if age_timer >= SECONDS_PER_YEAR:
        age += 1
        age_timer = 0
        if age == 1: # 1살이 될 때 배경음악 시작
             play_sound("bgm.wav")
    
    update_display()
    
    # 게임 종료 조건
    if age >= 40:
        messagebox.showinfo("게임 클리어!", f"축하합니다! 도티를 40살까지 성공적으로 키웠습니다!\n최종 구독자 수: {subscribers}명")
        root.destroy()
    else:
        root.after(1000, game_loop) # 1000ms = 1초 뒤에 다시 실행


# --- UI 위젯 생성 ---

# 상단 정보 프레임
info_frame = tk.Frame(root)
info_frame.pack(pady=10)
age_label = tk.Label(info_frame, text="나이: 0살", font=("Arial", 16))
age_label.pack(side="left", padx=10)
sub_label = tk.Label(info_frame, text="구독자: 0명", font=("Arial", 16))
sub_label.pack(side="left", padx=10)

# 도티 상태 표시 프레임
dotty_display_frame = tk.Frame(root, bg="#FFD1DC", bd=2, relief="solid")
dotty_display_frame.pack(pady=20, padx=20, fill="x")
dotty_status_label = tk.Label(dotty_display_frame, text="변기에서 태어난 아기 도티", font=("Arial", 20, "bold"), height=4)
dotty_status_label.pack(pady=20)

# 메인 액션 버튼
action_button = tk.Button(root, text="콘텐츠 제작!", font=("Arial", 18, "bold"), command=create_content, bg="#FF6B6B", fg="white")
action_button.pack(pady=10, ipadx=20, ipady=10)

# 업그레이드 프레임
upgrade_frame = tk.Frame(root)
upgrade_frame.pack(pady=20)
quality_button = tk.Button(upgrade_frame, text=f"영상 퀄리티 ({quality_upgrade_cost}명)", command=upgrade_quality)
quality_button.pack(side="left", padx=10, ipady=5)
equipment_button = tk.Button(upgrade_frame, text=f"장비 업그레이드 ({equipment_upgrade_cost}명)", command=upgrade_equipment)
equipment_button.pack(side="left", padx=10, ipady=5)


# --- 게임 시작 ---
play_sound("hoitjja.wav") # 게임 시작 시 "호잇짜" 재생
game_loop()
root.mainloop()