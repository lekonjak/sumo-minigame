import pygame, sys, random

window_width, window_height = 800, 800
icon_width, icon_height = 40, 40
clock = pygame.time.Clock()

class Game:   ##class for handling game itself
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))

        pygame.display.set_caption("~Sumozin kkk~")
        pygame.mouse.set_visible(False)

        self.bg = pygame.image.load("images/sumoring.jpg").convert()
        self.bg = pygame.transform.scale( self.bg, ( window_width, window_height))

        self.es = pygame.image.load("images/gameover.jpg").convert()
        self.es = pygame.transform.scale( self.es, ( window_width, window_height))

        self.font = pygame.font.SysFont("monospace", 16)

        self.sprite_list = pygame.sprite.Group()
        self.player = Player()
        self.sprite_list.add(self.player)
        self._running = True

        for i in range(5):
            self.sprite_list.add(Fighter())
            self.sprite_list.add(Gfood())
            self.sprite_list.add(Bfood())

    def on_exec(self):
        while ( self._running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            if not self.detect_collide():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.left()
                if keys[pygame.K_RIGHT]:
                    self.player.right()
                if keys[pygame.K_UP]:
                    self.player.up()
                if keys[pygame.K_DOWN]:
                    self.player.down()

            self.scoretext = self.font.render("Score {0}".format(self.player.getweight()), 1, (0,0,0))

            self.screen.blit( self.bg, (0, 0))
            self.screen.blit( self.scoretext, (5, 10))
            if self.update():
                return self.gameover()
            self.sprite_list.draw(self.screen)
            pygame.display.flip()
            clock.tick(45)

    def gameover(self):
        while True:
            self.screen.blit( self.es, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()

    def detect_collide(self):
        for sprite in self.sprite_list:
            if pygame.sprite.collide_rect(sprite,self.player):
                if sprite.__class__.__name__ != 'Player':
                    if sprite.__class__.__name__ == 'Gfood':
                        self.player.eat()
                        self.sprite_list.remove(sprite)
                        self.sprite_list.add(Gfood())
                    elif sprite.__class__.__name__ == 'Bfood':
                        self.player.damage()
                        self.sprite_list.remove(sprite)
                        self.sprite_list.add(Bfood())
                    else:
                        self.player.fly(sprite.getdir())

    def update(self):   # border collide
        end = False
        for sprite in self.sprite_list:
            if sprite.update() == True:
                if sprite.__class__.__name__ == 'Gfood':
                    new = Gfood()
                elif sprite.__class__.__name__ == 'Bfood':
                    new = Bfood()
                elif sprite.__class__.__name__ == 'Player':
                    end = sprite.death()
                    continue
                else:
                    new = Fighter()
                self.sprite_list.remove(sprite)
                self.sprite_list.add(new)
        return end

class Obj(pygame.sprite.Sprite):    ##class for every object in screen
    def __init__(self, str_icon, speed):
        super().__init__()

        self.image = pygame.image.load( str_icon).convert()
        self.image = pygame.transform.scale( self.image, ( icon_width, icon_height))

        self.rect = self.image.get_rect()
        self.speed = speed
        self.border = False

    def up(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.border = True
    def down(self):
        if self.rect.y + icon_height < window_height:
            self.rect.y += self.speed
        else:
            self.border = True
    def left(self):
        if self.rect.x > 0:
            self.rect.x -= self.speed
        else:
            self.border = True
    def right(self):
        if self.rect.x + icon_width < window_width :
            self.rect.x += self.speed
        else:
            self.border = True

class Player(Obj):
    def __init__(self):
        super().__init__("images/player.jpg", 30)
        self.life = 3
        self.rect.x, self.rect.y = (window_width/2) - (icon_width/2) , (window_height/2) - (icon_height/2)
        self.weight = 100

    def death(self):
        self.life -= 1
        self.rect.x, self.rect.y = (window_width/2) - (icon_width/2) , (window_height/2) - (icon_height/2)
        self.weight = 100
        self.border = False
        return self.end()

    def damage(self):
        self.weight -= 10

    def eat(self):
        self.weight += 10

    def fly(self, direction):
        if direction == 1:                 #top
            self.down()
        elif direction == 2:               #down
            self.up()
        elif direction == 3:               #left
            self.right()
        else:                              #right
            self.left()

    def update(self):
        if self.weight == 0:
            return True
        return self.border

    def getweight(self):
        return self.weight

    def end(self):
        if self.life == 0:
            return True
        else:
            return False

class Obj2(Obj):
    def __init__(self, str_icon):
        super().__init__( str_icon, random.randint(15, 45))
        self.counter = 0
        self.spawn_side = random.randint(1, 4)
        if self.spawn_side == 1:                 #top
            self.rect.x, self.rect.y =  random.randint(40, 760), 40
        elif self.spawn_side == 2:               #down
            self.rect.x, self.rect.y =  random.randint(40, 760), 760
        elif self.spawn_side == 3:               #left
            self.rect.x, self.rect.y =  40, random.randint(40, 760)
        elif self.spawn_side == 4:               #right
            self.rect.x, self.rect.y =  760, random.randint(40, 760)
        else:                               #center - should never happen
            self.rect.x, self.rect.y =  (window_width/2) - (icon_width/2) , (window_height/2) - (icon_height/2)
            self.spawn_side = random.randint(1,4)

    def update(self):
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            if self.spawn_side == 1:                 #top
                self.down()
            elif self.spawn_side == 2:               #down
                self.up()
            elif self.spawn_side == 3:               #left
                self.right()
            else:               #right
                self.left()

        return self.border

class Fighter(Obj2):
    def __init__(self):
        super().__init__("images/honda.jpg")
    def getdir(self):
        return self.spawn_side
class Gfood(Obj2):
    def __init__(self):
        super().__init__("images/gfood.jpg")
class Bfood(Obj2):
    def __init__(self):
        super().__init__("images/bfood.jpg")

# main
game = Game()
game.on_exec()
