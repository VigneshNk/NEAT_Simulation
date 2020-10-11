import pygame
import random
import os
import time
import neat
pygame.font.init()

# game window dimensions
WIN_WIDTH = 900
WIN_HEIGHT = 600

# font variables
STAT_FONT = pygame.font.SysFont("comicsans", 50)

# initialize pygame window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Simulator")

# import asteroid image
asteroid_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join("images","asteroid.png")).convert_alpha())

# import background image
bg_img = pygame.transform.scale(pygame.image.load(
    os.path.join("images","background.png")).convert_alpha(), (900, 600))

# import ufo image
ufo_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join("images","ufo.png")).convert_alpha())

# generation number
gen = 1

# score
score = 0

class Ufo:
    """
    Ufo class representing the ufo object
    """

    def __init__(self, x, y):
        """
        initialize the ufo object
        """
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = ufo_img

    def go_up(self):
        """
        make the ufo jump
        """
        self.vel = -4
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the ufo move
        """
        self.tick_count += 1
        
        displacement = self.vel * (self.tick_count) + (self.tick_count) ** 2

        self.y = self.y + displacement

    def draw(self, win):
        """
        draw the ufo
        """
        win.blit(self.img, (int(self.x), int(self.y)))

    def get_mask(self):
        """
        gets the mask for the current image of the ufo
        """
        return pygame.mask.from_surface(self.img)

class Asteroid():
    """
    represents an asteroid object
    """
    # x coordinate offset for asteroid columns
    OFFSET = [-40, 0, 40, 80]

    # bounds for random asteroid velocity
    A = 8
    B = 15

    def __init__(self, x):
        """
        initialize asteroid object
        """
        # x coordinate of 3 asteroids
        self.x1 = x + random.choice(self.OFFSET)
        self.x2 = x + random.choice(self.OFFSET)
        self.x3 = x + random.choice(self.OFFSET)

        self.x = min(self.x1, self.x1, self.x3)

        self.height = 0

        # y coordinate of 3 asteroids
        self.one = 0
        self.two = 0
        self.three = 0

        # images of 3 asteroids
        self.ASTEROID_1 = asteroid_img
        self.ASTEROID_2 = asteroid_img
        self.ASTEROID_3 = asteroid_img

        # increase speed of asteroid
        if score > 15:
            self.vel1 = random.randrange(self.A, self.B) + 12
            self.vel2 = random.randrange(self.A, self.B) + 12
            self.vel3 = random.randrange(self.A, self.B) + 12
        elif score > 10:
            self.vel1 = random.randrange(self.A, self.B) + 8
            self.vel2 = random.randrange(self.A, self.B) + 8
            self.vel3 = random.randrange(self.A, self.B) + 8
        elif score > 5:
            self.vel1 = random.randrange(self.A, self.B) + 4
            self.vel2 = random.randrange(self.A, self.B) + 4
            self.vel3 = random.randrange(self.A, self.B) + 4
        else:
            self.vel1 = random.randrange(self.A, self.B)
            self.vel2 = random.randrange(self.A, self.B)
            self.vel3 = random.randrange(self.A, self.B)

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of each asteroid
        """
        self.height = random.randrange(20, 150)
        self.one = self.height - (self.ASTEROID_1.get_height()) // 2
        self.two = self.one + self.ASTEROID_1.get_height() + random.randrange(60, 120)
        self.three = self.two + self.ASTEROID_2.get_height() + random.randrange(60, 100)

    def move(self):
        """
        move asteroid
        """
        # move all 3 asteroids
        self.x1 -= self.vel1
        self.x2 -= self.vel2
        self.x3 -= self.vel3

        self.x = min(self.x1, self.x1, self.x3)

    def draw(self, win):
        """
        draw asteroids
        """
        # draw asteroid 1
        win.blit(self.ASTEROID_1, (self.x1, self.one))
        # draw asteroid 2
        win.blit(self.ASTEROID_2, (self.x2, self.two))
        # draw asteroid 3
        win.blit(self.ASTEROID_3, (self.x3, self.three))

    def collide(self, ufo, win):
        """
        returns true if a ufo collides with asteroid
        """
        # ufo surface mask
        ufo_mask = ufo.get_mask()

        # asteroid surface masks
        one_mask = pygame.mask.from_surface(self.ASTEROID_1)
        two_mask = pygame.mask.from_surface(self.ASTEROID_2)
        three_mask = pygame.mask.from_surface(self.ASTEROID_3)

        # asteroid offsets from ufo
        one_offset = (self.x1 - ufo.x, self.one - round(ufo.y))
        two_offset = (self.x2 - ufo.x, self.two - round(ufo.y))
        three_offset = (self.x3 - ufo.x, self.three - round(ufo.y))

        # asteroid 1 collision
        one_point = ufo_mask.overlap(two_mask, two_offset)

        # asteroid 2 collision
        two_point = ufo_mask.overlap(one_mask,one_offset)

        # asteroid 3 collision
        three_point = ufo_mask.overlap(three_mask,three_offset)

        # collision detected
        if one_point or two_point or three_point:
            return True

        # no collision
        return False

