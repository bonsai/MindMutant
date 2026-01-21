import os
import json
import datetime
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.getcwd(), 'data')
G0_DIR = os.path.join(DATA_DIR, 'g0')

class Repository:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.g0_dir = G0_DIR

    def load_source_data(self) -> List[str]:
        """
        Loads source words from json files in g0 directory (excluding population/metadata).
        """
        words = []
        if not os.path.exists(self.g0_dir):
            return []
            
        # Load domains from g0
        for filename in os.listdir(self.g0_dir):
            if filename.endswith('.json') and filename not in ['population.json', 'metadata.json', 'situation.json', 'keywords.json']:
                filepath = os.path.join(self.g0_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            words.extend(data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        return words

    def load_and_archive_injected_words(self, target_g: int) -> List[str]:
        """
        Loads new words from poll/addwords.csv if it exists.
        Moves the file to data/g{target_g}/addwords_{timestamp}.csv after loading.
        """
        csv_path = os.path.join(self.data_dir, 'addwords.csv')
        if not os.path.exists(csv_path):
            return []
            
        words = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by newline or comma
                raw_words = content.replace(',', '\n').split('\n')
                words = [w.strip() for w in raw_words if w.strip()]
                
            # Move processed file to target generation directory
            g_dir = os.path.join(self.data_dir, f"g{target_g}")
            os.makedirs(g_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"addwords_{timestamp}.csv"
            new_path = os.path.join(g_dir, new_filename)
            
            os.rename(csv_path, new_path)
            print(f"Injected {len(words)} words. Moved file to {new_path}")
        except Exception as e:
            print(f"Error loading addwords.csv: {e}")
            
        return words

    def load_generation(self, g: int) -> List[Dict[str, Any]]:
        filepath = os.path.join(self.data_dir, f"g{g}", "population.json")
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading generation {g}: {e}")
            return []

    def ensure_generation_dir(self, g: int) -> str:
        g_dir = os.path.join(self.data_dir, f"g{g}")
        os.makedirs(g_dir, exist_ok=True)
        return g_dir

    def save_population(self, g: int, population: List[Dict[str, Any]]):
        g_dir = self.ensure_generation_dir(g)
        filepath = os.path.join(g_dir, "population.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(population, f, indent=2, ensure_ascii=False)

    def save_metadata(self, g: int, count: int):
        g_dir = self.ensure_generation_dir(g)
        meta = {
            "generation": g, 
            "count": count, 
            "timestamp": datetime.datetime.now().isoformat()
        }
        with open(os.path.join(g_dir, "metadata.json"), 'w', encoding='utf-8') as f:
             json.dump(meta, f, indent=2)

    def save_keywords(self, g: int, population: List[Dict[str, Any]]):
        g_dir = self.ensure_generation_dir(g)
        keywords = list(set(p['content'] for p in population))
        keywords.sort()
        with open(os.path.join(g_dir, "keywords.json"), 'w', encoding='utf-8') as f:
            json.dump(keywords, f, indent=2, ensure_ascii=False)

    def save_situation(self, g: int, situation_data: Dict[str, Any]):
        g_dir = self.ensure_generation_dir(g)
        with open(os.path.join(g_dir, "situation.json"), 'w', encoding='utf-8') as f:
            json.dump(situation_data, f, indent=2, ensure_ascii=False)
