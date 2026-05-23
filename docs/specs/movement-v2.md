# SPEC: Movimiento Cardinal y Espera (v2.0)
ID: `movement-v2`
Ref: [[abadia-monastic-logic]]

## 1. Introducción
Este documento define la extensión del sistema de movimiento del agente para soportar comandos cardinales directos y una operación de espera (`NOP`). El objetivo es simplificar la navegación del agente permitiendo abstracciones de alto nivel sobre los comandos crudos del emulador (`UP`, `LEFT`, `RIGHT`).

## 2. Definiciones de Comandos

### 2.1 Comandos Cardinales (Básicos)
| Comando | Descripción | Mapeo Lógico |
| :--- | :--- | :--- |
| `N` | Norte | Orientar al Norte + `UP` |
| `S` | Sur | Orientar al Sur + `UP` |
| `E` | Este | Orientar al Este + `UP` |
| `W` | Oeste | Orientar al Oeste + `UP` |

### 2.2 Comandos Diagonales (Complejos)
| Comando | Descripción | Mapeo Lógico |
| :--- | :--- | :--- |
| `NE` | Nordeste | Secuencia: `E` -> `N` (o similar según orientación) |
| `SE` | Sureste | Secuencia: `E` -> `S` |
| `SW` | Suroeste | Secuencia: `W` -> `S` |
| `NW` | Noroeste | Secuencia: `W` -> `N` |

*Nota sobre 'S para Southeast':* Siguiendo la instrucción literal del usuario, el comando `S` se mapeará inicialmente a Sur para mantener coherencia con `N`, `E`, `W`, pero se habilitará `SE` para Sureste. Si se confirma el requerimiento específico de `S = Southeast`, se ajustará el mapeo.

### 2.3 Comando de Espera (NOP)
| Comando | Descripción | Implementación |
| :--- | :--- | :--- |
| `NOP` | No Operación | GET a `abadIA/game/current` (refresco de estado sin input) |

## 3. Reglas de Validación
- Antes de ejecutar un movimiento cardinal, se debe verificar la **Regla del Volumen 2x2**.
- Si el destino está bloqueado, el comando debe devolver un error descriptivo indicando el obstáculo (pared o personaje).

## 4. Pruebas de Verificación
- `test_move_cardinal_n`: Guillermo mira al Norte y se mueve.
- `test_move_diagonal_ne`: Guillermo realiza una secuencia coordinada.
- `test_nop_execution`: El sistema refresca el estado sin enviar teclas.
