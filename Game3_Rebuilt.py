import random
import pygame
import sys
import math

pygame.init()
pygame.mixer.init()

#Image Processing
screen = pygame.display.set_mode((1300, 700))
menu_screen = pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_menu1.png")
settings_screen = pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_settings.png")
upgrades_screen = pygame.transform.scale(pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_upgrades.png"), (1300, 700))
level_screen = pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_levels.png")
back_screen = pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_background_2.png")
lock_icon = pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\adven_lock_icon.png")
herostanding = pygame.transform.scale(pygame.image.load(r"C:\Users\kael\OneDrive\Documents\Program Pictures\Hero_StandingRB.png"), (100, 100))



#musics
menu_music = r"C:\Users\kael\OneDrive\Documents\Program Music\Skyrim 8-Bit Theme.wav"
safe_music_1 = r"C:\Users\kael\OneDrive\Documents\Program Music\The Elder Scrolls V  Skyrim - Secunda 8 Bit Version.wav"
safe_music_2 = r"C:\Users\kael\OneDrive\Documents\Program Music\Hobbit Music - Lord of the Rings [8-bit].wav"
###ADD COMBAT MUSIC!!!###
victory_music_1 = r"C:\Users\kael\OneDrive\Documents\Program Music\Sigma Male Grindset Theme 8-bit remix.wav"
victory_music_2 = r"C:\Users\kael\OneDrive\Documents\Program Music\Theme Music 1 - Lord of the Rings [8-bit].wav"
boss_fight_music = r"C:\Users\kael\OneDrive\Documents\Program Music\Duel Of Fates 8-Bit.wav"

#Classes
class Game_State:
    
    def __init__(self, next_state=[]):
        self.next_state = next_state
        self.activated = False
        
    def switch_state(self, index):
        try:
            if self.activated == True:
                self.next_state[index].activated = True
                self.activated = False
            if self.activated == False:
                pass
        except IndexError:
            pass
        
    def __eq__(self, other):
        if isinstance(other, bool):
            if self.activated == other:
                return True
        return False
        
class Button:

    def __init__(self, x, y, width, height, func=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func

    def check_pressed(self, ax, ay):
        if ax >= self.x and ax <= self.x + self.width:
            if ay >= self.y and ay<= self.y + self.height:
                if self.func != None:
                    return self.func()
                return True
        return False
    
class background:

    def __init__(self, x, y, width, height, level=0, repeating=False):
        pass
    

def fun1(num):
    def rf1():
        global stage
        global levels_unlocked
        levels_unlocked = num+(10*stage)
    return rf1
        
def fun2():
    global stage
    if stage < 3:
        stage += 1

def fun3():
    global stage
    if stage > 0:
        stage -= 1
        
mouse_timer = 0        
game = True
dying = Game_State()
running = Game_State([dying])
levels = Game_State([running])
settings = Game_State()
upgrades = Game_State()
menu = Game_State([settings, levels, upgrades])
menu.activated = True
menu_button1 = Button(460, 155, 380, 105, lambda: menu.switch_state(1))
menu_button2 = Button(460, 280, 380, 105, lambda: menu.switch_state(2))
menu_button3 = Button(460, 410, 380, 105, lambda: menu.switch_state(0))
menu_button4 = Button(460, 560, 380, 105)
controls = Game_State([menu, settings])
settings.next_state = [menu, running, controls]
settings_button1 = Button(480, 590, 340, 85, lambda: settings.switch_state(0))
upgrades.next_state = [menu]
upgrades_button1 = Button(480, 590, 345, 85, lambda: upgrades.switch_state(0))
dying.next_state = [menu]
levels.next_state.append(menu)
levels_button1 = Button(15, 15, 235, 95, lambda: levels.switch_state(1))
level1 = Button(110, 310, 165, 130,  fun1(1))
level2 = Button(340, 310, 165, 130,  fun1(2))
level3 = Button(570, 310, 165, 130,  fun1(3))
level4 = Button(800, 310, 165, 130,  fun1(4))
level5 = Button(1030, 310, 165, 130,  fun1(5))
level6 = Button(110, 525, 165, 130,  fun1(6))
level7 = Button(340, 525, 165, 130,  fun1(7))
level8 = Button(570, 525, 165, 130,  fun1(8))
level9 = Button(800, 525, 165, 130,  fun1(9))
level10 = Button(1030, 525, 165, 130,  fun1(10))
stage_down = Button(225, 135, 100, 85, fun3)
stage_up = Button(975, 135, 105, 85, fun2)
music_set = False
music_start = False
memory_gathered = False
stage = 0
levels_unlocked = 0
unspent_xp = 0
level_buttons = [(110, 310), (340, 310), (570, 310), (800, 310), (1030, 310), (110, 525), (340, 525), (570, 525), (800, 525), (1030, 525)]
font = pygame.font.Font('freesansbold.ttf', 50)
true_level = 0
while game:

    if not memory_gathered:
        with open("G3_memory.txt", "r") as mem_file:
            mem_lines = mem_file.readlines() #line 1 is the number of unlocked levels, line 2 is the amount of unspent xp
            if len(mem_lines) > 0:
                levels_unlocked = int(mem_lines[0])
                unspent_xp = int(mem_lines[1])
        memory_gathered = True
    
    screen.fill((255,255,255))
    
    if menu == True:
        screen.blit(menu_screen, [0,0])
        
        if not music_set:
            pygame.mixer.music.load(menu_music)
            music_set = True
            
        
        if pygame.mouse.get_pressed()[0] and mouse_timer == 0:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            menu_button1.check_pressed(mouse_x, mouse_y)
            menu_button2.check_pressed(mouse_x, mouse_y)
            menu_button3.check_pressed(mouse_x, mouse_y)
            game = (not menu_button4.check_pressed(mouse_x, mouse_y))
                    
        
            #print(f"X: {mouse_x}, Y: {mouse_y}")
                
    if settings == True:
        screen.blit(settings_screen, [0,0])
        
        if pygame.mouse.get_pressed()[0] and mouse_timer == 0:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            if mouse_y <= 675 and mouse_y >= 590:
                if mouse_x <= 820 and mouse_x >= 480:
                    settings.switch_state(0)
                    
        #pygame.mixer.music.set_volume(0.5)
        #pygame.mixer.music.play(-1)

    if upgrades == True:
        screen.blit(upgrades_screen, [0,0])

        if pygame.mouse.get_pressed()[0] and mouse_timer == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y <=675 and mouse_y >= 590:
                if mouse_x <= 825 and mouse_x >= 480:
                    upgrades.switch_state(0)
                    
    if levels == True:
        screen.blit(level_screen, [0,0])
        
        if stage == 0:
            screen.blit(font.render("Forest Day Stage", 1, pygame.Color("Black")), [450, 150])
        elif stage == 1:
            screen.blit(font.render("Forest Night Stage", 1, pygame.Color("Black")), [440, 150])
        elif stage == 2:
            screen.blit(font.render("Moutain Stage", 1, pygame.Color("Black")), [500, 150])
        elif stage == 3:
            screen.blit(font.render("Abyssal Stage", 1, pygame.Color("Black")), [500, 150])

        if stage > math.floor(levels_unlocked/10):
            true_level = 0
        elif stage == math.floor(levels_unlocked/10):
            true_level = levels_unlocked%10
        else:
            true_level = 10
        for i in range(10 - true_level):
            #print(9-i)
            screen.blit(lock_icon, [level_buttons[9-i][0], level_buttons[9-i][1]])
        
        if pygame.mouse.get_pressed()[0] and mouse_timer == 0:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            levels_button1.check_pressed(mouse_x, mouse_y)
            level1.check_pressed(mouse_x, mouse_y)
            level2.check_pressed(mouse_x, mouse_y)
            level3.check_pressed(mouse_x, mouse_y)
            level4.check_pressed(mouse_x, mouse_y)
            level5.check_pressed(mouse_x, mouse_y)
            level6.check_pressed(mouse_x, mouse_y)
            level7.check_pressed(mouse_x, mouse_y)
            level8.check_pressed(mouse_x, mouse_y)
            level9.check_pressed(mouse_x, mouse_y)
            level10.check_pressed(mouse_x, mouse_y)
            stage_down.check_pressed(mouse_x, mouse_y)
            stage_up.check_pressed(mouse_x, mouse_y)
           
    if running == True:
        pass
                
    if dying == True:
        pass
       
    """if music_set and not music_start:
        print("Music should be playing")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        music_start = True"""
        
    if pygame.mouse.get_pressed()[0] and mouse_timer == 0:
        mouse_timer = 200
        
    if mouse_timer > 0:
        mouse_timer -= 1
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
    #Menu button borders:
    """pygame.draw.line(screen, "Black", (0, 135), (1300, 135))
    pygame.draw.line(screen, "Black", (0, 220), (1300, 220))
    pygame.draw.line(screen, "Black", (225, 0), (225, 700))
    pygame.draw.line(screen, "Black", (325, 0), (325, 700))#difference of 100

    pygame.draw.line(screen, "Black", (975, 0), (975, 700))
    pygame.draw.line(screen, "Black", (1080, 0), (1080, 700))"""
            
    pygame.display.flip()
with open("G3_memory.txt", "w") as mem_file:
    mem_file.write(f"{levels_unlocked}\n{unspent_xp}")