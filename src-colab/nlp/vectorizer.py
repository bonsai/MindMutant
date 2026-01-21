import math
import hashlib
import random
import numpy as np
import os

# Try to import spacy
try:
    import spacy
    SPACY_AVAILABLE = True
except Exception as e:
    # Catching generic Exception because ImportError might not catch DLL load failures or version conflicts
    print(f"Warning: Failed to import spacy ({e}). Using fallback vectorizer.")
    SPACY_AVAILABLE = False

class Vectorizer:
    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = None
        self.use_spacy = False
        self.dim = 96 # Dimension for fallback vectors
        
        if SPACY_AVAILABLE:
            try:
                # Suppress loading messages if possible, or just load
                # Try loading Japanese model first if context suggests, but default to en for now or small one
                # If user environment is Windows, loading models might be tricky if not installed.
                # We try 'en_core_web_sm' first, then 'en_core_web_md', then fallback.
                if spacy.util.is_package(model_name):
                    self.nlp = spacy.load(model_name)
                    self.use_spacy = True
                else:
                    print(f"Spacy model '{model_name}' not found. Using deterministic fallback vectors.")
            except Exception as e:
                print(f"Error loading Spacy model: {e}. Using deterministic fallback vectors.")
        else:
            print("Spacy library not found. Using deterministic fallback vectors.")

    def get_vector(self, text: str) -> list:
        """
        Returns a vector representation of the text.
        """
        if self.use_spacy and self.nlp:
            try:
                doc = self.nlp(text)
                if doc.has_vector and doc.vector_norm > 0:
                    return doc.vector.tolist()
            except Exception:
                pass
        
        # Fallback: Deterministic random vector based on hash
        return self._get_fallback_vector(text)

    def _get_fallback_vector(self, text: str) -> list:
        # Create a deterministic seed from the text
        hash_obj = hashlib.md5(text.encode('utf-8'))
        seed = int(hash_obj.hexdigest(), 16)
        rng = random.Random(seed)
        
        # Generate random vector
        vector = [rng.uniform(-1.0, 1.0) for _ in range(self.dim)]
        return vector

    @staticmethod
    def calculate_similarity(vec1: list, vec2: list) -> float:
        """
        Calculates Cosine Similarity between two vectors.
        Range: [-1.0, 1.0]
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(np.dot(v1, v2) / (norm1 * norm2))

    @staticmethod
    def calculate_distance(vec1: list, vec2: list) -> float:
        """
        Calculates Euclidean Distance.
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.linalg.norm(v1 - v2))
