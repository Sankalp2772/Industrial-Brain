from google import genai
from app.core.config import settings
from typing import List

class GeminiEmbeddingProvider:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-embedding-2"

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts.
        """
        if not texts:
            return []
            
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts
        )
        # Assuming response contains a list of embeddings
        # We may need to adapt based on exactly how google-genai formats output
        if hasattr(response, 'embeddings'):
             return [emb.values for emb in response.embeddings]
        elif isinstance(response, list):
             return [r.embeddings[0].values if hasattr(r, 'embeddings') else r for r in response]
        return response
        
    def embed_query(self, query: str) -> List[float]:
        """
        Embeds a single query string.
        """
        result = self.embed_texts([query])
        return result[0] if result else []
