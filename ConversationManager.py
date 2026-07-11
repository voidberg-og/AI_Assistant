class ConversationManager:

    def __init__(self): #conversations, current_conversation, conversations_storage
    # Variables
        self.conversations_storage = "conversation.json" #file path of where convos are stored 
        if os.path.exists(conversations_storage):
            with open(conversations_storage, "r") as conversations: 
                self.conversations = to_dict(conversations)
        

    #Functions 
    def create_conversation(self):
        new_convo = Conversation() 
        new_convo.id = #get system date/time 
        self.conversations.append(new_convo)
        self.current_conversation = new_convo 

    def get_current_conversation(self):
        return current_conversation 
        #who is calling this function? 
        
    def save_conversation(self):
        #save current_conversation to the conversation.json 
        current_conversation = to_json(current_conversation)
        
        
    def load_conversation(self):
        
    def switch_conversation(self):
        
    def delete_conversation(self):
        
    def list_conversations(self):
    







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