import time
import threading

from pygame import mixer


class StoppableThread(threading.Thread):

    def __init__(self, target, args):
        super(StoppableThread, self).__init__(target=target, args=args)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Item:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class Barrier(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "barrier")


class Wall(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "wall")


class Door(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "door")


class Fire(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fire")


class Player(Item):
    def __init__(self):
        super().__init__(1, 1, "player")
        self.bombsCount = 1
        self.bombsLeft = 1
        self.fireRange = 1
        self.score = 0
        self.remoteControl = False

    def has_bomb(self):
        return self.bombsLeft > 0


class Bomb(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "bomb")
        self.fires = []
        self.thread = None

    def detonate(self, new_game, wait, remotely):
        self.thread = StoppableThread(target=self.explode, args=(new_game, wait, remotely,))
        self.thread.start()

    def explode(self, new_game, wait, remotely):
        if wait:
            time.sleep(1)
        if self in new_game.activeBombs:
            if not remotely:
                new_game.activeBombs.remove(self)
                new_game.player.bombsLeft += 1
            stop_left = [False]
            stop_right = [False]
            stop_up = [False]
            stop_down = [False]
            fire = Fire(self.x, self.y)
            new_game.items[self.x][self.y] = fire
            self.fires.append(fire)
            new_game.window.screen.blit(new_game.window.images[fire.name],
                                        new_game.window.pygame.Rect((self.y + 1) * new_game.window.sqSize + 20,
                                                                    (self.x + 1) * new_game.window.sqSize + 20,
                                                                    new_game.window.sqSize, new_game.window.sqSize))
            if new_game.player.x == self.x and new_game.player.y == self.y:
                new_game.window.running = False
            for k in range(1, new_game.player.fireRange + 1, 1):
                self.fire_up(new_game, stop_up, self.x, self.y - k, remotely)
                self.fire_up(new_game, stop_left, self.x - k, self.y, remotely)
                self.fire_up(new_game, stop_right, self.x + k, self.y, remotely)
                self.fire_up(new_game, stop_down, self.x, self.y + k, remotely)
            mixer.Sound("resources/explosion.wav").play()
            time.sleep(0.5)
            for fire in self.fires:
                new_game.items[fire.x][fire.y] = None
            self.fires = []

    def fire_up(self, new_game, stop, i, j, remotely):
        if not stop[0]:
            if new_game.player.x == i and new_game.player.y == j:
                new_game.window.running = False
            elif new_game.items[i][j] is None and new_game.enemies[i][j] is None:
                fire = Fire(i, j)
                self.fires.append(fire)
                new_game.items[i][j] = fire
                new_game.window.screen.blit(new_game.window.images[fire.name],
                                            new_game.window.pygame.Rect((j + 1) * new_game.window.sqSize + 20,
                                                                        (i + 1) * new_game.window.sqSize + 20,
                                                                        new_game.window.sqSize, new_game.window.sqSize))
            elif new_game.enemies[i][j] is not None:
                enemy = new_game.enemies[i][j]
                enemy.destroy_me(new_game)
                if new_game.items[i][j] is not None and isinstance(new_game.items[i][j], Wall):
                    new_game.items[i][j] = None
                    stop[0] = True
                    new_game.player.score += 10
                fire = Fire(i, j)
                self.fires.append(fire)
                new_game.items[i][j] = fire
                new_game.window.screen.blit(new_game.window.images[fire.name],
                                            new_game.window.pygame.Rect((j + 1) * new_game.window.sqSize + 20,
                                                                        (i + 1) * new_game.window.sqSize + 20,
                                                                        new_game.window.sqSize, new_game.window.sqSize))
            elif isinstance(new_game.items[i][j], Wall):
                new_game.items[i][j] = None
                stop[0] = True
                new_game.player.score += 10
            elif isinstance(new_game.items[i][j], Barrier):
                stop[0] = True
            elif isinstance(new_game.items[i][j], Bomb):
                bomb = new_game.items[i][j]
                bomb.destroy_me(new_game)
                bomb.detonate(new_game, False, remotely)

    def destroy_me(self, new_game):
        if self.thread is not None:
            self.thread.stop()
            for fire in self.fires:
                new_game.items[fire.x][fire.y] = None
            self.fires = []


class FireRange(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fr")


class BombUp(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "bu")


class BombRemoteControl(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "brc")
