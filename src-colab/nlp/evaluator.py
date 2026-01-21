from typing import List, Dict, Tuple, Optional
from src.nlp.vectorizer import Vectorizer

class Evaluator:
    def __init__(self, vectorizer: Vectorizer):
        self.vectorizer = vectorizer

    def vectorize(self, text: str) -> List[float]:
        return self.vectorizer.get_vector(text)

    def calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        return self.vectorizer.calculate_similarity(vec1, vec2)

    def find_neighbors(self, target_id: str, vectors_map: Dict[str, List[float]]) -> Tuple[Optional[str], float, Optional[str], float]:
        """
        Finds the nearest and furthest neighbors for a target individual within the provided vectors map.
        Returns (best_mate_id, best_sim, worst_mate_id, worst_sim).
        """
        target_vec = vectors_map.get(target_id)
        if not target_vec:
            return None, -2.0, None, 2.0

        best_sim = -2.0
        best_mate = None
        worst_sim = 2.0
        worst_mate = None
        
        for other_id, other_vec in vectors_map.items():
            if target_id == other_id:
                continue
                
            sim = self.vectorizer.calculate_similarity(target_vec, other_vec)
            
            if sim > best_sim:
                best_sim = sim
                best_mate = other_id
            
            if sim < worst_sim:
                worst_sim = sim
                worst_mate = other_id
                
        return best_mate, best_sim, worst_mate, worst_sim
