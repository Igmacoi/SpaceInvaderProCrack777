import pygame
import random
#---------------------------------------------------------------------
# Juego Space Invader
# Para mover al jugador se utilizan las flechas de izqueirda <- y
# derecha ->, para disparar utilizamos la tecla Spacio
# El juego consiste en destruir a los aliens(enemigos) y generar el 
# mayor puntaje posible antes de que nuestra vida llege a 0
#---------------------------------------------------------------------

#Inicializamos Pygame
pygame.init()
pygame.mixer.init()

ScreenX,ScreenY = 500,700  #ventana

#para el While, True es para que se mantenga activo
Run = True

#Se define el color par que sea trasparente  
CoInvi = (255, 174, 201) #Color salmon

#crea la ventana
screen = pygame.display.set_mode((ScreenX, ScreenY)) 

#Se crea una variable para luego llamarla en el while principal 
fondo = pygame.image.load("cosas/Fondo.png").convert()
y = 0 

#Titulo de la ventana
pygame.display.set_caption("Space Invader Pro crack 2.0")

#Ayuda a controlar el tiempo (FPS)
clock = pygame.time.Clock()     

#Sonido al disparar
Sdisp = pygame.mixer.Sound('cosas/laser.wav')
#Sonido Explo enemigos
SexplE = pygame.mixer.Sound('cosas/explosound.wav') 

#ponemos las imagenes en una lista
explot = []
#toma los valores del 1 al 9 de las imagenes
for i in range(1,9):
    #{i}, itera entre los nombres de las explociones del 1 al 9
    Explo = pygame.image.load(f'Explociones/{i}.png')
    #habre la lista y guarda en ella lo que esta en Explo
    explot.append(Explo)

#El score empieza en 0
score = 0

#colores para los textos
blanco = (255,255,255)
negro  = (0,0,0)
verde  = (34,177,76)


#Entrada  frame  screen
#         nivel  vida
#         x      coordenada en x
#         y      coordenada en y
#Salida
def vida(frame, x,y, nivel):
    #(screen,  0, 0 ,player.vida)
    largo = 100 
    alto = 20 
    #la cantidad de vida, 100 puntos de vida 
    #fill es una variable que ira disminuyendo 
    fill = int((nivel/100)*largo)
    #Se crea un rectangulo en donde estara la vida
    # x,y posicion 
    border = pygame.Rect(x,y, largo, alto)
    #creamos la barra de vida 
    fill = pygame.Rect(x,y,fill, alto)
    #Dibujamos la barra de vida
    pygame.draw.rect(frame, verde ,fill)
    #Dibujamos los bordes,                espesor 
    pygame.draw.rect(frame, negro, border,5)

#Entrada  frame  screen
#         text   score
#         size - tamano
#         x      coordenada en x
#         y      coordenada en y
#Salida
def puntuacion(frame, text,   size,      x,       y):
#         (screen, str(score), 25, ScreenX // 2, 10)
                                #Tipo de letra-- tamano --negrita(que sea mas notoria)
	Fuente = pygame.font.SysFont('bahnschrift',  size,   bold=True) #creamos el tipo de letra
                            #  texto       colores
	text_frame = Fuente.render(text, True, blanco,negro)
        #Para obtener las coordenadas donde se pondra la puntuacion
	text_rect = text_frame.get_rect()
    #Damos las coordenadas
	text_rect.midtop = (x,y)
    #Lugar en el que se pondra el texto, en este caso en la ventana (screen)
	frame.blit(text_frame, text_rect)

class Jugador(pygame.sprite.Sprite):
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
        self.rect.x =  random.randrange(1, ScreenX - 50)                               
        self.rect.y = random.randrange(10, 340)
        #self.speedyE = -10 #velocidad de los enemigos en el eje Y, -50 es para donde se mueven (izquierda)

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
        bala = BalasEnemigos(self.rect.centerx, self.rect.top)
        #agg bala a los sprites
        Tsprites.add(bala)  
        balas_enemigos.add(bala)
        #poner sonido

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
        self.rect.y = random.randrange(10, 300)#pocicion de donde sale la bala en eje
                                         #y de forma aleatoria entre los parametros dados
        
        self.rect.centerx = x #pocicion de donde sale la bala en eje X, en el centro de la imagen
                            #del enemigo que la disparo
        self.speedx = 8 #velocidad de la bala en eje Y

    #entrada self -Es una instancia para llamar al objeto
    #salida 
    def update(self):
        self.rect.y += self.speedx
        #cuando llegen al limite (ScreenY)=700, inferior desaparece
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

player = Jugador()
Tsprites.add(player)
balas.add(player)


#rango de aparicion de los enemigos
for x in range(20):
    enemi = Enemigos(20,20) 
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
        enemi = Enemigos(10,10)
        enemigos.add(enemi)
        Tsprites.add(enemi)

        bum = Explo(i.rect.center) 
        Tsprites.add(bum)
        SexplE.play() #intentar se sean sonidos random xd 
                      #Sonidos By MatthiasTheLaw

    #colicion balas enemigos - jugador 
    colicionJ = pygame.sprite.spritecollide(player, balas_enemigos, True)
    for j in colicionJ:
        player.vida -= 10
        if player.vida <= 0:
            Run = False 
        bum = Explo(j.rect.center)
        Tsprites.add(bum)
        SexplE.play()

    #colicion jugador - enemigo
    hits = pygame.sprite.spritecollide(player, enemigos , False)
    for hit in hits:
        player.vida -= 100 
        if player.vida <=0:
            explo2 = Explo(hit.rect.center)
            Tsprites.add(explo2)
            Run = False
    
    puntuacion(screen, str(score), 20, ScreenX // 2, 10)
    vida(screen,0,0 ,player.vida)


    clock.tick(60)
    pygame.display.flip()
    

pygame.quit()