import random,pygame,sys,math

class Pad:
    
    def __init__(self, x, y, width, height, speed):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
    
    def move(self, direction, border):
        self.x = (self.x + self.speed*direction)%(border+self.width/2)
    
    def get_position(self):
        return [self.x, self.y]

class Ball:
    
    def __init__(self, x, y,width, height, vy):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = random.randint(2, 4)
        self.vy = vy

    
    def get_position(self):
        return self.x,self.y

    def fall(self, w, h, padpos, padheight, pw):
        self.x += self.vx
        self.y += self.vy

        if self.y < 0:
            self.vy *= -1
            self.y = 0
        
        if self.x + self.width > w:
            self.x = w - self.width
            self.vx *= -1
        
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        
        if self.y + self.height > padpos[1] and self.x + self.width >= padpos[0] and self.x <= padpos[0] + pw:        
            self.vy *= -1
            self.y = padpos[1]-padheight - self.height
            return True
        return False


            
class Pong:

    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.gameover = False
        self.pad = Pad(width/2 - 20, self.height - 10, 40, 10, 6)
        self.score = 0

    def reset(self):
        self.pad = Pad(self.width/2 - 20, self.height - 10, 40, 10, 6)
        self.gameover = False
        self.drop_ball()
        self.score = 0
    
    def upOrDown(self):
        return self.ball.vy > 0

    def drop_ball(self):
        bw = 10
        bh = 10
        x = random.randint(0, self.width-bw)
        y = 0
        self.ball = Ball(x,y,bw,bh,5)
    
    def update_state(self):
        if self.ball.fall(self.width, self.height, self.pad.get_position(), self.pad.height, self.pad.width):
            self.score += 1
        # check death
        if self.ball.y > self.height:
            self.gameover = True

class PongInterface:

    def __init__(self, width, height, game, screen):

        self.width = width
        self.height = height
        self.game = game
        self.screen = screen
    
    def draw_game(self, font):
        
        # draw pad
        px, py = self.game.pad.get_position()
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(
            px, py, self.game.pad.width, self.game.pad.height
        ))

        # draw ball
        bx, by = self.game.ball.get_position()
        pygame.draw.circle(self.screen, (255, 255, 0), (bx + self.game.ball.width/2,by + self.game.ball.height/2), self.game.ball.width)


def test_play():

    width, height = size =  500,600

    screen = pygame.display.set_mode(size)
    pygame.font.init()
    game = Pong(width, height)
    game.drop_ball()


    interface = PongInterface(width, height, game, screen)

    font = pygame.font.Font(None, 20)

    while 1:

        # controls

        k = pygame.key.get_pressed()
        d = 0
        if k[pygame.K_LEFT]:
            d -= 1
        if k[pygame.K_RIGHT]:
            d += 1
        
        if not game.gameover:
            game.pad.move(d, game.width)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game.reset()
                
        # update game
        if not game.gameover:
            
            game.update_state()

        # update interface
        interface.draw_game(font)

        pygame.display.flip()
        screen.fill((30,30,30))


