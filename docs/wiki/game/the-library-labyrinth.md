# La Biblioteca-Laberinto: Desafío de Navegación

## Reglas del Laberinto
Según el lore de la Abadía, el laberinto tiene reglas matemáticas y semánticas que el agente debe mapear:

1. **La Regla del Hilo:** Marcar el camino de vuelta (implementado en nuestra lógica de navegación como un `breadcrumb buffer`).
2. **La Regla del Aire:** Las corrientes de aire indican la proximidad de ventanas o pasadizos secretos.
3. **La Trampa de los Monjes:** Jorge de Burgos utiliza veneno en los libros. En términos de IA, esto es **Data Poisoning**. El agente debe verificar la integridad de la información antes de "ingerirla" (procesarla).

## Mapeo en el Juego
- **Nivel de Planta:** 1 (Superior).
- **Acceso:** Solo permitido en momentos específicos del horarium (Noche), lo cual requiere violar el obsequium.
- **Riesgo:** Perderse o quedarse sin luz (Failure State inmediato).

## Estrategia HE v3.0
Utilizaremos el **Monastic Dreamer** para reconstruir el plano de la biblioteca a partir de los intentos fallidos. Cada vez que Guillermo muere en el laberinto, el "sueño" (procesamiento de logs) actualiza el mapa en el `llmwiki`.
