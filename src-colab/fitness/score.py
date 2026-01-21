class FitnessScore:
    @staticmethod
    def calculate_novelty(nearest_similarity: float) -> float:
        """
        Calculates novelty based on similarity to nearest neighbor.
        Novelty is defined as (1.0 - nearest_similarity).
        If no neighbor found (similarity = -2.0), returns default 0.5.
        """
        if nearest_similarity == -2.0:
            return 0.5
            
        # Novelty (1.0 - best_similarity). 
        # If similarity is high (close to 1.0), novelty is low (0.0).
        # If similarity is low (close to 0.0 or negative), novelty is high.
        return 1.0 - nearest_similarity
