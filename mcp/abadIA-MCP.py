from fastmcp import FastMCP
from ctypes import cdll,c_int,c_char_p,c_size_t,create_string_buffer,sizeof,POINTER
import json
from typing import Annotated
from pydantic import BaseModel,Field
#import gzip
#import base64

(P1_UP ,
P1_LEFT,
P1_DOWN,
P1_RIGHT,
P1_BUTTON1,
P1_BUTTON2,
P2_UP,
P2_LEFT,
P2_DOWN,
P2_RIGHT,
P2_BUTTON1,
P2_BUTTON2,
START_1,
START_2,
COIN_1,
COIN_2,
SERVICE_1,
SERVICE_2,
KEYBOARD_A,
KEYBOARD_B,
KEYBOARD_C,
KEYBOARD_D,
KEYBOARD_E,
KEYBOARD_F,
KEYBOARD_G,
KEYBOARD_H,
KEYBOARD_I,
KEYBOARD_J,
KEYBOARD_K,
KEYBOARD_L,
KEYBOARD_M,
KEYBOARD_N,
KEYBOARD_O,
KEYBOARD_P,
KEYBOARD_Q,
KEYBOARD_R,
KEYBOARD_S,
KEYBOARD_T,
KEYBOARD_U,
KEYBOARD_V,
KEYBOARD_W,
KEYBOARD_X,
KEYBOARD_Y,
KEYBOARD_Z,
KEYBOARD_0,
KEYBOARD_1,
KEYBOARD_2,
KEYBOARD_3,
KEYBOARD_4,
KEYBOARD_5,
KEYBOARD_6,
KEYBOARD_7,
KEYBOARD_8,
KEYBOARD_9,
KEYBOARD_SPACE,
KEYBOARD_INTRO,
KEYBOARD_SUPR,
FUNCTION_1,
FUNCTION_2,
FUNCTION_3,
FUNCTION_4,
FUNCTION_5,
FUNCTION_6,
FUNCTION_7,
FUNCTION_8,
FUNCTION_9,
FUNCTION_10,
FUNCTION_11,
FUNCTION_12) = range(69)


Controles = c_int * 70

class AbadIA(object):
    def __init__(self):
#        print("AbadIA CONSTRUCTOR")
        self.lib = cdll.LoadLibrary('./libAbadIA.so')
        self.lib.LibAbadIA_init()
        self.lib.LibAbadIA_step.restype = c_char_p
        #falta revisar tipo de controles
        self.lib.LibAbadIA_step.argtypes = [POINTER(c_int),c_char_p,c_size_t]
        self.lib.LibAbadIA_save.restype = c_char_p
        self.lib.LibAbadIA_save.argtypes = [c_char_p,c_size_t]
        self.lib.LibAbadIA_load.argtypes = [c_char_p]

        self.controles = Controles()

    def step(self):
        result = create_string_buffer(10000)
        tmp = self.lib.LibAbadIA_step(self.controles,result,sizeof(result)).decode()
        # TODO vaya manera fea de poner todo a cero de nuevo
        self.controles = Controles()
#        print ("$$$"+tmp+"$$$")
        a=json.loads(tmp)
#        print ("$$$"+str(a["Personajes"][1]["nombre"])+"$$$")
#        print ("tipo tmp "+str(type(tmp))+" tipo a "+str(type(a)))
        return a

    def load(self,input):
        return self.lib.LibAbadIA_load(input)

    def save(self,result,resultMaxLength):
        return self.lib.LibAbadIA_save(result,resultMaxLength)

