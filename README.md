# s8-demo: agentes simples con Google ADK y Microsoft Foundry

Seis scripts chicos y probados, la mayoría con Google ADK (el foco de esta semana) y dos con Microsoft Foundry Agent Service (se profundiza la semana que viene). Todos corren contra plataformas reales, sin nada simulado.

```bash
uv sync
uv run python 01_agente_basico.py
```

## Google ADK (Vertex AI)

Configuración en [`adk_config.py`](./adk_config.py) — reemplazá `PROYECTO` por tu propio project id de Google Cloud (con billing activo y `aiplatform.googleapis.com` habilitado), y corré `gcloud auth application-default login` una vez.

- **`01_agente_basico.py`** — un `LlmAgent` con una tool, corrido con `InMemoryRunner`, imprimiendo la tool call y la respuesta final.
- **`02_agente_con_memoria.py`** — dos sesiones distintas del mismo usuario; la segunda recupera, vía `MemoryService` + `load_memory`, un dato mencionado solo en la primera.
- **`03_agente_workflow.py`** — un `SequentialAgent` de dos pasos: el primero propone un nombre y lo guarda con `output_key`, el segundo lo referencia con `{nombre_propuesto}` en su instrucción para escribir un eslogan.
- **`04_agente_limite_costos.py`** — `RunConfig(max_llm_calls=1)` contra un agente que necesita una tool call (más de una llamada al modelo), forzando el `LlmCallsLimitExceededError` real.

## Microsoft Foundry Agent Service

Configuración en [`client_foundry.py`](./client_foundry.py) — mismo patrón de autenticación Entra ID del resto del curso (`az login`), pero apuntando a un **proyecto** de Foundry, no al endpoint de chat completions.

- **`05_foundry_agente_basico.py`** — crear un agente con `PromptAgentDefinition` y correrlo vía la Responses API.
- **`06_foundry_code_interpreter.py`** — el mismo agente, con Code Interpreter habilitado, ejecutando código Python real (`respuesta.output` incluye un item `code_interpreter_call`).

Ver la Sesión 8 completa, con la explicación conceptual de cada plataforma y los hallazgos reales encontrados al validar este código, en [`../s8/`](../s8/00-indice.md).