def draw_window(win, ufos, asteroids, score, gen, ast_ind):
    """
    draws the windows for main game loop
    """
    # thickness and colour of lines from ufo to asteroid
    THICKNESS = 4
    COLOUR = (51, 255, 51)

    # draw background image
    win.blit(bg_img, (0,0))

    # draw asteroids on screen
    for asteroid in asteroids:
        asteroid.draw(win)

    for ufo in ufos:
        # draw lines from ufo to asteroid edge
        try:
            # line from ufo to asteroid 1
            pygame.draw.line(win, COLOUR, (int(ufo.x+ufo.img.get_width()/2), \
                int(ufo.y + ufo.img.get_height()/2)), (int(asteroids[ast_ind].x1 + 
                asteroids[ast_ind].ASTEROID_1.get_width()/2), int(asteroids[ast_ind].one + 
                asteroids[ast_ind].ASTEROID_1.get_height())), THICKNESS)

            # line from ufo to asteroid 2 top
            pygame.draw.line(win, COLOUR, (int(ufo.x+ufo.img.get_width()/2), \
                int(ufo.y + ufo.img.get_height()/2)), (int(asteroids[ast_ind].x2 + 
                asteroids[ast_ind].ASTEROID_2.get_width()/2), int(asteroids[ast_ind].two)), THICKNESS)
            
            # line from ufo to asteroid 2 bottom
            pygame.draw.line(win, COLOUR, (int(ufo.x+ufo.img.get_width()/2), \
                int(ufo.y + ufo.img.get_height()/2)), (int(asteroids[ast_ind].x2 + 
                asteroids[ast_ind].ASTEROID_2.get_width()/2), int(asteroids[ast_ind].two + 
                asteroids[ast_ind].ASTEROID_2.get_height())), THICKNESS)

            # line from ufo to asteroid 3
            pygame.draw.line(win, COLOUR, (int(ufo.x+ufo.img.get_width()/2), \
                int(ufo.y + ufo.img.get_height()/2)), (int(asteroids[ast_ind].x3 + 
                asteroids[ast_ind].ASTEROID_3.get_width()/2), int(asteroids[ast_ind].three)), THICKNESS)
        except:
            pass

        # draw ufo
        ufo.draw(win)

    # label colour
    LABEL_COLOUR = (255, 191, 17)

    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1,  LABEL_COLOUR)
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1), 1,  LABEL_COLOUR)
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(ufos)), 1,  LABEL_COLOUR)
    win.blit(score_label, (10, 50))

    # update display
    pygame.display.update()


