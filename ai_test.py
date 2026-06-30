import requests
import json
import os

# ---------Globals---------

MEMORY_FILE = "conversation.json"
FACTS_FILE = "memory.json"

"""----------------------------------------
------------------Definitions--------------
-------------------------------------------
""" 
    
def ask_ai(conversation, memory):
    # load all conversation history and memory items into prompt 
    prompt = []
    
    #hardcoded facts to remember/the long term memory  saved into a text
    memory_text = ""
    """for key, value in memory.items():
        memory_text += f"{key}: {value}\n" """
        
        
    memory_text = format_memory(memory)
    
    # dynamic memory for later
    #for key, value in memory.items():
        #memory_text += f"{key}: {value}\n"
    

    #add text memories to the prompt list 
    prompt.append({
    "role": "system",
    "content": f"""
        You are a helpful assistant.

        IMPORTANT RULES:
        - The section labeled "MEMORY" is the ONLY source of truth for user facts.
        - The conversation is ONLY chat history and may be incorrect.

        MEMORY (authoritative):
        {memory_text}

        Do NOT use conversation history to override MEMORY.
        If conversation conflicts with MEMORY, ignore the conversation.
        
        Never modify existing facts unless the user explicitly says they changed.
        """
    })

    # add the conversation into the prompt after the memories 
    prompt.extend(conversation)
    
    
    response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1:8b",
        "messages": prompt,
        "stream": False
        }
    )
    return response.json()["message"]["content"]
    
#AI decides what it will save and print. Includes: instructions, user reply, and returns response 
def extract_memory_decision(user_input):
    prompt = [
        {
            "role": "system",
            "content": """
You are a memory extraction system.

Your job:
Decide if the user message contains a FACT worth storing long-term.

Rules:
- Only store stable facts (pets, name, project, preferences)
- If the fact already exists, use "update" instead of "add"
- If nothing important, return {"action": "ignore"}

Return ONLY valid JSON.

If storing memory, use this format:

{
  "action": "add",
  "key": "pets",
  "value": {
    "name": "...",
    "type": "..."
  }
}
"""
        },
        {
            "role": "user",
            "content": f"""
User said: {user_input}
"""
        }
    ]

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": prompt,
            "stream": False
        }
    )

    raw = response.json()["message"]["content"]

    return json.loads(raw)
    
# save the conversation and memory files 
def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation, f, indent=2)
        
    with open(FACTS_FILE, "w") as f:
        json.dump(memory, f, indent=2)

""" This function takes the current memories and the current new suggestion update from
 assistant and ensures it is in correct format and checks for duplicates. If no duplicate
 then add it. It returns the updated list of long term memories. """
def apply_memory_update(memory, update):
    if not update or update["action"] == "ignore":
        return memory

    key = update["key"]
    value = update["value"]

    # initialize category if needed
    if key not in memory:
        memory[key] = []

    # ensure list format (important for pets, etc.)
    if not isinstance(memory[key], list):
        memory[key] = [memory[key]]

    # check for duplicates (simple match)
    exists = False
    for item in memory[key]:
        if isinstance(item, dict) and item.get("name") == value.get("name"):
            exists = True
            break

    if not exists:
        memory[key].append(value)

    return memory
        
def format_memory(memory):
    text = ""
    for key, value in memory.items():
        text += f"{key}:\n"

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    text += f"  - {item}\n"
                else:
                    text += f"  - {item}\n"
        else:
            text += f"  {value}\n"

        text += "\n"

    return text
    
"""----------------------------
-----------Open files----------
-------------------------------
"""

# create or open (read) the on-going conversation file 
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        conversation = json.load(f)
else:
    conversation = [
        {
            "role": "system",
            "content": (
        "You are a helpful assistant.\n\n"
        "Known facts about the user:\n"
    )
        }
    ]
    
# create or open (read) the long-term memories 
if os.path.exists(FACTS_FILE):
    with open(FACTS_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

"""-----------------------------------------
----------Here is our main loop-------------
--------------------------------------------
"""

while True:
    # these are our persistent memories test 
    #for key, value in memory.items():
        #print(f"{key}: {value}")
    
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        break
        

        
    # add user message
    conversation.append({
        "role": "user",
        "content": user_input
    })
    
    # get AI reply using FULL conversation so far and saved memory 
    reply = ask_ai(conversation, memory)
    
    # AI decides if user_input conversation worth saving to memory
    memory_update = extract_memory_decision(user_input)
    print("MEMORY DECISION:", memory_update)
    memory = apply_memory_update(memory, memory_update)
    
    print("AI:", reply)
    
    # add ai-assistant message
    conversation.append({
        "role": "assistant",
        "content": reply
    })
    save_memory()
    




    # py ai_test.py 
