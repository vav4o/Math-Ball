import pygame
import math
from math import sin as sin, cos as cos, tan as tan, sqrt as sqrt, log as log, pow as pow

class Ball :
    def __init__(self, game) :
        self.game = game
        self.size = game.TILE_SIZE
        self.start = (25, 25)
        self.centre = self.start
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
    
    def update(self) :
        self.movement()
        self.collision()
        self.check_for_finish()
           
    def addgravity(self) :
        self.velocity_y = self.velocity_y + 0.1
    
    def movement(self) :
        self.centre = (self.centre[0] + self.velocity_x, self.centre[1] + self.velocity_y)
        self.addgravity()
        if self.centre[1] > self.game.GRID_SIZE_Y or self.centre[0] < 0 or self.centre[0] > self.game.GRID_SIZE_X * 2:
            self.game.paused_game = True
            self.game.ball.reset()
    
    def friction(self) :
        self.velocity_x = self.velocity_x * 0.85
            
    def collision(self) :
        for ramp in self.game.calculator.ramps :
            for id, coordinates in enumerate(ramp) :
                distance = math.sqrt(math.pow((self.centre[0]-coordinates[0]), 2)+math.pow((self.centre[1]-coordinates[1]), 2))
                if 24 < distance < 25 :
                    if self.velocity_y > 0:
                        if self.velocity_y <= 0.25 and self.velocity_y >= -0.25 :
                            self.velocity_y = 0
                        else :    
                            self.velocity_y = self.velocity_y*-0.6                   
                    try :
                        self.slope(ramp[id-1], coordinates, ramp[id+1])
                    except IndexError :
                        pass
                    return
    
    def slope(self, prev_point, collision_point, next_point) :        
        if next_point[1] > collision_point[1] :  
            if self.velocity_x < 0 :
                self.velocity_x = self.velocity_x * -0.8
            else :        
                self.velocity_x = self.velocity_x + (next_point[1] - collision_point[1])
        elif prev_point[1] > collision_point[1] :
            if self.velocity_x > 0 :
                self.velocity_x = self.velocity_x * -0.9
            else :
                self.velocity_x = self.velocity_x - (prev_point[1] - collision_point[1])
        else :
            self.friction()

    def check_for_finish(self) :
        if self.game.finish_line.start[0] < self.centre[0] < self.game.finish_line.start[0] + self.size :
            if self.game.finish_line.start[1] < self.centre[1] < self.game.finish_line.start[1] + self.size : self.game.finish_line.final()
            
    def reset(self) :
        self.centre = self.start
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
    
    def draw(self) :
        pygame.draw.circle(self.game.screen, 'green', self.centre, self.game.TILE_SIZE / 2)

class Finish :
    def __init__(self, game) :
        self.game = game
        self.size = game.TILE_SIZE
        self.start = (950, 200)
    
    def draw(self) :
        pygame.draw.line(self.game.screen, 'black', self.start, (self.start[0], self.start[1] + 50), 3)
        pygame.draw.line(self.game.screen, 'black', (self.start[0] + 50, self.start[1]), (self.start[0] + 50, self.start[1] + 50), 3)
        pygame.draw.line(self.game.screen, 'black', (self.start[0], self.start[1]), (self.start[0] + 50, self.start[1]), 3)
        pygame.draw.line(self.game.screen, 'black', (self.start[0], self.start[1] + 20), (self.start[0] + 50, self.start[1] + 20), 3)
        [pygame.draw.rect(self.game.screen, pygame.Color('black'), (x, self.start[1], 5, 20)) for x in range(self.start[0], self.start[0] + 50, 10)]
        
    def final(self) :
        self.game.restart_btn.restart()
        self.game.highscore.save_score()
        self.game.finish.set_screen_size()
        self.game.active_screen = "finish"

