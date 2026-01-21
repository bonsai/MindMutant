import os
import json
import random

def generate_wordcrowd(g_dir: str):
    """
    Generates a Word Crowd HTML file from situation.json in the given generation directory.
    Uses vector analysis for visualization features (clustering, size, color).
    """
    situation_path = os.path.join(g_dir, "situation.json")
    if not os.path.exists(situation_path):
        print(f"Situation file not found: {situation_path}")
        return

    try:
        with open(situation_path, 'r', encoding='utf-8') as f:
            situation = json.load(f)
            analysis_data = situation.get("analysis", [])
            # Also get keywords for fallback or full list if analysis is partial
            # But analysis should cover all population.
            # Let's use analysis data primarily.
    except Exception as e:
        print(f"Error loading situation.json: {e}")
        return

    # HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindMutant Word Crowd (G{situation.get('generation', '?')})</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a1a;
            color: #e0e0e0;
            display: flex;
            flex-wrap: wrap;
            justify_content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }}
        .tag {{
            margin: 10px;
            padding: 5px 10px;
            background-color: #333;
            border-radius: 5px;
            transition: transform 0.2s;
            cursor: default;
            white-space: nowrap;
        }}
        .tag:hover {{
            transform: scale(1.1);
            background-color: #444;
            color: #fff;
            z-index: 10;
        }}
        .tag.selected {{
            background-color: #4CAF50;
            color: white;
            border: 1px solid #fff;
        }}
        #controls {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 10px;
            z-index: 100;
        }}
        button {{
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background-color: #0b7dda;
        }}
    </style>
</head>
<body>
    <div id="controls">
        <button onclick="copyPrompt()">📋 Generate & Copy Prompt</button>
    </div>
    <div id="container" style="text-align: center; margin-bottom: 80px;">
"""
    
    # Place words based on analysis data
    # analysis_data is expected to be a list of dicts: {'word': str, 'novelty': float, 'coherence': float, ...}
    
    if not analysis_data:
        # Fallback if analysis is empty but situation exists (should not happen normally)
        words = situation.get("population", []) # assuming simple list if not dict
        # Adapt to list of strings
        if words and isinstance(words[0], dict):
             words = [w['content'] for w in words]
        
        for word in words:
            size = random.randint(14, 48)
            hue = random.randint(0, 360)
            color = f"hsl({hue}, 70%, 75%)"
            html_content += f'        <span class="tag" style="font-size: {size}px; color: {color};" title="{word}" onclick="toggleSelection(this)">{word}</span>\n'
    else:
        # Use analysis metrics for visualization
        # Normalize novelty for size mapping (assuming range 0-1, map to 14-60px)
        # Use coherence for color (hue mapping)
        
        for item in analysis_data:
            word = item.get('content', item.get('word', '???'))
            novelty = item.get('novelty', 0.5)
            # coherence = item.get('coherence', 0.5) # Not used for color yet in this simple version
            
            # Map novelty to size: higher novelty = bigger
            # Novelty is roughly 0.0 to 1.0 (or up to 2.0). 
            # We want baseline 0.2 -> size 20. 0.8 -> size 50.
            size = 14 + int(novelty * 30) 
            if size > 80: size = 80
            if size < 12: size = 12
            
            # Map word hash to hue to keep same word same color, or use coherence if available
            # Let's use random for now but seeded by word to be consistent
            random.seed(word)
            hue = random.randint(0, 360)
            random.seed() # reset seed
            
            color = f"hsl({hue}, 75%, 70%)"
            
            # Add tooltip with metrics
            title = f"{word} (Novelty: {novelty:.2f})"
            
            html_content += f'        <span class="tag" style="font-size: {size}px; color: {color};" title="{title}" onclick="toggleSelection(this)">{word}</span>\n'

    html_content += """    </div>

    <script>
        function toggleSelection(element) {
            element.classList.toggle('selected');
        }

        function copyPrompt() {
            const selectedElements = document.querySelectorAll('.tag.selected');
            let words = [];
            
            if (selectedElements.length > 0) {
                // Use selected words
                selectedElements.forEach(el => words.push(el.innerText));
            } else {
                // If nothing selected, use all words (limit to 20 random to avoid too long prompt)
                const allTags = Array.from(document.querySelectorAll('.tag'));
                const shuffled = allTags.sort(() => 0.5 - Math.random());
                words = shuffled.slice(0, 20).map(el => el.innerText);
                alert("No words selected. Using 20 random words.");
            }

            const prompt = `Write a short story using these concepts:\\n\\n${words.join(', ')}`;
            
            navigator.clipboard.writeText(prompt).then(() => {
                alert('Prompt copied to clipboard!\\n\\n' + prompt);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                alert('Failed to copy to clipboard.');
            });
        }
    </script>
</body>
</html>"""

    # Output
    output_path = os.path.join(g_dir, "wordcrowd.html")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Word crowd generated: {output_path}")
    except Exception as e:
        print(f"Error writing wordcrowd.html: {e}")
