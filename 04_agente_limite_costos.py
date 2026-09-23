import asyncio

import adk_config
from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import RunConfig
from google.adk.runners import InMemoryRunner
from google.genai import types


def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b


async def main():
    agente = Agent(model=adk_config.MODELO, name="agente_limitado", instruction="Usá la tool 'sumar' para responder.", tools=[sumar])
    runner = InMemoryRunner(agent=agente, app_name="demo_limite")
    sesion = await runner.session_service.create_session(app_name="demo_limite", user_id="u1")
    contenido = types.Content(role="user", parts=[types.Part(text="¿Cuánto es 7 + 8? Usá la tool.")])

    try:
        async for evento in runner.run_async(user_id="u1", session_id=sesion.id, new_message=contenido, run_config=RunConfig(max_llm_calls=2)):
            for parte in (evento.content.parts if evento.content else []):
                if getattr(parte, "function_call", None):
                    print("1 llamada al modelo, permitida:", parte.function_call.name)
                if getattr(parte, "text", None):
                    print(f"[{evento.author}]", parte.text)
    except Exception as e:
        print(f"límite de costo disparado -- {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
