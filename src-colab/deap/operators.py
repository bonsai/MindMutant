import random
from typing import List, Dict, Any, Tuple
from deap import base, creator, tools

from src.nlp.evaluator import Evaluator
from src.fitness.score import FitnessScore

# Initialize Evaluator and FitnessScore globally or pass them in
# For DEAP operators, it's often easier to use closures or global/singleton access if state is needed
# Here we'll assume they are initialized in the main engine and passed or used via wrapper functions

def evaluate_novelty(individual: List[str], population_vectors: Dict[str, Any], evaluator: Evaluator) -> Tuple[float]:
    """
    Calculate novelty score for an individual.
    Returns a tuple (score,) as DEAP expects.
    """
    # Create a dummy ID for the individual to use existing evaluator logic if needed,
    # or just use the raw vector logic.
    # The existing analyzer calculates novelty based on the whole population.
    # In DEAP, evaluation is often per individual.
    # Novelty requires context of the population (or archive).
    
    # If population_vectors is available, we calculate distance to nearest neighbors.
    # For now, let's assume we calculate it based on the current population context provided.
    
    # Get vector for this individual
    text = " ".join(individual)
    vector = evaluator.vectorize(text)
    
    # Calculate similarity to others in the provided map
    if not population_vectors:
        return (1.0,) # Max novelty if alone
        
    # We need to find max similarity to any other individual in the population
    # distinct from self (if self is in population).
    
    max_sim = 0.0
    for other_id, other_vec in population_vectors.items():
        # We don't have an ID for 'individual' yet, so we just compare to all.
        # If the individual is exactly the same as one in population, sim is 1.0.
        sim = evaluator.calculate_similarity(vector, other_vec)
        if sim > max_sim:
            max_sim = sim
            
    # Novelty = 1.0 - Max Similarity
    novelty = 1.0 - max_sim
    return (novelty,)

def mate_combine(ind1: List[str], ind2: List[str]) -> Tuple[List[str], List[str]]:
    """
    Crossover: Combine words from two parents.
    Returns two new individuals.
    """
    # Simple one-point crossover on the list of words?
    # Or mixing words set-wise?
    # Existing logic: "Parents' words are combined, child gets a mix."
    
    # Let's do a simple set mix then split
    pool = list(set(ind1 + ind2))
    random.shuffle(pool)
    
    # Split point
    if len(pool) > 1:
        split = random.randint(1, len(pool) - 1)
        c1 = pool[:split]
        c2 = pool[split:]
    else:
        c1 = pool[:]
        c2 = pool[:]
        
    # Ensure they are not empty?
    if not c1: c1 = ["void"]
    if not c2: c2 = ["void"]
    
    # Update individuals in place (DEAP convention)
    ind1[:] = c1
    ind2[:] = c2
    
    return ind1, ind2

def mutate_words(individual: List[str], all_words_pool: List[str], indpb: float = 0.2) -> Tuple[List[str]]:
    """
    Mutation: Add or remove words.
    """
    if random.random() < 0.5:
        # Add a word
        if all_words_pool:
            word = random.choice(all_words_pool)
            if word not in individual:
                individual.append(word)
    else:
        # Remove a word
        if len(individual) > 1:
            individual.pop(random.randint(0, len(individual) - 1))
            
    return (individual,)
