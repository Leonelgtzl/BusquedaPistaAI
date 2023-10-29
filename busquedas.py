import random
import pygame, sys
from pygame.locals import *

'''
Título: Búsqueda en pista tipo espina de pescado.

Equipo 2:
Leonel Gutiérrez
Jese  
Ángel Hernández
Ángel González
 
28/10/2023 

Resumen: 
En uno de los extremos de las costillas, se coloca aleatoriamente el objetivo (tesoro).
El agente (móvil), debe de recorrer las rutas (líneas) para encontrar el objetivo.
Al localizar el objetivo, se desplaza directamente a la meta.
'''

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LILA = (174, 83, 255)
YELLOW = (245, 255, 83)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Búsqueda en Pista")
fuente = pygame.font.SysFont('Arial Black', 30)
texto = fuente.render('T', True, YELLOW)

tesoro_icon = pygame.image.load("tesoro2.png") 
tesoro_juego = pygame.image.load("tesoro1.png")
agente_icon = pygame.image.load("agentef.png")
pygame.display.set_icon(tesoro_icon)

agente = [0,0]
x, y = 0, 0
rectangulo_agente = None

pista = None
encontrado = False
memoria_agente = [[0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0]]


# Esta función se centrará en ubicar todas las lineas y círculos de la pista 
def crear_grafica(tesoro): 
    #Esta pista está constituida por una vértebra que la cruzan cuatro costillas.
    #En un extremo de la vértebra está el inicio y en el lado contrario estará ubicada la meta.
    vertebra = pygame.draw.line(window, WHITE, (100, WINDOW_HEIGHT/2), (800, WINDOW_HEIGHT/2), 4) 
    circulo_inicial = pygame.draw.circle(window, WHITE, (100,WINDOW_HEIGHT/2), 10, 0) # inicio
    circulo_final = pygame.draw.circle(window, WHITE, (800,WINDOW_HEIGHT/2), 10, 0) # meta
    
    if tesoro[1] == 0:
        tesoro_y = 1
        ajuste = -45
    else:
        tesoro_y = 2
        ajuste = 10
    
    # Colocamos el icono de nuestro tesoro dentro del juego de manera aleatoria
    window.blit(tesoro_juego, (WINDOW_WIDTH/6 * tesoro[0] + 63, WINDOW_HEIGHT/3 * tesoro_y + ajuste))

    # Utilizando un ciclo for recorreremos las filas de nuestra pista
    for x in range(1,5):
        
        #Cada línea ocupara ciertas coordenadas dependiendo del número de columna que sea
        pygame.draw.line(window, LILA, ((WINDOW_WIDTH/6 * x + 80), WINDOW_HEIGHT/3), ((WINDOW_WIDTH/6 * x + 80), WINDOW_HEIGHT/3 *2), 4)

        #Con este ciclo for anidado daremos los circulos ubicados en nuestras costillas 
        for y in range(1,4):
            match y:
                case 1:
                    pygame.draw.circle(window, WHITE, (WINDOW_WIDTH/6 * x + 80,WINDOW_HEIGHT/3), 10, 0)
                    
                case 2:
                    pygame.draw.circle(window, WHITE, (WINDOW_WIDTH/6 * x + 80,WINDOW_HEIGHT/2), 10, 0)
                    
                case 3:
                    pygame.draw.circle(window, WHITE, (WINDOW_WIDTH/6 * x + 80,WINDOW_HEIGHT/3 * 2), 10, 0)

              
# Esta función servirá unicamente para darnos la matriz que representará nuestra pista 
def crear_pista():
    pista = [[0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0]]
    
    #Podemos observar que hay una matriz pista y otra memoria_agente. Estrcturalmente son las mismas, sin embargo, como
    # se pide en las indicaciones, el agente no debe de saber donde se ubica el tesoro. Por lo que opté por utilizar
    #Una matriz unicamente para la logica de movimientos del agente, y la otra para el almacenamiento de info. del mismo
    
    # El inicio será en la primera fila/columna
    pista[0][0] = 'I'
    memoria_agente [0][0] = 'I'
    
    # La meta está colocada en la última fila
    pista[5][0] = 'M' 
    memoria_agente [5][0] = 'M'
    
    tesoro_fila = 0
    tesoro_columna = None
    
    # El siguiente ciclo while nos dará la columna donde se ubicará el tesoro, todo esto de forma aleatoria
    while tesoro_fila == 0 or tesoro_columna == None:
        if tesoro_fila == 0:
            tesoro_fila = random.randint(1, 4)
        
        if tesoro_columna == None:
            tesoro_columna = random.randint(0, 2)
            if tesoro_columna == 1:
                tesoro_columna = None
    
    tesoro_coords = [tesoro_fila, tesoro_columna]
    pista[tesoro_fila][tesoro_columna] = 'T'

    return pista, tesoro_coords


