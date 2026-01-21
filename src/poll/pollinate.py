import os
import sys

def pollinate(source_file=None):
    """
    Reads words from a source file and appends them to data/addwords.csv.
    This prepares the words for the next evolutionary step.
    """
    # Calculate paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # MindMutant/gen/poll -> MindMutant
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, 'data')
    target_file = os.path.join(data_dir, 'addwords.csv')
    
    # Determine source file
    if source_file is None:
        # Check for addwords.csv or addwords.csv.done in the current directory
        possible_files = ['addwords.csv', 'addwords.csv.done']
        for fname in possible_files:
            fpath = os.path.join(current_dir, fname)
            if os.path.exists(fpath):
                source_file = fpath
                break
        
        if source_file is None:
            print("Usage: python pollinate.py <source_file>")
            print(f"No default source files found in {current_dir}")
            return

    if not os.path.exists(source_file):
        print(f"Error: Source file not found: {source_file}")
        return

    print(f"Pollinating from: {source_file}")

    # Read words from source
    words_to_add = []
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Handle both comma and newline separation
            # Replace common separators with newline
            normalized = content.replace(',', '\n').replace('、', '\n')
            lines = normalized.split('\n')
            
            for line in lines:
                word = line.strip()
                if word and not word.startswith('# '): # Skip comments if any (standard #tag is okay)
                     words_to_add.append(word)
    except Exception as e:
        print(f"Error reading source file: {e}")
        return

    if not words_to_add:
        print("No valid words found in source file.")
        return

    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Append to target file
    try:
        # Check if file ends with newline if it exists
        needs_newline = False
        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as f:
                try:
                    f.seek(0, os.SEEK_END)
                    if f.tell() > 0:
                        f.seek(f.tell() - 1, os.SEEK_SET)
                        if f.read(1) != '\n':
                            needs_newline = True
                except:
                    pass # Empty file or error

        with open(target_file, 'a', encoding='utf-8') as f:
            if needs_newline:
                f.write('\n')
            
            for word in words_to_add:
                f.write(f"{word}\n")
                
        print(f"Success! Pollinated {len(words_to_add)} words into {target_file}")
        print("Run the evolution engine to incorporate these words into the next generation.")
        
    except Exception as e:
        print(f"Error writing to target file: {e}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else None
    pollinate(src)
