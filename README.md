# s8-demo: agentes simples con Google ADK y Microsoft Foundry

Seis scripts chicos y probados, la mayoría con Google ADK (el foco de esta semana) y dos con Microsoft Foundry Agent Service (se profundiza la semana que viene). Todos corren contra plataformas reales, sin nada simulado.

```bash
uv sync
uv run python 01_agente_basico.py
```

## Configurar Vertex AI desde cero (si nunca usaste Google Cloud)

Los scripts de ADK necesitan un proyecto de Google Cloud propio, con billing activo y la API de Vertex AI habilitada. Estos son los pasos reales, en orden, probados en este mismo entorno:

**1. Instalar la CLI de Google Cloud (`gcloud`)**, si no la tenés — instrucciones oficiales en [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install). En Windows, también podés instalarla con `winget install Google.CloudSDK`.

**2. Loguearte con tu cuenta de Google** (esto autentica la CLI en sí):

```bash
gcloud auth login
```

**3. Crear un proyecto nuevo** (o usar uno que ya tengas — en ese caso, saltá este paso y anotá su ID):

```bash
gcloud projects create MI-PROYECTO-ADK --name="Mi proyecto ADK"
gcloud config set project MI-PROYECTO-ADK
```

El ID del proyecto (`MI-PROYECTO-ADK`) es lo que va en `PROYECTO` dentro de [`adk_config.py`](./adk_config.py).

**4. Vincular una cuenta de facturación.** Vertex AI no funciona sin billing activo, aunque el uso de estos scripts (unas pocas llamadas con `gemini-2.5-flash-lite`) cuesta centavos. Primero mirá qué cuentas de facturación tenés disponibles:

```bash
gcloud billing accounts list
```

y vinculá una al proyecto:

```bash
gcloud billing projects link MI-PROYECTO-ADK --billing-account=TU_ACCOUNT_ID
```

Si no tenés ninguna cuenta de facturación todavía, se crea desde la consola de Google Cloud (requiere una tarjeta, aunque haya un tier gratuito).

**5. Habilitar la API de Vertex AI** en tu proyecto — este es el paso que faltaba más seguido al validar esta demo:

```bash
gcloud services enable aiplatform.googleapis.com --project=MI-PROYECTO-ADK
```

**6. Generar las credenciales que usan los SDKs** (distintas del login de la CLI del paso 2 — esto es lo que `adk_config.py` necesita para autenticar cada llamada):

```bash
gcloud auth application-default login
```

**7. Editar `adk_config.py`**: reemplazá `PROYECTO = "agentpay-latam-lab"` por tu propio ID del paso 3. `REGION` (`us-central1`) generalmente no hace falta tocarla.

**Si `gcloud` te avisa de un "mismatch" entre el proyecto y el quota project de las credenciales**, corré una vez:

```bash
gcloud auth application-default set-quota-project MI-PROYECTO-ADK
```

Con estos 7 pasos hechos una sola vez, `uv run python 01_agente_basico.py` (y el resto de los scripts de ADK) deberían andar directamente.

## Google ADK (Vertex AI)

- **`01_agente_basico.py`** — un `LlmAgent` con una tool, corrido con `InMemoryRunner`, imprimiendo la tool call y la respuesta final.
- **`02_agente_con_memoria.py`** — dos sesiones distintas del mismo usuario; la segunda recupera, vía `MemoryService` + `load_memory`, un dato mencionado solo en la primera.
- **`03_agente_workflow.py`** — un `SequentialAgent` de dos pasos: el primero propone un nombre y lo guarda con `output_key`, el segundo lo referencia con `{nombre_propuesto}` en su instrucción para escribir un eslogan.
- **`04_agente_limite_costos.py`** — `RunConfig(max_llm_calls=1)` contra un agente que necesita una tool call (más de una llamada al modelo), forzando el `LlmCallsLimitExceededError` real.

## Microsoft Foundry Agent Service

Configuración en [`client_foundry.py`](./client_foundry.py) — mismo patrón de autenticación Entra ID del resto del curso (`az login`), pero apuntando a un **proyecto** de Foundry, no al endpoint de chat completions.

- **`05_foundry_agente_basico.py`** — crear un agente con `PromptAgentDefinition` y correrlo vía la Responses API.
- **`06_foundry_code_interpreter.py`** — el mismo agente, con Code Interpreter habilitado, ejecutando código Python real (`respuesta.output` incluye un item `code_interpreter_call`).

Ver la Sesión 8 completa, con la explicación conceptual de cada plataforma y los hallazgos reales encontrados al validar este código, en [`../s8/`](../s8/00-indice.md).
