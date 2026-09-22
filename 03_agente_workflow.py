import asyncio

import adk_config
from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types


async def main():
    idea = Agent(
        model=adk_config.MODELO,
        name="agente_idea",
        instruction="Proponé, en una frase, un nombre para una cafetería de barrio.",
        output_key="nombre_propuesto",
    )
    eslogan = Agent(
        model=adk_config.MODELO,
        name="agente_eslogan",
        instruction="Tomá el nombre en {nombre_propuesto} y escribí un eslogan corto para esa cafetería.",
    )
    flujo = SequentialAgent(name="flujo_marca", sub_agents=[idea, eslogan])

    runner = InMemoryRunner(agent=flujo, app_name="demo_workflow")
    sesion = await runner.session_service.create_session(app_name="demo_workflow", user_id="u1")
    contenido = types.Content(role="user", parts=[types.Part(text="Dale")])

    async for evento in runner.run_async(user_id="u1", session_id=sesion.id, new_message=contenido):
        for parte in (evento.content.parts if evento.content else []):
            if getattr(parte, "text", None):
                print(f"[{evento.author}]", parte.text)


if __name__ == "__main__":
    asyncio.run(main())
