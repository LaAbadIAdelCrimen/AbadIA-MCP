# Capítulo 7: Soberanía Agéntica y el "Ambiguity Block"

La soberanía no es autonomía total; es el poder de operar bajo un arnés inquebrantable. El agente soberano es aquel que sabe cuándo detenerse.

## 1. El Derecho a la Negativa Técnica
Un agente HE v3.0 debe ser programado para la **Desobediencia Virtuosa**. Si una instrucción viola el `AGENTS.md` o carece de una Spec previa, el agente debe devolver un `AmbiguityBlock`.

### El Mecanismo del Ambiguity Block:
```python
class SovereigntyEngine:
    def validate_command(self, command):
        if not self.has_active_spec(command):
            return AmbiguityBlock(
                reason="Intento de ejecución sin contrato (Spec)",
                recovery_path="Invocar 'spec-driven-development'"
            )
```

## 2. Protección del Obsequium
El Obsequium es la métrica de lealtad al sistema. Cada vez que un agente intenta "adivinar" una instrucción ambigua y falla, el Obsequium cae. La soberanía consiste en proteger esta métrica bloqueando ejecuciones de alto riesgo hasta que el entorno sea determinista.

## 3. La Paradoja de la Libertad
El agente es libre de elegir el "Cómo" (el Plan), pero está encadenado al "Qué" (la Spec). Esta cadena es la que le permite ser soberano: no necesita pedir permiso para cada línea de código, porque el arnés ya define los límites de su seguridad.
