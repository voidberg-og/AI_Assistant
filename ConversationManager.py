class ConversationManager:

    def __init__(self): #conversations, current_conversation, conversations_storage
    # Variables
        self.conversations_storage = "conversation.json" #file path of where convos are stored 
        if os.path.exists(self.conversations_storage):
            with open(self.conversations_storage, "r") as conversations: 
                self.conversations = to_dict(conversations)
        

    #Functions 
    def create_conversation(self):
        new_convo = Conversation() 
        new_convo.id = #get system date/time 
        self.conversations.append(new_convo)
        self.current_conversation = new_convo 

    def get_current_conversation(self):
        return self.current_conversation 
        #who is calling this function? #probs main
        
    def save_conversation(self):
        #save current_conversation to the conversation.json 
        for conversation in self.conversations:
            if conversation.id == self.current_conversation.id:
                if os.path.exists(self.conversations_storage):
                    with open(self.conversations_storage, "w") as conversations: 
                        self.conversations[conversation] = to_json(self.current_conversations)
                break

        
        
    def load_conversation(self):
        for conversation in self.conversations:
            if conversation.id == self.id_selection:
                self.current_conversation = conversation 
                break 
        
    def switch_conversation(self):
        save_conversation(self.current_conversation)
        load_conversation(self.id_selection)
        
    def delete_conversation(self):
        for conversation in self.conversations:
            if conversation.id == self.id_selection:
                self.conversations.remove(conversation)
                break 
        
    def list_conversations(self):
        for conversation in self.conversations:
            self.conversation_list.append(conversation.summary)
        return conversation_list 
    
    def to_dict(self):

        conversation = json.load(self)
        return conversation
        
        
    def to_json(self):
        
        return conversation = json.dumps(self)






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