class Calculator :
    def __init__(self, game, score_coordinates) :
        self.game = game
        self.score_coordinates = score_coordinates 
        self.formulas = []
        self.ramps = []
        self.score = 0
        self.font = pygame.font.SysFont('Corbel',35)
        
    def calculate_second_point(self, y) :
        return eval(y)
    
    def calculate_ramps(self, formula) :
        ramp_coordinates = []
        for x in range(formula[1], formula[2]) :
            x_coordinate = x + 500
            y_coordinate = eval(formula[0])*(-1)+250
            if y_coordinate > 500 or y_coordinate < -500 : continue
            distance_to_ball = math.sqrt(math.pow((self.game.ball.centre[0]-x_coordinate), 2)+math.pow((self.game.ball.centre[1]-y_coordinate), 2))
            if distance_to_ball < 35 :
                return False
            ramp_coordinates.append((x_coordinate, y_coordinate))
        return ramp_coordinates          
    
    def add_ramp(self, formula) :
        new_ramp = self.calculate_ramps(formula)
        if new_ramp is False :
            self.game.formulaBox.warning_text = "Formula is too close to the ball!"
            return False
        self.formulas.append(formula)        
        self.ramps.append(new_ramp)
        self.score = self.score + len(new_ramp)
        return True
    
    def edit_ramp(self, id, formula) :
        new_ramp = self.calculate_ramps(formula)
        if new_ramp is False :
            self.game.formulaBox.warning_text = "Formula is too close to the ball!"
            return False
        self.formulas[id] = formula
        self.score = self.score - len(self.ramps[id])
        self.ramps[id] = new_ramp
        self.score = self.score + len(new_ramp)
        return True
    
    def delete_ramp(self, id) :
        self.formulas.pop(id)
        self.score = self.score - len(self.ramps[id])
        self.ramps.pop(id)
    
    def draw(self) :
        self.game.screen.blit(self.font.render('score: ' + str(self.score) , True , 'black'), (self.score_coordinates))
        for ramp in self.ramps :
            for id_c, coordinates in enumerate(ramp) :
                try :                    
                    pygame.draw.line(self.game.screen, 'blue', (coordinates[0], coordinates[1]), (ramp[id_c+1][0], ramp[id_c+1][1]), 3)
                except IndexError :
                    pass                                             

class EnterButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel',42)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Add' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 15 , self.rect.y + 5))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                if self.game.formulaBox.text != '' :
                    if len(self.game.storage.option_list) < 5:
                        formula = self.game.formulaBox.text
                        left_border = self.game.limitBox_left.text if self.game.limitBox_left.text != '' else '-500'
                        right_border = self.game.limitBox_right.text if self.game.limitBox_right.text != '' else '500'
                        if int(left_border)  < -500 : left_border = '-500' 
                        if int(right_border) > 500 : right_border = '500'
                        if int(left_border) > int(right_border) :
                            self.game.formulaBox.warning_text = "Left border can't be larger than right border!"
                            return                   
                        success = False
                        try :
                            success = self.game.calculator.add_ramp((formula, int(left_border), int(right_border)))
                        except :
                            self.game.formulaBox.warning_text = "Formula is written incorrectly!"
                            return
                        if success :
                            self.game.storage.option_list.append(formula)
                            id = len(self.game.storage.option_list) - 1
                            self.game.storage.selected = id
                            self.game.formulaBox.selected_formula(id)
                            self.game.limitBox_left.selected_formula(id)
                            self.game.limitBox_right.selected_formula(id)
                            self.game.delete_btn.current_selection = id
                            self.game.edit_btn.current_selection = id
                    else : self.game.formulaBox.warning_text = "Can't have more than 5 formulas!"
                else : self.game.formulaBox.warning_text = "Enter formula first!"
                                        
class StartButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 54)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Start' , True , self.color)
                    
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 30)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 30)
        self.game.screen.blit(self.text, (self.rect.x + 20 , self.rect.y + 5))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) : 
                self.game.formulaBox.warning_text = "" 
                self.game.paused_game = False
        
class RestartButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 28)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Restart' , True , self.color)
                    
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 25)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 25)
        self.game.screen.blit(self.text, (self.rect.x + 10 , self.rect.y + 12))
        
    def restart(self) :
        self.game.paused_game = True
        self.game.ball.reset()
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                self.game.formulaBox.warning_text = "" 
                self.restart()
                
class EditButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel',42)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Edit' , True , self.color)
        self.current_selection = 0
                    
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 15 , self.rect.y + 5))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                if self.game.formulaBox.text != '' :
                    formula = self.game.formulaBox.text
                    left_border = self.game.limitBox_left.text if self.game.limitBox_left.text != '' else '-500'
                    right_border = self.game.limitBox_right.text if self.game.limitBox_right.text != '' else '500'
                    if int(left_border)  < -500 : left_border = '-500' 
                    if int(right_border) > 500 : right_border = '500'
                    if int(left_border) > int(right_border) :
                        self.game.formulaBox.warning_text = "Left border can't be larger than right border!"
                        return
                    success = False
                    try :                     
                        success = self.game.calculator.edit_ramp(self.current_selection, (formula, int(left_border), int(right_border)))
                    except :  
                        self.game.formulaBox.warning_text = "Formula is written incorrectly!"
                        return
                    if success:
                        self.game.formulaBox.warning_text = "" 
                        self.game.storage.option_list[self.current_selection] = formula
                else : self.game.formulaBox.warning_text = "If you wish to delete the formula use the 'Delete' button"
                                       
class DeleteButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel',35)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Delete' , True , self.color)
        self.current_selection = 0
                    
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 5 , self.rect.y + 10))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                if len(self.game.storage.option_list) != 1 :
                    self.game.formulaBox.warning_text = "" 
                    self.game.storage.option_list.pop(self.current_selection)
                    self.game.calculator.delete_ramp(self.current_selection)
                    self.current_selection = 0
                    self.game.storage.selected = 0
                    self.game.formulaBox.selected_formula(0)
                    self.game.limitBox_left.selected_formula(0)
                    self.game.limitBox_right.selected_formula(0)
                else : self.game.formulaBox.warning_text = "You need to use at least 1 Formula"
                    
class BackButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 20)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Back' , True , self.color)
                    
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)
        self.game.screen.blit(self.text, (self.rect.x + 5 , self.rect.y + 15))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                self.game.menu.set_screen_size()
                self.game.active_screen = "menu"
                                                                        
class PlayButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 56)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Play' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 63 , self.rect.y + 10))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :  
                self.game.enter_game()
                
class ShowScoresButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 40)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Show scores' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 10 , self.rect.y + 20))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                self.game.go_to_scores()  

class BackToMenuButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 42)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Back' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 35 , self.rect.y + 5))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :  
                self.game.enter_menu()
        
class SaveNameButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel',42)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Enter' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 5 , self.rect.y + 5))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :  
                if self.game.namebox.text != '' :
                    self.game.enter_name()
                
class EditNameButton :
    def __init__(self, game, placement) :
        self.game = game
        self.placement = placement
        self.font = pygame.font.SysFont('Corbel', 38)
        self.rect = pygame.Rect(self.placement)
        self.color = pygame.Color('#965d52')
        self.text = self.font.render('Change name' , True , self.color)
        
    def draw(self) :
        pygame.draw.rect(self.game.screen, '#dd9b7f', self.rect, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2, 5)
        self.game.screen.blit(self.text, (self.rect.x + 5 , self.rect.y + 20))
        
    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :  
                self.game.edit_name() 
            
class ScoreBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.font = pygame.font.Font(None, 26)
        self.rect = pygame.Rect(self.placement[0], self.placement[1] - 5, self.placement[2], self.placement[3])        
        self.color = pygame.Color('#965d52')
        self.text = []
        
    def draw(self):
        pygame.draw.rect(self.game.screen, 'white', self.rect)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)
        self.txt_surface1 = self.font.render('Name', True, self.color)
        self.txt_surface2 = self.font.render('Level', True, self.color)
        self.txt_surface3 = self.font.render('Score', True, self.color)
        self.game.screen.blit(self.txt_surface1, (self.rect.x+20, self.placement[1]))
        self.game.screen.blit(self.txt_surface2, (self.rect.x+210, self.placement[1]))
        self.game.screen.blit(self.txt_surface3, (self.rect.x+335, self.placement[1]))
        for y, row in enumerate(self.text) :
            self.game.screen.blit(self.font.render(str(y + 1) + '.', True, self.color), (self.rect.x+2, y * 15 + self.placement[1] + 15))
            self.txt_surface1 = self.font.render(row[0], True, self.color)
            self.txt_surface2 = self.font.render(str(row[1]), True, self.color)
            self.txt_surface3 = self.font.render(str(row[2]), True, self.color)
            self.game.screen.blit(self.txt_surface1, (self.rect.x+20, y * 15 + self.placement[1] + 15))
            self.game.screen.blit(self.txt_surface2, (self.rect.x+210, y * 15 + self.placement[1] + 15))
            self.game.screen.blit(self.txt_surface3, (self.rect.x+335, y * 15 + self.placement[1] + 15))

class FormulaInputBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.COLOR_INACTIVE = pygame.Color('#dd9b7f')
        self.COLOR_ACTIVE = pygame.Color('#965d52')
        self.FONT = pygame.font.Font(None, 32)
        self.WARNING_FONT = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(self.placement)
        self.color = self.COLOR_INACTIVE
        self.text = ''
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.active = False
        self.warning_text = ''
        self.hint_txt_surface = self.FONT.render('f(x)=', True, self.COLOR_ACTIVE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.COLOR_ACTIVE
            else:
                self.active = False
                self.color = self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 23:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def selected_formula(self, id) :
        self.text = str(self.game.calculator.formulas[id][0])
        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self):
        self.game.screen.blit(self.hint_txt_surface, (self.rect.x-50, self.rect.y + 5))
        pygame.draw.rect(self.game.screen, 'white', self.rect)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)
        self.game.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        self.warning_txt_surface = self.WARNING_FONT.render(self.warning_text, True, 'red')
        self.game.screen.blit(self.warning_txt_surface, (self.rect.x+5, self.rect.y-20))
        
