# Capítulo 4: La "Beyoncé Rule" y el Ciclo Rojo-Verde Agéntico

*"If you liked it, you should have put a test on it."* Esta ley de HE v3.0 transforma el TDD tradicional en un arnés de seguridad para la inteligencia artificial.

## 1. El Ciclo de Retroalimentación de Alta Frecuencia
En un sistema soberano, el ciclo de desarrollo sigue estos pasos innegociables:
1. **The Red Stage (El Test Fallido):** El agente escribe el test basado en la Spec. El test **DEBE** fallar con un error esperado (ej. `ModuleNotFoundError` o `AssertionError`). Si el test pasa por accidente, el arnés se considera corrupto.
2. **The Green Stage (La Implementación Mínima):** El agente escribe el código estrictamente necesario para que el test pase. Nada de "ya que estoy aquí, añado esto".
3. **The Refactor Stage (La Purificación):** Con el test en verde, el agente optimiza la legibilidad y la estructura sin miedo a romper la funcionalidad.

## 2. Cobertura como Trinquete (Coverage Ratchet)
No aceptamos la cobertura como una sugerencia. Implementamos un "Gatekeeper" que impide el commit si la cobertura baja del 90%. Esto asegura que la calidad técnica sea un camino de una sola dirección.

## 3. Ejemplo de Test como Contrato
```python
# tests/test_obsequium.py
def test_guillermo_loses_obsequium_on_forbidden_action():
    state = GameState()
    result = guillermo.move_to("finis-africae", state)
    assert state.obsequium < 100
    assert result.status == "TERMINATED"
```
Este test no es solo código; es el contrato que define el comportamiento del sistema ante la seguridad.