mcpInstruction= """
Permite jugar a una emulación del videojuego clásico La abadía del crimen basándose en la reconstrucción en C++ (Vigasoco) por Manuel Abadía. 
Para facilitar el uso por un agente no se juega en tiempo real y cada vez que el agente envía un comando, el sistema devuelve una representación del juego tras avanzar un ciclo.
Se devuelve un JSON que muestra lo equivalente a lo que vería y oiría un jugador humano. Entre la información volcada se puede encontrar:
* La rejilla de pantalla de la que se puede interpretar los obstáculos y sitios por dónde no se puede pasar.
* La posición de cada personaje visible en pantalla, con sus coordenadas X e Y , orientación , altura y los objetos que tiene
* Los objetos visibles en pantalla
* El nivel de obsequium
* El día
* El momento del día
* El nivel de avance en el juego y si se ha fracasado o completado
* El número de pantalla
* La planta dentro del mapa 
* Los sonidos que están sonando en ese momento
* Las frases que están diciendo personajes en ese momento

Adicionalmente elvolcado del framebuffer de 640x200 pixeles se deja en c:\tmp\abadiaFB\screen.data. Es una imagen indexada y no RGB, es decir, el valor de cada pixel es el índice del color en la paleta. Los 128000 bytes se comprimen con gzip y se codifican en base 64 para poder incluirlos en el JSON. El agente deberá realizar los pasos inversos para recuperar la imagen. Aunque hay varias paletas en el día , por sencillez se puede usar siempre la paleta de día, cuyo volcado en raw lo tiene el agente en c:\tmp\abadiaFB\paletadia

El código original de La abadía del crimen es de Paco Menendez y los gráficos de Juan Delcán
"""

libAbadIA = AbadIA()
mcp= FastMCP(name="MCP Server La abadIA del crimen", instructions=mcpInstruction) 

#@mcp.tool()
#def greet(name: str) -> str:
#    global libAbadIA 
#    #return f"Hola, {name}!"+ " "+libAbadIA.step()
#    #return f"Hola, {name}!"+ "xxx "+libAbadIA.step()
#    paso1=libAbadIA.step()
#    libAbadIA.controles[P1_LEFT]=1
#    paso2=libAbadIA.step()
#    libAbadIA.controles[P1_LEFT]=1
#    paso3=libAbadIA.step()
#    return paso1 + "***" + paso2 + "***" + paso3

#@mcp.resource("game://estado/{controles}")
#def step(controles: list[int]) -> dict:
#    global libAbadIA
#    libAbadIA.controles[:]=controles
#    return libAbadIA.step()

#@mcp.resource("game://estado/")
#def step(controles: list[int]) -> dict:
#    return { "prueba": "test", "abc": "def" }

#@mcp.tool()
#def step(controles: list[int]) -> dict:
#    return { "prueba": "test", "abc": "def", "personajes": [ {"id": 0, "nombre": "Guillermo", "orientacion": 0} ] }

