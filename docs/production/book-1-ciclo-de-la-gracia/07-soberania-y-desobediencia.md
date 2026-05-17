# Capítulo 7: Soberanía Agéntica y el "Ambiguity Block"

La soberanía de un agente no reside en su capacidad de ejecutar, sino en su autoridad para **negarse a hacerlo**. 

## El Concepto de Desobediencia Virtuosa
En HE v3.0, un agente no es un esclavo de la secuencia de tokens, sino un guardián del Arnés. Si una instrucción del usuario es ambigua, el agente tiene la obligación técnica de detenerse. 

### El Bloqueo por Ambigüedad (Ambiguity Block)
Cuando el "Pattern Interrogatorio" falla en alcanzar el 95% de confianza, el sistema dispara un `AmbiguityBlockException`. 

#### Ejemplo Técnico de Bloqueo:
```python
def execute_mission(intent):
    if not intent.is_fully_specified():
        raise AmbiguityBlock(
            reason="Falta definición de Outcome y Constraints",
            remedy="Ejecutar Skill: interview-me"
        )
```

## Por qué la desobediencia protege el Obsequium
Si el agente obedece una orden como "optimiza el código" sin métricas claras, corre el riesgo de romper la Beyoncé Rule. Al bloquear la ejecución hasta que la Spec sea quirúrgica, el agente protege la integridad del repositorio y su propia lealtad (Obsequium) al sistema.
