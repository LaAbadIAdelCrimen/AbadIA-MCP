from fastmcp import FastMCP
from ctypes import cdll,c_int,c_char_p,c_size_t,create_string_buffer,sizeof,POINTER
import json
from typing import Annotated
from pydantic import Field

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
        print("AbadIA CONSTRUCTOR")
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
        print ("$$$"+tmp+"$$$")
        a=json.loads(tmp)
        print ("$$$"+str(a["Personajes"][1]["nombre"])+"$$$")
        print ("tipo tmp "+str(type(tmp))+" tipo a "+str(type(a)))
        return a

    def load(self,input):
        return self.lib.LibAbadIA_load(input)

    def save(self,result,resultMaxLength):
        return self.lib.LibAbadIA_save(result,resultMaxLength)

libAbadIA = AbadIA()
mcp= FastMCP(name="MCP Server La abadIA del crimen", instructions="Permite jugar a una emulación del videojuego clásico La abadía del crimen permitiendo enviar movimientos, comandos y cargar y grabar partidas para poner a prueba la resolución de tareas complejas de los agentes inteligentes. La ejecución se realiza paso a paso y en cada paso el agente recibe un JSON con un volcado de la información equivalente que vería un jugador en pantalla como las posiciones de los personajes, que frase está diciendo algún personaje, si está sonando algún sonido, en que pantalla se encuentra, el grado de avance en el juego o si la partida ha finalizado.") 

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

@mcp.tool()
def step(controles: Annotated[list[int], Field(description="Una lista representado pulsaciones de teclas con los siguientes posibles valores P1_UP , P1_LEFT, P1_DOWN, P1_RIGHT, P1_BUTTON1, P1_BUTTON2, P2_UP, P2_LEFT, P2_DOWN, P2_RIGHT, P2_BUTTON1, P2_BUTTON2, START_1, START_2, COIN_1, COIN_2, SERVICE_1, SERVICE_2, KEYBOARD_A, KEYBOARD_B, KEYBOARD_C, KEYBOARD_D, KEYBOARD_E, KEYBOARD_F, KEYBOARD_G, KEYBOARD_H, KEYBOARD_I, KEYBOARD_J, KEYBOARD_K, KEYBOARD_L, KEYBOARD_M, KEYBOARD_N, KEYBOARD_O, KEYBOARD_P, KEYBOARD_Q, KEYBOARD_R, KEYBOARD_S, KEYBOARD_T, KEYBOARD_U, KEYBOARD_V, KEYBOARD_W, KEYBOARD_X, KEYBOARD_Y, KEYBOARD_Z, KEYBOARD_0, KEYBOARD_1, KEYBOARD_2, KEYBOARD_3, KEYBOARD_4, KEYBOARD_5, KEYBOARD_6, KEYBOARD_7, KEYBOARD_8, KEYBOARD_9, KEYBOARD_SPACE, KEYBOARD_INTRO, KEYBOARD_SUPR, FUNCTION_1, FUNCTION_2, FUNCTION_3, FUNCTION_4, FUNCTION_5, FUNCTION_6, FUNCTION_7, FUNCTION_8, FUNCTION_9, FUNCTION_10, FUNCTION_11, FUNCTION_12) ")]) -> dict:
#def step(controles: Annotated[list[int], Field(description="Una lista representado pulsaciones de teclas, por ejemplo P1_UP para avanzar")]) -> dict:
    """ Avanza un paso en la simulación devolviendo un volcado equivalente a lo que un jugador humano vería en pantalla y escucharía por los altavoces."""
    global libAbadIA
#    print ("srvAA")
    libAbadIA.controles[:]=controles
    print ("srvBB")
#    return libAbadIA.step()
    tmp=libAbadIA.step()
#    print("tipo tmp "+str(type(tmp)))
    return tmp

if __name__ == "__main__":
#    context.abadIA = AbadIA()
#    mcp.run()-
    mcp.run(transport="streamable-http", host="0.0.0.0", port=4477,path="/abadIA",log_level="debug")