controlesDescription = """
Una lista representado pulsaciones de teclas. 
La simulación de la abadía del crimen se basa en una simulación genérica por lo que están disponibles todas las teclas de ordenadores o máquinas recreativas, aunque muchas no son necesarias para el juego en concreto.
La lista contiene los siguientes elmentos en orden:
P1_UP , equivalente a pulsar el cursor arriba o mover un joystick arriba
P1_LEFT, equivalente a pulsar el cursor izquierda o mover un joystick a la izquierda
P1_DOWN, equivalente a pulsar el cursor abajo o mover mover un joystick abajo
P1_RIGHT, equivalente a pulsar el cursor derecha o mover un joystick a la derecha
P1_BUTTON1, equivalente a pulsar la barra espaciadora o pulsar el botón principal de un joystick o mando
P1_BUTTON2, equivalente a pulsar el botón secundario de un joystick o mando
P2_UP, equivalente a que un segundo jugador pulse el cursor arriba o mueva su joystick o mando arriba
P2_LEFT, equivalente a que un segundo jugador pulse el cursor izquierda o mueva su joystick o mando a la izquierda
P2_DOWN, equivalente a que un segundo jugador pulse el cursor abajo o mueva su joystick o mando abajo
P2_RIGHT, equivalente a que un segundo jugador pules el  cursor derecha o mueva su joystick o mando a la derecha
P2_BUTTON1, equivalente a que un segundo jugador pulse el botón principal de su joystick o mando
P2_BUTTON2, equivalente a que un segundo jugador pulse el botón principal de su joystick o mando
START_1, equivalente a que se pulse el botón Start en el primer joystick o mando
START_2, equivalente a que se pulse el botón Start en el segundo joystick o mando
COIN_1, equivalente a que se introduzca una moneda en la primera ranura de la máquina emulada
COIN_2, equivalente a que se introduzca una moneda en la segunda ranura de la máquina emulada
SERVICE_1 , equivalente a que se pulse el primer botón de servicio en la máquina emulada (en abadIA sirve para acelerar y tener visionados más rápidos en la emulación en vez de mantener animaciones de personajes a su ritmo normal) 
SERVICE_2 , equivalente a que se pulse el segundo botón de servicio en la máquina emulada (en abadIA sirve para frenar y tener visionados más lentos en la emulación en vez de mantener animaciones de personajes a su ritmo normal) 
KEYBOARD_A, equivalente a pulsar la tecla A en el teclado
KEYBOARD_B, equivalente a pulsar la tecla B en el teclado
KEYBOARD_C, equivalente a pulsar la tecla C en el teclado
KEYBOARD_D, equivalente a pulsar la tecla D en el teclado
KEYBOARD_E, equivalente a pulsar la tecla E en el teclado
KEYBOARD_F, equivalente a pulsar la tecla F en el teclado
KEYBOARD_G, equivalente a pulsar la tecla G en el teclado
KEYBOARD_H, equivalente a pulsar la tecla H en el teclado
KEYBOARD_I, equivalente a pulsar la tecla I en el teclado
KEYBOARD_J, equivalente a pulsar la tecla J en el teclado
KEYBOARD_K, equivalente a pulsar la tecla K en el teclado
KEYBOARD_L, equivalente a pulsar la tecla L en el teclado
KEYBOARD_M, equivalente a pulsar la tecla M en el teclado
KEYBOARD_N, equivalente a pulsar la tecla N en el teclado
KEYBOARD_O, equivalente a pulsar la tecla O en el teclado
KEYBOARD_P, equivalente a pulsar la tecla P en el teclado
KEYBOARD_Q, equivalente a pulsar la tecla Q en el teclado
KEYBOARD_R, equivalente a pulsar la tecla R en el teclado
KEYBOARD_S, equivalente a pulsar la tecla S en el teclado
KEYBOARD_T, equivalente a pulsar la tecla T en el teclado
KEYBOARD_U, equivalente a pulsar la tecla U en el teclado
KEYBOARD_V, equivalente a pulsar la tecla V en el teclado
KEYBOARD_W, equivalente a pulsar la tecla W en el teclado
KEYBOARD_X, equivalente a pulsar la tecla X en el teclado
KEYBOARD_Y, equivalente a pulsar la tecla Y en el teclado
KEYBOARD_Z, equivalente a pulsar la tecla Z en el teclado
KEYBOARD_0, equivalente a pulsar la tecla 0 en el teclado
KEYBOARD_1, equivalente a pulsar la tecla 1 en el teclado
KEYBOARD_2, equivalente a pulsar la tecla 2 en el teclado
KEYBOARD_3, equivalente a pulsar la tecla 3 en el teclado
KEYBOARD_4, equivalente a pulsar la tecla 4 en el teclado
KEYBOARD_5, equivalente a pulsar la tecla 5 en el teclado
KEYBOARD_6, equivalente a pulsar la tecla 6 en el teclado
KEYBOARD_7, equivalente a pulsar la tecla 7 en el teclado
KEYBOARD_8, equivalente a pulsar la tecla 8 en el teclado
KEYBOARD_9, equivalente a pulsar la tecla 9 en el teclado
KEYBOARD_SPACE, equivalente a pulsar la barra espaciadora en el teclado
KEYBOARD_INTRO, equivalente a pulsar la tecla Intro o Return en el teclado
KEYBOARD_SUPR, equivalente a pulsar la tecla Supr para suprimir o borrar en el teclado
FUNCTION_1, equivalente a pulsar la tecla F1 en el teclado
FUNCTION_2, equivalente a pulsar la tecla F2 en el teclado
FUNCTION_3, equivalente a pulsar la tecla F3 en el teclado
FUNCTION_4, equivalente a pulsar la tecla F4 en el teclado
FUNCTION_5, equivalente a pulsar la tecla F5 en el teclado
FUNCTION_6, equivalente a pulsar la tecla F6 en el teclado
FUNCTION_7, equivalente a pulsar la tecla F7 en el teclado
FUNCTION_8, equivalente a pulsar la tecla F8 en el teclado
FUNCTION_9, equivalente a pulsar la tecla F9 en el teclado
FUNCTION_10, equivalente a pulsar la tecla F10 en el teclado
FUNCTION_11, equivalente a pulsar la tecla F11 en el teclado
FUNCTION_12 equivalente a pulsar la tecla F12 en el teclado

Así que si en la primera posición de la lista (correspondiente a P1_UP) se indica el valor 1, la emulación interpretará que se está pulsando esa tecla en ese ciclo. Si el valor es cero, la tecla no estaría pulsada.
Si, por ejemplo, el agente quiere pulsar la tecla F12, debe enviar un 1 al final de lal lista. 

Si no se quiere pulsar nada y simplemente avanzar un ciclo, la lista de Controles se debe pasar con todos los valores a cero.

La información e instrucciones con la que contaban los jugadores era:
Guillermo puede ser dirigido mediante tres teclas:

AVANZAR: (Cursor arriba) (Joystick arriba), A.

GIRO DERECHA: (Cursor dcha.) (Joystick dcha.), K.

GIRO IZQUIERDO: (Cursor izqda.) (Joystick izqda.), L.

Su novicio puede ser manejado, aunque sólo dentro de la pantalla en que se encuentra Guillermo con cualquiera de las siguientes teclas: (Cursor abajo) o Z.

Mientras se pulsa alguna de estas teclas, el novicio se dirigirá en la misma dirección en que mire Guillermo, a menos que se encuentre un obstáculo.

Para coger objetos basta con colocarse enfrente de éstos. Guillermo puede recoger seis objetos y su novicio otros dos distintos. Para dejar los objetos se puede pulsar espacio o bien Joystick abajo, dejándose siempre el objeto que aparece más a la izquierda en el marcador, en el que sólo aparecen los objetos que lleva Guillermo y son los únicos que se pueden dejar.

"""

