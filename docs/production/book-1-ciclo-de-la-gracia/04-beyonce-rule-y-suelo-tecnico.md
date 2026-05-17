# Capítulo 4: La "Beyoncé Rule" y el Suelo Técnico

En la Ingeniería de Arnés (HE) v3.0, la calidad no es una aspiración; es un **contrato físico**.

## La Regla de Beyoncé
*"If you liked it, you should have put a test on it."*

Esta máxima define el punto de no retorno en la construcción de sistemas agénticos. Un agente nunca debe implementar lógica sin antes tener un test que falle.
1. **Red:** El test define la frontera de lo posible y falla porque la realidad aún no existe.
2. **Green:** El agente construye la mínima lógica necesaria para cruzar esa frontera.
3. **Refactor:** El sistema se limpia bajo la protección del arnés.

## El Suelo Técnico (The Quality Floor)
A diferencia del desarrollo tradicional, donde los tests pueden ser opcionales, aquí el **Trinquete de la Complejidad** asegura que la cobertura de tests sea el suelo sobre el que caminamos. Si un cambio reduce la cobertura, el trinquete no gira y el cambio es rechazado por el sistema.

Esto garantiza que el sistema sea **Soberano**: no depende del "buen juicio" del programador, sino del arnés que lo encierra.
