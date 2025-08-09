
# file:///Users/carso/python_folder/my_scripts/clicky_clicker_remastered/roadmap.md

import json
from datetime import datetime
import os
import pygame
import colorsys
import ctypes
import configparser
import time

last_clickies = 0
digit_change_times = {}
dev_repeat = False

smoothscale = True

cps = 0
cps_inclusive = 0
cps_price = 10

cpsUpgradeUnlocked = True

cpc = 1
mult = 1

last_cps_time = time.time()
old_clickies = 0

build_num = 0
version = "0.0.1"
CLICKIES = 0
clicked_button = False

old_clickies = 0

fps_a = 0

os.chdir(os.path.dirname(__file__))

## Pygame Initialization

fps = []
flags = pygame.DOUBLEBUF |  pygame.RESIZABLE | pygame.SRCALPHA # pygame.RESIZABLE

pygame.init()
screen = pygame.display.set_mode((1920, 1080), flags, display=0)
pygame.display.set_caption("Clicky Clicker: Remastered")
clock = pygame.time.Clock()
font = pygame.font.Font("clicky_font_bold.otf", 150)
font2 = pygame.font.Font("clicky_font_medium.otf", 100)
font3 = pygame.font.Font("clicky_font_medium.otf", 40)
_7seg_font = pygame.font.Font("7seg_font.ttf", 40)
gear_font = pygame.font.Font("gear_font.ttf", 160)
notosans_symbols = pygame.font.Font("notosans_symbols.ttf", 160)

back_arrow = pygame.image.load("back_arrow.png").convert_alpha()

if dev_repeat:
    pygame.key.set_repeat(300, 50)
else:
    pygame.key.set_repeat(300, 200)

game_state = "main_menu"

game_states = [
    "main_menu",
    "ingame",
    "ingame_menu",
    "settings",
    "upgrades"
    "wip"
]

newgame_data = {
    "clickies": 0,
    "cps": 1,
    "cpc": 0,
    "hasGottenDailyGift": False,
    "hasDoneTutorial": False
}

dev = "DEV_ENABLED"

new_game_state = "main_menu"

## Definitions

def get_refresh_rate():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dc = user32.GetDC(0)
    refresh_rate = ctypes.windll.gdi32.GetDeviceCaps(dc, 116)  # 116 = VREFRESH
    return refresh_rate

### Saving

def get_build_number():
    try:
        with open("build", "r") as f:
            return int(f.read())
    except:
        return 0

def increment_build_number():
    num = get_build_number() + 1
    with open("build", "w") as f:
        f.write(str(num))
    return num

if dev == "DEV_ENABLED":
    build_num = increment_build_number()

def save(clickies=0, cps=0, cpc=1, hasGottenDailyGift=False, hasDoneTutorial=False):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    data = {
        "clickies": clickies,
        "cps": cps,
        "cpc": cpc,
        "hasGottenDailyGift": hasGottenDailyGift,
        "hasDoneTutorial": hasDoneTutorial
    }

    try:
        with open("save.json", "r") as f:
            old_data = json.load(f)
        
        with open(f"save_{formatted_time}.json", "w") as f:
            json.dump(data, f, indent=4)
    except:
        with open("save.json", "w") as f:
            json.dump(data, f, indent=4)
###

click_timestamps = []

prev_val = None
prev_time = None

def get_rate(current):
    global prev_val, prev_time
    now = time.time()
    
    if prev_val is None or prev_time is None:
        prev_val = current
        prev_time = now
        return 0.0  # no rate yet
    
    delta_val = current - prev_val
    delta_time = now - prev_time
    
    prev_val = current
    prev_time = now
    
    if delta_time == 0:
        return 0.0  # avoid div by zero
    
    return round(delta_val / delta_time, 2)