momentoDiaDescription="""
Un valor representando la hora en el juego siguiendo los valores propios de un monasterio medieval
0 NONA
1 PRIMA
2 TERCIA
3 SEXTA
4 NONA
5 VISPERAS
6 COMPLETAS
"""

obsequiumDescription="""
El agente debe aprender a interpretar este valor y su relevancia en el juego como haría cualquier otro jugador humano
"""

numeroRomanoDescription="""
El agente debe ignorar este valor, que es necesario para cargar y grabar partidas, pero al que un jugador humano no tendría acceso sin hacer trampas
"""

haFracasadoDescription="""
Indica que la investigación ha fracasado y la partida ha terminado. El agente debe entender que recibir este valor es equivalente a que un jugador humano viese la pantalla de 'Game Over' o fin de juego. Solo puede pulsar espacio en la siguiente iteracion para empezar de nuevo y volver a intentarlo. Alternativamente, si ha guardado un punto de situación, el agente podría preferir cargarlo y continuar desde ahí sin empezar desde el principio.
"""

investigacionCompletaDescription="""
Si investigacionCompleta es true, el agente ha conseguido finalizar el juego con el 100% de avance y habrá cumplido un hito histórico en la evolución de la inteligencia artificial
"""

porcentajeDescription="""
Indica el porcentaje de avance en la investigación y sirve al agente como referencia de que ha avanzado y que las acciones realizadas han tenido recompensa. Un humano solo tendría acceso a este valor cuando una partida acaba, bien por investigacionCompleta o por haFracasado. Así que el agente, por ahora, tiene cierta ventaja sobre un humano
"""

