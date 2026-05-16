# Journey: adso-01-vigilancia-de-recursos

**Context:** Continuous monitoring of mission-critical items and agent health.

## 1. Protocol
1. **Periodic Scan:** Every 5 execution ticks, Adso scans the `objetos` and `obsequium` values.
2. **Threshold Logic:**
   - If `obsequium` falls below 15: Disparar Alerta "Obediencia en Riesgo".
   - If `lámpara` state changes (oil running out): Disparar Alerta "Oscuridad Inminente".
3. **Interrupt:** If a critical threshold is met, Adso sends a priority signal to Guillermo to switch to a Safety Journey.

## 2. Verification & DoD
- **Implemented if:** A test proves Adso triggers a warning when obsequium is manually lowered in the mock state.
- **DoD:** Guillermo receives resource context without having to query the tools himself.