class LimitBox :
    def __init__(self, game, placement, side) :
        self.game = game
        self.placement = placement
        self.side = side
        self.COLOR_INACTIVE = pygame.Color('#da9d7f')
        self.COLOR_ACTIVE = pygame.Color('#965d52')
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(self.placement)
        self.color = self.COLOR_INACTIVE
        self.text = ''
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.active = False
        if side == 'left' :
            self.hint_txt_surface = self.FONT.render('left:', True, self.COLOR_ACTIVE)
        else :
            self.hint_txt_surface = self.FONT.render('right:', True, self.COLOR_ACTIVE)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                self.active = True
                self.color = self.COLOR_ACTIVE
            else:
                self.active = False
                self.color = self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 4:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)
                    
    def draw(self):
        if self.side == 'left' :
            self.game.screen.blit(self.hint_txt_surface, (self.rect.x-45, self.rect.y+5))
        else :
            self.game.screen.blit(self.hint_txt_surface, (self.rect.x-60, self.rect.y+5))
        pygame.draw.rect(self.game.screen, 'white', self.rect)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)
        self.game.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
    
    def selected_formula(self, id) :
        if self.side == 'left' :
            self.text = str(self.game.calculator.formulas[id][1])
        else :
            self.text = str(self.game.calculator.formulas[id][2])
        self.txt_surface = self.FONT.render(self.text, True, self.color)
                           
class NameBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.COLOR_INACTIVE = pygame.Color('#dd9b7f')
        self.COLOR_ACTIVE = pygame.Color('#965d52')
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(self.placement)
        self.color = self.COLOR_INACTIVE
        self.text = ''
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.hint_surface = self.FONT.render('Enter your name:', True, self.COLOR_ACTIVE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.COLOR_ACTIVE
            else:
                self.active = False
                self.color = self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 24:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self):
        self.game.screen.blit(self.hint_surface, ((self.rect.x+55, self.rect.y-25)))
        pygame.draw.rect(self.game.screen, 'white', self.rect)
        pygame.draw.rect(self.game.screen, self.color, self.rect, 2)
        self.game.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))                   
                    
class LevelBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.color = pygame.Color('#dd9b7f')
        self.highlight_color = (100, 200, 255)
        self.rect = pygame.Rect(self.placement)
        self.font = pygame.font.SysFont('Corbel', 30)
        
        self.selected = 0
        self.draw_menu = False
        self.menu_active = False
        self.active_option = 0
        self.option_list = ['1', '2', '3', '4', '5', '6', 'randomizer']     

    def draw(self):
        pygame.draw.rect(self.game.screen, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(self.game.screen, '#965d52', self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, '#965d52')
        self.game.screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(self.game.screen, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, '#965d52')
                self.game.screen.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(self.game.screen, '#965d52', outer_rect, 2)

    def update(self, event_list):                   
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.game.set_current_level(self.active_option)                    
                    
class ScoreLevelBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.color = pygame.Color('#dd9b7f')
        self.highlight_color = (100, 200, 255)
        self.rect = pygame.Rect(self.placement)
        self.font = pygame.font.SysFont('Corbel', 30)
        
        self.selected = 0
        self.draw_menu = False
        self.menu_active = False
        self.active_option = 0
        self.option_list = ['all', '1', '2', '3', '4', '5', '6', 'randomizer']     

    def draw(self):
        pygame.draw.rect(self.game.screen, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(self.game.screen, '#965d52', self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, '#965d52')
        self.game.screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(self.game.screen, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, '#965d52')
                self.game.screen.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(self.game.screen, '#965d52', outer_rect, 2)

    def update(self, event_list):                   
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False                   
                    self.game.sort_scores(self.active_option)
                    
class StorageBox :
    def __init__(self, game, placement):
        self.game = game
        self.placement = placement
        self.color = pygame.Color('#dd9b7f')
        self.highlight_color = (100, 200, 255)
        self.rect = pygame.Rect(self.placement)
        self.font = pygame.font.SysFont('Corbel', 30)
        
        self.selected = 0
        self.draw_menu = False
        self.menu_active = False
        self.active_option = 0
        self.option_list = []     

    def draw(self):
        pygame.draw.rect(self.game.screen, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(self.game.screen, '#965d52', self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, '#965d52')
        self.game.screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(self.game.screen, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, '#965d52')
                self.game.screen.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(self.game.screen, '#965d52', outer_rect, 2)

    def update(self, event_list):                   
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.game.formulaBox.selected_formula(self.active_option)
                    self.game.limitBox_left.selected_formula(self.active_option)
                    self.game.limitBox_right.selected_formula(self.active_option)
                    self.game.edit_btn.current_selection = self.active_option
                    self.game.delete_btn.current_selection = self.active_option                    
                                    