def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y)*(p2x - p1x)/(p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def hsl_rainbow(index, total):
    hue = index / total  # goes from 0.0 to 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)  # pastel-ish: lower saturation
    return (int(r * 255), int(g * 255), int(b * 255))

### Menus

class Menu:
    def renderBackground(self, r,g,b):
        screen.fill((r,g,b))
    def render(self):
        None

class MainMenu(Menu):
    def __init__(self):
        self.points_changelog = [
            (screen_width, (screen_height/9)*3),
            (screen_width, ((screen_height/9)*3)+100*(screen_width/1920)),
            (screen_width-(600 + hover[0])*(screen_width/1920),((screen_height/9)*3)+100*(screen_width/1920)),
            (screen_width-(500 + hover[0])*(screen_width/1920),((screen_height/9)*3)+0*(screen_width/1920))
        ]

        self.points_settings = [
            (screen_width, ((screen_height/9)*3) +120*(screen_width/1920)),
            (screen_width, ((screen_height/9)*3)+220*(screen_width/1920)),
            (screen_width-(600 + hover[1])*(screen_width/1920),((screen_height/9)*3)+220*(screen_width/1920)),
            (screen_width-(500 + hover[1])*(screen_width/1920),((screen_height/9)*3)+120*(screen_width/1920))
        ]

        self.points_more_games = [
            (screen_width, ((screen_height/9)*3) +240*(screen_width/1920)),
            (screen_width, ((screen_height/9)*3)+340*(screen_width/1920)),
            (screen_width-(600 + hover[2])*(screen_width/1920),((screen_height/9)*3)+340*(screen_width/1920)),
            (screen_width-(500 + hover[2])*(screen_width/1920),((screen_height/9)*3)+240*(screen_width/1920))
        ]
        self.renderBackground(30,30,30)
        scaled_r = 150 * (screen_width / 1920)

        self.isMouseAtPlay = (
            (mouse_x - (screen_width/2) - (mouse_xc / 8))**2
            + (mouse_y - (screen_height))**2
            ) <= scaled_r**2
    def render_2(self):
        title_surface = font.render("Clicky", True, (80, 255, 80))
        title_surface_2 = font.render("Clicker", True, (130, 255, 100))
        screen.blit(title_surface, (screen_width / 2 - title_surface.get_width(), 50))
        screen.blit(title_surface_2, (screen_width / 2 + 25, 50))
        text_x, text_y = int(screen_width / 2 - 200 * (screen_width / 1920)),int(180*(screen_height/1080))
        for i, char in enumerate(text):
            color = hsl_rainbow(i, num_letters - 1)
            # raise minimum brightness to 100 (any 0 becomes 100)
            color = tuple(max(c, 100) for c in color)

            surf = font2.render(char, True, color)
            screen.blit(surf, (text_x, text_y))
            text_x += surf.get_width()
        pygame.draw.circle(screen, (50,200,50), ((screen_width/2) - (mouse_xc / 32), (screen_height)), 200*(screen_width/1920), 0) #    + (mouse_yc / 32)
        pygame.draw.circle(screen, (100,255,100), ((screen_width/2) - (mouse_xc / 16), (screen_height)), 195*(screen_width/1920), 0) #  + (mouse_yc / 16)
        pygame.draw.circle(screen, (50,200,50), ((screen_width/2) - (mouse_xc / 10), (screen_height)), 150*(screen_width/1920), 0) #    + (mouse_yc / 8)
        pygame.draw.circle(screen, (80,255,80), ((screen_width/2) - (mouse_xc / 8), (screen_height)), 150*(screen_width/1920), 0)

        self.points_changelog = [
            (screen_width, (screen_height/9)*3),
            (screen_width, ((screen_height/9)*3)+100*(screen_width/1920)),
            (screen_width-(600 + hover[0])*(screen_width/1920),((screen_height/9)*3)+100*(screen_width/1920)),
            (screen_width-(500 + hover[0])*(screen_width/1920),((screen_height/9)*3)+0*(screen_width/1920))
        ]
        pygame.draw.polygon(screen, (255,70,70), self.points_changelog)

        self.points_settings = [
            (screen_width, ((screen_height/9)*3) +120*(screen_width/1920)),
            (screen_width, ((screen_height/9)*3)+220*(screen_width/1920)),
            (screen_width-(600 + hover[1])*(screen_width/1920),((screen_height/9)*3)+220*(screen_width/1920)),
            (screen_width-(500 + hover[1])*(screen_width/1920),((screen_height/9)*3)+120*(screen_width/1920))
        ]
        pygame.draw.polygon(screen, (70,255,70), self.points_settings)

        self.points_more_games = [
            (screen_width, ((screen_height/9)*3) +240*(screen_width/1920)),
            (screen_width, ((screen_height/9)*3)+340*(screen_width/1920)),
            (screen_width-(600 + hover[2])*(screen_width/1920),((screen_height/9)*3)+340*(screen_width/1920)),
            (screen_width-(500 + hover[2])*(screen_width/1920),((screen_height/9)*3)+240*(screen_width/1920))
        ]
        pygame.draw.polygon(screen, (70,70,255), self.points_more_games)


        changelog_text_surface = font2.render("Updates", True, (255, 220, 220))
        settings_text_surface = font2.render("Settings", True, (220, 255, 220))
        more_games_text_surface = font2.render("More Games", True, (200, 200, 255))

        screen.blit(changelog_text_surface, (screen_width-(480*(screen_width/1920))-hover[0]*(screen_width/1920),((screen_height/9)*3)-0*(screen_width/1920)) )
        screen.blit(settings_text_surface, (screen_width-(480*(screen_width/1920))-hover[1]*(screen_width/1920),((screen_height/9)*3)+124*(screen_width/1920)) )
        screen.blit(more_games_text_surface, (screen_width-(480*(screen_width/1920))-hover[2]*(screen_width/1920),((screen_height/9)*3)+244*(screen_width/1920)) )

        if isHover[0]:
            changelog_text_surface_2 = font2.render(f"v{version}", True, (255,255,255))
            changelog_text_surface_2.set_alpha(alphaHover[0])
            screen.blit(changelog_text_surface_2, (screen_width-(150*(screen_width/1920))-hover[0]*(screen_width/1920),((screen_height/9)*3)-0*(screen_width/1920)))

        playbutton_text_surface = font2.render("PLAY", True, (200, 255, 200))

        screen.blit(playbutton_text_surface, ((screen_width/2) - (mouse_xc / 9) - playbutton_text_surface.get_width()/2, (screen_height -100*(screen_width/1920))))

        build_num_surf = font3.render(f"cc_r-v{version}-b{build_num}", True, (255, 255, 255))
        build_num_surf.set_alpha(64)
        screen.blit(build_num_surf, (5, screen_height-60))
    
    def render(self):
        self.render_2()

class InGame(Menu):
    def __init__(self):
        self.isMouseAtSettingsButton = mouse_x > (screen_width/16)*14 and mouse_y < (screen_height/9)*4 and mouse_y > (screen_height/9)*2
        self.isMouseAtMenuButton = mouse_x > (screen_width/16)*14 and mouse_y < (screen_height/9)*2
        self.renderBackground(30,30,30)

        scaled_r = 150 * (screen_width / 1920)
        self.isMouseAtClicky = (
            (mouse_x - (screen_width/2) - (mouse_xc / 8))**2
            + (mouse_y - (screen_height/2))**2
            ) <= scaled_r**2 or ((mouse_x - (screen_width/2) - (mouse_xc / 10))**2+ (mouse_y - (screen_height/2))**2) <= scaled_r**2 or ((mouse_x - (screen_width/2) - (mouse_xc / 16))**2+ (mouse_y - (screen_height/2))**2) <= (195*(screen_width/1920))**2 or ((mouse_x - (screen_width/2) - (mouse_xc / 28))**2+ (mouse_y - (screen_height/2))**2) <= (200*(screen_width/1920))**2
    def render_clicky(self):
        pygame.draw.circle(screen, (50,200,50), ((screen_width/2) - (mouse_xc / 24), (screen_height/2) - (mouse_yc / 24)), 200*(screen_width/1920), 0)
        pygame.draw.circle(screen, (100,255,100), ((screen_width/2) - (mouse_xc / 16), (screen_height/2) - (mouse_yc / 16)), 195*(screen_width/1920), 0)
        pygame.draw.circle(screen, (50,200,50), ((screen_width/2) - (mouse_xc / 16), (screen_height/2) - (mouse_yc / 16)) if not clicked_button else ((screen_width/2) - (mouse_xc / 16), (screen_height/2) - (mouse_yc / 16)), 150*(screen_width/1920), 0)
        pygame.draw.circle(screen, (80,255,80) if not clicked_button else (65,235,65), ((screen_width/2) - (mouse_xc / 14), (screen_height/2) - (mouse_yc / 14)) if not clicked_button else ((screen_width/2) - (mouse_xc / 32), (screen_height/2) - (mouse_yc / 32)), 150*(screen_width/1920), 0)
        if clicked_button:
            pygame.draw.circle(screen, (100,255,100), ((screen_width/2) - (mouse_xc / 16), (screen_height/2) - (mouse_yc/16)), 195*(screen_width/1920), int(45*(screen_width/1920)))
    def render_clickies_text(self, clickies):
        def ease_out_quad(t):
            return 1 - (1 - t) ** 2
        
        # text_surf = font.render(str(clickies), True, (255,255,255))
        # screen.blit(text_surf, (((screen_width/2)-text_surf.get_width()), 150*(screen_height/1920)))

        global last_clickies, digit_change_times

        scale_amount = 0.2

        clickies_str = str(clickies)
        last_str = str(last_clickies).rjust(len(clickies_str), '0')

        now = time.time()
        duration = 0.3  # animation duration in seconds

        x_offset = (screen_width / 2)
        base_y = 150
        y = int(base_y * (screen_height / 1920))

        total_width = 0
        char_surfs = []

        for i, (cur, prev) in enumerate(zip(clickies_str, last_str)):
            if cur != prev:
                digit_change_times[i] = now  # record time of change

            # time since this digit last changed
            t = now - digit_change_times.get(i, 0)
            t_norm = min(max(t / duration, 0), 1)

            scale = 1.0 + scale_amount * (1 - ease_out_quad(t_norm)) if t < duration else 1.0
            size = int(150 * scale * (screen_width / 1920))

            font_temp = pygame.font.Font("clicky_font_bold.otf", size)
            surf = font_temp.render(cur, True, (255, 255, 255))

            base_size = int(150 * (screen_width / 1920))
            y_offset = (surf.get_height() - base_size) / 2

            char_surfs.append((surf, y - y_offset))  # pass y offset here
            total_width += surf.get_width()

        x = x_offset - total_width / 2

        for surf, y_adj in char_surfs:
            screen.blit(surf, (x, y_adj))
            x += surf.get_width()

        last_clickies = clickies

    def render_cps_text_fake(self, cps):
        text_surf = font3.render(f"{cps} cps", True, (255,255,255))
        screen.blit(text_surf, ((screen_width/2)-(text_surf.get_width()/2),(screen_height/9)*7))

    def render_cps_text_actual(self, cps):
        text_surf = font3.render(f"{cps} actual", True, (255,255,255))
        screen.blit(text_surf, ((screen_width/2)-(text_surf.get_width()/2),(screen_height/18)*15))

    def render_top_info(self, cpc, multiplier):
        text_surf = font3.render(f"{cpc} cpc | {multiplier}x mult", True, (255,255,255))
        screen.blit(text_surf, ((screen_width/2)-(text_surf.get_width()/2), (screen_height/18)*0.5))

    def render_sidebar(self):
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect((screen_width/16)*14, 0, 800, screen_height), border_radius=20)

        settings_button = True
        menu_button = True
        if settings_button == True:
            if mouse_x > (screen_width/16)*14 and mouse_y < (screen_height/9)*4 and mouse_y > (screen_height/9)*2:
                pygame.draw.rect(screen, (60, 60, 60), pygame.Rect((screen_width/16)*14, (screen_height/9)*2, 800, (screen_height/9)*2), border_radius=20)
        if menu_button == True:
            if mouse_x > (screen_width/16)*14 and mouse_y < (screen_height/9)*2:
                pygame.draw.rect(screen, (60, 60, 60), pygame.Rect((screen_width/16)*14, 0, 800, (screen_height/9)*2), border_radius=20)


            text_surf = notosans_symbols.render("☰", True, (255,255,255))
            screen.blit(text_surf, ((screen_width/16)*14.2, (screen_height/9)*-0.3))

        if settings_button == True:

            text_surf = gear_font.render("⚙", True, (255,255,255))
            screen.blit(text_surf, ((screen_width/16)*14.2, (screen_height/9)*2))
        
        #* TODO Multiplayer button: Noto Emoji "🎮"

    def render_upgrades_button(self):
        self.isMosueAtUpgradesButton = mouse_x > (screen_width/32)*1 and mouse_x < (screen_width/32)*1 + (screen_width/16)*4 and mouse_y > (screen_height/9)*3 and mouse_y < (screen_height/9)*3 + (screen_height/18)*1.5

        pygame.draw.rect(screen, (230, 50, 50), pygame.Rect((screen_width/32)*1, (screen_height/9)*3, (screen_width/16)*4, (screen_height/18)*1.5), border_radius=20)

        if self.isMosueAtUpgradesButton:
            pygame.draw.rect(screen, (250, 80, 80), pygame.Rect((screen_width/32)*1, (screen_height/9)*3, (screen_width/16)*4, (screen_height/18)*1.5), border_radius=20)

        text_surf = font2.render("Upgrades", True, (230,230,230))
        screen.blit(text_surf, ((screen_width/32)*1.5, (screen_height/9)*2.95))

    def render_class_upgrades_button(self):
        self.isMosueAtClassUpgradesButton = mouse_x > (screen_width/32)*1 and mouse_x < (screen_width/32)*1 + (screen_width/16)*4 and mouse_y > (screen_height/9)*4 and mouse_y < (screen_height/9)*4 + (screen_height/18)*1.5

        pygame.draw.rect(screen, (50, 50, 230), pygame.Rect((screen_width/32)*1, (screen_height/9)*4, (screen_width/16)*4, (screen_height/18)*1.5), border_radius=20)

        if self.isMosueAtClassUpgradesButton:
            pygame.draw.rect(screen, (80, 80, 250), pygame.Rect((screen_width/32)*1, (screen_height/9)*4, (screen_width/16)*4, (screen_height/18)*1.5), border_radius=20)

        text_surf = font2.render("Classes", True, (230,230,230))
        screen.blit(text_surf, ((screen_width/32)*1.5, (screen_height/9)*3.95))


    def render(self):
        self.render_clicky()
        self.render_clickies_text(f"{CLICKIES:.2f}")
        self.render_cps_text_fake(cps)
        self.render_cps_text_actual(cps_inclusive)
        self.render_top_info(cpc, mult)
        self.render_sidebar()
        self.render_upgrades_button()
        self.render_class_upgrades_button()

