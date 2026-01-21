import random
import uuid
from typing import List, Dict, Any

class Breeder:
    """
    Handles mating, constraints, and offspring creation.
    交配、制約チェック、個体生成を担当するクラス。
    """
    def __init__(self):
        pass

    def is_related(self, p1: Dict, p2: Dict) -> bool:
        """
        2つの個体が血縁関係（親子または兄弟）にあるかチェックします。
        Checks if two individuals are related (parent-child or siblings).
        """
        # 親子関係のチェック (Check parent-child relationship)
        # どちらかのIDがもう一方の親リストに含まれているか
        if p1['id'] in p2['parents'] or p2['id'] in p1['parents']:
            return True
            
        # 兄弟関係のチェック (Check siblings)
        # 親リストに共通のIDが含まれているか（共通の親を持つか）
        if p1['parents'] and p2['parents']:
            if set(p1['parents']) & set(p2['parents']):
                return True
        return False

    def create_offspring(self, parent1: Dict, parent2: Dict, generation: int) -> Dict[str, Any]:
        """
        Creates a new child from two parents.
        Applies naming rules (newer generation name comes first).
        """
        # Crossover: "New names come first" (新しい世代の親の名前を前にする)
        p1_gen = parent1.get('generation', 0)
        p2_gen = parent2.get('generation', 0)
        
        if p1_gen > p2_gen:
            # Parent1 is newer
            child_content = f"{parent1['content']} {parent2['content']}"
        elif p2_gen > p1_gen:
            # Parent2 is newer
            child_content = f"{parent2['content']} {parent1['content']}"
        else:
            # Same generation
            child_content = f"{parent1['content']} {parent2['content']}"

        child = {
            "id": str(uuid.uuid4()),
            "content": child_content,
            "parents": [parent1['id'], parent2['id']],
            "generation": generation,
            "fitness": {}
        }
        return child

    def breed_population(self, current_pop: List[Dict], next_g: int, target_children: int) -> List[Dict]:
        """
        Generates a list of children from the current population.
        """
        children = []
        attempts = 0
        children_created = 0
        max_attempts = target_children * 20 

        while children_created < target_children and attempts < max_attempts:
            attempts += 1
            parent1 = random.choice(current_pop)
            parent2 = random.choice(current_pop)
            
            # Self-check
            if parent1['id'] == parent2['id']:
                continue
                
            # Incest check
            if self.is_related(parent1, parent2):
                continue
            
            child = self.create_offspring(parent1, parent2, next_g)
            children.append(child)
            children_created += 1
            
        return children

if __name__ == "__main__":
    # Test logic integrated from verify_constraints.py
    print("Running Breeder Tests...")
    
    breeder = Breeder()
    
    # Setup IDs
    id_parent1 = str(uuid.uuid4())
    id_parent2 = str(uuid.uuid4())
    id_child1 = str(uuid.uuid4())
    id_child2 = str(uuid.uuid4())
    id_unrelated = str(uuid.uuid4())

    # Create Individuals
    p1 = {"id": id_parent1, "parents": [], "content": "P1", "generation": 0}
    p2 = {"id": id_parent2, "parents": [], "content": "P2", "generation": 0}
    
    # Child of P1 and P2
    c1 = {"id": id_child1, "parents": [id_parent1, id_parent2], "content": "C1", "generation": 1}
    
    # Another child of P1 and P2
    c2 = {"id": id_child2, "parents": [id_parent1, id_parent2], "content": "C2", "generation": 1}
    
    # Unrelated
    u1 = {"id": id_unrelated, "parents": [], "content": "U1", "generation": 0}

    # 1. Parent-Child Check
    assert breeder.is_related(p1, c1) == True, "Failed: Parent (P1) and Child (C1) should be related"
    assert breeder.is_related(c1, p1) == True, "Failed: Child (C1) and Parent (P1) should be related"
    print("PASS: Parent-Child checks")

    # 2. Sibling Check
    assert breeder.is_related(c1, c2) == True, "Failed: Siblings (C1, C2) should be related"
    print("PASS: Sibling checks")

    # 3. Unrelated Check
    assert breeder.is_related(p1, u1) == False, "Failed: P1 and U1 should NOT be related"
    print("PASS: Unrelated checks")

    # 4. Generation Naming Rule Check
    # P3 (Newer) x P4 (Older)
    p3 = {"id": str(uuid.uuid4()), "content": "New", "generation": 2}
    p4 = {"id": str(uuid.uuid4()), "content": "Old", "generation": 1}
    child_new_first = breeder.create_offspring(p3, p4, 3)
    assert child_new_first['content'] == "New Old", f"Failed: Expected 'New Old', got '{child_new_first['content']}'"
    
    child_old_last = breeder.create_offspring(p4, p3, 3)
    assert child_old_last['content'] == "New Old", f"Failed: Expected 'New Old', got '{child_old_last['content']}'"
    
    print("PASS: Naming rule checks")
    print("All Breeder tests passed.")
