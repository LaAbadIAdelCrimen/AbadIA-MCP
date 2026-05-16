# Journey: adso-03-seguimiento-y-seguridad

**Context:** Managing proximity to ensure Adso provides context without hindering movement.

## 1. Protocol
1. **Shadowing Guillermo:** Adso's target coordinate is always Guillermo's `pos(n-2)` to avoid blocking his path.
2. **Proximity Check:** If `Distance(Guillermo, Adso) > 5` cells:
   - Adso requests a `NOP` from Guillermo.
   - Guillermo enters "Waiting State" until Adso re-enters the context circle.
3. **Collision Avoidance:** Adso uses the same 2x2 volume validation as Guillermo.

## 2. Verification & DoD
- **Implemented if:** A simulation shows Adso following Guillermo through a door without both getting stuck.
- **DoD:** Adso is always within 5 cells of Guillermo during investigative journeys.
