import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def get_client():
    """
    Crea un cliente genai según si hay API key o se usa Vertex AI.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    use_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() in ("1","true","yes")

    if use_vertex:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        # client para Vertex AI
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        # cliente via API key (Gemini Developer API)
        client = genai.Client(api_key=api_key)
    return client

_client = None
def client():
    global _client
    if _client is None:
        _client = get_client()
    return _client

# Generación de texto (sugerir precios / chat)
def generate_text(prompt, model="gemini-2.5-flash"):
    c = client()
    # uses generate_content as shown in docs
    try:
        resp = c.models.generate_content(model=model, contents=prompt)
        # el SDK devuelve 'text' en el resultado
        return getattr(resp, "text", None) or str(resp)
    except Exception as e:
        logger.exception("Error al llamar a Gemini generate_content")
        return f"Error al generar texto: {e}"

# Generar embedding
def embed_text(text, model="gemini-embedding-001"):
    c = client()
    try:
        resp = c.models.embed_content(model=model, contents=text)
        # según SDK, el resultado trae resp.embeddings (lista de floats)
        embeddings = getattr(resp, "embeddings", None)
        if embeddings:
            # algunas versiones devuelven lista; tomamos el primer vector
            if isinstance(embeddings, list) and len(embeddings) > 0 and isinstance(embeddings[0], (list, tuple)):
                return embeddings[0]
            # si el shape es otro, devolvemos tal cual
            return embeddings
        # fallback: intentar acceder al primer campo
        return resp
    except Exception as e:
        logger.exception("Error al generar embedding")
        return None