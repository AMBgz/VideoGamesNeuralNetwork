from GameTests import *

def play_pong(game, nn, individu):
    game.reset()
    nn.new_weights(individu)

    itermax = 4

    while not game.gameover and game.score < itermax:
        inputs = [game.ball.x - game.pad.x, game.ball.y - game.pad.y, 1 if game.upOrDown() else 0]
        res = nn.compute(inputs, sigmoid)

        if res[0] > 0:
            if res[1]>0:
                d = 1
            else:
                d = -1
            game.pad.move(d, game.width)
        game.update_state()        
    return game.score

def genetic_algorithm_pong(game, nn, affichage = False, file = None, individual = []):


    if affichage:
        screen = pygame.display.set_mode((game.width, game.height))
        pygame.font.init()
        interface = PongInterface(game.width, game.height, game, screen)
        font = pygame.font.Font(None, 20)




    npop = 100

    iter = 100
    nbtest = 2

    population = [nn.make_individu(-1,1) for _ in range(npop)]
    if individual != [] and len(individual == len(population[0])):
        population[0] = individual

    for _ in range(iter):

        population = sorted(population,reverse=True,key = lambda x : sum([play_pong(game, nn, x) for _ in range(nbtest)]))
        print("best", play_pong(game, nn, population[0]))
        population = algogen1(npop, population, nn, randfloat(-1, 1), 5)

        if individual != []:
            score = play_pong(game, nn, population[0])
            best = readScore(file)
            if score > best:
                writeFile(file, score, population[0])
        # afficher la meilleure partie

        if affichage:
            game.reset()
            scoremax = 4
            while not game.gameover and game.score < scoremax:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                            sys.exit()
                    
                # update game
                inputs = [game.ball.x - game.pad.x, game.ball.y - game.pad.y, 1 if game.upOrDown() else 0]
                res = nn.compute(inputs, sigmoid)

                if res[0] > 0:
                    if res[1]>0:
                        d = 1
                    else:
                        d = -1
                    game.pad.move(d, game.width)
                game.update_state()
            
                # update interface
                interface.draw_game(font)

                pygame.display.flip()
                screen.fill((30,30,30))

def nn_pong(affichage = False, s = None):
    l = []

    if s != None:
        # create file
        f = open(s, "w+")
        f.close()
        f = open(s, "r+")
        l = readIndividual(f)
        print("entrainement = ", l)
    
    game = Pong(500,600)
    game.drop_ball()

    size = [3 , 2]
    nn = NeuralNet(size)

    genetic_algorithm_pong(game, nn , affichage,f,  l)

nn_pong(True, "pong.txt")