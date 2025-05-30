from fastmcp import FastMCP
from ctypes import cdll,c_int,c_char_p,c_size_t,create_string_buffer,sizeof,POINTER
import json
from typing import Annotated, List, Optional, Dict, Any
from pydantic import BaseModel,Field
from enum import Enum

# Constantes de control (copiadas del original)
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

# Enums para mayor claridad
class Orientacion(Enum):
    DERECHA = 0  # Este
    ABAJO = 1    # Sur
    IZQUIERDA = 2  # Oeste
    ARRIBA = 3   # Norte

class Accion(Enum):
    AVANZAR = "avanzar"
    GIRAR_DERECHA = "girar_derecha"
    GIRAR_IZQUIERDA = "girar_izquierda"
    CONTROLAR_ADSO = "controlar_adso"
    DEJAR_OBJETO = "dejar_objeto"
    ESPERAR = "esperar"

class TipoObjeto(Enum):
    LIBRO = 0x80
    GUANTES = 0x40
    GAFAS = 0x20
    PERGAMINO = 0x10
    LLAVE1 = 0x08
    LLAVE2 = 0x04
    LLAVE3 = 0x02
    LAMPARA = 0x01

# Wrapper optimizado de AbadIA
class AbadIAOptimizada(object):
    def __init__(self):
        self.lib = cdll.LoadLibrary('./libAbadIA.so')
        self.lib.LibAbadIA_init()
        self.lib.LibAbadIA_step.restype = c_char_p
        self.lib.LibAbadIA_step.argtypes = [POINTER(c_int),c_char_p,c_size_t]
        self.lib.LibAbadIA_save.restype = c_char_p
        self.lib.LibAbadIA_save.argtypes = [c_char_p,c_size_t]
        self.lib.LibAbadIA_load.argtypes = [c_char_p]
        self.controles = Controles()
        
        # Estado para optimizaciones
        self.ultimo_estado = None
        self.posicion_guillermo = None
        self.orientacion_guillermo = None

    def step_basico(self, controles_lista=None):
        """Ejecuta un paso básico con controles opcionales"""
        if controles_lista:
            self.controles[:] = controles_lista
        else:
            # Limpiar todos los controles
            self.controles = Controles()
            
        result = create_string_buffer(10000)
        tmp = self.lib.LibAbadIA_step(self.controles, result, sizeof(result)).decode()
        self.controles = Controles()  # Limpiar para el siguiente paso
        
        estado = json.loads(tmp)
#        print("estado step basico "+tmp)
        self.ultimo_estado = estado
        
        # Actualizar posición y orientación de Guillermo (usar nombres clave correctos)
        for personaje in estado.get('Personajes', estado.get('personajes', [])):
            if personaje.get('nombre') == 'Guillermo':
                self.posicion_guillermo = (personaje['posX'], personaje['posY'])
                self.orientacion_guillermo = personaje['orientacion']
                break
        
        # Si no se encontró Guillermo, mantener valores por defecto
        if self.posicion_guillermo is None:
            self.posicion_guillermo = (136, 168)  # Posición inicial conocida
        if self.orientacion_guillermo is None:
            self.orientacion_guillermo = 0  # Orientación inicial
                
        return estado

    def ejecutar_accion_simple(self, accion: Accion, duracion: int = 1):
        """Ejecuta una acción simple por la duración especificada"""
        controles_base = [0] * 70
        
        if accion == Accion.AVANZAR:
            controles_base[P1_UP] = 1
        elif accion == Accion.GIRAR_DERECHA:
            controles_base[P1_RIGHT] = 1
        elif accion == Accion.GIRAR_IZQUIERDA:
            controles_base[P1_LEFT] = 1
        elif accion == Accion.CONTROLAR_ADSO:
            controles_base[P1_DOWN] = 1
        elif accion == Accion.DEJAR_OBJETO:
            controles_base[P1_BUTTON1] = 1
        
        # Ejecutar la acción por la duración especificada
        estados = []
        for _ in range(duracion):
            if accion == Accion.ESPERAR:
                estado = self.step_basico()
            else:
                estado = self.step_basico(controles_base)
            estados.append(estado)
            
        return estados

    def mover_hasta_orientacion(self, orientacion_objetivo: Orientacion):
        """Gira hasta alcanzar la orientación objetivo"""
        estados = []
        intentos = 0
        max_intentos = 4  # Máximo una vuelta completa
        
        # Asegurar que tenemos la orientación actual
        if self.orientacion_guillermo is None:
            estado_actual = self.step_basico()
            for personaje in estado_actual.get('Personajes', estado_actual.get('personajes', [])):
                if personaje.get('nombre') == 'Guillermo':
                    self.orientacion_guillermo = personaje['orientacion']
                    break
        
        while intentos < max_intentos:
            if self.orientacion_guillermo == orientacion_objetivo.value:
                break
                
            # Determinar la dirección de giro más eficiente
            diff = (orientacion_objetivo.value - self.orientacion_guillermo) % 4
            if diff <= 2:
                # Girar a la derecha
                nuevos_estados = self.ejecutar_accion_simple(Accion.GIRAR_DERECHA, 2)
            else:
                # Girar a la izquierda
                nuevos_estados = self.ejecutar_accion_simple(Accion.GIRAR_IZQUIERDA, 2)
                
            estados.extend(nuevos_estados)
            intentos += 1
            
        return estados

    def avanzar_pasos(self, num_pasos: int):
        """Avanza el número especificado de pasos"""
        estados = []
        for _ in range(num_pasos):
            # Avanzar requiere aproximadamente 3-4 ciclos por paso
            nuevos_estados = self.ejecutar_accion_simple(Accion.AVANZAR, 4)
            estados.extend(nuevos_estados)
            
        return estados

