import pygame
import time
import random
import arabic_reshaper
from bidi.algorithm import get_display
import json
import os

# ==================== تنظیمات اولیه ====================
pygame.init()
pygame.mixer.init()

WINDOW_X = 1200
WINDOW_Y = 650
SNAKE_SPEED = 12

# ==================== رنگ‌ها ====================
BLACK = (10, 20, 10)           
WHITE = (240, 255, 240)        
RED = (200, 60, 40)            
GREEN = (100, 180, 70)         
DARK_GREEN = (20, 180, 30)     
BLUE = (60, 180, 255)          
GOLD = (200, 170, 100)         
PURPLE = (180, 80, 255)        
GRAY = (100, 130, 100)         
DARK_GRAY = (20, 40, 20)       
LIGHT_GRAY = (200, 230, 200)   

# ==================== کلاس Settings ====================
class Settings:
    def __init__(self):
        self.sound_enabled = True
        self.music_enabled = True
        self.snake_speed = SNAKE_SPEED
        self.difficulty = "normal"
        self.high_score = self.load_high_score()
        self.timer_enabled = True
        self.timer_duration = 15

    def load_high_score(self):
        try:
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0

    def save_high_score(self, score):
        try:
            with open("high_score.json", "w") as f:
                json.dump({"high_score": score}, f)
        except:
            pass

# ==================== کلاس SoundManager ====================
class SoundManager:
    def __init__(self, settings):
        self.settings = settings
        self.eat_sound = None
        self.game_over_sound = None
        self.click_sound = None
        self.level_up_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        pass
    
    def play_eat(self):
        if self.settings.sound_enabled:
            pass
    
    def play_game_over(self):
        if self.settings.sound_enabled:
            pass
    
    def play_click(self):
        if self.settings.sound_enabled:
            pass
    
    def play_level_up(self):
        if self.settings.sound_enabled:
            pass

