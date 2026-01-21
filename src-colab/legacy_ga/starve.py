import random
from typing import List, Dict, Any
from src.fitness.score import FitnessScore

class Starvation:
    def reap_population(self, population: List[Dict[str, Any]], next_g: int, force: bool = False) -> List[Dict[str, Any]]:
        """
        Applies disaster/starvation logic.
        Every 3 generations, kills half the population based on weakness (low novelty).
        If force=True, executes disaster regardless of generation count.
        """
        # Disaster Event check: g3, g6, g9... or Forced
        if force or (next_g > 0 and next_g % 3 == 0):
            if force:
                print(f"⚠️  FORCED DISASTER EVENT in g{next_g}! Half of the population will perish.")
            else:
                print(f"⚠️  DISASTER EVENT in g{next_g}! Half of the population will perish.")
            
            # Check for fitness data
            # Assuming if the first element has it, most/all have it or we rely on it.
            # If population is empty, nothing to do.
            if not population:
                return []

            has_fitness = 'fitness' in population[0] and 'novelty' in population[0]['fitness']
            
            if has_fitness:
                print("Sorting population by Novelty (Weakest will die)...")
                # Sort descending: Strongest (High Novelty) -> Weakest (Low Novelty)
                population.sort(key=lambda x: x['fitness'].get('novelty', 0), reverse=True)
            else:
                print("No fitness data found. Falling back to random selection.")
                random.shuffle(population)
            
            # Select survivors (top half)
            num_survivors = max(1, len(population) // 2)
            survivors = population[:num_survivors]
            
            return [p.copy() for p in survivors]
            
        else:
            # No disaster, everyone survives
            return [p.copy() for p in population]