# Modelos optimizados
class EstadoEsencial(BaseModel):
    """Estado esencial del juego, sin información redundante"""
    dia: int
    momento_dia: int
    obsequium: int
    ha_fracasado: bool
    investigacion_completa: bool
    porcentaje: int
    num_pantalla: int
    planta: int
    guillermo_pos: tuple[int, int]
    guillermo_orientacion: int
    guillermo_objetos: int
    adso_pos: Optional[tuple[int, int]] = None
    adso_objetos: Optional[int] = None
    sonidos_activos: list[int]
    frases_activas: list[int]
    otros_personajes: list[str]
    objetos_visibles: list[dict]

class ComandoMovimiento(BaseModel):
    """Comando de movimiento de alto nivel"""
    accion: str
    parametros: Optional[dict] = None

# Instancia global optimizada
abadia_opt = AbadIAOptimizada()

# Servidor MCP optimizado
mcp_opt = FastMCP(
    name="MCP Server La Abadía del Crimen - Optimizado",
    instructions="""
Servidor MCP optimizado para La Abadía del Crimen que reduce significativamente 
el número de llamadas necesarias para acciones básicas. Incluye herramientas de 
alto nivel para navegación eficiente y manejo simplificado del estado del juego.
"""
)

@mcp_opt.tool()
def obtener_estado_esencial() -> EstadoEsencial:
    """Obtiene solo la información esencial del estado actual del juego"""
    if not abadia_opt.ultimo_estado:
        # Si no hay estado, hacer un paso en vacío para obtenerlo
        abadia_opt.step_basico()
    
    estado = abadia_opt.ultimo_estado
    
    # Extraer información de Guillermo y Adso (manejar ambos formatos de clave)
    personajes = estado.get('Personajes', estado.get('personajes', []))
    guillermo_pos = None
    guillermo_orientacion = 0
    guillermo_objetos = 0
    adso_pos = None
    adso_objetos = None
    otros_personajes = []
    
    for personaje in personajes:
        if personaje['nombre'] == 'Guillermo':
            guillermo_pos = (personaje['posX'], personaje['posY'])
            guillermo_orientacion = personaje['orientacion']
            guillermo_objetos = personaje['objetos']
        elif personaje['nombre'] == 'Adso':
            adso_pos = (personaje['posX'], personaje['posY'])
            adso_objetos = personaje['objetos']
        else:
            otros_personajes.append(personaje['nombre'])
    
    # Filtrar sonidos activos (manejar ambos formatos)
    sonidos = estado.get('sonidos', estado.get('Sonidos', []))
    sonidos_activos = [i for i, sonido in enumerate(sonidos) if sonido == 1] if sonidos else []
    
    # Manejar diferentes formatos de clave
    return EstadoEsencial(
        dia=estado.get('dia', estado.get('Dia', 1)),
        momento_dia=estado.get('momentoDia', estado.get('MomentoDia', 0)),
        obsequium=estado.get('obsequium', estado.get('Obsequium', 0)),
        ha_fracasado=estado.get('haFracasado', estado.get('HaFracasado', False)),
        investigacion_completa=estado.get('investigacionCompleta', estado.get('InvestigacionCompleta', False)),
        porcentaje=estado.get('porcentaje', estado.get('Porcentaje', 0)),
        num_pantalla=estado.get('numPantalla', estado.get('NumPantalla', 23)),
        planta=estado.get('planta', estado.get('Planta', 0)),
        guillermo_pos=guillermo_pos or (136, 168),  # Posición inicial por defecto
        guillermo_orientacion=guillermo_orientacion,
        guillermo_objetos=guillermo_objetos,
        adso_pos=adso_pos,
        adso_objetos=adso_objetos,
        sonidos_activos=sonidos_activos,
        frases_activas=estado.get('frases', estado.get('Frases', [])),
        otros_personajes=otros_personajes,
        objetos_visibles=estado.get('objetos', estado.get('Objetos', []))
    )

