import _thread
import random
import time

from Items import *


class Enemy(object):

    def __init__(self, x, y, name):
        self.points = 0
        self.set_points()
        self.alive = True
        self.x = x
        self.y = y
        self.name = name
        self.thread = None

    def start_moving(self, new_game):
        self.thread = _thread.start_new_thread(self.move, (new_game,))

    def move(self, new_game):
        pass

    def set_points(self):
        pass

    def destroy_me(self, new_game):
        self.alive = False
        # self.thread._stop.set()
        new_game.player.score += self.points
        new_game.enemies[self.x][self.y] = None
        # new_game.GameWindow.LevelMap.Children.Remove(Image);


class Ballom(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y, "ballom")

    def move(self, new_game):
        rand = random.randint(0, 20)
        direction = 1 if (rand % 2 == 0) else -1

        while self.alive:
            time.sleep(1)

            new_game.enemies[self.x][self.y] = None
            item = new_game.items[self.x][self.y + direction]
            enemy = new_game.enemies[self.x][self.y + direction]

            game_over = False
            kill_me = False
            if item is not None and item.name == "fire":
                kill_me = True
                self.y += direction
            elif item is not None or enemy is not None:
                direction = -direction
            elif new_game.player.x == self.x and new_game.player.y == self.y + direction:
                game_over = True
                self.y += direction
            elif item is None and enemy is None:
                self.y += direction

            new_game.enemies[self.x][self.y] = self
            new_game.window.screen.blit(new_game.window.images[self.name],
                                        new_game.window.pygame.Rect((self.y + 1) * new_game.window.sqSize + 20,
                                                                    (self.x + 1) * new_game.window.sqSize + 20,
                                                                    new_game.window.sqSize, new_game.window.sqSize))

            if game_over:
                new_game.window.running = False
            if kill_me:
                self.destroy_me(new_game)

    def set_points(self):
        self.points = 100


class Onil(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y, "onil")

    def set_points(self):
        self.points = 300

    def move(self, new_game):
        while self.alive:
            time.sleep(0.55)
            new_game.enemies[self.x][self.y] = None
            items = new_game.items
            enemies = new_game.enemies
            player = new_game.player
            available_positions = []
            if enemies[self.x + 1][self.y] is None and (items[self.x + 1][self.y] is None
                                                        or isinstance(items[self.x + 1][self.y], Fire)):
                available_positions.append([self.x + 1, self.y])
            if enemies[self.x - 1][self.y] is None and (items[self.x - 1][self.y]  is None
                                                        or isinstance(items[self.x - 1][self.y] , Fire)):
                available_positions.append([self.x - 1, self.y])
            if enemies[self.x][self.y + 1] is None and (items[self.x][self.y + 1] is None
                                                        or isinstance(items[self.x][self.y + 1], Fire)):
                available_positions.append([self.x, self.y + 1])
            if enemies[self.x][self.y - 1] is None and (items[self.x][self.y - 1] is None
                                                        or isinstance(items[self.x][self.y - 1], Fire)):
                available_positions.append([self.x, self.y - 1])

            size = len(available_positions)
            if size > 0:
                rand = random.randint(0, 100)
                self.x = available_positions[rand % size][0]
                self.y = available_positions[rand % size][1]
            new_game.enemies[self.x][self.y] = self
            new_game.window.screen.blit(new_game.window.images[self.name],
                                        new_game.window.pygame.Rect((self.y + 1) * new_game.window.sqSize + 20,
                                                                    (self.x + 1) * new_game.window.sqSize + 20,
                                                                    new_game.window.sqSize, new_game.window.sqSize))

            if player.x == self.x and player.y == self.y:
                new_game.window.running = False
            if items[self.x][self.y] is not None and isinstance(items[self.x][self.y], Fire):
                self.destroy_me(new_game)


