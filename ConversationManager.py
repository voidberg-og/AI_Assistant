class ConversationManager:

    def __init__(self): #conversations, current_conversation, conversations_storage
    # Variables
        self.conversations_storage = "conversation.json" #file path of where convos are stored 
        if os.path.exists(self.conversations_storage):
            with open(self.conversations_storage, "r") as conversations: #conversations is a list of dicts
                #load json into a dict 
                conversations_loading = json.load(conversations) #load the list of dicts into local conversations list 
                #loop through the list and turn each dict into an object 
                for conversation in conversations_loading:
                    self.conversations.append(to_object(conversation))  #turn the dict into object
        

    #Functions 
    def create_conversation(self):
        new_convo = Conversation() 
        new_convo.id_num = #get system date/time 
        self.conversations.append(new_convo)
        self.current_conversation = new_convo 

    def get_current_conversation(self):
        return self.current_conversation 
        #who is calling this function? #probs main
        
    def save_conversation(self):
        #save current_conversation to the conversation.json 
        for conversation in self.conversations: #loop through the list of conversations 
            if conversation.id_num == self.current_conversation.id_num: #to find the current conversation 
                current_conversation_loading = to_dict(current_conversation) # turn the current conversation into a dict stored locally here
                if os.path.exists(self.conversations_storage): #if file exists 
                    with open(self.conversations_storage, "w") as conversations: #and file is open with our list of saved conversations  
                        self.conversations[conversation] = json.dump(current_conversation_loading) # the list of saved conversations[this conversation] now equals our local conversation dict 
                break

        
        
    def load_conversation(self):
        for conversation in self.conversations:
            if conversation.id_num == self.id_selection:
                self.current_conversation = conversation 
                break 
        
    def switch_conversation(self):
        save_conversation(self.current_conversation)
        load_conversation(self.id_selection)
        
    def delete_conversation(self):
        for conversation in self.conversations:
            if conversation.id_num == self.id_selection:
                self.conversations.remove(conversation)
                break 
        
    def list_conversations(self):
        for conversation in self.conversations:
            self.conversation_list.append(conversation.summary)
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