# La siguiente función colocará el icono del agente conforme su ubicación en la matriz utilizando la info. de
# los parametros dados.
def colocar_objetos(agente, tesoro):
    
    if agente[0] == 0:
        x, y = 73, WINDOW_HEIGHT/2 - 38
        window.blit(agente_icon, (x, y))
        #pygame.draw.rect(window, RED, (x , y, 60,40))
    else:
        #La coordenadas actualizadas se darán con ayuda de la posición del agente
        
        if agente[0] == 5:
            x = WINDOW_WIDTH/6 * agente[0] + 20 
        else:
            x = WINDOW_WIDTH/6 * agente[0] + 48 
        
        match agente[1]:
            case 0:
                y = WINDOW_HEIGHT/3 - 38
                
            case 1:
                y = WINDOW_HEIGHT/2 - 38
                
            case 2:
                y = WINDOW_HEIGHT/3 * 2 - 38
        
        # Teniendo las nuevas coordenadas, actualizaremos nuestra pantalla
        window.fill(BLACK)
        crear_grafica(tesoro)
        window.blit(agente_icon, (x, y))
        
        #rectangulo_agente = pygame.Rect(x , y, 60,40)
        #pygame.draw.rect(window, RED, rectangulo_agente)

     
# La función encargada del movimiento del agente y las acciones a tomar conforme la posición de este mismo
def movimiento_busqueda(pista, memoria, agente, tesoro, encontrado):
    
    # En caso de que haya iniciado el juego:
    if agente[0] == 0:
        memoria_agente[agente[0]][agente[1]] = 1
        agente = [1,1]
    elif agente[0] == 5:
            print('HA TERMINADO EL JUEGO.')
            agente[1] = 1
            colocar_objetos(agente, tesoro)
            pygame.display.update() 
            pygame.time.delay(1000)
            sys.exit()
    else:
        # Comenzamos verificando si el tesoro ha sido encontrado. 
        if encontrado:
            if pista[agente[0]][agente[1]] == 'T': 
                memoria_agente[agente[0]][agente[1]] = 'T'
            else: 
                memoria_agente[agente[0]][agente[1]] = 1
                
            if agente[1] != 1:
                agente[1] = 1
            else:
                if agente[0] == 4:
                    agente[1] = 0
                agente[0] += 1 
            
            # Si se encontró el tesoro daremos el siguiente mensaje
            window.blit(fuente.render('SE LOCALIZÓ EL TESORO!!', True, WHITE, RED), (WINDOW_WIDTH/5 ,100))
        else:
            
            # Actualizamos la memoria del agente para así poder reunir la información
            memoria_agente[agente[0]][agente[1]] = 1
            match agente[1]:
                # Aquí veremos la columna en la que se encuentra el agente
                # Si está en la columna 0, volveremos a la columna 1
                case 0:
                    agente[1] = 1
                
                # Si está en la columna 1, verificaremos algunas condiciones para ver el siguiente movimiento
                case 1:
                    if memoria_agente[agente[0]][2] == 1 and memoria_agente[agente[0]][0] != 1:
                        agente[1] = 0
                    elif memoria_agente[agente[0]][2] != 1 and memoria_agente[agente[0]][0] == 1:
                        agente[1] = 2
                    elif memoria_agente[agente[0]][0] == 0 and memoria_agente[agente[0]][2] == 0:
                        while agente[1] == 1:
                            agente[1] = random.randint(0, 2)
                    else:
                        agente[0] += 1
                # Al igual que en la columna 0, si está en la columna 2 se devolverá a la columna 1   
                case 2:
                    agente[1] = 1
                    
    #Verificamos si la coordenada del agente coincide con la del tesoro                
    if agente[0] == tesoro[0] and agente[1] == tesoro[1]:
        print('SE LOCALIZÓ EL TESORO!!')
        encontrado = True  
    
    memoria_agente[agente[0]][agente[1]] = 'A'
    
    return memoria, agente, encontrado


while True:
    
    # Si la pista todavía no exite, quiere decir que apenas comenzaremos el juego
    if pista == None:
        pista, tesoro = crear_pista()
        crear_grafica(tesoro)     
    else:
        # En caso de que exista la pista, sólo haremos nuestros movimientos y actualizaciones de pantallas
        colocar_objetos(agente, tesoro)
        pista, agente, encontrado = movimiento_busqueda(pista, memoria_agente,agente, tesoro, encontrado)
    
    # Si se busca salir del juego antes de que termine podemos simplemente darle a la x de la ventana
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Imprimimos la memoria del agente para ver la información almacenada del mismo
    # Esto se hará en la consola. 
    for fila in memoria_agente:
        print(fila, end= '  ')
    print('\n')
    
    # Actualizamos la pantalla
    pygame.display.update() 
    
    pygame.time.delay(1000)  # Retraso para ver el estado inicial
