from GameTests import *



def snake_inputs(game):
    # ce qu'on donne en input
    def encodage(x, y, grille):
        if x < 0 or y < 0 or x >= game.cols or y >= game.rows or grille[y][x].is_tail():
            return -1
        return 1
    def encodage_pomme(x, y, tetex, tetey):
        if x == tetex:
            a = 0
        elif x > tetex:
            a = 1
        else:
            a = -1
        if y == tetey:
            b = 0
        elif y > tetey:
            b = 1
        else:
            b = -1
        return a, b

    a, b, c, d = game.get_neighbors()
    x, y = game.get_apple()

    grille = game.grid
    n1 = encodage(a[0], a[1], grille)
    n2 = encodage(b[0], b[1], grille)
    n3 = encodage(c[0], c[1], grille)
    n4 = encodage(d[0], d[1], grille)
    n5, n6 = encodage_pomme(x, y, game.snake[0][0], game.snake[0][1])


    return [n1, n2, n3, n4, n5, n6]

def play_snake(game, nn, individu, walls = True, interface = None):
    nn.new_weights(individu)
    game.reset()
    iteration = 1200
    directions = [(-1,0), (0,-1), (1, 0), (0,1)]


    while not game.gameover and iteration > 0 :

        inputs = snake_inputs(game)
        output = nn.compute(inputs, tanh)

        # find max // 0 -> left 1 -> up , 2 -> right , 3 -> down
        maxi = 0
        for i in range(len(output)):
            if output[i] > output[maxi]:
                maxi = i
        
        game.direction = directions[maxi]
        game.next_state()
        score = game.get_score()
        iteration -= 1
        if interface != None:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            interface.draw_game()
            pygame.display.flip()
            interface.screen.fill((50,50,50))

        #limit
        if iteration == 300 and score[0] < 2:
            break

    return score

def genetic_algorithm_snake(game, nn, affichage = False, interface = None, file = None, fromFile = False):
    nb_individu = 400
    nbiter = 500
    walls = True

    population = [nn.make_individu(-1, 1) for _ in range(nb_individu)]
    # replace first individual by trained individual from file
    if  fromFile != [] and file != None:
        population[0] = fromFile

    for n in range(nbiter):
        print("iteration", n)
        population = sorted(population, key = lambda x : play_snake(game, nn, x), reverse = True)
        # update population
        population = algogen1(nb_individu, population, nn, randfloat(-2, 2))

        score = play_snake(game, nn, population[0])
        print("score = ", score)

        # update file
        if file != None:
            sc = readScore(file)
            if score[0] > sc or sc == 0:
                writeFile(file, score[0], population[0])

        
        # draw best game
        if affichage:
            play_snake(game, nn, population[0], True, interface)

def nn_snake(affichage = False, s = None):
    if s != None:
        file = open(s, "r+")
        l = readIndividual(file)
        print(l)

    rows, cols = 17, 17
    game = SnakeGame(rows, cols)
    game.begin()
    interface = None
    if affichage:
        width, height = cols*30, rows*30
        screen = pygame.display.set_mode((width, height))
        pygame.font.init()
        interface = SnakeInterface(game, width//cols, screen)
        font = pygame.font.Font(None, 20)


    size = [6 , 6, 6, 4]

    nn = NeuralNet(size)
    if s != None:
        genetic_algorithm_snake(game, nn, affichage, interface, file, l)
    else:
        genetic_algorithm_snake(game, nn, affichage, interface)

nn_snake(True, "snakew.txt")

