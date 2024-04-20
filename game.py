from entities import *
from menus import *
from data import *

class Game:
    def __init__(self) :
        pygame.init()
        self.WINDOW_SIZE_X = 1000
        self.WINDOW_SIZE_Y = 700
        self.GRID_SIZE_X = 1000
        self.GRID_SIZE_Y = 500
        self.TILE_SIZE = 50
        self.levels = [((525,25),(200, 450)), ((25,25),(550, 450)), ((25,225),(950, 200)), ((825,25),(700, 450)), ((825,25),(750, 450)), ((25,25),(800,300))]
        self.current_level = 0
        self.active_screen = "name"
        self.paused_game = True
        self.set_screen_size() 
        self.clock = pygame.time.Clock()
        self.new_game()
        
    def set_screen_size(self) :
        self.screen = pygame.display.set_mode([self.WINDOW_SIZE_X, self.WINDOW_SIZE_Y])    
    
    def draw_grid(self) :
        [pygame.draw.line(self.screen, [50] * 3, (x, 0), (x, self.GRID_SIZE_Y)) for x in range(0, self.WINDOW_SIZE_X + 50, self.TILE_SIZE)]
        [pygame.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE_X, y)) for y in range(0, self.GRID_SIZE_Y + 50, self.TILE_SIZE)]
        [self.screen.blit(pygame.font.SysFont('Arial', 10).render(str(x - 500), True, 'black'), (x - 18, 250)) for x in range(0, 500, self.TILE_SIZE)]
        [self.screen.blit(pygame.font.SysFont('Arial', 10).render(str(x - 500), True, 'black'), (x - 15, 250)) for x in range(550, self.WINDOW_SIZE_X + 50, self.TILE_SIZE)]
        [self.screen.blit(pygame.font.SysFont('Arial', 10).render(str(250 - y), True, 'black'), (484, y)) for y in range(0, 250, self.TILE_SIZE)]
        [self.screen.blit(pygame.font.SysFont('Arial', 10).render(str(250 - y), True, 'black'), (482, y)) for y in range(300, self.GRID_SIZE_Y, self.TILE_SIZE)]
        self.screen.blit(pygame.font.SysFont('Arial', 10).render('0', True, 'black'), (493, 250))
        pygame.draw.line(self.screen, [50] * 3, (500, 0), (500, 500), 3)
        pygame.draw.line(self.screen, [50] * 3, (0, 250), (1000, 250), 3)
    
    def new_game(self) :
        self.highscore = HighscoreManager(self)        
        self.menu = Menu(self)
        self.finish = FinishScreen(self)
        self.ball = Ball(self)
        self.finish_line = Finish(self)
        self.calculator = Calculator(self, (420, 510))
        self.formulaBox = FormulaInputBox(self, (60, 525, 300, 30))
        self.limitBox_left = LimitBox(self, (100, 575, 70, 30), 'left')
        self.limitBox_right = LimitBox(self, (250, 575, 70, 30), 'right')
        self.enter_btn = EnterButton(self, (20, 625, 100, 50))
        self.start_btn = StartButton(self, (425, 550, 150, 60))
        self.restart_btn = RestartButton(self, (450, 625, 100, 50))
        self.edit_btn = EditButton(self, (140, 625, 100, 50))
        self.delete_btn = DeleteButton(self, (260, 625, 100, 50))
        self.back_btn = BackButton(self, (950, 650, 50, 50))
        self.storage = StorageBox(self, (625, 515, 300, 30))
        self.name_ask = AskName(self)
    
    def update(self) :
        if not self.paused_game :
            self.ball.update()
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw(self) :
        self.screen.fill('white')
        self.screen.fill('#ffd9ab', (0, self.GRID_SIZE_Y, self.GRID_SIZE_X, self.WINDOW_SIZE_Y))
        self.draw_grid()
        self.ball.draw()
        self.finish_line.draw()
        self.calculator.draw()
        self.formulaBox.draw()
        self.limitBox_left.draw()
        self.limitBox_right.draw()
        self.enter_btn.draw()
        self.start_btn.draw()
        self.restart_btn.draw()
        self.edit_btn.draw()
        self.delete_btn.draw()
        self.back_btn.draw()
        self.storage.draw()
    
    def check_event(self) :
        event_list = pygame.event.get()
        for event in event_list :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            self.formulaBox.handle_event(event)
            self.limitBox_left.handle_event(event)
            self.limitBox_right.handle_event(event)
            self.enter_btn.handle_event(event)
            self.start_btn.handle_event(event)
            self.restart_btn.handle_event(event)
            self.edit_btn.handle_event(event)
            self.delete_btn.handle_event(event)
            self.back_btn.handle_event(event)
        self.storage.update(event_list)
    
    def run(self) :
        while True :    
            self.update()
            if self.active_screen == "menu" :
                self.menu.check_event()               
                self.menu.draw()
            elif self.active_screen == "finish" :
                self.finish.check_event()                
                self.finish.draw()
            elif self.active_screen == "name" :
                self.name_ask.check_event()                
                self.name_ask.draw()
            else :
                self.check_event()               
                self.draw()
        
if __name__ == '__main__' :
    pygame.display.set_caption("Math Ball")
    game = Game()
    game.run()