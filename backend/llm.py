import requests

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama default local endpoint

def query_phi(prompt):
    """Send a prompt to the local phi model and return the response."""
    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False  # We want full output at once, not stream
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    return result['response']
