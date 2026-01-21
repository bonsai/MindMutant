import os
import random
import json
import shutil
import uuid
from typing import List, Dict, Any
from deap import base, creator, tools, algorithms

from src.deap.repository import Repository
from src.deap.starvation import Starvation
from src.nlp.evaluator import Evaluator
from src.nlp.vectorizer import Vectorizer
from src.deap.operators import evaluate_novelty, mate_combine
from src.deap.mutation import mutate_sentence

# Define DEAP types
# Fitness: Maximize Novelty
if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax, id=str, content=str)

class Evolution:
    def __init__(self, data_dir: str = "data"):
        self.vectorizer = Vectorizer()
        self.repo = Repository()
        self.starvation = Starvation()
        self.evaluator = Evaluator(self.vectorizer)
        self.toolbox = base.Toolbox()
        self.setup_toolbox()
        
    def setup_toolbox(self):
        # Attribute generator (not used directly for population loading, but needed for new randoms if any)
        # self.toolbox.register("attr_word", ...) 
        
        # Structure initializers (we'll load from JSON mostly)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, lambda: [])
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # Operators
        self.toolbox.register("evaluate", evaluate_novelty)
        self.toolbox.register("mate", mate_combine)
        # Mutation needs a pool of words. We'll update this alias dynamically or pass it.
        self.toolbox.register("mutate", mutate_sentence, all_words_pool=[]) 
        self.toolbox.register("select", tools.selBest) # Select best novelty
        # Or tournament: self.toolbox.register("select", tools.selTournament, tournsize=3)

    def load_generation(self, gen_idx: int) -> List[Any]:
        """Load population from JSON files into DEAP individuals."""
        data = self.repo.load_generation(gen_idx)
        population = []
        for item in data:
            # Create individual from 'content' (space separated string)
            words = item['content'].split()
            ind = creator.Individual(words)
            ind.id = item['id']
            ind.content = item['content']
            # We might need to re-evaluate fitness later
            population.append(ind)
        return population

    def save_generation(self, population: List[Any], gen_idx: int):
        """Save DEAP population to JSON files."""
        data_list = []
        situation_list = []
        
        for ind in population:
            # Update content from list
            content = " ".join(ind)
            ind.content = content
            
            # Extract fitness if available
            fitness_val = ind.fitness.values[0] if ind.fitness.valid else 0.0
            
            item = {
                "id": ind.id, 
                "content": content,
                "fitness": {"novelty": fitness_val},
                "tags": [] # Legacy support
            }
            data_list.append(item)
            
            situation_list.append({
                "id": ind.id,
                "content": content,
                "fitness": {"novelty": fitness_val}
            })
            
        self.repo.save_population(gen_idx, data_list)
        self.repo.save_metadata(gen_idx, len(population))
        self.repo.save_keywords(gen_idx, data_list)
        
        # Save situation.json for visualization (with wrapper)
        situation_data = {
            "generation": gen_idx,
            "analysis": situation_list
        }
        self.repo.save_situation(gen_idx, situation_data)

    def evolve(self, current_g: int, force_disaster: bool = False) -> int:
        next_g = current_g + 1
        print(f"🧬 Evolving from g{current_g} to g{next_g} using DEAP...")
        
        # 1. Load Population
        population = self.load_generation(current_g)
        if not population:
            print("⚠️  No population found.")
            return current_g

        # 2. Inject New Words (Pollination)
        new_words = self.repo.load_and_archive_injected_words(next_g)
        if new_words:
            print(f"✨ Injected {len(new_words)} new words.")
            for word in new_words:
                words_list = word.split()
                ind = creator.Individual(words_list)
                ind.id = str(uuid.uuid4())
                ind.content = word
                population.append(ind)
            
        # 3. Vectorize Population for Evaluation context
        pop_vectors = {}
        all_words_pool = set()
        for ind in population:
            content = " ".join(ind)
            pop_vectors[ind.id] = self.evaluator.vectorize(content)
            for w in ind:
                all_words_pool.add(w)
        
        # Update mutation pool
        self.toolbox.register("mutate", mutate_words, all_words_pool=list(all_words_pool))

        # 4. Evaluate Fitness (Novelty)
        for ind in population:
            ind.fitness.values = self.toolbox.evaluate(ind, pop_vectors, self.evaluator)

        print(f"📊 Evaluated {len(population)} individuals.")

        # 5. Disaster Event (Selection) via Starvation Component
        survivors = self.starvation.reap_population(population, next_g, force=force_disaster)
        
        # 6. Breeding (Offspring Generation)
        target_size = 50 # Max population constraint
        current_size = len(survivors)
        
        offspring = []
        num_children = target_size - current_size
        if num_children < 0: num_children = 0
        
        if num_children > 0 and len(survivors) >= 2:
            for _ in range(num_children):
                # Select 2 parents
                parent1 = self.toolbox.select(survivors, 1)[0]
                parent2 = self.toolbox.select(survivors, 1)[0]
                
                # Clone
                child1, child2 = self.toolbox.clone(parent1), self.toolbox.clone(parent2)
                
                # Mate & Mutate
                self.toolbox.mate(child1, child2)
                self.toolbox.mutate(child1)
                
                # Assign new ID
                child1.id = str(uuid.uuid4())
                del child1.fitness.values # Invalidate fitness
                
                offspring.append(child1)
        
        # 7. Next Generation Population
        next_population = survivors + offspring
        
        # 8. Max Population Constraint (Final Check)
        if len(next_population) > 50:
            print("✂️  Capping population at 50.")
            # Evaluate new offspring to have valid fitness for comparison
            # We'll eval them against the survivors (established culture)
            for ind in offspring:
                if not ind.fitness.valid:
                    ind.fitness.values = self.toolbox.evaluate(ind, pop_vectors, self.evaluator)
            
            # Select best 50
            next_population = tools.selBest(next_population, 50)
            
        # 9. Save
        self.save_generation(next_population, next_g)
        
        # 10. Visualize (Wordcrowd)
        try:
            from src.viz.wordcrowd_generator import generate_wordcrowd
            g_dir = self.repo.ensure_generation_dir(next_g)
            generate_wordcrowd(g_dir)
            print(f"Word crowd generated: {os.path.join(g_dir, 'wordcrowd.html')}")
        except Exception as e:
            print(f"⚠️  Visualization failed: {e}")
            
        print(f"\nSuccess! Generation g{next_g} created.")
        return next_g