def eval_genomes(genomes, config):
    """
    runs the simulation on the current population of
    ufos and sets their fitness based on the distance reached
    """
    global WIN, gen, score
    win = WIN
    gen += 1

    # arrays to hold genome data
    nets = []
    ufos = []
    ge = []

    #initialize current generation using NEAT neural network
    for genome_id, genome in genomes:
        # intialize fitness level to 0
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        # spawn 40 ufos
        ufos.append(Ufo(230,350))
        ge.append(genome)

    # initilize incoming asteroids for current generation
    asteroids = [Asteroid(700)]

    # reset score and velocity to initial
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(ufos) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # end simulation
                run = False
                pygame.quit()
                quit()
                break

        ast_index = 0

        # determine which column of incoming asteroids to use
        if len(ufos) > 0 and len(asteroids) > 1 and ufos[0].x > asteroids[0].x + \
            asteroids[0].ASTEROID_1.get_width():
            ast_index = 1

        for x, ufo in enumerate(ufos):  
            # increase ufo fitness by 0.1 each frame
            ge[x].fitness += 0.1

            # move ufo
            ufo.move()

            # use network to calculate movement through top gap
            output_top = nets[ufos.index(ufo)].activate((ufo.y, abs(ufo.y - \
                asteroids[ast_index].height), abs(ufo.y - asteroids[ast_index].two)))

            # use network to calculate movement through bottom gap
            output_bottom = nets[ufos.index(ufo)].activate((ufo.y, abs(ufo.y - \
                (asteroids[ast_index].two + asteroids[ast_index].height)), abs(ufo.y - 
                asteroids[ast_index].three)))

            # distance from ufo to asteroid 1
            top = asteroids[ast_index].one + asteroids[ast_index].ASTEROID_1.get_height()

            # distance from ufo to asteroid 2
            middle_top = asteroids[ast_index].two
            middle_bottom = asteroids[ast_index].two + asteroids[ast_index].ASTEROID_2.get_height()

            # distance from ufo to asteroid 3
            bottom = asteroids[ast_index].three

            # top gap
            if ufo.y > top and ufo.y < middle_top and output_top[0] > 0.5:
                # move ufo up
                ufo.go_up()

            # bottom gap
            if ufo.y > middle_bottom and ufo.y < bottom and output_bottom[0] > 0.5:
                # move ufo up
                ufo.go_up()

        rem = []
        add_asteroid = False
        for a in asteroids:
            # move asteroids
            a.move()

            # check for collision
            for ufo in ufos:
                if a.collide(ufo, win):
                    ge[ufos.index(ufo)].fitness -= 1
                    # remove ufo from simulation
                    nets.pop(ufos.index(ufo))
                    ge.pop(ufos.index(ufo))
                    ufos.pop(ufos.index(ufo))

            # asteroids have moved off screen
            if a.x1 + a.ASTEROID_1.get_width() < 0 and a.x2 + a.ASTEROID_1.get_width() < 0 \
                and a.x3 + a.ASTEROID_1.get_width() < 0:
                # remove asteroids from simulation
                rem.append(a)

            # all asteroids have passed by ufo
            if not a.passed and a.x1 < ufo.x and a.x2 < ufo.x and a.x3 < ufo.x:
                a.passed = True

                # spawn next column of asteroids
                add_asteroid = True

        if add_asteroid:
            score += 1

            # add fitness for passing through asteroid
            for genome in ge:
                genome.fitness += 3
            asteroids.append(Asteroid(WIN_WIDTH))

        for r in rem:
            asteroids.remove(r)

        for ufo in ufos:
            if ufo.y + ufo.img.get_height() - 10 >= 600 or ufo.y < -50:
                ge[ufos.index(ufo)].fitness -= 1
                # remove ufo from simulation
                nets.pop(ufos.index(ufo))
                ge.pop(ufos.index(ufo))
                ufos.pop(ufos.index(ufo))

        # redraw window each frame
        draw_window(WIN, ufos, asteroids, score, gen, ast_index)

        # break if score gets large enough
        if score > 50:
            break

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to dodge asteroids
    """
    # configure NEAT neural network
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # create population object for NEAT model
    p = neat.Population(config)

    # output each generations statistics
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # 50 geneartion limit
    winner = p.run(eval_genomes, 50)

    # output final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # link to NEAT config file in local directory
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'genetic_algorithm_configuration.txt')
    run(config_path)

