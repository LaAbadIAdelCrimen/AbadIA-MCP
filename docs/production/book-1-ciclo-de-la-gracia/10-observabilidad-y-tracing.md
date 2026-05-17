# Capítulo 10: El Hilo de Alinardo (Observability y Tracing)

En la complejidad asíncrona de los sistemas agénticos, perder el rastro de una decisión es perder la soberanía. El **Tracing** es el hilo de seda que nos permite salir del laberinto. En este capítulo exploramos cómo implementar una observabilidad de "Capa Blanca" que permita al sistema auto-explicarse.

## 1. De los Logs Silenciosos a la Observabilidad Activa
El logging tradicional registra eventos: "Entré en la habitación 102". La observabilidad HE v3.0 responde al "Por qué": "Entré en la habitación 102 porque Guillermo-Persona detectó un cambio en el vector de olor y la Spec-04 priorizaba la búsqueda de objetos de vidrio".

### Los Tres Pilares de Alinardo:
1. **Métricas de Rendimiento:** No solo CPU/RAM, sino latencia de razonamiento (Time to First Thought) y densidad de información (Tokens por Acción).
2. **Eventos Estructurados:** Cada entrada y salida de herramienta debe ser un JSON tipado que incluya el `request_id` y el `parent_span_id`.
3. **Trace Context:** El contexto que viaja entre agentes. Si Guillermo delega en Adso, Adso hereda el "Gen de la Intención" de la tarea original.

## 2. Implementación Técnica: El ID de Correlación
Implementamos un sistema de identificadores de traza (`Trace-ID`) que vincula cada movimiento del juego con el fragmento de la Spec que lo motivó.

```python
# Ejemplo de inyección de contexto de observabilidad
def perform_action(agent, action, trace_id):
    span = tracer.start_span(action, trace_id=trace_id)
    with span:
        try:
            result = agent.execute(action)
            span.set_attribute("status", "success")
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_attribute("status", "failed")
            # El Cronista usará este reporte para el post-mortem
            raise
```

## 3. Visualización del Laberinto de Datos
La observabilidad permite generar mapas de calor de decisión. ¿En qué áreas de la biblioteca el agente duda más? ¿Dónde el skill `doubt-driven` dispara más excepciones? Estos datos son los que Alinardo, el monje anciano, utiliza para advertir a Guillermo sobre las zonas de "Niebla de Contexto".
