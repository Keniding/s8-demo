import asyncio

import adk_config  # configura el backend de Vertex AI antes de importar ADK
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types


def get_current_time(city: str) -> dict:
    """Devuelve la hora actual en la ciudad indicada."""
    return {"status": "success", "city": city, "time": "10:30 AM"}


async def main():
    agente = Agent(
        model=adk_config.MODELO,
        name="agente_horas",
        instruction="Sos un asistente útil que informa la hora en ciudades. Usá 'get_current_time'.",
        tools=[get_current_time],
    )
    runner = InMemoryRunner(agent=agente, app_name="demo_horas")
    sesion = await runner.session_service.create_session(app_name="demo_horas", user_id="u1")
    contenido = types.Content(role="user", parts=[types.Part(text="¿Qué hora es en Bogotá?")])

    async for evento in runner.run_async(user_id="u1", session_id=sesion.id, new_message=contenido):
        for parte in (evento.content.parts if evento.content else []):
            if getattr(parte, "function_call", None):
                print("tool call:", parte.function_call.name, dict(parte.function_call.args))
            if getattr(parte, "text", None):
                print("respuesta:", parte.text)


if __name__ == "__main__":
    asyncio.run(main())
