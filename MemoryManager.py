class MemoryManager:

	def __init__(self):
        #Variables 
		self.memories = []
        self.memory_storage = "memories.json" #file path of where memories are stored 


    #Functions 
    def load_memories(self):
        self.memories = []
        if os.path.exists(self.memory_storage):
            with open(self.memory_storage, "r") as memories: #conversations is a list of dicts
                #load json into a dict 
                try:
                    memories_loading = json.load(memories) #load the list of dicts into local memories list 
                    #see if list is empty, nothing was loaded
                    if not memories_loading:
                        print("No memories were loaded.")
                    #loop through the list and turn each dict into an object 
                    for memory_dict in memories_loading:
                        memory = Memory.from_dict(memory_dict)
                        self.memories.append(memory)
                #print errors 
                except json.JSONDecodeError as json_err:
                    print(f"The server returned invalid JSON Formatting: {json_err}")
                    return None
                    
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
"""
    #Functions 

    def create_conversation(self):
        new_convo = Conversation() 
        next_id = 1
        if self.conversations:
            next_id = max(conversation.id_num for conversation in self.conversations) + 1
        new_convo.id_num = next_id 
        self.conversations.append(new_convo)
        self.current_conversation = new_convo 

    def get_current_conversation(self):
        return self.current_conversation 
        #who is calling this function? #probs main
        
    def save_conversations(self):
        #empty list 
        conversations_loading = []
        #loop through the list of objects and turn each object into a dict
        for conversation in self.conversations:
            #and store the dict in a new list
            conversations_loading.append(conversation.to_dict())
        
        #save all conversations to the conversation.json 
        with open(self.conversations_storage, "w") as conversations: #and file is open with our list of saved conversations  
            #dump the list into storage 
            json.dump(conversations_loading, conversations) 

        
        
    def load_conversation(self, id_selection):
        self.current_conversation = None 
        for conversation in self.conversations:
            if conversation.id_num == id_selection:
                self.current_conversation = conversation 
                break 
        
    def switch_conversation(self, id_selection):
        self.save_conversations()
        self.load_conversation(self.id_selection)
        
    def delete_conversation(self):
        for conversation in self.conversations:
            if conversation.id_num == self.id_selection:
                self.conversations.remove(conversation)
                break 
        
    def list_conversations(self):
        conversation_list = []
        for conversation in self.conversations:
            conversation_list.append(conversation.summary)
        return conversation_list """