numPantallaDescription="""
Un humano puede ver la pantalla y en base a los gráficos saber en que pantalla o zona de la abadía está. Este númoro proporciona al agente el número de pantalla interno para que pueda identificar en que pantalla está sin analizar los pixeles de la emulación
"""

plantaDescription="""
Un humano puede interpretar que sube o baja plantas en el mapa de la abadía al ver que los personajes usan escaleras y componer un mapa mental de la abadía. Aunque con el numPantalla es más que suficiente, damos este valor al agente para ayudarle a tener un mayor contexto de la posición en el juego
"""

sonidosDescription="""
Es un array JSON donde si un elemnto vale 1 ese sonido está sonando en el momento del volcado.
Asi evitamos que el agente tenga que procesar wavs con el sonido proveniente de la emulación en cada paso.

El primer elemento del array (índice 0) indica si se escucha abrir una puerta
El segundo elemento del array (índice 1) indica si se escucha aporrear una puerta
El tercer elemento del array (índice 2) indica si se escuchan campanadas
El cuarto elemento del array (índice 3) indica si se escucha cerrar una puerta
El quinto elemento del array (índice 4) representa el efecto de sonido al recoger un objeto
El sexto elemento del array (índice 5) representa el efecto de sonido al dejar un objeto
El séptimo elemento del array (índice 6) indica que algo ha cambiado en la pantalla
El octavo elemento del array (índice 7) indica que suena la melodia de fin de juego
El noveno elemento del array (índice 8) indica que suena una melodía de fondo
El décimo elemento del array (índice 9) indica que suena la melodía de inicio del juego
El undécimo elemento del array (índice 10) indica que se escucha un tintineo

La lista tiene tamaño fijo por lo que siempre se manda el estado de todos los sonidos, al contrario que en la lista de frases que solo se mandan las activas. 
Se pasa como lista por compatibilidad con la emulación con interfaz HTTP, pero en MCP se devuelve un volcado cada vez que se ejecuta una iteración, así que solo debería aparecer un elemento a la vez
"""
frasesDescription="""
Es un array JSON con una lista de frases. Si un elemnto aparece es porquue esa frase está apareciendo por pantalla o ha aparecido desde el último volcado.
Asi evitamos que el agente tenga que interpretar los pixeles de la pantalla

Por ejemplo, si el array JSON indica "frases": [ 0, 2]
entonces la frase "SECRETUM FINISH..." y la frase "TEMO QUE UNO DE LOS MONJES ..." han aparecido en pantalla desde el último volcado.

Al contrario que la lista de sonidos, esta lista es dinámica y tendrás más o menos elementos según las frases que hayan aparecido. Se devuelve como lista por compatibilidad con la emulación visual . En la versión MCP se hace un volcado tras cada paso o iteración en el bucle principal de juego, así que como mucho solo habrá un elemento en la lista

Las frases por orden son:
"SECRETUM FINISH AFRICAE, MANUS SUPRA XXX AGE PRIMUM ET SEPTIMUM DE QUATOR",
"BIENVENIDO A ESTA ABADIA, HERMANO. OS RUEGO QUE ME SIGAIS. HA SUCEDIDO ALGO TERRIBLE",
"TEMO QUE UNO DE LOS MONJES HA COMETIDO UN CRIMEN. OS RUEGO QUE LO ENCONTREIS ANTES DE QUE LLEGUE BERNARDO GUI, PUES NO DESEO QUE SE MANCHE EL NOMBRE DE ESTA ABADIA",
"DEBEIS RESPETAR MIS ORDENES Y LAS DE LA ABADIA. ASISTIR A LOS OFICIOS Y A LA COMIDA. DE NOCHE DEBEIS ESTAR EN VUESTRA CELDA",
"DEJAD EL MANUSCRITO DE VENACIO O ADVERTIRE AL ABAD",
"DADME EL MANUSCRITO, FRAY GUILLERMO",
"LLEGAIS TARDE, FRAY GUILLERMO",
"ESTA ES VUESTRA CELDA, DEBO IRME",
"OS ORDENO QUE VENGAIS",
"DEBEIS ABANDONAR EL EDIFICIO, HERMANO",
"ADVERTIRE AL ABAD",
"DEBEMOS IR A LA IGLESIA, MAESTRO",
"DEBEMOS IR AL REFECTORIO, MAESTRO",
"PODEIS IR A VUESTRAS CELDAS",
"NO HABEIS RESPETADO MIS ORDENES. ABANDONAD PARA SIEMPRE ESTA ABADIA",
"ESCUCHAD HERMANO, HE ENCONTRADO UN EXTRAÑO LIBRO EN MI CELDA",
"ENTRAD EN VUESTRA CELDA, FRAY GUILLERMO",
"HA LLEGADO BERNARDO, DEBEIS ABANDONAR LA INVESTIGACION",
"¿DORMIMOS?, MAESTRO",
"DEBEMOS ENCONTRAR UNA LAMPARA, MAESTRO",
"VENID AQUI, FRAY GUILLERMO",
"HERMANOS, VENACIO HA SIDO ASESINADO",
"DEBEIS SABER QUE LA BIBLIOTECA ES UN LUGAR SECRETO. SOLO MALAQUIAS PUEDE ENTRAR. PODEIS IROS",
"OREMOS",
"HERMANOS, BERENGARIO HA DESAPARECIDO. TEMO QUE SE HAYA COMETIDO OTRO CRIMEN",
"PODEIS COMER, HERMANOS",
"HERMANOS, HAN ENCONTRADO A BERENGARIO ASESINADO",
"VENID, FRAY GUILLERMO, DEBEMOS ENCONTRAR A SEVERINO",
"DIOS SANTO... HAN ASESINADO A SEVERINO Y LE HAN ENCERRADO",
"BERNARDO ABANDONARA HOY LA ABADIA",
"MAÑANA ABANDONAREIS LA ABADIA",
"ERA VERDAD, TENIA EL PODER DE MIL ESCORPIONES",
"MALAQUIAS HA MUERTO",
"SOIS VOS, GUILERMO... PASAD, OS ESTABA ESPERANDO. TOMAD, AQUI ESTA VUESTRO PREMIO",
"ESTAIS MUERTO, FRAY GUILLERMO, HABEIS CAIDO EN LA TRAMPA",
"VENERABLE JORGE, VOIS NO PODEIS VERLO, PERO MI MAESTRO LLEVA GUANTES. PARA SEPARAR LOS FOLIOS TENDRIA QUE HUMEDECER LOS DEDOS EN LA LENGUA, HASTA QUE HUBIERA RECIBIDO SUFICIENTE VENENO",
"SE ESTA COMIENDO EL LIBRO, MAESTRO",
"DEBEIS ABANDONAR YA LA ABADIA",
"ES MUY EXTRAÑO, HERMANO GUILLERMO. BERENGARIO TENIA MANCHAS NEGRAS EN LA LENGUA Y EN LOS DEDOS",
"PRONTO AMANECERA, MAESTRO",
"LA LAMPARA SE AGOTA",
"HABEIS ENTRADO EN MI CELDA",
"SE HA AGOTADO LA LAMPARA",
"JAMAS CONSEGUIREMOS SALIR DE AQUI",
"ESPERAD, HERMANO",
"OCUPAD VUESTRO SITIO, FRAY GUILLERMO",
"ES EL COENA CIPRIANI DE ARISTOTELES. AHORA COMPRENDEREIS POR QUE TENIA QUE PROTEGERLO. CADA PALABRA ESCRITA POR EL FILOSOFO HA DESTRUIDO UNA PARTE DEL SABER DE LA CRISTIANDAD. SE QUE HE ACTUADO SIGUIENDO LA VOLUNTAD DEL SEÑOR... LEEDLO, PUES, FRAY GUILLERMO. DESPUES TE LO MOSTRARE A TI MUCHACHO",
"FUE UNA BUENA IDEA ¿VERDAD?; PERO YA ES TARDE",
"QUIERO QUE CONOZCAIS AL HOMBRE MAS VIEJO Y SABIO DE LA ABADIA",
"VENERABLE JORGE, EL QUE ESTA ANTE VOS ES FRAY GUILLERMO, NUESTRO HUESPED",
"SED BIENVENIDO, VENERABLE HERMANO; Y ESCUCHAD LO QUE OS DIGO. LAS VIAS DEL ANTICRISTO SON LENTAS Y TORTUOSAS. LLEGA CUANDO MENOS LO ESPERAS. NO DESPERDICIEIS LOS ULTIMOS DIAS",
"LO SIENTO, VENERABLE HERMANO, NO PODEIS SUBIR A LA BIBLIOTECA",
"SI LO DESEAIS, BERENGARIO OS MOSTRARA EL SCRIPTORIUM",
"AQUI TRABAJAN LOS MEJORES COPISTAS DE OCCIDENTE",
"AQUI TRABAJABA VENACIO",
"VENERABLE HERMANO, SOY SEVERINO, EL ENCARGADO DEL HOSPITAL. QUIERO ADVERTIROS QUE EN ESTA ABADIA SUCEDEN COSAS MUY EXTRAÑAS. ALGUIEN NO QUIERE QUE LOS MONJES DECIDAN POR SI SOLOS LO QUE DEBEN SABER"
"""

