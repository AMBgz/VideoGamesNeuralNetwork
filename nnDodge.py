from GameTests import *


def output_dodge(res):
    dx = dy = 0
    if res[0] > 0:
        dx += 1
    if res[1] > 0:
        dx -= 1
    if res[2] > 0:
        dy += 1
    if res[3] > 0:
        dy -= 1
    return dx, dy

def inputs_dodge2(game):
    px, py = game.player.get_position()
    w, h = game.width, game.height
    res = []
    # i1, i2, i3, i4 = position par rapport au mur
    res.extend([px/w, py/h, 1 - px/w, 1 - py/h])
    l = game.get_input_closer(1)
    for [x, y] in l:
        if x > 0:
            a = [0, abs(x/w)]
        else:
            a = [abs(x/w), 0]
        if y > 0:
            b = [0, abs(y/h)]
        else:
            b = [abs(y/h), 0]
        res.extend(a + b)
    
    return res

def play_dodge(game, nn, individu, interface = None):

    nn.new_weights(individu)
    game.reset()

    maxtime = 300 # nombre maximal de score qu'il peut avoir
    count = 0

    while not game.gameover and game.time < maxtime:
        if count == 50:
            count = 0
            game.player.energy += 25
        inputs = inputs_dodge2(game)
        res = nn.compute(inputs, tanh)
        dx, dy = output_dodge(res)
        game.player_action(dx, dy)
        game.next_state()
        if interface != None:
            # draw game
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            
            interface.draw_game()
            pygame.display.flip()
            interface.screen.fill((65,65,65))

    return game.get_score()

def genetic_algorithm_dodge(game, nn, affichage = False, interface = None, file = None, l = []):

    npop = 200
    nbtest = 1 # entre 1 et 3

    iterations = 1000 # si entrainement toute la nuit, mettre 100000 et un fichier

    population = [nn.make_individu(-2,2) for _ in range (npop)]
    if l != []:
        population[0] = l

    for i in range(iterations):
        population = sorted(population, reverse=True, key = lambda x : sum([play_dodge(game, nn, x) for _ in range(nbtest)]))
        population = algogen1(npop, population, nn, randfloat(-2, 2))
        best_score = play_dodge(game, nn, population[0])
        print("Iteration ",i, "score :", best_score)
        # enregistrement des poids
        if file != None:
            score = readScore(file)
            if best_score > score:
                writeFile(file, best_score, population[0])

        if affichage:
            play_dodge(game, nn, population[0], interface)

def nn_dodge(affichage = False, s = None):
    interface = None
    if s != None:
        f = open(s, "r+")
        l = readIndividual(f)
        print("l=", l)


    width, height = 600, 600
    game = DodgeGame(width, height)

    size = [8, 6, 4]
    nn = NeuralNet(size)

    if affichage:
        pygame.init()
        screen = pygame.display.set_mode((game.width, game.height))
        pygame.font.init()
        interface = DodgeInterface(game.width, game.height, game, screen)
        interface.font = pygame.font.Font(None, 20)

    if s != None:
        genetic_algorithm_dodge(game, nn, affichage, interface, f, l)
        f.close()
    else:
        genetic_algorithm_dodge(game, nn, affichage, interface)


nn_dodge(True, "dodging.txt")