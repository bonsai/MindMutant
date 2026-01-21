import os
import random
import uuid
import sys
from typing import List, Dict, Any

# Ensure we can import from src.viz and src.nlp
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.viz.wordcrowd_generator import generate_wordcrowd
from src.nlp.vectorizer import Vectorizer
# Note: These imports might fail if src.ga doesn't exist (it was archived to src/.ga)
# Since this file is inside src/.ga, we should import relatively or update paths if we want to run this archived code.
# However, for now, we just update the strings as requested to match the 'src' rename.
from src.ga.repository import Repository 
from src.ga.analyzer import Analyzer
from src.ga.breeder import Breeder
from src.ga.starve import Starvation

class Evolution:
    def __init__(self):
        self.vectorizer = Vectorizer()
        self.repository = Repository()
        self.analyzer = Analyzer(self.vectorizer)
        self.breeder = Breeder()
        self.starvation = Starvation()

    def initialize_population(self, size: int = 20) -> int:
        """
        Generates g0 population from source data in g0.
        Returns the generation number (0).
        """
        words = self.repository.load_source_data()

        if not words:
            # Fallback if empty
            words = ["Idea", "Innovation", "System", "Growth", "Future"]

        population = []
        for _ in range(size):
            word = random.choice(words) if words else "Empty"
            individual = {
                "id": str(uuid.uuid4()),
                "content": word,
                "parents": [],
                "generation": 0,
                "fitness": {}
            }
            population.append(individual)
        
        self._process_and_save_generation(0, population)
        return 0

    def evolve_generation(self, current_g: int, force_disaster: bool = False) -> int:
        """
        Loads current_g, evolves to next generation, saves as g{current_g+1}.
        Returns the new generation number.
        """
        MAX_POPULATION = 50

        current_pop = self.repository.load_generation(current_g)
        if not current_pop:
            # If current gen missing, init g0
            return self.initialize_population()

        next_g = current_g + 1
        
        # Disaster Event: Delegated to Starvation module
        # Applies "survival of the fittest" (Novelty-based) every 3 generations
        next_pop = self.starvation.reap_population(current_pop, next_g, force=force_disaster)
        
        # Inject new words if any
        new_words = self.repository.load_and_archive_injected_words(next_g)
        for word in new_words:
             individual = {
                "id": str(uuid.uuid4()),
                "content": word,
                "parents": [], # Immigrant
                "generation": next_g,
                "fitness": {}
            }
             next_pop.append(individual)

        # Create children
        # Target: Add 50% more population, but cap total at MAX_POPULATION
        current_count = len(next_pop)
        
        # Calculate how many children we want (50% growth)
        desired_children = max(1, current_count // 2)
        
        # Calculate how many children we can have (Cap at MAX_POPULATION)
        allowed_children = max(0, MAX_POPULATION - current_count)
        
        # Final number of children
        num_children = min(desired_children, allowed_children)
        
        if num_children > 0:
            print(f"Breeding: Creating {num_children} children (Current: {current_count}, Max: {MAX_POPULATION})")
            children = self.breeder.breed_population(current_pop, next_g, num_children)
            next_pop.extend(children)
        else:
            print(f"Breeding skipped: Population limit reached ({current_count}/{MAX_POPULATION})")

        self._process_and_save_generation(next_g, next_pop)
        return next_g


    def _process_and_save_generation(self, g: int, population: List[Dict[str, Any]]):
        """
        Saves population, metadata, keywords, analyzes situation, and generates wordcloud.
        """
        # Analyze Situation FIRST to populate fitness data in population
        situation_data = self.analyzer.analyze(g, population)
        self.repository.save_situation(g, situation_data)

        # Save Core Data (now includes fitness/novelty)
        self.repository.save_population(g, population)
        self.repository.save_metadata(g, len(population))
        self.repository.save_keywords(g, population)
            
        # Generate Word Crowd
        g_dir = self.repository.ensure_generation_dir(g)
        generate_wordcrowd(g_dir)

if __name__ == "__main__":
    evo = Evolution()
    print("Initializing g0...")
    evo.initialize_population()
    print("Evolving to g1...")
    evo.evolve_generation(0)
    print("Done.")