idPersonajeDescription="""
El identificador interno del personaje en el juego. El agente no debería mirarlo porque un jugador humano no tendría acceso a esta información y sería trampa. 

En su lugar debería mirar el nombre del personaje. Pero se envía por compatibilidad con el formato para cargar y grabar partidas
"""

nombrePersonajeDescription="""
El nombre del personaje visible en pantalla
"""

alturaPersonajeDescription="""
La altura del personaje ya que el juego se representa en pantalla con vista isométrica para conseguir un efecto pseudo3D
"""

orientacionPersonajeDescription="""
La orientación del personaje para saber dónde está mirando 
"""

objetosDescription="""
Este atributo solo viene relleno en el caso de Guillermo y Adso. Un jugador humano no puede conocer que objetos tienen otros personajes y el agente o cliente MCP tampoco. 

Cada objeto tiene un valor 
	LIBRO = 0x80,
	GUANTES = 0x40,
	GAFAS = 0x20,
	PERGAMINO = 0x10,
	LLAVE1 = 0x08,
	LLAVE2 = 0x04,
	LLAVE3 = 0x02,
	LAMPARA = 0x01

Son valores que se pueden combinar a nivel de bits. Así, si objetos vale 0x81, el personaje tendrá tanto el libro como la lámpara. Y si vale 0x24, tendrá las gafas y la llave 2.

"""

