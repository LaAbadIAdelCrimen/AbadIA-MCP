import os
import json

def st_loop_demonstration(goal_text):
    print(f"Goal: {goal_text}")
    print("--- [HE v3.0 ST-Loop Started] ---")
    
    # 1. Consult Vault (Services)
    vault_services_path = "docs/vault/services.md"
    print(f"1. CONSULTING VAULT: {vault_services_path}")
    # In a real agent, this would be a semantic search. Here we mock the extraction.
    available_tools = ["get_full_game_state", "move_to_location", "talk_to_character"]
    
    # 2. Consult Vault (Security)
    vault_security_path = "docs/vault/security.md"
    print(f"2. CONSULTING SECURITY POLICIES: {vault_security_path}")
    policies = ["Respect Horarium", "Maintain Obsequium > 15"]
    
    # 3. Generate Task List
    print("3. GENERATING ATOMIC TASKS...")
    tasks = [
        {"id": "T001", "action": "get_full_game_state", "context": "Find Guillermo's position"},
        {"id": "T002", "action": "move_to_location", "params": {"location": "Abbot's Cell"}, "constraint": "Horarium: Prime"},
        {"id": "T003", "action": "talk_to_character", "params": {"character": "Abbot"}, "context": "Meet the Abbot"}
    ]
    
    # 4. Create Harness Requirement
    print("4. DEFINING HARNESS (Beyoncé Rule)...")
    harness = "tests/test_meeting_abbot.py"
    
    print("\n--- [RESULT: Taskified Plan] ---")
    for task in tasks:
        print(f"[{task['id']}] {task['action']}({task.get('params', '')}) -> {task['context'] if 'context' in task else ''}")
    
    print(f"\nVerification Harness Required: {harness}")

if __name__ == "__main__":
    st_loop_demonstration("Arrive at the abbey and meet the Abbot.")
