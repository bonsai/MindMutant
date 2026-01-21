import random
from typing import List

# Connectors for sentence formation
CONNECTORS = [
    "みたいな", "を使って", "のような", "的", "としての", 
    "と", "や", "あるいは", "もしくは", "の中の", 
    "における", "に対する", "関する", "基づく"
]

def mutate_sentence(individual: List[str], all_words_pool: List[str], indpb: float = 0.2) -> tuple[List[str]]:
    """
    Mutates an individual (list of words) by:
    1. Replacing a word with a random word from the pool (standard mutation).
    2. Inserting a connector between words to form phrases/sentences.
    3. Appending a connector + new word.
    
    Args:
        individual: List of strings (words/tokens).
        all_words_pool: List of available words to sample from.
        indpb: Independent probability for each attribute to be mutated.
    """
    
    # 1. Standard Word Replacement
    for i in range(len(individual)):
        if random.random() < indpb and all_words_pool:
            individual[i] = random.choice(all_words_pool)
            
    # 2. Structure Mutation (Sentence Formation)
    # Probability to add a connector/phrase extension
    if random.random() < indpb:
        action = random.choice(["insert_connector", "append_phrase", "prepend_phrase"])
        
        if action == "insert_connector" and len(individual) >= 2:
            # Insert a connector between two existing words
            idx = random.randint(1, len(individual) - 1)
            connector = random.choice(CONNECTORS)
            # Avoid double connectors
            if individual[idx-1] not in CONNECTORS and individual[idx] not in CONNECTORS:
                individual.insert(idx, connector)
                
        elif action == "append_phrase" and all_words_pool:
            # Add "connector + new_word" at the end
            connector = random.choice(CONNECTORS)
            new_word = random.choice(all_words_pool)
            individual.append(connector)
            individual.append(new_word)

        elif action == "prepend_phrase" and all_words_pool:
             # Add "new_word + connector" at the start
            connector = random.choice(CONNECTORS)
            new_word = random.choice(all_words_pool)
            individual.insert(0, connector)
            individual.insert(0, new_word)

    return individual,
