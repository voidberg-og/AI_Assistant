class MemoryManager:

	def __init__(self):
        #Variables 
		self.memories = [] #list of memory objects 
        self.memory_storage = "memories.json" #file path of where memories are stored 


    #Functions 
    def load_memories(self):
        self.memories = [] #list of memory objects 
        if os.path.exists(self.memory_storage):
            with open(self.memory_storage, "r") as memories: #memories is a list of dicts from json storage 
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
                    
    '''def save_memory():
        
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)'''
            
    def save_memories():
    #empty list 
    memories_loading = []
    #loop through the list of objects and turn each object into a dict
    for memory in self.memories:
        #and store the dict in a new list
        memories_loading.append(memory.to_dict())
    
    #save all conversations to the conversation.json 
    with open(self.memory_storage, "w") as memories: #and file is open with our list of saved conversations  
        #dump the list into storage 
        json.dump(memories_loading, memories)

    """ This function takes the current memories and the current new suggestion update from
     assistant and ensures it is in correct format and checks for duplicates. If no duplicate
     then add it. It returns the updated list of long term memories. FIX THIS DESCRIPTION"""
    def apply_memory_update(update): #this will take one argument - the extract_memory_decision dict/json, and use our self.memories 
        if not update or update["action"] == "ignore":
            return None 
    #we should have two more options here, if action = update and if action = add #actually maybe not. I still want to check the list to see if topic or entry is already present for both add and update, so they can essentially be the same thing. But if that is the case, we only need add, not both add and update. Let me think on this. 
        topic = update["topic"] #string 
        entries = update["entries"] #list of dicts 
        if not topic or entries is None:
            return memory

        # initialize category if needed
        if topic not in self.memories(topic):
            #memory[topic] = [] empty list #this will just be a string , but this logic still does not make sense. If topic is not in topics, then we need to "add" a new topic, and start a lits of entries. 
            #I think I need to create a new memory object here instead of an empty list 
            new_memory = Memory()
            new_memory = new_memory.topic(topic).entries(entries)
            

        # ensure list format (important for pets, etc.) #this needs to be a list of entries, which are dicts 
        if not isinstance(new_memory.entries, list):
            memory.entries = [memory{entries}]

        # check for duplicates (simple match) #FIX ME this realy needs worked on. This is where I currently am, and cannot connect the logic of what I had previously written to where it should belong now in memory manager. 
        #what I want to do is go through my new object, check if the topic exists, and if it does we want to see if the entry already exists. If it entry does exist yet, then we add the entry to the memory object in our list of memory objects that matches our topic. 
        #Ok lets do the pseudocode
        #for memory in memories, 
            #if memory.topic == new_memory topic: 
                #check entries for memory.topic and see if it matches new_memory entries #we need to compare first the key in the dict, and then the value in the dict, then move on to the next dict key. 
                    #if it does, we do nothing with it, we can break here. 
                #else, add to the list of entries for memory.topic with new_memory.entries 
            #else 
                #add the new_memory to the list of memories 
        match_index = None
        for i, item in enumerate(memory.topic):
            if isinstance(item, string) and isinstance(entries, dict) and item.get("name") == entries.get("name"): #this line needs looked at.
                #The line above is saying: if item in topic is a string, and entries is a dict, and "name"=="name", then match index = i and break, meaning we did not find a duplicate. Not sure this is what I want here. 
                #
                match_index = i
                break
        #we should probably implode this function. It is doing too much. We should have one job per function, and Memory objects can own some of these functions. 
                
        #the below does not make sense. if match index is not none, meaning we are adding a memory, then ... i dont think this applies here at all anymore. 
        #I am not sure if we need the rest of this function down below 
        if match_index is not None:
            memory.topic(match_index) = entries  
        else: 
            memory.topic.(entries)

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
        
    #AI decides what it will save and print. Includes: instructions, user reply, and returns response 
    def extract_memory_decision(user_input):
        topic_list = ""
        for topic in memory_manager.get_topics():
            topic_list += f"[topic] " #I think this is not syntax correct 
            
        prompt = [
            {
                "role": "system",
                "content": """
    You are a memory extraction system within a personal ai assistant system. 

    Your job:
    Decide if the user message contains a FACT worth storing long-term.

    Rules:
    - Only store stable facts (pets, name, project, preferences, etc.) 
    - Some common topics expected to be long-term: pets, career, projects, work, finanicals, family, troubleshooting, health, philosophy. 
    - Here is the working list of current memory topics: 
        {topic_list} 
    - If the topic is not included in the common or working list of current memory topics, it can still be saved if it is a stable fact worth storing long-term.
    - If updating a current working topic, use {"action": "update"} and set the "topic": to the same "topic" from the list of current memory topics 
    - If adding a new memory, use {"action": "add"}
    - If nothing important, return {"action": "ignore"}

    Return ONLY valid JSON.

    If adding or updating memory, use this format:

    {
      "action": "add",
      "topic": "pets",
      "entries": {
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
            
    def get_topics():
        current_topics = []
        for memory in self.memories:
            current_topics.append(memory.topic)
        return current_topics

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