class Ovape(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y, "ovape")

    def set_points(self):
        self.points = 1000

    def move(self, new_game):
        while self.alive:
            time.sleep(0.7)
            new_game.enemies[self.x][self.y] = None
            items = new_game.items
            enemies = new_game.enemies
            player = new_game.player
            available_positions = []
            if enemies[self.x + 1][self.y] is None and (items[self.x + 1][self.y] is None
                                                        or isinstance(items[self.x + 1][self.y], Fire)
                                                        or isinstance(items[self.x + 1][self.y], Wall)
                                                        and not isinstance(items[self.x + 1][self.y], Bomb)):
                available_positions.append([self.x + 1, self.y])
            if enemies[self.x - 1][self.y] is None and (items[self.x - 1][self.y] is None
                                                        or isinstance(items[self.x - 1][self.y], Fire)
                                                        or isinstance(items[self.x - 1][self.y], Wall)
                                                        and not isinstance(items[self.x - 1][self.y], Bomb)):
                available_positions.append([self.x - 1, self.y])
            if enemies[self.x][self.y + 1] is None and (items[self.x][self.y + 1] is None
                                                        or isinstance(items[self.x][self.y + 1], Fire)
                                                        or isinstance(items[self.x][self.y + 1], Wall)
                                                        and not isinstance(items[self.x][self.y + 1], Bomb)):
                available_positions.append([self.x, self.y + 1])
            if enemies[self.x][self.y - 1] is None and (items[self.x][self.y - 1] is None
                                                        or isinstance(items[self.x][self.y - 1], Fire)
                                                        or isinstance(items[self.x][self.y - 1], Wall)
                                                        and not isinstance(items[self.x][self.y - 1], Bomb)):
                available_positions.append([self.x, self.y - 1])

            size = len(available_positions)
            if size > 0:
                rand = random.randint(0, 100)
                self.x = available_positions[rand % size][0]
                self.y = available_positions[rand % size][1]
            new_game.enemies[self.x][self.y] = self
            new_game.window.screen.blit(new_game.window.images[self.name],
                                        new_game.window.pygame.Rect((self.y + 1) * new_game.window.sqSize + 20,
                                                                    (self.x + 1) * new_game.window.sqSize + 20,
                                                                    new_game.window.sqSize, new_game.window.sqSize))

            if player.x == self.x and player.y == self.y:
                new_game.window.running = False
            if items[self.x][self.y] is not None and isinstance(items[self.x][self.y], Fire):
                self.destroy_me(new_game)


class Pontan(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y, "pontan")

    def set_points(self):
        self.points = 1500

    def move(self, new_game):
        while self.alive:
            time.sleep(0.4)
            new_game.enemies[self.x][self.y] = None
            items = new_game.items
            enemies = new_game.enemies
            player = new_game.player
            available_positions = []
            if enemies[self.x + 1][self.y] is None and (items[self.x + 1][self.y] is None
                                                        or isinstance(items[self.x + 1][self.y], Fire)
                                                        or isinstance(items[self.x + 1][self.y], Wall)
                                                        and not isinstance(items[self.x + 1][self.y], Bomb)):
                available_positions.append([self.x + 1, self.y])
            if enemies[self.x - 1][self.y] is None and (items[self.x - 1][self.y] is None
                                                        or isinstance(items[self.x - 1][self.y], Fire)
                                                        or isinstance(items[self.x - 1][self.y], Wall)
                                                        and not isinstance(items[self.x - 1][self.y], Bomb)):
                available_positions.append([self.x - 1, self.y])
            if enemies[self.x][self.y + 1] is None and (items[self.x][self.y + 1] is None
                                                        or isinstance(items[self.x][self.y + 1], Fire)
                                                        or isinstance(items[self.x][self.y + 1], Wall)
                                                        and not isinstance(items[self.x][self.y + 1], Bomb)):
                available_positions.append([self.x, self.y + 1])
            if enemies[self.x][self.y - 1] is None and (items[self.x][self.y - 1] is None
                                                        or isinstance(items[self.x][self.y - 1], Fire)
                                                        or isinstance(items[self.x][self.y - 1], Wall)
                                                        and not isinstance(items[self.x][self.y - 1], Bomb)):
                available_positions.append([self.x, self.y - 1])

            size = len(available_positions)
            if size > 0:
                rand = random.randint(0, 100)
                self.x = available_positions[rand % size][0]
                self.y = available_positions[rand % size][1]
            new_game.enemies[self.x][self.y] = self
            new_game.window.screen.blit(new_game.window.images[self.name],
                                        new_game.window.pygame.Rect((self.y + 1) * new_game.window.sqSize + 20,
                                                                    (self.x + 1) * new_game.window.sqSize + 20,
                                                                    new_game.window.sqSize, new_game.window.sqSize))

            if player.x == self.x and player.y == self.y:
                new_game.window.running = False
            if items[self.x][self.y] is not None and isinstance(items[self.x][self.y], Fire):
                self.destroy_me(new_game)


