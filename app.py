import os
import sys
import argparse
import re

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.poll.pollinate import pollinate
from src.deap.evolution import Evolution

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def get_latest_generation():
    """
    Scans data directory for g{n} folders and returns the max n.
    Returns -1 if no generation exists.
    """
    max_g = -1
    if not os.path.exists(DATA_DIR):
        return max_g
        
    for name in os.listdir(DATA_DIR):
        if re.match(r'^g\d+$', name):
            g_num = int(name[1:])
            if g_num > max_g:
                max_g = g_num
    return max_g

def command_poll(force_disaster=False, engine_type='standard'):
    """
    1. Pollinate (inject words from poll/addwords.csv.done or similar)
    2. Evolve to next generation
    """
    print("--- Step 1: Pollination ---")
    pollinate()
    
    print("\n--- Step 2: Evolution ---")
    current_g = get_latest_generation()
    
    new_g = current_g # Default
    
    if engine_type == 'deap':
        print("Using Engine: DEAP")
        evo = DeapEvolution()
        if current_g == -1:
             print("No generation found. Please run 'standard' engine first to initialize g0.")
             return
        else:
             print(f"Current generation is g{current_g}. Evolving to g{current_g + 1}...")
             new_g = evo.evolve(current_g, force_disaster=force_disaster)
             
    else:
        print("Using Engine: Standard (Custom)")
        evo = Evolution()
        if current_g == -1:
            print("No generation found. Initializing g0...")
            new_g = evo.initialize_population()
        else:
            print(f"Current generation is g{current_g}. Evolving to g{current_g + 1}...")
            new_g = evo.evolve_generation(current_g, force_disaster=force_disaster)
        
    print(f"\nSuccess! Generation g{new_g} created.")

def command_now():
    """
    Prints the latest generation number.
    """
    g = get_latest_generation()
    if g == -1:
        print("No generations found.")
    else:
        print(f"Latest generation: g{g}")

def main():
    parser = argparse.ArgumentParser(description="MindMutant Evolution CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # New command: Generate next generation
    new_parser = subparsers.add_parser("new", help="Generate next generation")
    new_parser.add_argument("--engine", default="deap", help="Engine to use (default: deap)")
    new_parser.add_argument("--die", action="store_true", help="Force a disaster event")
    
    args = parser.parse_args()
    
    if args.command == 'poll':
        # Legacy poll command mapping to new evolution logic if needed
        # But for now, let's just use 'new' logic as poll is handled via CSV check inside evolve
        print("Polling new words...")
        current_g = get_latest_generation()
        
        # Use DEAP by default or specified
        engine = Evolution()
        
        engine.evolve(current_g, force_disaster=args.die)

    elif args.command == 'new':
        current_g = get_latest_generation()
        print(f"Current generation: g{current_g}")
        
        # Always use Evolution (DEAP based)
        engine = Evolution()
        engine.evolve(current_g, force_disaster=args.die)

    elif args.command == 'now':
        command_now()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
