import requests
import json
import os
import datetime 

# ---------Globals---------

manager = ConversationManager() 
MEMORY_FILE = "memory.json"

"""----------------------------------------
------------------Definitions--------------
-------------------------------------------
""" 
    
def ask_ai(conversation, memory): #this takes two dicts 
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
    
    
    reply = query_llm(prompt) #send the list of thw two dicts 
    if reply is None:
        return "Something went wrong. Make sure Ollama is running and retry."
    return reply 
    
#AI decides what it will save and print. Includes: instructions, user reply, and returns response 
def extract_memory_decision(user_input):
    prompt = [
        {
            "role": "system",
            "content": """
You are a memory extraction system within a personal ai assistant system. 

Your job:
Decide if the user message contains a FACT worth storing long-term.

Rules:
- Only store stable facts (pets, name, project, preferences)
- Some common topics expected to be long-term: pets, career, projects, work, finanicals, family, troubleshooting, health, philosophy. 
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

    raw = query_llm(prompt)
    if raw is None:
        return {"action":"ignore"}
    try: 
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"action": "ignore"}

   
def query_llm(prompt)
    
    try:
    response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1:8b",
        "messages": prompt, 
        "stream": False
        }
    )
    return response.json()["message"]["content"] 
    except requests.exceptions.ConnectionError:
        return None 
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"The server returned invalid JSON Formatting: {json_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"a network, HTTP, or connection error occured: {req_err}") 
        return None
    
# save the conversation and memory files 
def save_memory():
        
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

""" This function takes the current memories and the current new suggestion update from
 assistant and ensures it is in correct format and checks for duplicates. If no duplicate
 then add it. It returns the updated list of long term memories. """
def apply_memory_update(memory, update):
    if not update or update["action"] == "ignore":
        return memory

    key = update["key"]
    value = update["value"]
    if not key or value is None:
        return memory

    # initialize category if needed
    if key not in memory:
        memory[key] = []

    # ensure list format (important for pets, etc.)
    if not isinstance(memory[key], list):
        memory[key] = [memory[key]]

    # check for duplicates (simple match)
    match_index = None
    for i, item in enumerate(memory[key]):
        if isinstance(item, dict) and isinstance(value, dict) and item.get("name") == value.get("name"):
            match_index = i
            break
            
    if match_index is not None:
        memory[key][match_index] = value 
    else: 
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
manager = ConversationManager() #conversation manager intializes: list of conversations[conversation objects] from file
#now we can select any previous conversation, but we start with current_conversation = None 
manager.load_conversations() 

while True:
    #if user chooses new conversation: 
    print("Available conversations:\n")
    for conversation in manager.conversations:
        print(f"{conversation.id_num} - {conversation.name}")
    user_input = input("Enter new or conversation number:")
        # user input asks for either a new conversation or an id of stored conversation
    if user_input.lower() == "new":
        manager.create_conversation() #this starts the application out with a fresh conversation object. It adds this fresh 
        #conversation to the conversation[] list and sets the current_conversation to this one. 
        break
        
    manager.load_conversation(int(user_input)) #else load the selected conversation 
        
    if manager.get_current_conversation() is not None: #if input was incorrect and nothing loaded, then current_conversation will still be None and we should loop again
        break
    print("Conversation not found.")

# create or open (read) the long-term memories 
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
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
    conversation = manager.get_current_conversation()
    conversation.add_message("user", user_input)
    
    # get AI reply using FULL conversation so far and saved memory 
    reply = ask_ai(manager.get_current_conversation().history, memory) 
    
    # AI decides if user_input conversation worth saving to memory
    memory_update = extract_memory_decision(user_input)
    print("MEMORY DECISION:", memory_update)
    memory = apply_memory_update(memory, memory_update)
    
    print("AI:", reply)
    
    # add ai-assistant message
    conversation().add_message("assistant", reply)

    #this is where we need to summarize the create_conversation, we will get to that here in a bit 
    manager.save_conversations() #This saves all conversations, including the current_conversation that we just updated
    print("Saved Conversation ID: " + manager.get_current_conversation().id_num) #this is so we can see the id of the conversation we are on, this will be taken out at a later time 
    save_memory()
    




    # py ai_test.py 
    