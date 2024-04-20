import pygame, sys
from entities import PlayButton, BackToMenuButton, NameBox, SaveNameButton, EditNameButton, LevelBox, ShowScoresButton, ScoreBox, ScoreLevelBox
import random

class Menu :
    def __init__(self, game) :
        self.game = game
        self.set_screen_size()
        self.new_menu()

    def set_screen_size(self) :
        self.screen = pygame.display.set_mode([500, 275])
    
    def new_menu(self) :
        self.play_btn = PlayButton(self, (30, 20, 220, 75))
        self.edit_btn = EditNameButton(self, (30, 180, 220, 75))
        self.level_select = LevelBox(self, (275, 20, 200, 30))
        self.scores_btn = ShowScoresButton(self, (30, 100, 220, 75))
                     
    def draw(self) :
        self.game.screen.fill('#ffd9ab')
        self.play_btn.draw()
        self.edit_btn.draw()
        self.level_select.draw()
        self.scores_btn.draw()
      
    def set_current_level(self, level) :
        if level == 6 :
            self.game.current_level = 'randomize'
        else :
            self.game.current_level = level  
        
    def enter_game(self) :
        if self.game.current_level == 'randomize' :
            r1 = random.randint(0, 19)
            r2 = random.randint(0, 8)
            self.game.ball.start = (r1 * 50 + 25, r2 * 50 + 25)
            r3 = random.randint(0, 19) 
            r4 = random.randint(r2, 9)  
            self.game.finish_line.start = (r3 * 50, r4 * 50)      
        else :
            self.game.ball.start = self.game.levels[self.game.current_level][0]
            self.game.finish_line.start = self.game.levels[self.game.current_level][1]
        self.game.formulaBox.warning_text = "" 
        self.game.storage.option_list = ['-250']
        self.game.calculator.formulas = []
        self.game.calculator.ramps = []
        self.game.calculator.score = 0
        self.game.calculator.add_ramp(('-250', int('-500'), int('500')))
        self.game.storage.selected = 0
        self.game.formulaBox.selected_formula(0)
        self.game.limitBox_left.selected_formula(0)
        self.game.limitBox_right.selected_formula(0)
        self.game.active_screen = ""
        self.game.ball.reset()
        self.game.set_screen_size()
        
    def go_to_scores(self) :
        self.game.finish.set_screen_size()
        self.game.highscore.show_scores()
        self.game.active_screen  = "finish"
        
    def edit_name(self) :
        self.game.active_screen  = "name"
        
    def check_event(self) :
        event_list = pygame.event.get()
        for event in event_list :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            self.play_btn.handle_event(event)
            self.edit_btn.handle_event(event)
            self.scores_btn.handle_event(event)
        self.level_select.update(event_list)
            
class FinishScreen :
    def __init__(self, game) :
        self.game = game
        self.set_screen_size()
        self.new_finish()

    def set_screen_size(self) :
        self.screen = pygame.display.set_mode([450, 660])
    
    def new_finish(self) :
        self.back_btn = BackToMenuButton(self, (40, 20, 150, 50))
        self.score_box = ScoreBox(self, (30, 90, 390, 550))
        self.level_list = ScoreLevelBox(self, (210, 30, 200, 30))
         
    def draw(self) :
        self.game.screen.fill('#ffd9ab')
        self.back_btn.draw()
        self.score_box.draw()
        self.level_list.draw()
        
    def enter_menu(self) :
        self.game.active_screen  = "menu"
        self.game.menu.set_screen_size()
        
    def sort_scores(self, level) :
        self.game.highscore.show_per_level(level)   
        
    def check_event(self) :
        event_list = pygame.event.get()
        for event in event_list :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            self.back_btn.handle_event(event)
        self.level_list.update(event_list)
            
class AskName :
    def __init__(self, game) :
        self.game = game
        self.set_screen_size()
        self.new_menu()

    def set_screen_size(self) :
        self.screen = pygame.display.set_mode([500, 275])
    
    def new_menu(self) :
        self.namebox = NameBox(self, (100, 100, 300, 30))
        self.save_btn = SaveNameButton(self, (200, 150, 100, 50))
        
    def enter_name(self) :
        self.game.highscore.name = self.namebox.text
        self.game.active_screen  = "menu"
                     
    def draw(self) :
        self.game.screen.fill('#ffd9ab')
        self.namebox.draw()
        self.save_btn.draw()
        
    def check_event(self) :
        event_list = pygame.event.get()
        for event in event_list :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            self.namebox.handle_event(event)
            self.save_btn.handle_event(event)