import tkinter as tk
import random
import time

# --- 게임 설정 ---
WIDTH = 500
HEIGHT = 700
NOTE_SPEED = 5
NOTE_WIDTH = 80
NOTE_HEIGHT = 20

# --- 색상 ---
COLORS = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF"] # A, S, D, F 키 색상
BACKGROUND_COLOR = "#333333"
LINE_COLOR = "#FFFFFF"

# --- 효과음 (Windows 전용) ---
# winsound는 Windows에만 기본 포함된 라이브러리입니다.
try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("알림: 현재 운영체제에서는 효과음을 재생할 수 없습니다. (Windows 전용)")

def play_hit_sound():
    if SOUND_ENABLED:
        # SND_ASYNC: 소리가 나는 동안 게임이 멈추지 않도록 함
        winsound.PlaySound("assets/hit_sound.wav", winsound.SND_ASYNC)

def play_miss_sound():
    if SOUND_ENABLED:
        winsound.PlaySound("assets/miss_sound.wav", winsound.SND_ASYNC)

# --- 게임 상태 변수 ---
score = 0
combo = 0
notes = [] # 현재 화면의 노트들을 저장하는 리스트

# --- 게임 창 설정 ---
root = tk.Tk()
root.title("No-Install Rhythm Game")
root.resizable(False, False) # 창 크기 변경 불가

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

# --- 게임 요소 그리기 ---
# 게임 라인
for i in range(5):
    x = 50 + i * 100
    canvas.create_line(x, 0, x, HEIGHT, fill=LINE_COLOR, width=2)

# 판정선
JUDGEMENT_LINE_Y = HEIGHT - 100
canvas.create_line(50, JUDGEMENT_LINE_Y, 450, JUDGEMENT_LINE_Y, fill="#FFFF00", width=5)

# 점수 및 콤보 텍스트
score_text = canvas.create_text(10, 10, text=f"Score: {score}", fill=LINE_COLOR, font=("Arial", 16), anchor="nw")
combo_text = canvas.create_text(10, 40, text=f"Combo: {combo}", fill=LINE_COLOR, font=("Arial", 16), anchor="nw")
start_text = canvas.create_text(WIDTH/2, HEIGHT/2, text="Press Any Key to Start", fill=LINE_COLOR, font=("Arial", 24))

# --- 게임 로직 ---
def create_note():
    lane = random.randint(0, 3)
    x1 = 50 + lane * 100 + 10
    y1 = -NOTE_HEIGHT
    x2 = x1 + NOTE_WIDTH
    y2 = 0
    
    note_id = canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[lane])
    notes.append({'id': note_id, 'lane': lane})

def move_notes():
    global combo
    
    # 리스트 복사본을 순회하여 삭제 오류 방지
    for note in notes[:]:
        canvas.move(note['id'], 0, NOTE_SPEED)
        pos = canvas.coords(note['id'])
        
        # 판정선을 지나치면 MISS 처리
        if pos and pos[1] > JUDGEMENT_LINE_Y + 20:
            canvas.delete(note['id'])
            notes.remove(note)
            combo = 0
            canvas.itemconfig(combo_text, text=f"Combo: {combo}")
            play_miss_sound()

def check_hit(lane_to_check):
    global score, combo
    
    hit = False
    for note in notes[:]:
        if note['lane'] == lane_to_check:
            pos = canvas.coords(note['id'])
            # 판정선 근처에 있는지 확인
            if pos and abs(pos[3] - JUDGEMENT_LINE_Y) < 30:
                canvas.delete(note['id'])
                notes.remove(note)
                
                score += 100
                combo += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
                canvas.itemconfig(combo_text, text=f"Combo: {combo}")
                play_hit_sound()
                hit = True
                break # 한 번에 하나의 노트만 처리
    
    if not hit:
        combo = 0
        canvas.itemconfig(combo_text, text=f"Combo: {combo}")
        play_miss_sound()

# --- 키 입력 처리 ---
key_map = {'a': 0, 's': 1, 'd': 2, 'f': 3}
for key, lane in key_map.items():
    # 람다 함수를 사용하여 올바른 lane 값을 전달
    root.bind(f"<KeyPress-{key}>", lambda event, l=lane: check_hit(l))

# --- 메인 게임 루프 ---
game_running = False
note_spawn_counter = 0

def game_loop():
    global note_spawn_counter
    
    if game_running:
        move_notes()
        
        note_spawn_counter += 1
        if note_spawn_counter >= 50: # 노트 생성 주기
            create_note()
            note_spawn_counter = 0

    # 1/60초(약 16ms)마다 game_loop 함수를 다시 실행
    root.after(16, game_loop)

def start_game(event):
    global game_running
    if not game_running:
        game_running = True
        canvas.delete(start_text)
        game_loop()

# 아무 키나 누르면 게임 시작
root.bind("<KeyPress>", start_game)

root.mainloop()