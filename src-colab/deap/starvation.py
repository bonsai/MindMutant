import random
from typing import List, Dict, Any

class Starvation:
    def reap_population(self, population: List[Any], next_g: int, force: bool = False) -> List[Any]:
        """
        Applies disaster/starvation logic.
        Every 3 generations, kills half the population based on weakness (low novelty).
        If force=True, executes disaster regardless of generation count.
        Supports both Dict-based population and DEAP Individual objects.
        """
        # Disaster Event check: g3, g6, g9... or Forced
        if force or (next_g > 0 and next_g % 3 == 0):
            reason = "FORCED DISASTER" if force else "SCHEDULED DISASTER"
            print(f"⚠️  {reason} in g{next_g}! Half of the population will perish.")
            
            if not population:
                return []

            # Helper to get novelty
            def get_novelty(ind):
                if hasattr(ind, 'fitness') and hasattr(ind.fitness, 'values'):
                    # DEAP Individual
                    return ind.fitness.values[0] if ind.fitness.valid else 0.0
                elif isinstance(ind, dict):
                    # Dict based
                    return ind.get('fitness', {}).get('novelty', 0.0)
                return 0.0

            # Sort descending: Strongest (High Novelty) -> Weakest (Low Novelty)
            population.sort(key=get_novelty, reverse=True)
            
            # Select survivors (top half)
            num_survivors = max(1, len(population) // 2)
            survivors = population[:num_survivors]
            
            print(f"💀 Population reduced from {len(population)} to {len(survivors)}.")
            
            # For objects, we usually copy? 
            # In DEAP, `toolbox.select` or slicing is fine if we don't need deep copy for next step immediately.
            # But let's return a slice.
            return survivors
            
        else:
            # No disaster, everyone survives
            return population[:]
