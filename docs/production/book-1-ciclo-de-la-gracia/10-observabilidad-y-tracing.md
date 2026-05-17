# Capítulo 10: El Hilo de Alinardo (Observability y Tracing)

En la complejidad asíncrona de los sistemas agénticos, perder el rastro de una decisión es perder la soberanía. El **Tracing** es el hilo de seda que nos permite salir del laberinto.

## Observabilidad vs. Logging
No basta con registrar eventos; necesitamos entender el estado interno del sistema a través de sus salidas. Alinardo, nuestro Centinela, nos enseña que:
1. **Métricas (El Pulso):** Latencia, errores y consumo de tokens.
2. **Logs (La Crónica):** El registro secuencial de los hechos.
3. **Tracing (El Hilo):** La correlación de eventos a través de diferentes capas y agentes.

## El Hilo de Ariadna Agéntico
Implementamos identificadores de correlación únicos para cada Journey. Esto permite reconstruir la cadena causal completa de un error, desde el `Ambiguity Block` del Abad hasta el fallo de memoria en la Capa 8. Sin este hilo, la autopsia del Cronista sería imposible.
