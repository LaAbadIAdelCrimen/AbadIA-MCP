# PLAN: Implementación de Movimiento Cardinal v2
ID: `guillermo-03-movimiento-cardinal`
Ref: [[movement-v2]]

## 1. Fase de Construcción (Build)
- [ ] **Modificar `server/logic.py`**:
    - Implementar `move_cardinal_internal(direction: str)`.
    - Usar el diccionario `path2Pos` (actualmente en `main.py`) para centralizar la lógica de rotación y avance.
    - Implementar `wait_internal(ticks: int = 1)`.
- [ ] **Modificar `server/main.py`**:
    - Registrar la herramienta MCP `@mcp.tool() move_cardinal(direction: str)`.
    - Registrar la herramienta MCP `@mcp.tool() nop()`.
    - Refactorizar el endpoint legacy `/game/move/{cmd}` para que use la lógica centralizada.

## 2. Fase de Verificación (Verify)
- [ ] Crear un nuevo archivo de test `tests/test_movement_v2.py`.
- [ ] Verificar que `move_cardinal("N")` envía los comandos correctos según la orientación actual.
- [ ] Verificar que `nop()` no envía comandos de teclado pero refresca el estado.

## 3. Fase de Documentación (Distill)
- [ ] Actualizar la skill `abadia-monastic-logic` para incluir los nuevos comandos.
- [ ] Commit y Push de los cambios.
