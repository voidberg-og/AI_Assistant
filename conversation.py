class Conversation: 
    
    # Initialize 
    def __init__(self): #name, summary, history, id
        #idk this is empty 


    # Functions 
    def add_message(self, role, content):
        #check if history is full
        if len(self.history) == 100:
            #if full, remove first
            history.pop(0) 
        #add new message to history 
        history.append({
            "role": role,
            "content": content
        }]
        #summarize the new conversation whole 
        summary = llm_manager.summarize(self.history) #call to llm_manager #i am thinking of removing this here. In main when we call add_message(), we will do user input, and then ai reply. We don't need a summary each time user and each time ai, only once after one user and one ai message. So maybe we call this where we also call add_message(). 
    
    def to_dict(self):

        conversation = json.load(self)
        return conversation
        
        
    def to_json(self):
        
        return conversation = json.dumps(self)
        
        
