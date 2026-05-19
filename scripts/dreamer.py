import os
import re
import json
import sys
from datetime import datetime

# GBrain Layer 8: The Dreamer (Alpha v1.0)
# Purpose: Semantic synthesis of session logs into the Research Hub (~/wiki)

WIKI_PATH = os.path.expanduser("~/wiki")
LOG_DIR = os.path.join(WIKI_PATH, "logs")
CONCEPTS_DIR = os.path.join(WIKI_PATH, "concepts")
ENTITIES_DIR = os.path.join(WIKI_PATH, "entities")

def ensure_dirs():
    for d in [CONCEPTS_DIR, ENTITIES_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

def synthesize_log(log_path):
    """
    In a real production environment, this would call an LLM to extract signal.
    For this harness-alpha, we use a structured heuristic that simulates the 
    semantic extraction based on the latest HE v3.0 session patterns.
    """
    print(f"Dreaming over {log_path}...")
    with open(log_path, 'r') as f:
        content = f.read()
    
    # Simulate extraction of potential concepts (Markdown headers or bold terms)
    concepts = re.findall(r'\*\*([^*]{3,20})\*\*', content)
    
    for concept in set(concepts):
        # Normalize name for file
        clean_name = re.sub(r'[^a-z0-9]', '-', concept.lower()).strip('-')
        if not clean_name: continue
        
        target_path = os.path.join(CONCEPTS_DIR, f"{clean_name}.md")
        
        # Check if exists to avoid overwriting metadata
        if os.path.exists(target_path):
            print(f"Updating concept: {clean_name}")
            with open(target_path, 'a') as f:
                f.write(f"\n- Updated during Dream Cycle: {datetime.now().isoformat()}\n")
        else:
            print(f"Discovering new concept: {clean_name}")
            with open(target_path, 'w') as f:
                f.write(f"# {concept}\n\nStatus: Synthesized\nSource: {os.path.basename(log_path)}\n\n## Description\nGenerated via GBrain Layer 8 Synthesis.\n")

if __name__ == "__main__":
    ensure_dirs()
    # Process the latest logs from today
    today_str = datetime.now().strftime("%Y%m%d")
    for log_file in os.listdir(LOG_DIR):
        if today_str in log_file and log_file.endswith(".md"):
            synthesize_log(os.path.join(LOG_DIR, log_file))
