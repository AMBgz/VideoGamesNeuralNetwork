import pygame
import random, sys
from Entity import *
from math import sqrt

class Player(Entity):

    def __init__(self, x, y, w, h, energy):
        super().__init__(x, y, w, h)
        self.energy = energy

    def move(self, dx, dy, speed):
        if dx != 0 and dy != 0:
            self.x += dx * speed * 0.90
            self.y += dy * speed * 0.90
        else:
            self.x += dx * speed
            self.y += dy * speed
        self.x, self.y = int(self.x), int(self.y)
    
class Asteroid(Entity):

    def __init__(self, x, y, w, h, direction):
        super().__init__(x, y, w, h)
        self.direction = direction
    
    def move(self, speedr):
        # circle equation : x**2 + y**2 = r
        if (self.direction[0]**2 + self.direction[1]**2) == 0:
            return
        alpha = sqrt(speedr/(self.direction[0]**2 + self.direction[1]**2))
        x = alpha*self.direction[0]
        y = alpha*self.direction[1]
        self.x += x
        self.y += y
        

class DodgeGame:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.gameover = False
        self.player = self.make_player()
        self.time = 0
        self.asteroids = []
        self.limit_asteroids = 7
        while len(self.asteroids) < self.limit_asteroids:
            self.add_asteroid()

    def get_first_input(self, direction):
        dx, dy = direction
        x, y = self.player.get_center()
        seg = Segment(x, y, x+dx, y+dy)
        # init min
        distance = float('inf')
        next = None
        for asteroid in self.asteroids:
            if asteroid.lineInRectangle(seg):
                if next == None:
                    next = asteroid
                    distance = self.player.get_distance(asteroid)
                else:
                    d = self.player.get_distance(asteroid)
                    if d < distance:
                        next = asteroid
                        distance = d

        return next, distance




    def reset(self):
        self.gameover = False
        self.player = self.make_player()
        self.time = 0
        self.asteroids = []
        while len(self.asteroids) < self.limit_asteroids:
            self.add_asteroid()
    
    def make_player(self):
        x = int(self.width/2)
        y = int(self.height/2)
        w = 30
        h = 30
        energy = 100
        return Player(x - w/2, y - h/2, w, h, energy)



    def get_score(self):
        return self.time


    def get_input_closer(self, k = 1):
        l = [[float('inf'), None, None, None] for _ in range(k)]
        s = set()
        for i in range(k):
            for ast in self.asteroids:
                d = ast.get_distance(self.player)
                if d < l[i][0] and not ast in s:
                    l[i][0] = d
                    l[i][1] = ast
                    l[i][2] = ast.x - self.player.x
                    l[i][3] = ast.y - self.player.y
            s.add(l[i][1])
        return [[e[2], e[3]] for e in l]
        

    def add_asteroid(self):
        w = h = 20 # taille de l'asteroid
        # cote ou apparait l'asteroid
        side = random.randint(0,3)
        # left or right side
        if side == 0 or side == 1:
            y = random.randint(0, self.height - h)
            if side == 0:
                x = 0
            else:
                x = self.width - w
        # up or down
        else:
            x = random.randint(0, self.width - w)
            if side == 2:
                y = 0
            else:
                y = self.height - h

        # direction 
        radius = 60
        px = random.randint(self.player.x - radius, self.player.x + self.player.width + radius) # rayon autour du personnage
        py = random.randint(self.player.y - radius, self.player.y + self.player.height + radius)
        direction = (px - x, py - y)
        self.asteroids.append(Asteroid(x, y, w, h, direction))

    def in_screen(self, entity):
        return entity.x + entity.width >= 0 and entity.x  <= self.width and entity.y + entity.height >= 0 and entity.y <= self.height

    def next_state(self):
        self.time += 0.1
        while len(self.asteroids) < self.limit_asteroids:
            self.add_asteroid()
        
        speed_radius = 2.5
        for ast in self.asteroids:
            ast.move(speed_radius)
            # check collision
            if self.player.check_collision(ast):
                self.player.energy -= 30
        
        # remove asteroid if outside screen or collision
        self.asteroids = [ast for ast in self.asteroids if (self.in_screen(ast) and not self.player.check_collision(ast))]

        if self.player.energy <= 0:
            self.gameover = True


    def player_action(self, dx, dy):
        self.player.move(dx, dy, 5)
        self.player.clip(0, 0, self.width, self.height)


class DodgeInterface:

    def __init__(self, width, height, game, screen):
        self.width = width
        self.height = height
        self.game = game
        self.screen = screen
        self.colors = [(0, 255, 0), (255,0,0)]
        self.rectangle = Entity(0,0,self.game.width, self.game.height)
    
    def draw_game(self):
        
        # draw player
        pygame.draw.rect(self.screen,(100,180,255),self.game.player.to_rect())

        # draw asteroids
        for ast in self.game.asteroids:
            pygame.draw.circle(self.screen, (255, 255, 255), ast.get_center(), ast.width//2)

        # draw score

        textsurface = self.font.render("SCORE:" + str(self.game.get_score()), False, (255,255,255))
        self.screen.blit(textsurface, (20, 20))
        textenergy = self.font.render("ENERGY:" + str(self.game.player.energy), False, (255,255,255))
        self.screen.blit(textenergy, (20, 40))
         


    
def test_play():

    pygame.init()

    size = width, height = 600, 600
    game = DodgeGame(width, height)

    screen = pygame.display.set_mode(size)

    interface = DodgeInterface(width, height, game, screen)
    interface.font = pygame.font.Font(None, 20)

    while 1:


        # move player 
        if not game.gameover:
            k = pygame.key.get_pressed()
            dx = dy = 0
            if k[pygame.K_LEFT]:
                dx = -1
            if k[pygame.K_RIGHT]:
                dx = 1
            if k[pygame.K_DOWN]:
                dy = 1
            if k[pygame.K_UP]:
                dy = -1

            game.player_action(dx, dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()    
            # keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

        if not game.gameover:
            game.next_state()
        #pygame.time.wait(30)
        interface.draw_game()
        pygame.display.flip()
        screen.fill((50, 50, 50))

