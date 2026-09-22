from azure.ai.projects.models import PromptAgentDefinition

from client_foundry import MODELO, ejecutar_agente, proyecto

proyecto().agents.create_version(
    agent_name="demo-foundry-basico",
    definition=PromptAgentDefinition(
        model=MODELO,
        instructions="Sos un asistente breve. Respondé en una oración.",
    ),
)

respuesta = ejecutar_agente("demo-foundry-basico", "Decime una curiosidad breve sobre Saturno.")
print(respuesta)
