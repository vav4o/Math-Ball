import sqlite3

class HighscoreManager :
    def __init__(self, game) :
        self.game = game
        self.name = ''
        
        sqlite3.connect('highscores.db')
        self.conn = sqlite3.connect('highscores.db')
        self.curs = self.conn.cursor()
        
        self.curs.execute('''
            CREATE TABLE if not exists Highscores
            ([Name] TEXT, [Level] INTEGER, [Score] INTEGER);            
            ''')
        
    def save_score(self) :
        if self.game.current_level != 'randomize' : self.game.current_level = self.game.current_level + 1
        self.curs.execute('Insert into Highscores(Name, Level, Score) values (?, ?, ?)', (self.name, str(self.game.current_level), self.game.calculator.score))
        self.conn.commit()
        self.show_scores()
        
    def show_scores(self) :
        scores = self.curs.execute('SELECT * FROM Highscores ORDER BY Score LIMIT 35').fetchall()
        self.game.finish.score_box.text = scores
        
    def show_per_level(self, level) :
        if level == 0 :
            self.show_scores()
        elif level == 7 :
            scores = self.curs.execute('SELECT * FROM Highscores WHERE Level = "randomize" ORDER BY Score LIMIT 35',).fetchall()
            self.game.finish.score_box.text = scores
        else :
            scores = self.curs.execute('SELECT * FROM Highscores WHERE Level = ? ORDER BY Score LIMIT 35',(str(level))).fetchall()
            self.game.finish.score_box.text = scores
            