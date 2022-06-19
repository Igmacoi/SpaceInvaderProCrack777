from platform import platform
import pygame
import random
#---------------------------------------------------------------------
# Juego Space Invader
# Para mover al jugador se utilizan las flechas de izqueirda <- y
# derecha ->, para disparar utilizamos la tecla Spacio
# El juego consiste en destruir a los aliens(enemigos) y generar el 
# mayor puntaje posible antes de que nuestra vida llege a 0
#---------------------------------------------------------------------

ScreenX,ScreenY = 500,700  #ventana

Run = True


#Se define el color par que sea trasparente 
BLACK = (0, 0, 0)        
CoInvi = (255, 174, 201) #Color salmon
Blanco = (160,0,240)

pygame.init()
pygame.mixer.init()


#crea la ventana
screen = pygame.display.set_mode((ScreenX, ScreenY)) 

#Se crea una variable para luego llamarla en el while principal 
fondo = pygame.image.load("cosas/Fondo.png").convert()
y = 0 

#Titulo de la ventana
pygame.display.set_caption("Space Invader Pro crack 2.0")

clock = pygame.time.Clock()

#Sonido al disparar
Sdisp = pygame.mixer.Sound('cosas/laser.wav')
#Sonido Explo enemigos
SexplE = pygame.mixer.Sound('cosas/explosound.wav') 

#ponemos las imagenes en una lista
explot = []
for i in range(1,9):
    Explo = pygame.image.load(f'Explociones/{i}.png')
    explot.append(Explo)

score = 0
vida = 100


def vida(frame, x,y, nivel):
    largo = 100
    alto = 20 
    fill = int((nivel/100)*largo)
    border = pygame.Rect(x,y, largo, alto)
    fill = pygame.Rect(x,y,fill, alto)
    pygame.draw.rect(frame, (255,0,55),fill)
    pygame.draw.rect(frame, negro, border,4)


window = pygame.display.set_mode((ScreenX, ScreenY))
blanco = (255,255,255)
negro = (0,0,0)
def puntuacion(frame, text, size, x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, blanco,negro)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame, text_rect)

class Player(pygame.sprite.Sprite):
    #entrada self -Es una instancia para llamar al objeto
    #salida  
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cosas/navecita.png").convert() #llamamos a la imagen
        self.image.set_colorkey(CoInvi) #ponemos el color trasparente
        self.rect = self.image.get_rect() 
        self.rect.centerx = ScreenX // 2 #pocicion X en donde aparece la nave
        self.rect.bottom = ScreenY  #pocicion Y en donde aparece la nave
        self.speed_x = 0 #velocidad en X, mas abajo se define la velocidad
        self.vida = 100 

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def update(self):
        self.speed_x = 0
        # update para actualizar y saber que tecla se preciono
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
           self.speed_x = -6
        if keys[pygame.K_RIGHT]:
            self.speed_x = 6
        
        #limites de la nave
        self.rect.x += self.speed_x
        if self.rect.right > ScreenX:
            self.rect.right = ScreenX
        if self.rect.left < 0:
            self.rect.left = 0

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def disparo(self):
        #posicion de la bala (de donde sale)
        #llamamos a la clase Balas
        bala = Balas(self.rect.centerx, self.rect.top)
        #agg bala a los sprites
        Tsprites.add(bala)  
        balas.add(bala)
        Sdisp.play() #sonido al disparar

class Balas(pygame.sprite.Sprite):
    #entrada self -Es una instancia para llamar al objeto
    #         X eje x en pantalla
    #         Y eje y en pantalla
    #salida 
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('cosas/Balita.png').convert()#llamamos a la imagen
        self.image.set_colorkey(CoInvi)#ponemos el color trasparente
        self.rect = self.image.get_rect()
        self.rect.y = y #pocicion de donde sale la bala en eje y
        self.rect.centerx = x #pocicion de donde sale la bala en eje x
        self.speedy = -10 #velocidad de la bala de la nave

    #hacia donde se dirige la bala
    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def update(self):
        self.rect.y += self.speedy
        # cuando llege a 0 en el eje Y, se borra la bala
        if self.rect.bottom < 0:
            self.kill() #kill - desaparece la bala

