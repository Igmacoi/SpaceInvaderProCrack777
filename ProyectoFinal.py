
import pygame,sys,random

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

#Se define el color par que sea trasparente  
CoInvi = (255, 174, 201) #Color salmon

#crea la ventana
screen = pygame.display.set_mode((ScreenX, ScreenY)) 

#Se crea una variable para luego llamarla en el while principal 


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

    #entrada self -Es una instancia para llamar al objetoSS
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




#-------------------------
# MENU
#-------------------------



class Opcion:

#Entrada  self       - Es una instancia para llamar al objeto
#         fuente     - Fuente de letra
#         titulo     - Lo que ira escrito en cada opcion    
#         x          - coordenada en x
#         y          - coordenada en y
#   funcion_asignada - La funcion que le daremos a cada opcion del menu 
#Salida

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (255, 255, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

#Entrada  self       - Es una instancia para llamar al objeto

    def update(self):
## AJUSTE POSICION TEXTO EJE X
        destino_x = 140
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

#Entrada  self   - Es una instancia para llamar al objeto
#         screen - Referencia a la pantalla

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

#Entrada  self  - Es una instancia para llamar al objeto
## Sirve parar asignar una funcion a una opcion del menu
    def activar(self):
        self.funcion_asignada()


class Cursor:
#Entrada: self - Es una instancia para llamar al objeto
#         x    - coordenada en x
#         y    - coordenada en y
#         dy   - distancia entre puntos en el eje y

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('menu/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

#Entrada: self - Es una instancia para llamar al objeto
    def update(self):
## Velocidad en la que se mueve entre cada espacio
        self.y += (self.to_y - self.y) / 15.0
        self.rect.y = int(self.y)

#Entrada: self   - Es una instancia para llamar al objeto
#         indice - indice de las lista "opciones"

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

#Entrada  self   - Es una instancia para llamar al objeto
#         screen - Referencia a la pantalla

## Pintamos el cursor por pantalla
    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    ## AJUSTES DE POSICION DEL TEXTO DEL MENU

#Entrada  self   - Es una instancia para llamar al objeto
#         opciones - lista de las opciones

    def __init__(self, opciones):
        self.opciones = []
    ## INDICAMOS DONDE ESTA LA FUENTE DE LA LETRAS QUE USAREMOS Y TAMBIEN EL TAMAÑO QUE ESTA TENDRA
        fuente = pygame.font.Font('menu/dejavu.ttf', 80)
    ## POSICION EJE X CURSOR ANIMACION
        x = 155
    ## POSICION EJE Y TEXTO
        y = 350
        paridad = 1
    ## AJUSTES DEL MOVIMIENTO DE LA ANIMACION DE CURSOR
        self.cursor = Cursor(x - 65, y, 85)

## INDICAMOS EL ESPACIO ENTRE LINEAS DE TEXTO 
## Creamos un bluqle for para que funcione en cada momento la estructura del menu
        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 85
      
        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

#Entrada  self   - Es una instancia para llamar al objeto

    def update(self):
        """Altera el valor de 'self.seleccionado' con los direccionales."""

        keys = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if keys[pygame.K_UP]:
                self.seleccionado -= 1
            elif keys[pygame.K_DOWN]:
                self.seleccionado += 1
            elif keys[pygame.K_RETURN]:
                # Invoca a la función asociada a la opción.
                self.opciones[self.seleccionado].activar()

        ## procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        ## indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RETURN]

        self.cursor.update()
## Creamos un bluqle for para que funcione siempre el movimiento del cursor
        for o in self.opciones:
            o.update()

#Entrada  self   - Es una instancia para llamar al objeto
#         screen - Referencia a la pantalla

    def imprimir(self, screen):

## Imprimimos el cursor por pantalla
        self.cursor.imprimir(screen)
## Creamos un bluqle for para mostrarlo siempre en pantalla
        for opcion in self.opciones:
            opcion.imprimir(screen)


## designamos la opcion jugar

def comenzar_juego():
    fondo = pygame.image.load("cosas/Fondo.png").convert()

#rango de aparicion de los enemigos
    for x in range(20):
        enemi = Enemigos(20,20) 
        enemigos.add(enemi)
        Tsprites.add(enemi)

#para el While, True es para que se mantenga activo
    y = 0 
    Run = True
#El score empieza en 0
    score = 0

    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.disparo() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Run = False
                    
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

## definimos la opcion salir
## usamos la libreria sys para cerrar el programa
def salir_del_programa():
    print (" Gracias por utilizar este programa.")
    sys.exit(0)


## Designamos todo lo que ira escrito en el menu y llamamos las funciones antes creadas
## Las funciones funcionaran dependiendo de la opcion que el usuario elija en el menu
    
salir = False
opciones = [
    ("JUGAR", comenzar_juego),
    ("SALIR", salir_del_programa)
    ]

pygame.font.init()
screen = pygame.display.set_mode((500, 700))
fondo = pygame.image.load("menu/fondomenu.png").convert()
menu = Menu(opciones)

while not salir:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            salir = True

    screen.blit(fondo, (0, 0))
    menu.update()
    menu.imprimir(screen)

    pygame.display.flip()
    pygame.time.delay(10)



pygame.quit()