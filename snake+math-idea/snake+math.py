import pygame
import time
import random
import arabic_reshaper
from bidi.algorithm import get_display

snake_speed = 15

window_x = 1000
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(200, 200, 50)

pygame.init()

pygame.display.set_caption('Snake Game By : R.N')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


def render_persian_text(font, text, color, screen, position):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        text_surface = font.render(bidi_text, True, color)
        screen.blit(text_surface, position)
    except Exception as e:
        print(f"خطا در رندر متن فارسی: {e}")
        try:
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, position)
        except:
            pass


def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)


def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


questions = [
    {"question": "حاصل عبارت 5 - (3 - 7) کدام است؟", "options": ["9", "-9", "1", "-1"], "correct_index": 0},
    {"question": "بزرگترین عدد صحیح کوچکتر از 3.7- کدام است؟", "options": ["4-", "3-", "0", "5-"], "correct_index": 0},
    {"question": "اگر a = -2 و b = 3 باشد، حاصل (a² - b) × (a + b) برابر است با:", "options": ["7-", "5", "-5", "1"], "correct_index": 2},
    {"question": "کدام یک از اعداد زیر گویا نیست؟", "options": ["2/3", "0.5", "7", "√2"], "correct_index": 3},
    {"question": "حاصل جمع 1/2 + 1/3 کدام است؟", "options": ["2/5", "5/6", "1/6", "1"], "correct_index": 1},
    {"question": "عدد 0.313131... به صورت کسر کدام است؟", "options": ["31/100", "31/99", "31/10", "3/10"], "correct_index": 1},
    {"question": "مجموع زاویه‌های داخلی یک مثلث چند درجه است؟", "options": ["90", "180", "270", "360"], "correct_index": 1},
    {"question": "مجموع زاویه‌های داخلی یک پنج‌ضلعی منتظم کدام است؟", "options": ["540", "720", "900", "1080"], "correct_index": 0},
    {"question": "اگر یک زاویه خارجی یک چندضلعی منتظم 40 درجه باشد، این چندضلعی چند ضلع دارد؟", "options": ["7", "8", "9", "10"], "correct_index": 2},
    {"question": "حاصل x + 3x کدام است؟", "options": ["3x", "4x", "3x²", "x"], "correct_index": 1},
    {"question": "حل معادله 2x - 5 = 7 کدام است؟", "options": ["x=3", "x=4", "x=5", "x=6"], "correct_index": 3},
    {"question": "اگر 3(x - 2) = 2(x + 1) باشد، مقدار x برابر است با:", "options": ["8", "7", "6", "5"], "correct_index": 0},
    {"question": "نقطه (3, 2) در کدام ربع صفحه مختصات قرار دارد؟", "options": ["اول", "دوم", "سوم", "چهارم"], "correct_index": 0},
    {"question": "بردار بین نقاط A(1, 2) و B(4, 6) کدام است؟", "options": ["(3, 4)", "(5, 8)", "(3, 8)", "(5, 4)"], "correct_index": 0},
    {"question": "اگر نقطه M(2, 5) وسط پاره‌خط AB باشد و A=(1, 3) باشد، مختصات نقطه B کدام است؟", "options": ["(3, 7)", "(2, 4)", "(1, 7)", "(3, 2)"], "correct_index": 0},
    {"question": "مساحت یک مربع با ضلع 5 سانتی‌متر کدام است؟", "options": ["10", "20", "25", "50"], "correct_index": 2},
    {"question": "مساحت یک مستطیل با طول 8 و عرض 3 کدام است؟", "options": ["11", "24", "22", "48"], "correct_index": 1},
    {"question": "اگر مساحت یک مثلث 30 سانتی‌متر مربع و ارتفاع آن 6 سانتی‌متر باشد، طول قاعده آن چقدر است؟", "options": ["5", "10", "15", "20"], "correct_index": 1},
    {"question": "حاصل 3 به توان 2 کدام است؟", "options": ["6", "9", "5", "8"], "correct_index": 1},
    {"question": "حاصل جذر 16 کدام است؟", "options": ["2", "4", "8", "256"], "correct_index": 1},
    {"question": "حاصل (2³)² کدام است؟", "options": ["6", "16", "32", "64"], "correct_index": 3},
    {"question": "اگر یک تاس را پرتاب کنیم، احتمال آمدن عدد 4 کدام است؟", "options": ["1/6", "1/4", "1/2", "1"], "correct_index": 0},
    {"question": "در یک کیسه 5 مهره قرمز و 3 مهره آبی داریم. احتمال خارج کردن یک مهره قرمز چند است؟", "options": ["5/8", "3/8", "5/3", "1/2"], "correct_index": 0},
    {"question": "اگر نمودار میله‌ای نشان دهد که در یک کلاس 10 دانش‌آموز درس خوانده‌اند، 8 نفر علوم، 12 نفر ریاضی و 5 نفر علوم اجتماعی، میانگین تعداد دانش‌آموزان در هر درس چقدر است؟", "options": ["8.25", "8.5", "9", "10"], "correct_index": 0},
    {"question": "شعاع دایره‌ای با قطر 10 سانتی‌متر کدام است؟", "options": ["2", "5", "10", "20"], "correct_index": 1},
    {"question": "محیط دایره‌ای با شعاع 7 سانتی‌متر (با تقریب π ≈ 22/7) کدام است؟", "options": ["22", "38.5", "44", "154"], "correct_index": 2},
    {"question": "اگر مساحت یک دایره 144π سانتی‌متر مربع باشد، طول قطر آن چقدر است؟", "options": ["12", "24", "144", "72"], "correct_index": 1},
]


