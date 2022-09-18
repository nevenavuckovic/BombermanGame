import pygame
from Game import *


class Window:
    def __init__(self):
        self.pygame = pygame
        self.width = 1200
        self.height = 600
        self.rows = 13
        self.columns = 27
        self.sqSize = 40
        self.images = {}
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        icon = pygame.image.load("resources/bomberman.png")
        pygame.display.set_caption("Bomberman")
        pygame.display.set_icon(icon)
        self.load_images()
        self.game = NewGame(self)

    def load_images(self):
        self.images["ballom"] = pygame.transform.scale(pygame.image.load("resources/ballom.png"), (self.sqSize, self.sqSize))
        self.images["barrier"] = pygame.transform.scale(pygame.image.load("resources/barrier.png"), (self.sqSize, self.sqSize))
        self.images["bomb"] = pygame.transform.scale(pygame.image.load("resources/bomb.jpg"), (self.sqSize, self.sqSize))
        self.images["player"] = pygame.transform.scale(pygame.image.load("resources/player.png"), (self.sqSize, self.sqSize))
        self.images["door"] = pygame.transform.scale(pygame.image.load("resources/door.png"), (self.sqSize, self.sqSize))
        self.images["fire"] = pygame.transform.scale(pygame.image.load("resources/fire.png"), (self.sqSize, self.sqSize))
        self.images["onil"] = pygame.transform.scale(pygame.image.load("resources/onil.png"), (self.sqSize, self.sqSize))
        self.images["ovape"] = pygame.transform.scale(pygame.image.load("resources/ovape.gif"), (self.sqSize, self.sqSize))
        self.images["pontan"] = pygame.transform.scale(pygame.image.load("resources/pontan.gif"), (self.sqSize, self.sqSize))
        self.images["brc"] = pygame.transform.scale(pygame.image.load("resources/rc.png"), (self.sqSize, self.sqSize))
        self.images["bu"] = pygame.transform.scale(pygame.image.load("resources/bu.png"), (self.sqSize, self.sqSize))
        self.images["fr"] = pygame.transform.scale(pygame.image.load("resources/fr.png"), (self.sqSize, self.sqSize))
        self.images["wall"] = pygame.transform.scale(pygame.image.load("resources/wall.png"), (self.sqSize, self.sqSize))

    def write_text(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text, text_rect)

    def draw_fields(self):
        i = self.game.items
        e = self.game.enemies
        p = self.game.player
        for r in range(self.rows):
            for c in range(self.columns):
                item = i[r][c]
                enemy = e[r][c]
                if item is not None:
                    self.screen.blit(self.images[item.name], pygame.Rect((c+1)*self.sqSize+20, (r+1)*self.sqSize+20, self.sqSize, self.sqSize))
                if enemy is not None:
                    self.screen.blit(self.images[enemy.name], pygame.Rect((c+1)*self.sqSize+20, (r+1)*self.sqSize+20, self.sqSize, self.sqSize))
        self.screen.blit(self.images["player"], pygame.Rect((p.y + 1) * self.sqSize + 20, (p.x + 1) * self.sqSize + 20, self.sqSize, self.sqSize))
        door = self.game.door
        if i[door.x][door.y] is None:
            self.screen.blit(self.images[door.name], pygame.Rect((door.y + 1) * self.sqSize + 20, (door.x + 1) * self.sqSize + 20, self.sqSize, self.sqSize))
        power = self.game.power
        if self.game.power is not None and i[power.x][power.y] is None:
            self.screen.blit(self.images[power.name], pygame.Rect((power.y + 1) * self.sqSize + 20, (power.x + 1) * self.sqSize + 20, self.sqSize, self.sqSize))


def main():
    pygame.init()
    window = Window()
    while window.running:
        i = window.game.player.x
        j = window.game.player.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    window.game.move_bomberman(i, j - 1)
                if event.key == pygame.K_RIGHT:
                    window.game.move_bomberman(i, j + 1)
                if event.key == pygame.K_UP:
                    window.game.move_bomberman(i - 1, j)
                if event.key == pygame.K_DOWN:
                    window.game.move_bomberman(i + 1, j)
                if event.key == pygame.K_b:
                    window.game.place_bomb(i, j)
                if event.key == pygame.K_SPACE:
                    window.game.bombs_explode()

        window.screen.fill((255, 255, 255))
        window.draw_fields()
        window.write_text( "Score: " + str(window.game.player.score), 140, 30)
        window.write_text( "Time: " + str(window.game.gameTime), 1050, 30)
        pygame.display.update()

    window.screen = pygame.display.set_mode((300, 300))
    window.running = True
    while window.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.running = False

        window.screen.fill((255, 255, 255))
        window.write_text("Your score is: " + str(window.game.player.score), 300/2, 300/2)
        pygame.display.update()


if __name__ == "__main__":
    main()
