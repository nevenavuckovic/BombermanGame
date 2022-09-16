from Level import *
import random
import threading
import time
import _thread


stopThis = False


class MyThread(threading.Thread):
    pass


class Item:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.bombsCount = 1
        self.bombsLeft = 1
        self.fireRange = 1
        self.score = 0
        self.remoteControl = False

    def has_bomb(self):
        return self.bombsLeft > 0


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fires = []
        self.thread = None

    def detonate(self, new_game, wait, remotely):
        self.thread = _thread.start_new_thread(self.explode, (new_game, wait, remotely))

    def explode(self, new_game, wait, remotely):
        if wait:
            time.sleep(1)
        if not remotely:
            new_game.activeBombs.remove(self)
            new_game.player.bombsLeft += 1

        # newGame.GameWindow.Dispatcher.Invoke(() =>

        stop_left = [False]
        stop_right = [False]
        stop_up = [False]
        stop_down = [False]
        # newGame.GameWindow.LevelMap.Children.Remove(Image);
        fire = Item(self.x, self.y, "fire")
        new_game.items[self.x][self.y] = fire.name
        self.fires.append(fire)
        # new_ame.GameWindow.LevelMap.Children.Add(fire.Image)
        if new_game.player.x == self.x and new_game.player.y == self.y:
            new_game.window.running = False

        for k in range(1, new_game.player.fireRange + 1, 1):
            self.fire_up(new_game, stop_up, self.x, self.y - k, remotely)
            self.fire_up(new_game, stop_left, self.x - k, self.y, remotely)
            self.fire_up(new_game, stop_right, self.x + k, self.y, remotely)
            self.fire_up(new_game, stop_down, self.x, self.y + k, remotely)

        time.sleep(0.5)
        # newGame.GameWindow.Dispatcher.Invoke(() =>
        for fire in self.fires:
            new_game.items[fire.x][fire.y] = ""
            # new_game.GameWindow.LevelMap.Children.Remove(fire.Image)
        self.fires = []

    def fire_up(self, new_game, stop, i, j, remotely):
        if not stop[0]:
            if new_game.player.x == i and new_game.player.y == j:
                new_game.window.running = False
            elif new_game.items[i][j] == "" and new_game.enemies[i][j] == "":
                fire = Item(i, j, "fire")
                self.fires.append(fire)
                new_game.items[i][j] = fire.name
                # newGame.GameWindow.LevelMap.Children.Add(fire.Image);
            elif new_game.enemies[i][j] != "":
                enemy = new_game.enemies[i][j]
                # enemy.DestroyMe(new_game, True)
                # new_game.GameWindow.ScoreLabel.Content = "Score: " + newGame.Player.Score;
                if new_game.items[i][j] != "" and new_game.Items[i][j] != "w":
                    # new_game.GameWindow.LevelMap.Children.Remove(newGame.Items[i, j].Image);
                    new_game.items[i][j] = ""
                    stop[0] = True
                    new_game.player.score += 10
                    # newGame.GameWindow.ScoreLabel.Content = "Score: " + newGame.Player.Score;

                fire = Item(i, j, "fire")
                self.fires.append(fire)
                new_game.items[i][j] = fire.name
                # new_game.GameWindow.LevelMap.Children.Add(fire.Image)
            elif new_game.items[i][j] == "w":
                # new_game.GameWindow.LevelMap.Children.Remove(newGame.Items[i, j].Image);
                new_game.items[i][j] = ""
                stop[0] = True
                new_game.player.score += 10
                # newGame.GameWindow.ScoreLabel.Content = "Score: " + newGame.Player.Score;

            elif new_game.items[i][j] == "b":
                stop[0] = True
            elif new_game.items[i][j] == "bomb":
                bomb = new_game.items[i][j]
                bomb.destroy_me(new_game)
                bomb.detonate(new_game, False, remotely)

    def destroy_me(self, new_game):
        if self.thread is not None:
            self.thread.exit()
            for fire in self.fires:
                new_game.items[fire.x][fire.y] = ""
                # newGame.GameWindow.LevelMap.Children.Remove(fire.Image);
            self.fires = []


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
        self.items = levels[self.level]
        self.enemies = enemies[self.level]
        self.activeBombs = []
        self.load_level(self.level)

    def load_powers(self, level):
        i = random.randint(0, self.window.rows - 1)
        j = random.randint(0, self.window.columns - 1)
        while self.items[i][j] != "w":
            i = random.randint(0, self.window.rows - 1)
            j = random.randint(0, self.window.columns - 1)
        if level == 1:
            fr = Item(i, j, "fr")
            self.power = fr
        elif level == 2:
            fr = Item(i, j, "bu")
            self.power = fr
        elif level == 3:
            fr = Item(i, j, "brc")
            self.power = fr
        elif level == 4:
            fr = Item(i, j, "bu")
            self.power = fr
        elif level == 5:
            fr = Item(i, j, "fr")
            self.power = fr

        i = random.randint(0, self.window.rows - 1)
        j = random.randint(0, self.window.columns - 1)
        while self.items[i][j] != "w" or (i == self.power.x and j == self.power.y):
            i = random.randint(0, self.window.rows - 1)
            j = random.randint(0, self.window.columns - 1)
        self.door = Item(i, j, "door")

    def start_time(self):
        while self.gameTime > 0:
            time.sleep(1)
            self.gameTime -= 1
            # GameWindow.TimeLabel.Content = "Time: " + time;
        self.window.running = False

    def load_level(self, level):
        if self.timeThread is not None:
            self.timeThread.exit()
        if level < 6:
            if self.activeBombs is not None:
                for bomb in self.activeBombs:
                    bomb.DestroyMe(self)

            self.power = None
            self.door = None
            # GameWindow.LevelLabel.Content = "Level: " + level;
            self.gameTime = 250 + (level - 1) * 50
            # GameWindow.TimeLabel.Content = "Time: " + time;
            self.items = levels[level]
            self.activeBombs = []
            self.enemies = enemies[level]
            self.load_powers(level)
            self.player.x = 1
            self.player.y = 1
            self.player.bombsLeft = self.player.bombsCount
            self.timeThread = _thread.start_new_thread(self.start_time, ())
            # self.timeThread.Start();
        else:
            self.window.running = False

    def move_bomberman(self, i, j):
        if self.items[i][j] == "":
            self.player.x = i
            self.player.y = j
            if i == self.door.x and j == self.door.y:
                all_killed = True
                for n in range(0, self.window.rows, 1):
                    for m in range(0, self.window.columns, 1):
                        if self.enemies[n][m] != "":
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
            elif self.enemies[i][j] != "":
                self.window.running = False
        elif self.items[i][j] == "fire":
            self.window.running = False

    def place_bomb(self, i, j):
        if self.player.has_bomb():
            if self.items[i][j] == "":
                bomb = Bomb(i, j)
                self.activeBombs.append(bomb)
                self.items[i][j] = bomb
                self.player.bombsLeft -= 1
                # GameWindow.LevelMap.Children.Add(bomb.Image);
                if not self.player.remoteControl:
                    bomb.detonate(self, True, False)

    def bombs_explode(self):
        if self.player.remoteControl and len(self.activeBombs) > 0:
            for bomb in self.activeBombs:
                bomb.detonate(self, False, True)
            self.player.bombsLeft += len(self.activeBombs)
            self.activeBombs = []
