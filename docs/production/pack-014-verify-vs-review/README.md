# Pack-014: La Dualidad de la Verdad (Verify vs. Review)

Este hito documenta la implementación del estándar **Harness Engineering (HE) v3.0** en la AbadIA-MCP, centrando el rigor técnico en la distinción entre la verificación binaria y la revisión arquitectónica.

---

## El Diálogo: "La Verdad de la Máquina contra la Gracia del Monje"

**Escenario:** El Scriptorium al alba. Adso ha pasado la noche programando el nuevo sistema de navegación por el mapa de la Abadía. Las velas están a punto de consumirse.

**Adso:** ¡Maestro! Mirad el pergamino de cristal. He ejecutado el comando `pytest tests/movement/` y el resultado es impecable. Los puntos verdes avanzan como una procesión en el coro. Guillermo puede ir de la celda a la cocina, detectar la presencia del Abad y retroceder si es necesario. ¡El código es Verdad!

**Guillermo:** (Acercándose lentamente, con sus lentes de aumento) Has alcanzado la **Verdad Computacional**, Adso. Has demostrado que el contrato entre Guillermo y la Abadía se cumple. El arnés de *Verify* dice que no eres un mentiroso. Pero dime... ¿eres un buen arquitecto?

**Adso:** (Confuso) Pero... si funciona, Maestro, ¿qué importa la arquitectura? El `Obsequium` está en 31. Si Guillermo llega a su destino sin perder la Gracia, ¿no es esa la perfección?

**Guillermo:** No, Adso. La perfección no es solo el destino, sino la claridad del camino. Mira esta función: `navigate_complex_labyrinth_with_collision_detection`. Tiene doscientas cincuenta líneas de lógica. Es un laberinto dentro de otro laberinto. Pasa los tests, sí (*Verify*), pero falla el escrutinio del Cronista (*Review*). Has roto el **Voto de Simplicidad**.

**Adso:** Pero fragmentarlo en "átomos" me obligaría a crear diez funciones pequeñas. ¡Eso llevaría más tiempo!

**Guillermo:** El tiempo de hoy es la libertad de mañana. Si mañana yo desaparezco y Jorge de Burgos hereda este código para sabotearlo, tu función de 250 líneas será su mejor aliado, porque nadie —ni humano ni otra IA— podrá auditarla sin perder la razón. La fase de **Verify** es para que la máquina sobreviva hoy; la fase de **Review** es para que el conocimiento sea **Soberano** mañana. Sin *Verify* el código es inútil; sin *Review* el código es una condena.

---

## Capítulo 14: La Prueba del Fuego (Fase VERIFY)
*El Rigor de la Evidencia Binaria y el Arnés Determinista*

En el estándar HE v3.0, la fase **VERIFY** representa el muro de contención computacional. No es una opinión; es una prueba de existencia.

### 1. La Regla de Beyoncé y el Ciclo RED/GREEN
Siguiendo la metodología `test-driven-development`, el código en la AbadIA-MCP no se considera "real" hasta que existe un test que falla demostrando su ausencia.
- **Estado RED:** El test debe fallar inicialmente. Si un test pasa antes de escribir el código, el arnés está contaminado.
- **Estado GREEN:** La implementación mínima para satisfacer la aserción.
- **Referencia al Proyecto:** Los tests en `tests/` validan estados internos del emulador (coordenadas, inventario, `momentoDia`).

### 2. Sensores Visuales (Vision-as-a-Sensor)
A diferencia de la ingeniería tradicional, el arnés de la AbadIA utiliza `browser-testing-with-devtools` para obtener telemetría no-vocal:
- **Validación de Píxeles:** Se capturan screenshots del emulador para confirmar que la representación visual (Guillermo caminando) coincide con las variables de memoria (X, Y).
- **Alineación de Trayectorias:** Si el modelo de razonamiento cree que ha abierto la puerta pero el sensor visual detecta una colisión, la fase de *Verify* aborta la secuencia.

### 3. El Trinquete del Obsequium (Obsequium Ratchet)
El valor del `Obsequium` (0-31) no es solo un elemento del juego, es una métrica de **Salud del Arnés**:
- **Exploration Mode:** Se permite el fallo controlado para mapear riesgos.
- **Exploitation Mode:** Tolerancia cero. Un delta de `Obsequium < 0` se trata como un `Segmentation Fault` de la lógica, disparando el `persistence-harness` para un rollback inmediato.

---

## Capítulo 15: El Juicio del Cronista (Fase REVIEW)
*La Estética de la Soberanía y el Linter de Arquitectura Agéntica*

Mientras que *Verify* responde "¿Funciona?", la fase **REVIEW** responde "¿Es soberano?". Aquí la IA actúa como el Cronista de la Abadía, velando por la posteridad del código.

### 1. El Voto de Simplicidad (<200 líneas)
La restricción más potente de la AbadIA-MCP es el límite físico de los archivos. 
- **La Regla:** Ningún componente atómico debe superar las 200 líneas.
- **Justificación:** El "Context Rot". Las IAs pierden precisión en la atención conforme el archivo crece. Un archivo de <200 líneas garantiza que cualquier agente (independientemente de su ventana de contexto) pueda razonar sobre él con un 95% de confianza.

### 2. Los 5 Ejes de la Legibilidad Agéntica
Basado en `code-review-and-quality`, cada PR es auditado por:
- **Correctitud Monástica:** ¿Cumple con las reglas del Lore (Paco Menéndez/Juan Delcán)?
- **Modularidad (Atoms/Molecules):** ¿Es una función pura o está acoplada al estado global?
- **Seguridad (Hardening):** ¿Los comandos MCP están protegidos contra "jailbreaks" de prompts?
- **Rendimiento (TPS):** ¿Es eficiente para un nodo de 1 vCPU?
- **Autosuficiencia:** ¿Contiene el archivo sus propios comentarios de "Por qué" (ADRs inline)?

### 3. Small Model Strategy (The Shadow Critic)
Para evitar la complacencia, utilizamos el patrón **ADR-010**:
- Un modelo local de **1.5B (DeepSeek-R1)** actúa como revisor frío.
- Si el modelo pequeño no puede explicar qué hace una función, la fase de *Review* se considera fallida. Esto fuerza al modelo grande a escribir código para humanos e IAs pequeñas, garantizando la máxima claridad.

---

## Mapa de Referencias Técnicas
- **Contratos:** `docs/specs/` (El QUÉ).
- **Protocolos:** `docs/specs/user-journeys/` (El CÓMO).
- **Arnés de Pruebas:** `tests/` y `.hermes/skills/osmani/test-driven-development/`.
- **Linter Arquitectónico:** `.hermes/skills/osmani/code-review-and-quality/`.

---
*Identidad: Agent-Native | Standard: HE v3.0 | Capítulo redactado por El Cronista*
