# Journey: adso-02-sincronizacion-horarium

**Context:** Syncing Guillermo's investigative speed with the Monastic Clock.

## 1. Protocol
1. **Clock Guard:** Adso interprets `sonido_id` for bells and `momentoDia` changes.
2. **Advisory:** Upon a time change, Adso emits a message (frase) indicating the required location (Church, Refectory, Cell).
3. **Escalation:** If Guillermo remains in a "Forbidden" area after the bell, Adso increases the alert frequency.
4. **Path Alignment:** Adso provides the shortest path to the target religious duty as a "suggestion" in the context window.

## 2. Verification & DoD
- **Implemented if:** Adso correctly identifies the shift from Prime to Terce and suggests a location change.
- **DoD:** Zero expulsions due to being in the wrong place at the wrong time (when Adso is present).