class Enemigos(pygame.sprite.Sprite):
    #entrada self -Es una instancia para llamar al objeto
    #         X eje x en pantalla
    #         Y eje y en pantalla
    #salida 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('cosas/Enemi1.png').convert()#llamamos a la imagen
        self.image.set_colorkey(CoInvi)#ponemos el color trasparente
        self.rect = self.image.get_rect()
        self.rect.x =  random.randrange(1, ScreenX - 50)#pocicion de donde sale la bala en eje
                                                #x de forma aleatoria entre los parametros dados
        self.rect.y = random.randrange(1, 400)#pocicion de donde sale la bala en eje
                                         #y de forma aleatoria entre los parametros dados
        self.speedy = -50 #velocidad de los enemigos en el eje Y, -50 es para donde se mueven (izquierda)

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def update(self):
        self.time = 1 #velocidad
        self.rect.x += self.time
        #cuando llegen al limite, estos bajaran 50 pixeles
        #en el eje Y
        if self.rect.x >= ScreenX:
            self.rect.x = 0
            self.rect.y += 50

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def disparo_enemigo(self):
        #pocicion de la bala (de donde sale)
        #llamamos a la clase BalasEnemigos
        balaE = BalasEnemigos(self.rect.centerx, self.rect.top)
        #agg bala a los sprites
        Tsprites.add(balaE)  
        balas.add(balaE)

class BalasEnemigos(pygame.sprite.Sprite):
    #entrada self -Es una instancia para llamar al objeto
    #         X -eje x en pantalla
    #         Y -eje y en pantalla
    #salida 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('cosas/BalitaEnemigo.png').convert_alpha()#llamamos a la imagen
        self.image = pygame.transform.rotate(self.image, 180)#rotamos la imagen en 180 grados
        self.image.set_colorkey(CoInvi)#ponemos el color trasparente
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(10, ScreenX)#pocicion de donde sale la bala en eje
                                         #y de forma aleatoria entre los parametros dados
        
        self.rect.centerx = x #pocicion de donde sale la bala en eje X, en el centro de la imagen
                            #del enemigo que la disparo
        self.speedy = 10 #velocidad de la nave en eje Y, pisitivo para que suba

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def update(self):
        self.rect.y += self.speedy
        #cuando llegen al limite (ScreenY)=700, inferior
        #desaparece
        if self.rect.bottom > 700:
            self.kill()

class Explo(pygame.sprite.Sprite):
    #entrada self -Es una instancia para llamar al objeto
    #        poci -Posicion de la explosion 
    def __init__(self, poci):
        super().__init__()
        self.image = explot[0] #inicia la Explosion posicion 0 
        self.rect = self.image.get_rect()
        self.rect.center = poci
        self.time = pygame.time.get_ticks() #Tiempo trascurrido
        self.Vel_Explot = 40 # Velocidad de la explo-Mientras mas alto, mas se demora
        self.frames = 0 #variable que aumenta para cambiar la imagen
                        #de la explosion
    
    #entrada self -Es una instancia para llamar al objeto
    #Salida
    def update(self):
        tiempo = pygame.time.get_ticks() #Cuanto tiempo a trascurrudi desde la explicion 
        #si han trascurrido mas de (vel_explot), NO SE COMO EXPLICARR XDDXDXDXDXDXDXDX
        if tiempo - self.time > self.Vel_Explot:
            #Aumenta en 1 los frames para ir variando en las imagenes
            self.time = tiempo 
            self.frames+=1
            #Una vez pase por todas las imagenes de la explision, esta se detiene
            if self.frames == len(explot):
                self.kill()#elimina la ultima imagen de la explosion de la pantalla
            #De lo contrario, que carge las imagenes. 
            else:
                position = self.rect.center
                self.image = explot[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position

#Tsprites, es para guardar todos los sprites a los que se les asigna
# --  pygame.sprite.Group() -- 
Tsprites = pygame.sprite.Group()

#llamamos al sprite para despues agg a la clase correspondiente
balas = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas_enemigos = pygame.sprite.Group()

player = Player()
Tsprites.add(player)

#rango de aparicion de los enemigos
 #VER COMO FUNCIONA

for x in range(20):
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

    #Colicion bala Jugador - Enemigo
    colicionE = pygame.sprite.groupcollide(enemigos, balas,True,True)
    for i in colicionE:
        score+=10
        #Disparo del enemigo 
        enemi.disparo_enemigo()
        #Cada vez que muera 1, aparece otro        
        enemigoss = Enemigos(300,10) #ver para que es
        enemigos.add(enemigoss)
        Tsprites.add(enemigoss)

        bum = Explo(i.rect.center) 
        Tsprites.add(bum)
        SexplE.play() #intentar se sean sonidos random xd 
                      #Sonidos By MatthiasTheLaw

    #colicion balas enemigos - jugador 
    colicionJ = pygame.sprite.spritecollide(player, balas_enemigos, True)
    for a in colicionJ:
        player.vida -= 10
        if player.vida <= 0:
            run = False 
        explo1 = Explo(a.rect.center)
        Tsprites.add(explo1)
    
    

    puntuacion(window, ('  SCORE: '+ str(score)+'       '), 30, ScreenX-85, 2)
    vida(window, ScreenX-285, 0, player.vida)


    clock.tick(60)
    pygame.display.flip()
    

pygame.quit()