class ConversationManager:

    def __init__(self): #conversations, current_conversation, conversations_storage
    # Variables
        self.current_conversation = None
        self.conversations = [] 
        self.conversations_storage = "conversation.json" #file path of where convos are stored 
        

    #Functions 
    def load_conversations(self):
        if os.path.exists(self.conversations_storage):
            with open(self.conversations_storage, "r") as conversations: #conversations is a list of dicts
                #load json into a dict 
                conversations_loading = json.load(conversations) #load the list of dicts into local conversations list 
                #loop through the list and turn each dict into an object 
                for conversation_dict in conversations_loading:
                    conversation = Conversation.from_dict(conversation_dict)
                    self.conversations.append(conversation)
                    
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
        for conversation in self.conversations:
            if conversation.id_num == id_selection:
                self.current_conversation = conversation 
                break 
        
    def switch_conversation(self):
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
        return conversation_list 
    







"""All conversations.

Which one is currently active.

How to load them from disk.

How to save them to disk.

How to create a new conversation.

How to switch conversations.

How to delete conversations.
--------------

Attributes:

conversations — a dictionary or list of Conversation objects

current_id — which conversation is currently active

storage_path — where conversations are saved

Methods:

create_conversation()

get_current()

switch_conversation(id)

delete_conversation(id)

list_conversations()

save()

load()
"""