class UpgradesMenu(Menu):
    def __init__(self):
        self.renderBackground(30,30,30)
        self.isMouseAtBackArrow = mouse_x < (screen_height/9)*1 and mouse_y < 200*(screen_height/1920)
        self.isMouseAtCpsUpgrade = mouse_x > (screen_width/32)*1 and mouse_x < (screen_width/32)*1 + (screen_width/32)*4 and mouse_y > (screen_height/32)*5 and mouse_y < (screen_height/32)*5 + (screen_height/32)*5
        if smoothscale:
            self.scaled_back_arrow = pygame.transform.smoothscale(back_arrow, ((screen_height/9)*1, (screen_height/9)*1))
        else:
            self.scaled_back_arrow = pygame.transform.scale(back_arrow, ((screen_height/9)*1, (screen_height/9)*1))
        
    def renderTopbar(self):
        pygame.draw.rect(screen, (50,50,50), pygame.Rect(0,0,screen_width, 200*(screen_height/1920)))
        
        if self.isMouseAtBackArrow:
            pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(0,0,(screen_height/9)*1,200*(screen_height/1920)), border_bottom_right_radius=20)

        screen.blit(self.scaled_back_arrow, ((screen_width/16)*0.01, (screen_height/9)*-0.05))


    def renderUpgrades(self):

        if cpsUpgradeUnlocked:
            pygame.draw.rect(screen, (60,60,230), pygame.Rect((screen_width/32)*1, (screen_height/32)*5, (screen_width/32)*4, (screen_height/32)*5), border_radius=20)
            if self.isMouseAtCpsUpgrade:
                pygame.draw.rect(screen, (80,80,250), pygame.Rect((screen_width/32)*1, (screen_height/32)*5, (screen_width/32)*4, (screen_height/32)*5), border_radius=20)
            text_surf = font2.render("CPS", True, (230, 230, 230))
            screen.blit(text_surf, ((screen_width/32)*1.15, (screen_height/32)*5))

            text_surf = font3.render(f"{cps_price:.2f} cs", True, (255, 255, 255))
            text_surf.set_alpha(127)
            screen.blit(text_surf, ((screen_width/32)*1.15, (screen_height/32)*8.5))


    def render(self):
        self.renderTopbar()
        self.renderUpgrades()

