from typing import List, Dict, Any
from src.nlp.vectorizer import Vectorizer
from src.nlp.evaluator import Evaluator
from src.fitness.score import FitnessScore

class Analyzer:
    def __init__(self, vectorizer: Vectorizer):
        self.vectorizer = vectorizer
        self.evaluator = Evaluator(vectorizer)

    def analyze(self, g: int, population: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes the population to generate situation data including vectors and similarity/novelty metrics.
        """
        situation_data = {
            "generation": g,
            "vectors": {},
            "analysis": []
        }
        
        # 1. Calculate vectors for all individuals
        # Map id -> vector
        vectors_map = {}
        for ind in population:
            # For performance, only vectorizing the content once per unique content might be better,
            # but population is small for now.
            vec = self.vectorizer.get_vector(ind['content'])
            vectors_map[ind['id']] = vec
            situation_data["vectors"][ind['id']] = vec
            
        # 2. Calculate pairwise similarities (Analysis)
        ids = list(vectors_map.keys())
        
        # Limit analysis if population is too large (e.g., > 200) to avoid slow O(N^2)
        # For now, assuming N is small enough.
        
        for id1 in ids:
            best_mate_id, best_sim, worst_mate_id, worst_sim = self.evaluator.find_neighbors(id1, vectors_map)
            
            # Find content for readability
            content1 = next(p['content'] for p in population if p['id'] == id1)
            mate_content = next((p['content'] for p in population if p['id'] == best_mate_id), None) if best_mate_id else None
            worst_content = next((p['content'] for p in population if p['id'] == worst_mate_id), None) if worst_mate_id else None
            
            # Calculate Novelty
            novelty = FitnessScore.calculate_novelty(best_sim)
            
            # Store in population individual as well
            ind = next(p for p in population if p['id'] == id1)
            if 'fitness' not in ind:
                ind['fitness'] = {}
            ind['fitness']['novelty'] = novelty
            
            situation_data["analysis"].append({
                "id": id1,
                "content": content1,
                "novelty": round(novelty, 4),
                "nearest": {
                    "id": best_mate_id,
                    "content": mate_content,
                    "similarity": round(best_sim, 4)
                },
                "furthest": {
                    "id": worst_mate_id,
                    "content": worst_content,
                    "similarity": round(worst_sim, 4)
                }
            })
            
        return situation_data
