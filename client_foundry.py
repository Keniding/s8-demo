from functools import lru_cache

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = "https://kenidinghk-5470-resource.services.ai.azure.com/api/projects/kenidinghk-5470"
MODELO = "gpt-5.4-nano"


@lru_cache(maxsize=1)
def proyecto() -> AIProjectClient:
    return AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())


@lru_cache(maxsize=1)
def cliente_openai():
    return proyecto().get_openai_client()


def ejecutar_agente(nombre_agente: str, mensaje: str) -> str:
    respuesta = cliente_openai().responses.create(
        extra_body={"agent_reference": {"name": nombre_agente, "type": "agent_reference"}},
        input=mensaje,
    )
    return respuesta.output_text
