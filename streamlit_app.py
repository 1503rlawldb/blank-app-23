import pygame
import random
import os

# 게임 화면 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Pygame 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("간단 리듬 게임")
clock = pygame.time.Clock()

# --- 음악 및 효과음 로드 ---
# 아래 'assets' 폴더를 만들고 사운드 파일을 넣어주세요.
# 예시 파일: https://drive.google.com/drive/folders/1-ABGq_xM2_6Yk2gDaY4gZ3d7B_c7B-9b?usp=sharing
# 위 링크에서 파일을 다운받아 코드 파일과 같은 위치에 'assets' 폴더를 만들어 넣어주세요.

try:
    pygame.mixer.music.load(os.path.join("assets", "background_music.mp3"))
    hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit_sound.wav"))
    miss_sound = pygame.mixer.Sound(os.path.join("assets", "miss_sound.wav"))
    pygame.mixer.music.set_volume(0.5)
    hit_sound.set_volume(0.8)
    miss_sound.set_volume(0.4)
except pygame.error as e:
    print(f"오디오 파일을 불러올 수 없습니다: {e}")
    print("게임 실행을 위해 'assets' 폴더와 사운드 파일이 필요합니다.")
    # 필요한 경우, 여기서 프로그램을 종료하거나 기본값으로 계속 진행할 수 있습니다.


# 노트 클래스
class Note(pygame.sprite.Sprite):
    def __init__(self, column):
        super().__init__()
        self.column = column
        self.image = pygame.Surface([100, 20])
        colors = [RED, GREEN, BLUE, YELLOW]
        self.image.fill(colors[column])
        self.rect = self.image.get_rect()
        self.rect.x = 50 + column * 125
        self.rect.y = -50
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # 화면 밖으로 나가면 노트 제거

# 게임 변수
all_sprites = pygame.sprite.Group()
notes = pygame.sprite.Group()
score = 0
combo = 0
font = pygame.font.SysFont("malgungothic", 40)
spawn_timer = 0
spawn_rate = 30 # 숫자가 작을수록 노트가 자주 나옴

# 판정선
judgment_line_y = SCREEN_HEIGHT - 100

# 키 상태를 저장할 딕셔너리
key_pressed_effect = {pygame.K_a: 0, pygame.K_s: 0, pygame.K_d: 0, pygame.K_f: 0}
key_mapping = {
    pygame.K_a: 0,
    pygame.K_s: 1,
    pygame.K_d: 2,
    pygame.K_f: 3
}
key_positions = [100, 225, 350, 475]


# 게임 루프
running = True
game_started = False

while running:
    clock.tick(FPS)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True
                pygame.mixer.music.play(-1) # 음악 무한 반복 재생

            if event.key in key_pressed_effect:
                key_pressed_effect[event.key] = 10 # 키 누름 효과 타이머 설정
                col = key_mapping[event.key]
                hit = False
                # 판정선 근처 노트 찾기
                for note in notes:
                    if note.column == col and abs(note.rect.centery - judgment_line_y) < 40:
                        hit_sound.play()
                        score += 100
                        combo += 1
                        note.kill()
                        hit = True
                        break
                if not hit:
                    miss_sound.play()
                    combo = 0


    # 게임 로직
    if game_started:
        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            spawn_timer = 0
            new_note = Note(random.randint(0, 3))
            all_sprites.add(new_note)
            notes.add(new_note)

        all_sprites.update()

        # 판정선을 지나친 노트 처리
        for note in notes:
            if note.rect.top > judgment_line_y + 40:
                 miss_sound.play()
                 combo = 0
                 note.kill()


    # 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # UI 그리기 (라인, 판정선, 점수 등)
    for i in range(5):
        pygame.draw.line(screen, WHITE, (50 + i * 125, 0), (50 + i * 125, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, YELLOW, (50, judgment_line_y), (550, judgment_line_y), 5)

    # 키 누름 효과
    for key, timer in key_pressed_effect.items():
        if timer > 0:
            col = key_mapping[key]
            pygame.draw.rect(screen, WHITE, [50 + col * 125, judgment_line_y - 50, 100, 100], 5)
            key_pressed_effect[key] -= 1

    # 시작 화면
    if not game_started:
        start_text = font.render("아무 키나 눌러서 시작하세요!", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))

    # 점수와 콤보 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    combo_text = font.render(f"Combo: {combo}", True, YELLOW if combo > 0 else WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 60))

    pygame.display.flip()

pygame.quit()