def get_question():
    return random.choice(questions)


def ask_question(screen):
    q = get_question()
    if not q or "question" not in q:
        print("Error: سوال دریافت نشد.")
        return False

    font = pygame.font.Font('Vazirmatn-Medium.ttf', 24)
    small_font = pygame.font.Font('Vazirmatn-Medium.ttf', 20)

    question_text = get_display(arabic_reshaper.reshape(q["question"]))

    option_rects = []
    selected = None
    answered = False
    is_correct = False

    clock = pygame.time.Clock()
    start_time = time.time()

    while time.time() - start_time < 10:
        screen.fill((0, 0, 0))

        # نمایش سوال
        q_surface = font.render(question_text, True, (255, 255, 255))
        screen.blit(q_surface, (50, 40))

        # نمایش گزینه‌ها
        option_rects.clear()
        for i, opt in enumerate(q["options"]):
            y = 130 + i * 60

            # رنگ دایره
            if answered:
                if i == int(q["correct_index"]):
                    circle_color = (0, 255, 0)   # سبز = جواب درست
                elif i == selected:
                    circle_color = (255, 0, 0)   # قرمز = انتخاب اشتباه
                else:
                    circle_color = (255, 255, 255)
            else:
                circle_color = (255, 255, 255)

            circle_pos = (70, y + 15)
            pygame.draw.circle(screen, circle_color, circle_pos, 12, 2)

            # پر کردن دایره
            if answered:
                if i == int(q["correct_index"]):
                    pygame.draw.circle(screen, (0, 255, 0), circle_pos, 7)
                elif i == selected:
                    pygame.draw.circle(screen, (255, 0, 0), circle_pos, 7)

            # رنگ متن
            if answered:
                if i == int(q["correct_index"]):
                    text_color = (0, 255, 0)
                elif i == selected:
                    text_color = (255, 0, 0)
                else:
                    text_color = (200, 200, 50)
            else:
                text_color = (200, 200, 50)

            opt_text = get_display(arabic_reshaper.reshape(f"{i+1}. {opt}"))
            opt_surface = small_font.render(opt_text, True, text_color)
            opt_rect = opt_surface.get_rect(topleft=(100, y))
            screen.blit(opt_surface, opt_rect)

            full_rect = pygame.Rect(50, y, 500, 40)
            option_rects.append(full_rect)

        pygame.display.update()

        # ⬇️ پردازش رویدادها
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not answered:
                mouse_pos = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        selected = i
                        is_correct = (str(i) == q["correct_index"])
                        answered = True
                        break

        # ⬇️ اگه جواب داده شده، اول یه فریم رنگی رسم کن، بعد صبر کن
        if answered:
            # ۱. رسم دوباره با دایره‌های رنگی
            screen.fill((0, 0, 0))
            q_surface = font.render(question_text, True, (255, 255, 255))
            screen.blit(q_surface, (50, 40))

            for i, opt in enumerate(q["options"]):
                y = 130 + i * 60
                if i == int(q["correct_index"]):
                    circle_color = (0, 255, 0)
                    text_color = (0, 255, 0)
                elif i == selected:
                    circle_color = (255, 0, 0)
                    text_color = (255, 0, 0)
                else:
                    circle_color = (255, 255, 255)
                    text_color = (200, 200, 50)

                circle_pos = (70, y + 15)
                pygame.draw.circle(screen, circle_color, circle_pos, 12, 2)
                pygame.draw.circle(screen, circle_color, circle_pos, 7)

                opt_text = get_display(arabic_reshaper.reshape(f"{i+1}. {opt}"))
                opt_surface = small_font.render(opt_text, True, text_color)
                opt_rect = opt_surface.get_rect(topleft=(100, y))
                screen.blit(opt_surface, opt_rect)

            pygame.display.update()

            # ۲. حالا ۱.۵ ثانیه صبر کن
            wait_start = time.time()
            while time.time() - wait_start < 1.5:
                pygame.event.pump()
                clock.tick(60)

            pygame.event.clear()
            return is_correct

        clock.tick(60)

    return False
# ====== حلقه‌ی اصلی بازی ======
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))

    correct = False

    # ⬇️ تشخیص برخورد مار با سیب
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        print("مار به سیب رسید! سوال پرسیده میشه...")
        correct = ask_question(game_window)
        if correct:
            score += 10
            fruit_spawn = False
        else:
            fruit_spawn = True

    if not correct:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

    game_window.fill(green)

    for pos in snake_body:
        pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(white, 'times new roman', 20)
    pygame.display.update()

    fps.tick(snake_speed)