# ==================== کلاس SnakeGame ====================
class SnakeGame:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        pygame.display.set_caption('🐍 Snake Math Quiz Game')
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.sound_manager = SoundManager(self.settings)
        self.running = True
        self.state = "menu"
        
        # ========== فونت‌ها ==========
        self.font_large = pygame.font.SysFont('Tahoma', 32, bold=True)
        self.font_medium = pygame.font.SysFont('Tahoma', 22, bold=True)
        self.font_small = pygame.font.SysFont('Tahoma', 14)
        self.font_tiny = pygame.font.SysFont('Tahoma', 11)
        # ========== بارگذاری صداها ==========
        print("🎵 در حال بارگذاری صداها...")

        try:
            pygame.mixer.music.load('background.mp3')
            pygame.mixer.music.set_volume(0.3)
            print("✅ background.mp3")
        except Exception as e:
            print(f"❌ background.mp3: {e}")

        try:
            self.eat_sound = pygame.mixer.Sound('eat.wav')
            print("✅ eat.wav")
        except Exception as e:
            self.eat_sound = None
            print(f"❌ eat.wav: {e}")

        # ✅ صدای جدید برای پاسخ صحیح
        try:
            self.correct_sound = pygame.mixer.Sound('correct.mp3')
            print("✅ correct.mp3")
        except Exception as e:
            self.correct_sound = None
            print(f"❌ correct.mp3: {e}")

        # ✅ صدای جدید برای پاسخ اشتباه
        try:
            self.wrong_sound = pygame.mixer.Sound('wrong.mp3')
            print("✅ wrong.mp3")
        except Exception as e:
            self.wrong_sound = None
            print(f"❌ wrong.mp3: {e}")

        try:
            self.game_over_sound = pygame.mixer.Sound('game_over.mp3')
            print("✅ game_over.mp3")
        except Exception as e:
            self.game_over_sound = None
            print(f"❌ game_over.mp3: {e}")

        try:
            self.level_up_sound = pygame.mixer.Sound('level_up.mp3')
            print("✅ level_up.mp3")
        except Exception as e:
            self.level_up_sound = None
            print(f"❌ level_up.mp3: {e}")

        try:
            self.click_sound = pygame.mixer.Sound('click.wav')
            print("✅ click.wav")
        except Exception as e:
            self.click_sound = None
            print(f"❌ click.wav: {e}")

        self.music_started = False
        
        self.reset_game()
        self.load_questions()
        
    def reset_game(self):
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.level = 1
        self.combo = 0
        self.max_combo = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.fruit_position = self.generate_fruit()
        self.questions_asked = 0
        self.questions_correct = 0
        self.particles = []
        self.floating_texts = []
        self.lives = 3
        self.max_lives = 5


    
    def load_questions(self):
        # ========== سوالات آسان (سطح ۱-۳) ==========
        self.easy_questions = [
            {"question": "حاصل ۲³ × ۲⁴ کدام است؟", "options": ["۲⁷", "۲¹²", "۴⁷", "۸⁷"], "correct_index": 0},
            {"question": "حاصل ۰/۳ + ۰/۷ کدام است؟", "options": ["۱", "۰/۱۰", "۰/۰۴", "۱/۰"], "correct_index": 0},
            {"question": "مساحت مربعی با ضلع ۶ سانتی‌متر کدام است؟", "options": ["۱۲", "۲۴", "۳۶", "۴۸"], "correct_index": 2},
            {"question": "میانگین اعداد ۴, ۶, ۸, ۱۰ کدام است؟", "options": ["۶", "۷", "۸", "۹"], "correct_index": 1},
            {"question": "نقطه (۳, ۲) در کدام ربع قرار دارد؟", "options": ["اول", "دوم", "سوم", "چهارم"], "correct_index": 0},
            {"question": "حل معادله ۲x - ۵ = ۷ کدام است؟", "options": ["x=۳", "x=۴", "x=۵", "x=۶"], "correct_index": 3},
            {"question": "حاصل (۳²)³ کدام است؟", "options": ["۳⁵", "۳⁶", "۹⁶", "۲۷⁶"], "correct_index": 1},
            {"question": "√۲۵ × √۴ کدام است؟", "options": ["۱۰", "۲۰", "۵۰", "۱۰۰"], "correct_index": 0},
            {"question": "محیط مستطیلی به طول ۸ و عرض ۵ کدام است؟", "options": ["۱۳", "۲۶", "۴۰", "۸۰"], "correct_index": 1},
            {"question": "اگر a=۲- باشد، مقدار ۳a+۵ کدام است؟", "options": ["۱-", "۱", "۱۱-", "۱۱"], "correct_index": 0},
            {"question": "حاصل ۵ - (۳ - ۷) کدام است؟", "options": ["۹", "۱", "۵-", "۹-"], "correct_index": 0},
            {"question": "بزرگترین عدد اول بین ۲۰ تا ۳۰ کدام است؟", "options": ["۲۳", "۲۷", "۲۹", "۳۱"], "correct_index": 2},
            {"question": "کدام عدد گویا نیست؟", "options": ["۰/۵", "√۴", "√۲", "۲/۳"], "correct_index": 2},
            {"question": "حاصل (۲-)(۳-) کدام است؟", "options": ["۶", "۶-", "۱-", "۵"], "correct_index": 0},
            {"question": "حاصل ۱۰³ ÷ ۱۰² کدام است؟", "options": ["۱۰", "۱۰⁵", "۱۰⁶", "۱۰۰"], "correct_index": 0},
        ]
        
        # ========== سوالات متوسط (سطح ۴-۶) ==========
        self.normal_questions = [
            {"question": "اگر a=۳ و b=۲- باشد، a²-b کدام است؟", "options": ["۷", "۱۱", "۱", "۹"], "correct_index": 1},
            {"question": "حاصل (x+۲)(x-۲) کدام است؟", "options": ["x²-۴", "x²+۴", "x²-۲", "x²+۲"], "correct_index": 0},
            {"question": "کدام عدد بین ۵ و ۶ قرار دارد؟", "options": ["√۲۰", "√۳۰", "√۴۰", "√۵۰"], "correct_index": 1},
            {"question": "اگر x=۳ باشد، ۲x² + ۱ کدام است؟", "options": ["۷", "۱۳", "۱۹", "۳۷"], "correct_index": 2},
            {"question": "مجموع زاویه‌های داخلی پنج‌ضلعی کدام است؟", "options": ["۳۶۰°", "۴۲۰°", "۵۴۰°", "۷۲۰°"], "correct_index": 2},
            {"question": "مساحت دایره‌ای با شعاع ۵ (π≈۳/۱۴) کدام است؟", "options": ["۱۵/۷", "۳۱/۴", "۷۸/۵", "۱۵۷"], "correct_index": 2},
            {"question": "در پرتاب دو سکه، احتمال آمدن دو شیر کدام است؟", "options": ["۱/۲", "۱/۳", "۱/۴", "۳/۴"], "correct_index": 2},
            {"question": "فاصله دو نقطه (۱, ۲) و (۴, ۶) در صفحه مختصات کدام است؟", "options": ["۳", "۴", "۵", "۶"], "correct_index": 2},
            {"question": "قرینه نقطه (۲, ۳-) نسبت به محور xها کدام است؟", "options": ["(۲, ۳-)", "(۳-, ۲-)", "(۲, ۳)", "(۳-, ۲)"], "correct_index": 2},
            {"question": "بردار AB با A(۱, ۲) و B(۴, ۶) کدام است؟", "options": ["(۳, ۴)", "(۵, ۸)", "(۳, ۸)", "(۵, ۴)"], "correct_index": 0},
            {"question": "محیط دایره‌ای با شعاع ۷ (π≈۲۲/۷) کدام است؟", "options": ["۲۲", "۴۴", "۱۵۴", "۳۰۸"], "correct_index": 1},
            {"question": "میانه اعداد ۳, ۵, ۷, ۹, ۱۱ کدام است؟", "options": ["۵", "۶", "۷", "۸"], "correct_index": 2},
            {"question": "حجم مکعبی با ضلع ۴ سانتی‌متر کدام است؟", "options": ["۱۶", "۳۲", "۶۴", "۱۲۸"], "correct_index": 2},
            {"question": "در مثلث متساوی‌الساقین با زاویه راس ۴۰°، زاویه‌های پا چند درجه است؟", "options": ["۴۰°", "۷۰°", "۱۴۰°", "۲۰°"], "correct_index": 1},
            {"question": "جمله عمومی دنباله ۳, ۶, ۹, ۱۲, ... کدام است؟", "options": ["۲n", "۳n", "n+۳", "n×۳"], "correct_index": 1},
            ]
        
        # ========== سوالات سخت (سطح ۷-۱۰) ==========
        self.hard_questions = [
            {"question": "حاصل (√۳ + √۲)(√۳ - √۲) کدام است؟", "options": ["۱", "۲", "۳", "۵"], "correct_index": 0},
            {"question": "اگر x² = ۴۹ باشد، کدام گزینه درست است؟", "options": ["x=۷ فقط", "x=۷- فقط", "x=۷±", "x=۴۹"], "correct_index": 2},
            {"question": "اگر ۵x - ۳ = ۲x + ۱۲ باشد، x کدام است？", "options": ["۳", "۴", "۵", "۶"], "correct_index": 2},
            {"question": "حاصل (x - ۳)² کدام است؟", "options": ["x²-۹", "x²-۶x+۹", "x²+۶x+۹", "x²-۳x+۹"], "correct_index": 1},
            {"question": "مساحت ذوزنقه‌ای با قاعده‌های ۴ و ۶ و ارتفاع ۳ کدام است؟", "options": ["۱۰", "۱۵", "۲۰", "۳۰"], "correct_index": 1},
            {"question": "قطر مربعی با ضلع ۵√۲ کدام است؟", "options": ["۵", "۱۰", "۱۵", "۲۰"], "correct_index": 1},
            {"question": "در پرتاب دو تاس، احتمال مجموع ۷ چقدر است؟", "options": ["۱/۶", "۱/۸", "۱/۱۲", "۱/۴"], "correct_index": 0},
            {"question": "میانگین ۵ عدد متوالی برابر ۱۲ است. بزرگترین عدد کدام است؟", "options": ["۱۰", "۱۲", "۱۴", "۱۶"], "correct_index": 2},
            {"question": "اگر شعاع دایره‌ای ۵۰٪ افزایش یابد، مساحت آن چند درصد افزایش می‌یابد؟", "options": ["۵۰%", "۱۰۰%", "۱۲۵%", "۱۵۰%"], "correct_index": 2},
            {"question": "در مثلث قائم‌الزاویه‌ای با وتر ۱۰ و یک ضلع ۶، ضلع دیگر چند است؟", "options": ["۴", "۶", "۸", "۱۰"], "correct_index": 2},
            {"question": "اگر ۲⁵ = ۳۲ و ۲⁷ = ۱۲۸ باشد، ۲⁶ کدام است؟", "options": ["۶۴", "۹۶", "۱۲۸", "۳۲"], "correct_index": 0},
            {"question": "مساحت یک لوزی با قطرهای ۸ و ۶ کدام است؟", "options": ["۱۴", "۲۴", "۴۸", "۹۶"], "correct_index": 1},
            {"question": "مجموع زاویه‌های داخلی یک هشت‌ضلعی کدام است؟", "options": ["۷۲۰°", "۹۰۰°", "۱۰۸۰°", "۱۲۶۰°"], "correct_index": 2},
            {"question": "حاصل ۲-³ × ۲⁵ کدام است？", "options": ["۲²", "۲-²", "۲⁸", "۴"], "correct_index": 0},
            {"question": "در یک چندضلعی منتظم، اگر هر زاویه خارجی ۴۵° باشد، این چندضلعی چند ضلع دارد؟", "options": ["۶", "۷", "۸", "۹"], "correct_index": 2},
        ]
        
        # ========== سوالات خیلی سخت (سطح ۱۱+) ==========
        self.expert_questions = [
            {"question": "اگر x و y دو عدد صحیح باشند و x + y = ۵ و xy = ۶، مقدار x² + y² کدام است؟", "options": ["۱۱", "۱۳", "۱۹", "۲۵"], "correct_index": 1},
            {"question": "حاصل (۲x - ۳)² - (۲x + ۳)² کدام است؟", "options": ["۲۴x-", "۲۴x", "۱۲x", "۱۲x-"], "correct_index": 0},
            {"question": "معادله ۳x - ۲ = ۴x + ۵ را حل کنید", "options": ["x=۳", "x=۷-", "x=۷", "x=۳-"], "correct_index": 1},
            {"question": "اگر a=۲ و b=۳- باشد، a²b - ab² کدام است؟", "options": ["۶", "۶-", "۱۸", "۱۸-"], "correct_index": 0},
            {"question": "اگر مساحت مثلثی ۲۴ سانتی‌متر مربع و ارتفاع آن ۶ سانتی‌متر باشد، قاعده آن چقدر است؟", "options": ["۴", "۶", "۸", "۱۲"], "correct_index": 2},
            {"question": "در یک دایره، زاویه مرکزی ۶۰° است. زاویه محاطی نظیر آن چند درجه است؟", "options": ["۳۰°", "۶۰°", "۱۲۰°", "۱۸۰°"], "correct_index": 0},
            {"question": "اگر شعاع دایره‌ای ۴ برابر شود، محیط آن چند برابر می‌شود؟", "options": ["۲", "۴", "۸", "۱۶"], "correct_index": 1},
            {"question": "احتمال خارج کردن یک مهره قرمز از کیسه‌ای با ۴ قرمز و ۶ آبی کدام است؟", "options": ["۲/۵", "۳/۵", "۴/۱۰", "۶/۱۰"], "correct_index": 0},
            {"question": "میانگین وزن ۵ دانش‌آموز ۴۲ کیلوگرم است. اگر یک نفر با وزن ۳۲ کیلوگرم خارج شود، میانگین جدید چند است؟", "options": ["۴۰", "۴۲", "۴۴", "۴۶"], "correct_index": 2},
            {"question": "در یک آزمون ۲۰ سوالی، هر پاسخ صحیح ۳ امتیاز و هر پاسخ غلط ۱- امتیاز دارد. اگر کسی ۱۵ سوال صحیح و ۵ سوال غلط بزند، امتیاز او چقدر است؟", "options": ["۳۰", "۳۵", "۴۰", "۴۵"], "correct_index": 2},
            {"question": "حاصل ۱۲/۵ - ۷/۳ کدام است؟", "options": ["۱/۱۵", "۱/۵", "۲/۱۵", "۳/۱۵"], "correct_index": 0},
            {"question": "اگر x=۵ باشد، مقدار (x² - ۲۵)/(x - ۵) کدام است؟", "options": ["۰", "۵", "۱۰", "۲۵"], "correct_index": 2},
            {"question": "در دنباله ۲, ۶, ۱۲, ۲۰, ... جمله بعدی کدام است؟", "options": ["۲۸", "۳۰", "۳۲", "۳۴"], "correct_index": 1},
            {"question": "بردار (۳, ۴-) و (۱, ۲) حاصل جمعشان کدام است؟", "options": ["(۴, ۲-)", "(۲, ۶-)", "(۴, ۶-)", "(۲, ۲-)"], "correct_index": 0},
            {"question": "نقطه (۲-, ۳-) قرینه نقطه (۲, ۳-) نسبت به کدام محور است؟", "options": ["محور x", "محور y", "مبدا", "خط y=x"], "correct_index": 2},
        ]
        
        self.questions = self.easy_questions + self.normal_questions + self.hard_questions + self.expert_questions

    def get_question_for_level(self):
        """بر اساس سطح، سوال مناسب رو انتخاب کن"""
        if self.level <= 3:
            return random.choice(self.easy_questions)
        elif self.level <= 6:
            return random.choice(self.easy_questions + self.normal_questions)
        elif self.level <= 10:
            return random.choice(self.normal_questions + self.hard_questions)
        elif self.level <= 15:
            return random.choice(self.hard_questions + self.expert_questions)
        else:
            return random.choice(self.expert_questions)
    def generate_fruit(self):
        margin = 20
        x = random.randrange(margin, (WINDOW_X - margin) // 10) * 10
        y = random.randrange(margin, (WINDOW_Y - margin) // 10) * 10
        return [x, y]
    def render_persian_text(self, surface, text, font, color, position, center=False):
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            text_surface = font.render(bidi_text, True, color)
            if center:
                rect = text_surface.get_rect(center=position)
                surface.blit(text_surface, rect)
            else:
                surface.blit(text_surface, position)
        except:
            if center:
                rect = font.render(text, True, color).get_rect(center=position)
                surface.blit(font.render(text, True, color), rect)
            else:
                surface.blit(font.render(text, True, color), position)
    
    def add_particles(self, x, y, color, count=20):
        for _ in range(count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(1, 5)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': speed * 0.5 * (0.5 - random.random()) * 2,
                'dy': speed * 0.5 * (0.5 - random.random()) * 2 - 2,
                'life': random.randint(20, 40),
                'color': color,
                'size': random.randint(3, 6)
            })
    
    def add_floating_text(self, x, y, text, color):
        self.floating_texts.append({
            'x': x,
            'y': y,
            'text': text,
            'color': color,
            'life': 60,
            'dy': -2
        })
    def update_particles(self):
        for p in self.particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['dy'] += 0.2
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
        
        for ft in self.floating_texts[:]:
            ft['y'] += ft['dy']
            ft['life'] -= 1
            if ft['life'] <= 0:
                self.floating_texts.remove(ft)
    
    def draw_particles(self):
        for p in self.particles:
            alpha = p['life'] / 40
            color = list(p['color'])
            color = [int(c * alpha) for c in color]
            pygame.draw.circle(self.window, color, (int(p['x']), int(p['y'])), p['size'])
        
        for ft in self.floating_texts:
            alpha = ft['life'] / 60
            color = list(ft['color'])
            color = [int(c * alpha) for c in color]
            self.render_persian_text(self.window, ft['text'], self.font_medium, color, (ft['x'], ft['y']), True)

            
    def play_sound(self, sound):
        """پخش صدا فقط اگر صدا روشن باشه"""
        if self.settings.sound_enabled:
            try:
                sound.play()
            except:
                pass
    
    # ==================== منوها ====================
    def draw_menu(self):
        self.window.fill(DARK_GRAY)
        
        for i in range(WINDOW_Y):
            progress = i / WINDOW_Y
            r = int(30 + 30 * progress)
            g = int(30 + 20 * progress)
            b = int(50 + 30 * progress)
            pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
        
        title_y = 120
        self.render_persian_text(self.window, "«کابينه رياضي و مار»", self.font_large, GOLD, (WINDOW_X//2, title_y), True)
        self.render_persian_text(self.window, "snake Math Quiz" ,self.font_small,LIGHT_GRAY, (WINDOW_X//2,title_y + 70), True)
        
        buttons = [
        ("شروع بازی", "start", (WINDOW_X//2, 250)),
        ("تنظیمات", "settings", (WINDOW_X//2, 310)),
        ("امتیازات", "scores", (WINDOW_X//2, 370)),
        ("راهنما", "help", (WINDOW_X//2, 430)),
        ("خروج", "exit", (WINDOW_X//2, 490))
        ]
        mouse_pos = pygame.mouse.get_pos()
        self.menu_buttons = []
        
        for text, action, pos in buttons:
            button_rect = pygame.Rect(pos[0] - 150, pos[1] - 30, 300, 60)
            is_hover = button_rect.collidepoint(mouse_pos)
            
            color = BLUE if not is_hover else GOLD
            pygame.draw.rect(self.window, color, button_rect, border_radius=15)
            pygame.draw.rect(self.window, WHITE, button_rect, 2, border_radius=15)
            
            self.render_persian_text(self.window, text, self.font_medium, WHITE, (pos[0], pos[1]), True)
            self.menu_buttons.append((button_rect, action))
        
        self.render_persian_text(self.window, f" بهترین امتیاز: {self.settings.high_score}", 
                                self.font_small, GOLD, (WINDOW_X//2, 570), True)
        
        self.render_persian_text(self.window, "ساخته شده با عشق", self.font_tiny, GRAY, (WINDOW_X//2, WINDOW_Y - 30), True)

    def draw_settings(self):
        self.window.fill(DARK_GRAY)
        
        for i in range(WINDOW_Y):
            progress = i / WINDOW_Y
            r = int(30 + 30 * progress)
            g = int(30 + 20 * progress)
            b = int(50 + 30 * progress)
            pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
        
        self.render_persian_text(self.window, "تنظیمات", self.font_large, GOLD, (WINDOW_X//2, 80), True)
        
        mouse_pos = pygame.mouse.get_pos()
        self.settings_buttons = []
        
        # تنظیمات صدا
        sound_text = "صدا: " + ("روشن" if self.settings.sound_enabled else "خاموش")
        sound_rect = pygame.Rect(WINDOW_X//2 - 150, 160, 300, 50)
        is_hover = sound_rect.collidepoint(mouse_pos)
        color = BLUE if not is_hover else GOLD
        pygame.draw.rect(self.window, color, sound_rect, border_radius=10)
        self.render_persian_text(self.window, sound_text, self.font_medium, WHITE, (WINDOW_X//2, 185), True)
        self.settings_buttons.append((sound_rect, "toggle_sound"))
        
        # تنظیمات موسیقی
        music_text = "موسیقی: " + ("روشن" if self.settings.music_enabled else "خاموش")
        music_rect = pygame.Rect(WINDOW_X//2 - 150, 230, 300, 50)
        is_hover = music_rect.collidepoint(mouse_pos)
        color = BLUE if not is_hover else GOLD
        pygame.draw.rect(self.window, color, music_rect, border_radius=10)
        self.render_persian_text(self.window, music_text, self.font_medium, WHITE, (WINDOW_X//2, 255), True)
        self.settings_buttons.append((music_rect, "toggle_music"))
        
        # تنظیمات سرعت
        speed_text = f"سرعت: {self.settings.snake_speed}"
        speed_rect = pygame.Rect(WINDOW_X//2 - 150, 300, 300, 50)
        is_hover = speed_rect.collidepoint(mouse_pos)
        color = BLUE if not is_hover else GOLD
        pygame.draw.rect(self.window, color, speed_rect, border_radius=10)
        self.render_persian_text(self.window, speed_text, self.font_medium, WHITE, (WINDOW_X//2, 325), True)
        self.settings_buttons.append((speed_rect, "toggle_speed"))
        
        # تنظیمات سختی
        difficulty_text = f" سختی: {self.settings.difficulty}"
        diff_rect = pygame.Rect(WINDOW_X//2 - 150, 370, 300, 50)
        is_hover = diff_rect.collidepoint(mouse_pos)
        color = BLUE if not is_hover else GOLD
        pygame.draw.rect(self.window, color, diff_rect, border_radius=10)
        self.render_persian_text(self.window, difficulty_text, self.font_medium, WHITE, (WINDOW_X//2, 395), True)
        self.settings_buttons.append((diff_rect, "toggle_difficulty"))
        
        #  تنظیمات تایمر (جدید)
        timer_text = "️ تایمر: " + ("فعال" if self.settings.timer_enabled else "غیرفعال")
        timer_rect = pygame.Rect(WINDOW_X//2 - 150, 440, 300, 50)
        is_hover = timer_rect.collidepoint(mouse_pos)
        color = PURPLE if not is_hover else GOLD
        pygame.draw.rect(self.window, color, timer_rect, border_radius=10)
        self.render_persian_text(self.window, timer_text, self.font_medium, WHITE, (WINDOW_X//2, 465), True)
        self.settings_buttons.append((timer_rect, "toggle_timer"))
        
        # دکمه بازگشت
        back_rect = pygame.Rect(WINDOW_X//2 - 150, 510, 300, 50)
        is_hover = back_rect.collidepoint(mouse_pos)
        color = RED if not is_hover else GOLD
        pygame.draw.rect(self.window, color, back_rect, border_radius=10)
        self.render_persian_text(self.window, " بازگشت", self.font_medium, WHITE, (WINDOW_X//2, 535), True)
        self.settings_buttons.append((back_rect, "back"))
    #======================================    
    def draw_scores(self):
        self.window.fill(DARK_GRAY)
        for i in range(WINDOW_Y):
            progress = i / WINDOW_Y
            r = int(30 + 30 * progress)
            g = int(30 + 20 * progress)
            b = int(50 + 30 * progress)
            pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
        
        self.render_persian_text(self.window, "امتیازات", self.font_large, GOLD, (WINDOW_X//2, 80), True)
        
        stats = [
            f"بهترین امتیاز: {self.settings.high_score}",
            f"تعداد بازی‌ها: {self.get_games_played()}",
            f"میانگین امتیاز: {self.get_average_score()}"
        ]
        y = 180
        for stat in stats:
            self.render_persian_text(self.window, stat, self.font_medium, LIGHT_GRAY, (WINDOW_X//2, y), True)
            y += 60
        
        # ========== تاریخچه ==========
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
            if history:
                y += 30
                self.render_persian_text(self.window, "آخرین بازی‌ها:", self.font_medium, GOLD, (WINDOW_X//2, y), True)
                for game in history[-2:]:
                    y += 40
                    text = f"{game['date']} | {game['score']} | سطح{game['level']}"
                    self.render_persian_text(self.window, text, self.font_small, LIGHT_GRAY, (WINDOW_X//2, y), True)
        except:
            pass
        
        # ========== دکمه بازگشت ==========
        mouse_pos = pygame.mouse.get_pos()
        back_rect = pygame.Rect(WINDOW_X//2 - 100, WINDOW_Y - 70, 200, 45)
        is_hover = back_rect.collidepoint(mouse_pos)
        color = RED if not is_hover else GOLD
        pygame.draw.rect(self.window, color, back_rect, border_radius=10)
        self.render_persian_text(self.window, "بازگشت", self.font_medium, WHITE, (WINDOW_X//2, WINDOW_Y - 47), True)
        self.scores_buttons = [(back_rect, "back")]
    #=======================================
    def draw_help(self):
        self.window.fill(DARK_GRAY)
        
        for i in range(WINDOW_Y):
            progress = i / WINDOW_Y
            r = int(30 + 30 * progress)
            g = int(30 + 20 * progress)
            b = int(50 + 30 * progress)
            pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
        
        self.render_persian_text(self.window, "راهنما", self.font_large, GOLD, (WINDOW_X//2, 50), True)
        
        help_texts = [
            "هدف: با خوردن میوه، به سوالات ریاضی پاسخ دهید",
            "",
            "کنترل: کلیدهای جهت‌دار برای حرکت مار",
            "",
            "امتیاز: پاسخ صحیح = ۱۰ امتیاز (+ پاداش زمان و کامبو)",
            "پشت سر هم: پاسخ‌های پیاپی امتیاز بیشتری می‌دهند",
            "جان‌ها: ۳ جان اولیه، هر اشتباه ۱ جان کم می‌شود",
            "",
            "کلیدها:",
            "  P = مکث",
            "  ESC = بازگشت به منو",
            "  M = قطع/وصل صدا",
            "",
            "سطح‌بندی: هر ۵۰ امتیاز، سطح بالا می‌رود"
        ]
        
        y = 110
        for text in help_texts:
            self.render_persian_text(self.window, text, self.font_small, LIGHT_GRAY, (WINDOW_X//2, y), True)
            y += 28
        
        # ========== دکمه بازگشت ==========
        mouse_pos = pygame.mouse.get_pos()
        back_rect = pygame.Rect(WINDOW_X//2 - 100, WINDOW_Y - 70, 200, 45)
        is_hover = back_rect.collidepoint(mouse_pos)
        color = RED if not is_hover else GOLD
        pygame.draw.rect(self.window, color, back_rect, border_radius=10)
        self.render_persian_text(self.window, "بازگشت", self.font_medium, WHITE, (WINDOW_X//2, WINDOW_Y - 47), True)
        self.help_buttons = [(back_rect, "back")]        
    #=============================================
    def save_game_history(self):
        history = {
        "score": self.score,
        "level": self.level,
        "correct": self.questions_correct,
        "wrong": self.wrong_answers,
        "combo": self.max_combo,
        "date": time.strftime("%Y-%m-%d %H:%M")
        }
        try:
            with open("history.json", "r") as f:
                data = json.load(f)
        except:
            data = []
        data.append(history)
        if len(data) > 20:
            data = data[-20:]
        with open("history.json", "w") as f:
            json.dump(data, f, indent=2)

    #===============================================

    def get_games_played(self):
        try:
            with open("history.json", "r") as f:
                data = json.load(f)
                return len(data)
        except:
            return 0

    def get_average_score(self):
        try:
            with open("history.json", "r") as f:
                data = json.load(f)
                if not data:
                    return 0
                total = sum(game.get("score", 0) for game in data)
                return total // len(data)
        except:
            return 0
    #================== سوال =======================
    def ask_question(self):
        q = self.get_question_for_level()
        selected = None
        answered = False
        is_correct = False
        show_result_timer = 0
        
        if self.level <= 3:
            TIME_LIMIT = 20
        elif self.level <= 6:
            TIME_LIMIT = 15
        elif self.level <= 10:
            TIME_LIMIT = 12
        elif self.level <= 15:
            TIME_LIMIT = 10
        else:
            TIME_LIMIT = 8
        
        if not self.settings.timer_enabled:
            TIME_LIMIT = 999
        
        start_time = pygame.time.get_ticks()
        time_left = TIME_LIMIT
        
        while True:
            if self.settings.timer_enabled:
                elapsed = (pygame.time.get_ticks() - start_time) / 1000
                time_left = max(0, TIME_LIMIT - elapsed)
                if time_left <= 0 and not answered:
                    answered = True
                    is_correct = False
                    show_result_timer = pygame.time.get_ticks()
                    self.add_floating_text(WINDOW_X//2, WINDOW_Y//2 - 50, " زمان تمام شد!", RED)
                    self.add_particles(WINDOW_X//2, WINDOW_Y//2, RED, 30)
                    self.window.fill(DARK_GRAY)
            card_width = 700
            card_height = 400
            card_x = (WINDOW_X - card_width) // 2
            card_y = (WINDOW_Y - card_height) // 2 - 30
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            pygame.draw.rect(self.window, (20, 20, 30), (card_x + 10, card_y + 10, card_width, card_height), border_radius=20)
            pygame.draw.rect(self.window, (60, 60, 80), card_rect, border_radius=20)
            pygame.draw.rect(self.window, GOLD, (card_x, card_y, card_width, 5), border_radius=5)
            
            level_text = f" سطح {self.level}"
            if self.level <= 3:
                level_text += "  آسان"
            elif self.level <= 6:
                level_text += "  متوسط"
            elif self.level <= 10:
                level_text += "  سخت"
            else:
                level_text += "  خیلی سخت"
            
            self.render_persian_text(self.window, level_text, self.font_small, GOLD, (card_x + 20, card_y + 15))
            q_y = card_y + 60
            self.render_persian_text(self.window, q["question"], self.font_medium, WHITE, (WINDOW_X//2, q_y), True)
            option_rects = []
            opt_width = 500
            opt_height = 45
            for i, opt in enumerate(q["options"]):
                y_pos = card_y + 120 + i * 55
                opt_rect = pygame.Rect(card_x + (card_width - opt_width)//2, y_pos, opt_width, opt_height)
                option_rects.append(opt_rect)
                current_color = (70, 70, 90)
                border_color = (100, 100, 120)
                text_color = WHITE
                if answered:
                    if i == q["correct_index"]:
                        current_color = (35, 90, 35)
                        border_color = GREEN
                    elif selected == i and i != q["correct_index"]:
                        current_color = (90, 35, 35)
                        border_color = RED
                elif opt_rect.collidepoint(pygame.mouse.get_pos()):
                    current_color = (90, 90, 120)
                pygame.draw.rect(self.window, current_color, opt_rect, border_radius=10)
                pygame.draw.rect(self.window, border_color, opt_rect, 2, border_radius=10)
                self.render_persian_text(self.window, f"{chr(65 + i)}. {opt}", self.font_small, text_color, (opt_rect.centerx, opt_rect.centery), True)
            
            # HUD
            self.render_persian_text(self.window, f" امتياز:{self.score} |  پشت سر هم:{self.combo}", self.font_small, GOLD, (150, 30))
            lives_text = "+" * self.lives + "-" * (self.max_lives - self.lives)
            self.render_persian_text(self.window, lives_text, self.font_medium, RED, (WINDOW_X//2, 65))
            if self.settings.timer_enabled:
                timer_color = GREEN if time_left > 5 else RED if time_left > 2 else (255, 100, 0)
                timer_text = f"️{int(time_left)}s"
                self.render_persian_text(self.window, timer_text, self.font_medium, timer_color, (WINDOW_X - 100, 30))
                bar_width = 150
                bar_height = 8
                bar_x = WINDOW_X - bar_width - 40
                bar_y = 65
                progress = time_left / TIME_LIMIT
                pygame.draw.rect(self.window, (50, 50, 70), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
                pygame.draw.rect(self.window, timer_color, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=4)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not answered:
                    mouse_pos = event.pos
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            selected = i
                            answered = True
                            is_correct = (i == q["correct_index"])
                            show_result_timer = pygame.time.get_ticks()
                            if is_correct:
                                self.add_particles(rect.centerx, rect.centery, GREEN)
                                self.add_floating_text(rect.centerx, rect.centery - 30, " صحیح!", GREEN)
                                # ========== صدای پاسخ صحیح ==========
                                self.play_sound(self.correct_sound)
                            else:
                                self.add_particles(rect.centerx, rect.centery, RED)
                                self.add_floating_text(rect.centerx, rect.centery - 30, " اشتباه!", RED)
                                # ========== صدای پاسخ اشتباه ==========
                                self.play_sound(self.wrong_sound)
                            break
            
            self.update_particles()
            self.draw_particles()
            
            if answered and pygame.time.get_ticks() - show_result_timer > 1500:
                self.questions_asked += 1
                if is_correct:
                    self.questions_correct += 1
                    self.combo += 1
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo
                    base_score = 10
                    if self.level > 10:
                        base_score = 25
                    elif self.level > 6:
                        base_score = 20
                    elif self.level > 3:
                        base_score = 15
                    time_bonus = 0
                    if self.settings.timer_enabled and time_left > 0:
                        time_bonus = int(time_left // 2)
                    combo_bonus = min(self.combo // 3, 5)
                    earned = base_score + combo_bonus + time_bonus
                    self.score += earned
                    bonus_text = f"{earned}امتياز! (پشت سر هم:{self.combo})"
                    if time_bonus > 0:
                        bonus_text += f" ({time_bonus})"
                    self.add_floating_text(WINDOW_X//2, WINDOW_Y//2 - 50, bonus_text, GOLD)
                    
                    # پاداش جان
                    if self.questions_correct % 5 == 0 and self.lives < self.max_lives:
                        self.lives += 1
                        self.add_floating_text(WINDOW_X//2, WINDOW_Y//2 - 100, " جان!", GOLD)
                    
                    if self.score >= self.level * 50:
                        self.level_up()
                else:
                    self.combo = 0
                    self.wrong_answers += 1
                    self.lives -= 1
                    if self.lives <= 0:
                        self.add_floating_text(WINDOW_X//2, WINDOW_Y//2, " جان‌ها تمام شد!", RED)
                        time.sleep(1)
                        self.game_over()
                        return False
                return is_correct
    def level_up(self):
        self.level += 1
        self.settings.snake_speed = min(self.settings.snake_speed + 1, 20)
        self.add_floating_text(WINDOW_X//2, WINDOW_Y//2, f" سطح {self.level}! ", GOLD)
        self.add_particles(WINDOW_X//2, WINDOW_Y//2, GOLD, 50)
        
        # ========== صدای سطح‌آپ ==========
        self.play_sound(self.level_up_sound)
        
        self.window.fill(DARK_GRAY)
        self.render_persian_text(self.window, f" سطح {self.level - 1} کامل شد! ", self.font_large, GOLD, (WINDOW_X//2, WINDOW_Y//2 - 50), True)
        self.render_persian_text(self.window, f" سرعت افزایش یافت!", self.font_medium, WHITE, (WINDOW_X//2, WINDOW_Y//2 + 30), True)
        pygame.display.flip()
        time.sleep(1.5)
    # ==================== گیم‌اور ====================
    def game_over(self):
        self.state = "game_over"

        # ========== صدای پایان بازی ==========
        self.play_sound(self.game_over_sound)
        #=====توقف موسيقي=======
        try:
            pygame.mixer.music.stop()
            print("🎵 موسيقي متوقف شد")
        except:
            pass
        
        if self.score > self.settings.high_score:
            self.settings.high_score = self.score
            self.settings.save_high_score(self.score)

        self.save_game_history()
        
        while self.state == "game_over":
            self.window.fill(DARK_GRAY)
            
            for i in range(WINDOW_Y):
                progress = i / WINDOW_Y
                r = int(30 + 20 * progress)
                g = int(20 + 10 * progress)
                b = int(40 + 20 * progress)
                pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
            
            # ========== عنوان ==========
            self.render_persian_text(self.window, "بازی تمام شد!", self.font_large, RED, (WINDOW_X//2, 100), True)
            
            # ========== آمار ==========
            stats = [
                f"امتیاز نهایی: {self.score}",
                f"بهترین امتیاز: {self.settings.high_score}",
                f"سطح: {self.level}",
                f"پاسخ صحیح: {self.questions_correct}",
                f"پاسخ اشتباه: {self.wrong_answers}",
                f"بيشترين پاسخ پياپي: {self.max_combo}"
            ]
            
            y = 170
            for stat in stats:
                self.render_persian_text(self.window, stat, self.font_medium, LIGHT_GRAY, (WINDOW_X//2, y), True)
                y += 38
            
            # ========== دکمه‌ها ==========
            mouse_pos = pygame.mouse.get_pos()
            buttons = [
                ("بازی مجدد", "restart", (WINDOW_X//2, 420)),
                ("منو اصلی", "menu", (WINDOW_X//2, 480)),
                ("خروج", "exit", (WINDOW_X//2, 540))
            ]
            
            self.go_buttons = []
            for text, action, pos in buttons:
                rect = pygame.Rect(pos[0] - 100, pos[1] - 20, 200, 40)
                is_hover = rect.collidepoint(mouse_pos)
                color = BLUE if not is_hover else GOLD
                pygame.draw.rect(self.window, color, rect, border_radius=10)
                self.render_persian_text(self.window, text, self.font_medium, WHITE, (pos[0], pos[1]), True)
                self.go_buttons.append((rect, action))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for rect, action in self.go_buttons:
                        if rect.collidepoint(mouse_pos):
                            if action == "restart":
                                self.reset_game()
                                self.state = "playing"
                                return
                            elif action == "menu":
                                self.reset_game()
                                self.state = "menu"
                                return
                            elif action == "exit":
                                pygame.quit()
                                exit()
    def game_loop(self):
        # ========== شروع موسیقی پس‌زمینه (فقط یک بار) ==========
        if not self.music_started:
            try:
                pygame.mixer.music.play(-1)
                self.music_started = True
                print("🎵 موسیقی پس‌زمینه شروع شد")
            except:
                pass
        
        current_speed = self.settings.snake_speed + (self.level - 1)
        current_speed = min(current_speed, 25)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    return
                elif event.key == pygame.K_p:
                    self.state = "paused"
                    return
                elif event.key == pygame.K_m:
                    self.settings.sound_enabled = not self.settings.sound_enabled
                    status = "روشن" if self.settings.sound_enabled else "خاموش"
                    self.add_floating_text(WINDOW_X//2, WINDOW_Y//2 - 50, f"افکت‌ها: {status}", GOLD)
        
        if self.direction == 'UP':
            self.snake_position[1] -= 10
        elif self.direction == 'DOWN':
            self.snake_position[1] += 10
        elif self.direction == 'LEFT':
            self.snake_position[0] -= 10
        elif self.direction == 'RIGHT':
            self.snake_position[0] += 10
        
        self.snake_body.insert(0, list(self.snake_position))
        
        if (self.snake_position[0] == self.fruit_position[0] and 
            self.snake_position[1] == self.fruit_position[1]):
            
            self.play_sound(self.eat_sound)  # صدای خوردن میوه
            
            if self.ask_question():
                self.fruit_position = self.generate_fruit()
                self.add_particles(self.fruit_position[0], self.fruit_position[1], GOLD, 30)
            else:
                self.snake_body.pop()
        else:
            self.snake_body.pop()
        
        if (self.snake_position[0] < 0 or self.snake_position[0] >= WINDOW_X or
            self.snake_position[1] < 0 or self.snake_position[1] >= WINDOW_Y):
            self.game_over()
            return
        
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.game_over()
                return
        
        self.window.fill(DARK_GRAY)
        
        for x in range(0, WINDOW_X, 20):
            pygame.draw.line(self.window, (50, 50, 70), (x, 0), (x, WINDOW_Y), 1)
        for y in range(0, WINDOW_Y, 20):
            pygame.draw.line(self.window, (50, 50, 70), (0, y), (WINDOW_X, y), 1)
        
        for i, pos in enumerate(self.snake_body):
            if i == 0:
                pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10), border_radius=5)
                if self.direction == 'RIGHT':
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 8, pos[1] + 3), 2)
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 8, pos[1] + 7), 2)
                elif self.direction == 'LEFT':
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 2, pos[1] + 3), 2)
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 2, pos[1] + 7), 2)
                elif self.direction == 'UP':
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 3, pos[1] + 2), 2)
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 7, pos[1] + 2), 2)
                elif self.direction == 'DOWN':
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 3, pos[1] + 8), 2)
                    pygame.draw.circle(self.window, WHITE, (pos[0] + 7, pos[1] + 8), 2)
            else:
                pygame.draw.rect(self.window, (0, 200, 0), pygame.Rect(pos[0], pos[1], 10, 10), border_radius=3)
        
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        size = 5 + pulse * 2
        pygame.draw.circle(self.window, RED, (self.fruit_position[0] + 5, self.fruit_position[1] + 5), size)
        pygame.draw.circle(self.window, (255, 100, 100), (self.fruit_position[0] + 5, self.fruit_position[1] + 5), size/2)
        
        self.update_particles()
        self.draw_particles()
        
        progress = (self.score % 50) / 50
        bar_width = 300
        bar_height = 12
        bar_x = WINDOW_X // 2 - bar_width // 2
        bar_y = 10
        pygame.draw.rect(self.window, (50, 50, 70), (bar_x, bar_y, bar_width, bar_height), border_radius=6)
        if progress > 0:
            color = GOLD if progress < 0.7 else (255, 150, 0) if progress < 0.9 else RED
            pygame.draw.rect(self.window, color, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=6)
        level_text = f"سطح {self.level} → {self.level + 1}  ({int(progress * 100)}%)"
        self.render_persian_text(self.window, level_text, self.font_tiny, WHITE, (WINDOW_X//2, bar_y + bar_height//2 - 2), True)
        
        self.render_persian_text(self.window, f" {self.score}", self.font_medium, GOLD, (100, 30))
        lives_text = "+" * self.lives + "-" * (self.max_lives - self.lives)
        self.render_persian_text(self.window, lives_text, self.font_medium, RED, (100, 70))
        if self.combo > 2:
            self.render_persian_text(self.window, f"پشت سر هم{self.combo}", self.font_small, (255, 150, 0), (100, 110))
        self.render_persian_text(self.window, f" سطح {self.level}", self.font_small, LIGHT_GRAY, (WINDOW_X - 150, 30))
        self.render_persian_text(self.window, f" {current_speed}", self.font_small, GRAY, (WINDOW_X - 150, 65))
        self.render_persian_text(self.window, "ESC: منو | P: مکث | M: صدا", self.font_tiny, GRAY, (10, WINDOW_Y - 30))
        
        pygame.display.flip()
        self.clock.tick(current_speed)
    # ==================== حلقه اصلی بازی ====================
    def run(self):
        while self.running:
            
            # ============================================================
            # ۱. منوی اصلی
            # ============================================================
            if self.state == "menu":
                self.draw_menu()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.play_sound(self.click_sound)  # ✅ صدای کلیک
                        mouse_pos = event.pos
                        for rect, action in self.menu_buttons:
                            if rect.collidepoint(mouse_pos):
                                if action == "start":
                                    self.reset_game()
                                    self.state = "playing"
                                elif action == "settings":
                                    self.state = "settings"
                                elif action == "scores":
                                    self.state = "scores"
                                elif action == "help":
                                    self.state = "help"
                                elif action == "exit":
                                    self.running = False
                                break
            
            # ============================================================
            # ۲. تنظیمات
            # ============================================================
            elif self.state == "settings":
                self.draw_settings()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.play_sound(self.click_sound)  # ✅ صدای کلیک
                        mouse_pos = event.pos
                        for rect, action in self.settings_buttons:
                            if rect.collidepoint(mouse_pos):
                                if action == "toggle_sound":
                                    self.settings.sound_enabled = not self.settings.sound_enabled
                                elif action == "toggle_music":
                                    self.settings.music_enabled = not self.settings.music_enabled
                                    if self.settings.music_enabled:
                                        try:
                                            pygame.mixer.music.unpause()
                                        except:
                                            pass
                                    else:
                                        try:
                                            pygame.mixer.music.pause()
                                        except:
                                            pass
                                elif action == "toggle_speed":
                                    speeds = [8, 10, 12, 14, 16, 18, 20]
                                    try:
                                        current = speeds.index(self.settings.snake_speed)
                                    except ValueError:
                                        current = 2
                                    self.settings.snake_speed = speeds[(current + 1) % len(speeds)]
                                elif action == "toggle_difficulty":
                                    difficulties = ["easy", "normal", "hard"]
                                    current = difficulties.index(self.settings.difficulty)
                                    self.settings.difficulty = difficulties[(current + 1) % len(difficulties)]
                                elif action == "toggle_timer":
                                    self.settings.timer_enabled = not self.settings.timer_enabled
                                elif action == "back":
                                    self.state = "menu"
                                break
            
            # ============================================================
            # ۳. امتیازات
            # ============================================================
            elif self.state == "scores":
                self.draw_scores()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.play_sound(self.click_sound)  # ✅ صدای کلیک
                        mouse_pos = event.pos
                        if hasattr(self, 'scores_buttons'):
                            for rect, action in self.scores_buttons:
                                if rect.collidepoint(mouse_pos) and action == "back":
                                    self.state = "menu"
                                    break
            
            # ============================================================
            # ۴. راهنما
            # ============================================================
            elif self.state == "help":
                self.draw_help()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.play_sound(self.click_sound)  # ✅ صدای کلیک
                        mouse_pos = event.pos
                        if hasattr(self, 'help_buttons'):
                            for rect, action in self.help_buttons:
                                if rect.collidepoint(mouse_pos) and action == "back":
                                    self.state = "menu"
                                    break
            
            # ============================================================
            # ۵. حالت بازی (اجرای اصلی)
            # ============================================================
            elif self.state == "playing":
                self.game_loop()
            
            # ============================================================
            # ۶. گیم‌اور
            # ============================================================
            elif self.state == "game_over":
                self.game_over()
            
            # ============================================================
            # ۷. حالت مکث
            # ============================================================
            elif self.state == "paused":
                self.window.fill(DARK_GRAY)
                for i in range(WINDOW_Y):
                    progress = i / WINDOW_Y
                    r = int(30 + 20 * progress)
                    g = int(20 + 10 * progress)
                    b = int(40 + 20 * progress)
                    pygame.draw.line(self.window, (r, g, b), (0, i), (WINDOW_X, i))
                
                self.render_persian_text(self.window, "مکث", self.font_large, GOLD, (WINDOW_X//2, WINDOW_Y//2 - 60), True)
                self.render_persian_text(self.window, "برای ادامه P را بزنید", self.font_medium, LIGHT_GRAY, (WINDOW_X//2, WINDOW_Y//2 + 20), True)
                self.render_persian_text(self.window, "ESC برای بازگشت به منو", self.font_small, GRAY, (WINDOW_X//2, WINDOW_Y//2 + 70), True)
                self.render_persian_text(self.window, f"امتیاز: {self.score} | سطح: {self.level}", 
                                        self.font_small, GOLD, (WINDOW_X//2, WINDOW_Y//2 + 120), True)
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.state = "playing"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
            
            # ============================================================
            # ۸. سطح‌آپ (نمایش پیام)
            # ============================================================
            elif self.state == "level_complete":
                pass
        
        pygame.quit()
#----اجراي بازي-----------
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