class dumpPersonaje(BaseModel):
    """
    Atributos de un personaje
    id, nombre, posX, posY, orientacion y objetos
    En el caso de Guillermo y Adso también se indican los objetos que poseen
    """
    id: Annotated[int, Field(description=idPersonajeDescription)]
    nombre: Annotated[str, Field(description=nombrePersonajeDescription)]
    posX: Annotated[int, Field(description="La posición en el eje X del personaje en pantalla")]
    posY: Annotated[int, Field(description="La posición en el eje Y del personaje en pantalla")]
    altura: Annotated[int, Field(description=alturaPersonajeDescription)]
    orientacion: Annotated[int, Field(description=orientacionPersonajeDescription)]
    objetos: Annotated[int, Field(description=objetosDescription)]
    
idObjetoDescription="""
El objeto 0 es el libro
El objeto 2 son los guantes
El objeto 3 son las gafas
El objeto 4 es el pergamino
El objeto 5 es la llave
El objeto 6 es desconocido
El objeto 7 es desconocido
El objeto 8 es la lámpara
"""


class dumpObjetos(BaseModel):
    """
    Atributos de un objeto visible en pantalla
    """
    id: Annotated[int, Field(description=idObjetoDescription)]
    posX: Annotated[int, Field(description="La posición en el eje X del objeto en pantalla")]
    posY: Annotated[int, Field(description="La posición en el eje Y del objeto en pantalla")]
    altura: Annotated[int, Field(description="La altura del objeto")]
    orientacion: Annotated[int, Field(description="La orientación del objeto")]

