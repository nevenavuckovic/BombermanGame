from Items import *
import Levels
import Enemies
import random
import time
import _thread


class NewGame:

    def __init__(self, window):
        self.window = window
        self.level = 1
        self.gameTime = 0
        self.timeThread = None
        self.power = None
        self.door = None
        self.finished = False
        self.player = Player()
        self.items = Levels.levels[self.level]
        self.enemies = Levels.enemies[self.level]
        self.activeBombs = []
        self.load_level(self.level)

    def load_powers(self, level):
        i = random.randint(0, self.window.rows - 1)
        j = random.randint(0, self.window.columns - 1)
        while not isinstance(self.items[i][j], Wall):
            i = random.randint(0, self.window.rows - 1)
            j = random.randint(0, self.window.columns - 1)
        if level == 1:
            p = FireRange(i, j)
            self.power = p
        elif level == 2:
            p = BombUp(i, j)
            self.power = p
        elif level == 3:
            p = BombRemoteControl(i, j)
            self.power = p
        elif level == 4:
            p = BombUp(i, j)
            self.power = p
        elif level == 5:
            p = FireRange(i, j)
            self.power = p

        i = random.randint(0, self.window.rows - 1)
        j = random.randint(0, self.window.columns - 1)
        while not isinstance(self.items[i][j], Wall) or (i == self.power.x and j == self.power.y):
            i = random.randint(0, self.window.rows - 1)
            j = random.randint(0, self.window.columns - 1)
        self.door = Door(i, j)

    def start_time(self):
        while self.gameTime > 0:
            time.sleep(1)
            self.gameTime -= 1
            # GameWindow.TimeLabel.Content = "Time: " + time;
        self.window.running = False

    def load_level(self, level):
        #if self.timeThread is not None:
            #self.timeThread.exit()
        if level < 6:
            if self.activeBombs is not None:
                for bomb in self.activeBombs:
                    bomb.destroy_me(self)

            self.power = None
            self.door = None
            # GameWindow.LevelLabel.Content = "Level: " + level;
            self.gameTime = 250 + (level - 1) * 50
            # GameWindow.TimeLabel.Content = "Time: " + time;
            self.items = Levels.levels[level]
            self.activeBombs = []
            self.enemies = Levels.enemies[level]
            self.player.x = 1
            self.player.y = 1
            self.window.screen.blit(self.window.images[self.player.name],
                                    self.window.pygame.Rect((self.player.y + 1) * self.window.sqSize + 20,
                                                            (self.player.x + 1) * self.window.sqSize + 20,
                                                            self.window.sqSize, self.window.sqSize))

            self.player.bombsLeft = self.player.bombsCount
            self.timeThread = _thread.start_new_thread(self.start_time, ())
            for r in range(self.window.rows):
                for c in range(self.window.columns):
                    item = self.items[r][c]
                    if item == "":
                        self.items[r][c] = None
                    if item != "":
                        if item == "b":
                            barrier = Barrier(r, c)
                            self.items[r][c] = barrier
                            self.window.screen.blit(self.window.images[barrier.name],
                                                    self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                            (r + 1) * self.window.sqSize + 20,
                                                                            self.window.sqSize, self.window.sqSize))
                        elif item == "w":
                            wall = Wall(r, c)
                            self.items[r][c] = wall
                            self.window.screen.blit(self.window.images[wall.name],
                                                    self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                            (r + 1) * self.window.sqSize + 20,
                                                                            self.window.sqSize, self.window.sqSize))
                    if self.enemies[r][c] == "":
                        self.enemies[r][c] = None
                    elif self.enemies[r][c] == "1":
                        enemy = Enemies.Ballom(r, c)
                        self.enemies[r][c] = enemy
                        self.window.screen.blit(self.window.images[enemy.name],
                                                self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                        (r + 1) * self.window.sqSize + 20,
                                                                        self.window.sqSize, self.window.sqSize))
                        enemy.start_moving(self)
                    elif self.enemies[r][c] == "2":
                        enemy = Enemies.Onil(r, c)
                        self.enemies[r][c] = enemy
                        self.window.screen.blit(self.window.images[enemy.name],
                                                self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                        (r + 1) * self.window.sqSize + 20,
                                                                        self.window.sqSize, self.window.sqSize))
                        enemy.start_moving(self)
                    elif self.enemies[r][c] == "3":
                        enemy = Enemies.Pontan(r, c)
                        self.enemies[r][c] = enemy
                        self.window.screen.blit(self.window.images[enemy.name],
                                                self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                        (r + 1) * self.window.sqSize + 20,
                                                                        self.window.sqSize, self.window.sqSize))
                        enemy.start_moving(self)
                    elif self.enemies[r][c] == "4":
                        enemy = Enemies.Ovape(r, c)
                        self.enemies[r][c] = enemy
                        self.window.screen.blit(self.window.images[enemy.name],
                                                self.window.pygame.Rect((c + 1) * self.window.sqSize + 20,
                                                                        (r + 1) * self.window.sqSize + 20,
                                                                        self.window.sqSize, self.window.sqSize))
                        enemy.start_moving(self)
            self.load_powers(level)
        else:
            self.window.running = False

    def move_bomberman(self, i, j):
        if self.items[i][j] is None:
            self.player.x = i
            self.player.y = j
            self.window.screen.blit(self.window.images[self.player.name],
                                    self.window.pygame.Rect((j + 1) * self.window.sqSize + 20,
                                                            (i + 1) * self.window.sqSize + 20,
                                                            self.window.sqSize, self.window.sqSize))

            if i == self.door.x and j == self.door.y:
                all_killed = True
                for n in range(0, self.window.rows, 1):
                    for m in range(0, self.window.columns, 1):
                        if self.enemies[n][m] is not None:
                            all_killed = False
                            break
                if all_killed:
                    self.level += 1
                    self.player.score += self.gameTime * 10
                # GameWindow.ScoreLabel.Content = "Score: " + Player.Score;
                    self.load_level(self.level)
            elif self.power is not None and (i == self.power.x and j == self.power.y):
                if self.power.name == "bcr":
                    self.player.remoteControl = True
                elif self.power.name == "bu":
                    self.player.bombsCount += 1
                    self.player.bombsLeft += 1
                elif self.power.name == "fr":
                    self.player.fireRange += 1
                self.player.score += 500
                # GameWindow.ScoreLabel.Content = "Score: " + Player.Score;
                # GameWindow.LevelMap.Children.Remove(power.Image);
                self.power = None
            elif self.enemies[i][j] is not None:
                self.window.running = False
        elif isinstance(self.items[i][j], Fire):
            self.window.running = False

    def place_bomb(self, i, j):
        if self.player.has_bomb():
            if self.items[i][j] is None:
                bomb = Bomb(i, j)
                self.activeBombs.append(bomb)
                self.items[i][j] = bomb
                self.player.bombsLeft -= 1
                self.window.screen.blit(self.window.images[bomb.name],
                                        self.window.pygame.Rect((j + 1) * self.window.sqSize + 20,
                                                                (i + 1) * self.window.sqSize + 20,
                                                                self.window.sqSize, self.window.sqSize))
                if not self.player.remoteControl:
                    bomb.detonate(self, True, False)

    def bombs_explode(self):
        if self.player.remoteControl and len(self.activeBombs) > 0:
            for bomb in self.activeBombs:
                bomb.detonate(self, False, True)
            self.player.bombsLeft += len(self.activeBombs)
            self.activeBombs = []
