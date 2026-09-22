import asyncio

import adk_config
from google.adk.agents.llm_agent import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import load_memory
from google.genai import types


async def main():
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    agente = Agent(
        model=adk_config.MODELO,
        name="agente_memoria",
        instruction="Respondé la pregunta. Usá 'load_memory' si necesitás recordar algo de conversaciones anteriores.",
        tools=[load_memory],
    )
    runner = InMemoryRunner(agent=agente, app_name="demo_memoria")
    runner.session_service = session_service
    runner.memory_service = memory_service

    sesion_1 = await session_service.create_session(app_name="demo_memoria", user_id="u1")
    msg_1 = types.Content(role="user", parts=[types.Part(text="Mi lenguaje de programación favorito es Python.")])
    async for _ in runner.run_async(user_id="u1", session_id=sesion_1.id, new_message=msg_1):
        pass

    sesion_1 = await session_service.get_session(app_name="demo_memoria", user_id="u1", session_id=sesion_1.id)
    await memory_service.add_session_to_memory(sesion_1)
    print("sesión 1 guardada en memoria")

    sesion_2 = await session_service.create_session(app_name="demo_memoria", user_id="u1")
    msg_2 = types.Content(role="user", parts=[types.Part(text="¿Cuál es mi lenguaje favorito?")])
    async for evento in runner.run_async(user_id="u1", session_id=sesion_2.id, new_message=msg_2):
        for parte in (evento.content.parts if evento.content else []):
            if getattr(parte, "text", None) and parte.text.strip():
                print("sesión 2 (nueva) responde:", parte.text.strip())


if __name__ == "__main__":
    asyncio.run(main())