class WIPMenu(Menu):
    def __init__(self):
        global game_state
        self.renderBackground(30,30,30)

        text_surf = font.render("This menu is WIP!! Sorry!", True, (255, 255, 255))
        a = text_surf.get_width() / 2
        screen.blit(text_surf, (screen_width/2-a, screen_height/2))


## Main Loop
incr = 0
incr_2 = 0
incr_3 = 0
incr_4 = 1
incr_5 = 0
tab = "  "

running = True

text = "REMASTERED"
num_letters = len(text)

screen_width, screen_height = screen.get_size()
mouse_x, mouse_y = pygame.mouse.get_pos()
mouse_xc = mouse_x - screen_width/2
mouse_yc = mouse_y - screen_height/2

new_game_state = "main_menu"
hover = [0,0,0]
isHover = [False, False, False]
alphaHover = [0,0,0]


while running:
    game_state = new_game_state
    if game_state == "main_menu":
        main_menu = MainMenu()
        main_menu.render()

        smoothness = 1.3
        alphaSmoothness_changelog = [1.1, 1.2]

        if point_in_poly(mouse_x, mouse_y, main_menu.points_changelog):
            hover[0] = (hover[0] / smoothness) + 20
            isHover[0] = True
            alphaHover[0] = (alphaHover[0] / alphaSmoothness_changelog[0]) + 20
        else: 
            hover[0] = (hover[0] / smoothness) + 0
            alphaHover[0] = (alphaHover[0] / alphaSmoothness_changelog[1]) + 0

        if point_in_poly(mouse_x, mouse_y, main_menu.points_settings):
            hover[1] = (hover[1] / smoothness) + 20
            isHover[1] = True
        else:
            hover[1] = (hover[1] / smoothness) + 0
            isHover[1] = False

        if point_in_poly(mouse_x, mouse_y, main_menu.points_more_games):
            hover[2] = (hover[2] / smoothness) + 20
            isHover[2] = True
        else:
            hover[2] = (hover[2] / smoothness) + 0
            isHover[2] = False
    elif game_state == "ingame":
        ingame = InGame()
        ingame.render()

    elif game_state == "upgrades":
        upgrades = UpgradesMenu()
        upgrades.render()

    elif game_state == "wip":
        
        wip_menu = WIPMenu()
        if (incr_2 / 170) == 1:
            new_game_state = prev_game_state
            incr_2 = 0
        incr_2 += 1

    dt = clock.tick(fps_a) / 1000.0
    fps.insert(0, 1/dt)
    fps_a = sum(fps) / len(fps) if fps else 1
    fps_a2 = sum(fps) / len(fps) if fps else 1
    try:
        del fps[round(fps_a*2)]
    except:
        pass
    try:
        del fps[round(fps_a*16)]
    except:
        pass

    gear_font = pygame.font.Font("gear_font.ttf", int(200*(screen_width/1920)))
    notosans_symbols = pygame.font.Font("notosans_symbols.ttf", int(200*(screen_width/1920)))
    font = pygame.font.Font("clicky_font_bold.otf", int(125*(screen_width/1920)))
    font2 = pygame.font.Font("clicky_font_medium.otf", int(75*(screen_width/1920)))
    screen_width, screen_height = screen.get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_xc = mouse_x - screen_width/2
    mouse_yc = mouse_y - screen_height/2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "main_menu":

                ## Play button click detection
                if event.button == 1:
                    if main_menu.isMouseAtPlay:
                        new_game_state = "ingame"
                    
                    if point_in_poly(mouse_x, mouse_y, main_menu.points_changelog) or point_in_poly(mouse_x, mouse_y, main_menu.points_settings) or point_in_poly(mouse_x, mouse_y, main_menu.points_more_games):
                        prev_game_state = game_state
                        new_game_state = "wip"


            if game_state == "ingame":
                if event.button == 1:
                    if ingame.isMouseAtClicky:
                        CLICKIES += cpc
                        clicked_button = True
                        incr_3 = 0
                    if ingame.isMouseAtSettingsButton:
                        print("mouse clicked settings")
                        prev_game_state = game_state
                        new_game_state = "wip"
                    
                    if ingame.isMouseAtMenuButton:
                        print("mouse clicked menu")
                        prev_game_state = game_state
                        new_game_state = "main_menu" #! <<< ---============================================================================================================--- >>> Placeholder function

                    if ingame.isMosueAtUpgradesButton:
                        print("mouse clicked upgrades")
                        new_game_state = "upgrades"

                    if ingame.isMosueAtClassUpgradesButton:
                        print("mouse clicked class upgrades")
                        prev_game_state = game_state
                        new_game_state = "wip"

            if game_state == "upgrades":
                if event.button == 1:
                    if upgrades.isMouseAtBackArrow:
                        new_game_state = "ingame"
                    
                    if upgrades.isMouseAtCpsUpgrade and cpsUpgradeUnlocked:
                        
                        if CLICKIES >= cps_price:
                            cps += 1
                            CLICKIES -= cps_price
                            cps_price *= 1.1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                CLICKIES += cpc
                clicked_button = True
                incr_3 = 0

    # print("\n"*100)
    # print("Game State:")
    # print(tab + game_state)
    # print(f"Clicked Button: {clicked_button}")
    # print(f"incr_3 = {incr_3}")
    # print(f"incr_4 = {incr_4}")
    # print(f"{cps / max(get_refresh_rate() / 2, 1):.10f}")
    incr += 1
    incr_3 += 1
    incr_4 += 1
    incr_5 += 1

    CLICKIES += cps * (dt * 2)

    if incr_3 > 10:
        clicked_button = False

    if incr_5 > (fps_a / 5):
        cps_inclusive = get_rate(CLICKIES)
        incr_5 = 0

    fps_surf = _7seg_font.render(f"{round(fps_a) if fps_a else '[null]'} fps", True, (255, 255, 255))
    fps_surf_2 = _7seg_font.render(f"{min(get_refresh_rate(), round(fps_a))} disp", True, (255, 255, 255))

    fps_surf.set_alpha(64)
    fps_surf_2.set_alpha(64)
    screen.blit(fps_surf, (5,5))
    screen.blit(fps_surf_2, (5,35))

    pygame.display.flip()
    clock.tick(fps_a2)