import pygame
import random

ScreenX,ScreenY = 500,700  #ventana

Run = True


#Se define el color par que sea trasparente 
BLACK = (0, 0, 0)        
CoInvi = (255, 174, 201) #Color salmon

pygame.init()
pygame.mixer.init()



screen = pygame.display.set_mode((ScreenX, ScreenY)) #crea la ventana

#Se crea una variable para luego llamarla en el while principal 
fondo = pygame.image.load("cosas/Fondo.png").convert()

#Titulo de la ventana
pygame.display.set_caption("Space Invader Pro crack 2.0")

clock = pygame.time.Clock()

#Sonido al disparar
Sdisp = pygame.mixer.Sound('cosas/laser.wav') 
y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cosas/navecita.png").convert() #llamamos a la imagen
        self.image.set_colorkey(CoInvi) #ponemos el color trasparente
        self.rect = self.image.get_rect() 
        self.rect.centerx = ScreenX // 2 #pocicion X en donde aparece la nave
        self.rect.bottom = ScreenY  #pocicion Y en donde aparece la nave
        self.speed_x = 0 #velocidad en X, mas abajo se define la velocidad

    def update(self):
        self.speed_x = 0
        # update para actualizar y saber que tecla se preciono
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
           self.speed_x = -3
        if keys[pygame.K_RIGHT]:
            self.speed_x = 3
        
        #limites de la nave
        self.rect.x += self.speed_x
        if self.rect.right > ScreenX:
            self.rect.right = ScreenX
        if self.rect.left < 0:
            self.rect.left = 0


    def disparo(self):
        #pocicion de la bala (de donde sale)
        #llamamos a la clase Balas
        bala = Balas(self.rect.centerx, self.rect.top)
        #agg bala a los sprites
        Tsprites.add(bala)  
        balas.add(bala)
        Sdisp.play() #sonido al disparar

class Balas(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('cosas/Balita.png').convert()
        self.image.set_colorkey(CoInvi)
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.centerx = x
        self.speedy = -10

    #hacia donde se dirige la bala
    def update(self):
        self.rect.y += self.speedy
        # cuando llege a 0 en el eje Y, se borra
        if self.rect.bottom < 0:
            self.kill() #kill - desaparece la bala

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('cosas/Enemi1.png').convert()
        self.image.set_colorkey(CoInvi)
        self.rect = self.image.get_rect()
        self.rect.x =  random.randrange(1, ScreenX - 50)
        self.rect.y = random.randrange(1, 400)
        self.speedy = -50

    def update(self):
        self.time = 1 #velocidad
        self.rect.x += self.time
        #cuando llegen al limite, estos bajaran 50 pixeles
        #en el eje Y
        if self.rect.x >= ScreenX:
            self.rect.x = 0
            self.rect.y += 50

    def disparo(self):
        balaE = BalasEnemigos(self.rect.centerx, self.rect.top)
        Tsprites.add(balaE)
        balas.add(balaE)

class BalasEnemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('cosas/Balita.png').convert()
        self.image.set_colorkey(CoInvi)
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(10, ScreenX)
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        #cuando llegen al limite (ScreenY)=700
        #desaparece
        if self.rect.bottom > 700:
            self.kill()


#Tsprites, es para guardar todos los sprites a los que se les asigna
# --  pygame.sprite.Group() -- 
Tsprites = pygame.sprite.Group()

balas = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas_enemigos = pygame.sprite.Group()

player = Player()

Tsprites.add(player)

#rango de aparicion de los enemigos
for x in range(40):
    enemi = Enemigos(10,10)
    enemigos.add(enemi)
    Tsprites.add(enemi)
 
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparo() 

    #llamamos a todos los sprites
    Tsprites.update()

    #Fondo
    #Con esto logramos que se mueva en un loop infinito en el eje Y
    yr = y % fondo.get_rect().width
    screen.blit(fondo, [0, yr -fondo.get_rect().width])
    if yr < ScreenY:
         screen.blit(fondo,(0,yr))
    y += 4

 
    Tsprites.draw(screen)

    #Colicion de los enemigos
    colicionE = pygame.sprite.groupcollide(enemigos, balas,True,True)

    clock.tick(60)
    pygame.display.flip()
    

pygame.quit()