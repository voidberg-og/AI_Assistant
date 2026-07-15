class Conversation: 
    
    # Initialize 
    def __init__(self): #name, summary, history, id
        self.name = ""
        self.summary = ""
        self.id_num = #get system date/time 
        self. history = []


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
    
    def to_dict(self):#name, summary, history, id
        self.conversation_dict = {"name" : self.current_conversation.name, 
            "summary" : self.current_conversation.summary, 
            "id_num" : self.current_conversation.id_num, 
            "history" : self.current_conversation.history}

        #self.conversation_dict = json.dump(self)
        return conversation_dict 
        
        
    def to_object(self):
        current_conversation_loading = Conversation()
        current_conversation_loading.name = conversation["name"]
        current_conversation_loading.summary = conversation["summary"]
        current_conversation_loading.id_num = conversation["id_num"]
        current_conversation_loading.history = conversation["history"]
                
                
        #return current_conversation = json.load(self)
        return current_conversation_loading
        
        
