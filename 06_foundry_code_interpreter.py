from azure.ai.projects.models import AutoCodeInterpreterToolParam, CodeInterpreterTool, PromptAgentDefinition

from client_foundry import MODELO, cliente_openai, proyecto

proyecto().agents.create_version(
    agent_name="demo-foundry-code-interpreter",
    definition=PromptAgentDefinition(
        model=MODELO,
        instructions="Sos un asistente que puede ejecutar código Python cuando hace falta.",
        tools=[CodeInterpreterTool(container=AutoCodeInterpreterToolParam())],
    ),
)

respuesta = cliente_openai().responses.create(
    extra_body={"agent_reference": {"name": "demo-foundry-code-interpreter", "type": "agent_reference"}},
    input="Calculá cuánto es 17 al cubo usando código Python.",
)
print(respuesta.output_text)
print("tipos de item:", [item.type for item in respuesta.output])