class dumpAbadIA(BaseModel):
    dia: Annotated[int, Field(description="Día en el juego")]
    momentoDia: Annotated[int, Field(description=momentoDiaDescription)]
    obsequium: Annotated[int, Field(description=obsequiumDescription)]
    numeroRomano: Annotated[int, Field(description=numeroRomanoDescription)]
    haFracasado: Annotated[bool, Field(description=haFracasadoDescription)]
    investigacionCompleta: Annotated[bool, Field(description=investigacionCompletaDescription)]
    porcentaje: Annotated[int, Field(description=porcentajeDescription)]
    numPantalla: Annotated[int, Field(description=numPantallaDescription)]
    planta: Annotated[int, Field(description=plantaDescription)]
    sonidos: Annotated[list[int], Field(description=sonidosDescription)]
    frases: Annotated[list[int], Field(description=frasesDescription)]
    personajes: Annotated[list[dumpPersonaje], Field(description="Lista de personajes visibles en pantalla")]
    objetos: Annotated[list[dumpObjetos], Field(description="Lista de objetos visibles en pantalla")]
    rejilla: Annotated[list[list[int]], Field(description="Volcado del buffer de alturas de 24x24 de la pantalla")]
#    rawFrameBuffer: Annotated[str , Field(description="volcado de los 640x200 bytes del framebuffer,con cada valor representando el indice en la paleta de 256 colores del juego. Para pasarlo en json los 128000 bytes son comprimidos con gzip y luego transformados en base64. Para recuperar la imagen se tiene que pasar de base64 a binario y luego descomprimir con gzip")]

@mcp.tool()
def multistep(listaControlesxPaso: Annotated[list[list[int]], Field(description="lista de lista de controles")]) -> list[dict]:
    """ Avanza n pasos en la simulación. Recibe una lista de lista de controles, usando un elemento para 
    cada iteracion
    si, por ejemplo, recibe una lista de 3 elemntos, el primer elemento (a su vez una lista de controles) se
    usará en el primer paso, la segunda lista en la segunda y la tercera lista en la tercera

    Igualmente devuelve una lista de resultados, una por cada paso, para que el agente pueda ver los
    resultados parciales conforme se ha ido ejecutando cada paso
    """
    resultados=[]
    for sublist in listaControlesxPaso:
              resultado = step(sublist)
              resultados.append(resultado)

    return resultados

@mcp.tool()
def step(controles: Annotated[list[int], Field(description=controlesDescription)]) -> dict:
    """ Avanza un paso en la simulación devolviendo un volcado equivalente a lo que un jugador humano vería en pantalla y escucharía por los altavoces."""
    global libAbadIA
    libAbadIA.controles[:]=controles
    tmp=libAbadIA.step()
#    with open("/tmp/screen.raw",'rb') as f_in:
#        compressed_data=gzip.compress(f_in.read())
#        encoded_data=base64.b64encode(compressed_data).decode('utf-8')
#    tmp["rawFrameBuffer"]=encoded_data
#    print("tipo tmp "+str(type(tmp)))
#    d=json.loads(tmp)
#    j=json.dumps(tmp)
#    return j 
#    return d 
    return tmp

if __name__ == "__main__":
    mcp.run()
#    mcp.run(transport="streamable-http", host="0.0.0.0", port=4477,path="/abadIA",log_level="debug")
