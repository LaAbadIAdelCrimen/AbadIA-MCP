---
name: github-credential-manager
description: Gestiona credenciales de GitHub, limpieza de caché y autenticación robusta para push en entornos agénticos. Úsalo cuando el push falle por 403 Forbidden o problemas de identidad.
---

# GitHub Credential Manager

Este skill automatiza la lección aprendida durante la crisis del PAT del 17 de mayo. Evita que el agente use identidades cacheadas incorrectas.

## Flujo de Trabajo

1. **Rechazo de Credenciales**: Ejecuta `git credential reject` para limpiar el helper de memoria.
2. **Unset de Helpers**: Elimina helpers globales que puedan estar interfiriendo.
3. **Inyección de Token**: Configura el remoto usando el formato `https://<user>:<token>@github.com/...` de forma temporal.
4. **Verificación**: Realiza un `ls-remote` para confirmar acceso de escritura.
5. **Restauración**: Tras el push, restaura la URL del remoto a HTTPS estándar para no dejar el token en el archivo `.git/config`.

## Comando sugerido
```bash
git -C <repo> remote set-url origin https://<user>:<token>@github.com/<owner>/<repo>.git
git -C <repo> push origin <branch>
git -C <repo> remote set-url origin https://github.com/<owner>/<repo>.git
```

## Troubleshooting
Si el error persiste, verifica que el PAT tenga el scope `repo` y que el usuario tenga permisos de "Write" en la organización/repo.