@mcp_opt.tool()
def ejecutar_accion(
    accion: Annotated[str, Field(description="Acción a ejecutar: 'avanzar', 'girar_derecha', 'girar_izquierda', 'controlar_adso', 'dejar_objeto', 'esperar'")],
    duracion: Annotated[int, Field(description="Número de ciclos para ejecutar la acción (por defecto 1)")] = 1
) -> EstadoEsencial:
    """Ejecuta una acción simple y devuelve el estado esencial resultante"""
    try:
        accion_enum = Accion(accion)
    except ValueError:
        raise ValueError(f"Acción '{accion}' no válida. Acciones válidas: {[a.value for a in Accion]}")
    
    abadia_opt.ejecutar_accion_simple(accion_enum, duracion)
    return obtener_estado_esencial()

@mcp_opt.tool()
def girar_hacia_orientacion(
    orientacion: Annotated[int, Field(description="Orientación objetivo: 0=Derecha, 1=Abajo, 2=Izquierda, 3=Arriba")]
) -> EstadoEsencial:
    """Gira Guillermo hacia la orientación especificada de la forma más eficiente"""
    try:
        orientacion_enum = Orientacion(orientacion)
    except ValueError:
        raise ValueError(f"Orientación '{orientacion}' no válida. Valores válidos: 0-3")
    
    abadia_opt.mover_hasta_orientacion(orientacion_enum)
    return obtener_estado_esencial()

@mcp_opt.tool()
def avanzar_pasos(
    pasos: Annotated[int, Field(description="Número de pasos a avanzar en la dirección actual")]
) -> EstadoEsencial:
    """Avanza el número especificado de pasos en la dirección actual"""
    if pasos <= 0:
        raise ValueError("El número de pasos debe ser positivo")
    if pasos > 10:
        raise ValueError("Máximo 10 pasos por llamada para evitar problemas")
    
    abadia_opt.avanzar_pasos(pasos)
    return obtener_estado_esencial()

@mcp_opt.tool()
def mover_a_orientacion_y_avanzar(
    orientacion: Annotated[int, Field(description="Orientación objetivo: 0=Derecha, 1=Abajo, 2=Izquierda, 3=Arriba")],
    pasos: Annotated[int, Field(description="Número de pasos a avanzar")]
) -> EstadoEsencial:
    """Comando compuesto: gira hacia una orientación y luego avanza los pasos especificados"""
    if pasos <= 0 or pasos > 10:
        raise ValueError("El número de pasos debe estar entre 1 y 10")
    
    try:
        orientacion_enum = Orientacion(orientacion)
    except ValueError:
        raise ValueError(f"Orientación '{orientacion}' no válida. Valores válidos: 0-3")
    
    # Girar primero
    abadia_opt.mover_hasta_orientacion(orientacion_enum)
    # Luego avanzar
    abadia_opt.avanzar_pasos(pasos)
    
    return obtener_estado_esencial()

@mcp_opt.tool()
def ejecutar_secuencia_acciones(
    secuencia: Annotated[List[str], Field(description="Lista de acciones a ejecutar en orden")]
) -> EstadoEsencial:
    """Ejecuta una secuencia de acciones simples"""
    if len(secuencia) > 20:
        raise ValueError("Máximo 20 acciones por secuencia")
    
    for accion_str in secuencia:
        try:
            accion_enum = Accion(accion_str)
            abadia_opt.ejecutar_accion_simple(accion_enum, 1)
        except ValueError:
            raise ValueError(f"Acción '{accion_str}' no válida en la secuencia")
    
    return obtener_estado_esencial()

@mcp_opt.tool()
def obtener_mapa_rejilla() -> List[List[int]]:
    """Obtiene la rejilla de la pantalla actual para análisis de navegación"""
    if not abadia_opt.ultimo_estado:
        abadia_opt.step_basico()
    
    # Manejar ambos formatos de clave
    rejilla = abadia_opt.ultimo_estado.get('rejilla', abadia_opt.ultimo_estado.get('Rejilla', []))
    return rejilla

@mcp_opt.tool()
def analizar_objetos_guillermo() -> Dict[str, bool]:
    """Analiza qué objetos tiene Guillermo actualmente"""
    estado = obtener_estado_esencial()
    objetos = estado.guillermo_objetos
    
    return {
        "libro": bool(objetos & TipoObjeto.LIBRO.value),
        "guantes": bool(objetos & TipoObjeto.GUANTES.value),
        "gafas": bool(objetos & TipoObjeto.GAFAS.value),
        "pergamino": bool(objetos & TipoObjeto.PERGAMINO.value),
        "llave1": bool(objetos & TipoObjeto.LLAVE1.value),
        "llave2": bool(objetos & TipoObjeto.LLAVE2.value),
        "llave3": bool(objetos & TipoObjeto.LLAVE3.value),
        "lampara": bool(objetos & TipoObjeto.LAMPARA.value)
    }

@mcp_opt.tool()
def paso_raw_compatible(
    controles: Annotated[List[int], Field(description="Lista de 70 controles (compatibilidad con MCP original)")]
) -> Dict[str, Any]:
    """Herramienta de compatibilidad con el MCP original para casos especiales"""
    return abadia_opt.step_basico(controles)

if __name__ == "__main__":
    mcp_opt.run()
