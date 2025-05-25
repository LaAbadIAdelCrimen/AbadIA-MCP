import asyncio
import json
from fastmcp import Client
from ctypes import c_int

#client = Client("../mcp/abadIA-MCP.py")
client = Client("http://localhost:4477/mcp")

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

# Función para enviar los controles y obtener el estado actualizado
async def ejecutar_paso(acontroles):
    async with client:
        print ("A")
        control = [1,0,1]
        #response = await client.read_resource("game://estado/{control}")
        response = await client.call_tool("step",{"controles": acontroles})
        print("tipo response "+str(type(response)))
        print("tipo response[0] "+str(type(response[0])))
        print ("B")
        rd = json.loads(response[0].text)
        print ("***"+rd["Personajes"][1]["nombre"]+"***")
        # TODO falta control de errores y no probar siempre con Guillermo
        return rd

async def test_orientacion_guillermo():
    # 1. Primer paso sin pulsar nada
    controles_iniciales = [0] * 70  # Todas las teclas sin pulsar
    print ("1")
    estado1 = await ejecutar_paso(controles_iniciales)

    # Verificar que Guillermo inicia con orientación 0
    assert estado1["Personajes"][0]["id"] == 0, "El personaje esperado no tiene ID 0"
    assert estado1["Personajes"][0]["nombre"] == "Guillermo", "El nombre esperado no es Guillermo"
    assert estado1["Personajes"][0]["orientacion"] == 0, "La orientación inicial debería ser 0"

    # 2. Segundo paso con P1_LEFT activo
    controles_izquierda_1 = [0] * 70
    controles_izquierda_1[P1_LEFT] = 1
    print ("2")
    estado2 = await ejecutar_paso(controles_izquierda_1)

    # Verificar que la orientación cambia a 1
    assert estado2["Personajes"][0]["orientacion"] == 1, "La orientación debería ser 1 tras girar a la izquierda"

    # 3. Tercer paso con P1_LEFT activo de nuevo
    controles_izquierda_2 = [0] * 70
    controles_izquierda_2[P1_LEFT] = 1
    print ("3")
    estado3 = await ejecutar_paso(controles_izquierda_2)

    # Verificar que la orientación cambia a 2
    assert estado3["Personajes"][0]["orientacion"] == 2, "La orientación debería ser 2 tras girar nuevamente"

    print("✅ Todas las pruebas pasaron correctamente")

# Ejecutar el test
import asyncio
asyncio.run(test_orientacion_guillermo())

