class Memory:
	
	#Initialize 
	def __init__(self): 
		self.topic = "" #string
        self.entries = [] #list of dicts 
        
        
    @classmethod 
    def from_dict(cls, memory):
        current_memory_loading = cls()
        current_memory_loading.topic = memory["topic"]
        current_memory_loading.summary = memory["entries"]

        #return current_conversation = json.load(self)
        return current_memory_loading
        
    def to_dict(self):#topic, entries 
        return {"topic" : self.topic, 
            "entries" : self.summary}
            
            
            
"""class Conversation: 
    
    # Initialize 
    def __init__(self): #name, summary, history, id
        self.name = ""
        self.summary = ""
        self.id_num = 0
        self.history = []


    # Functions 
    def add_message(self, role, content):
        #check if history is full
        if len(self.history) == 100:
            #if full, remove first
            self.history.pop(0) 
        #add new message to history 
        self.history.append({
            "role": role,
            "content": content
        })
        #summarize the new conversation whole 
        #summary = llm_manager.summarize(self.history) #call to llm_manager #i am thinking of removing this here. In main when we call add_message(), we will do user input, and then ai reply. We don't need a summary each time user and each time ai, only once after one user and one ai message. So maybe we call this where we also call add_message(). 
    


        

        """