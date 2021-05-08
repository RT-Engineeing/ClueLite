class MessageManager:
    
   def __init__(self):
      self.messageMap = {}
      
   def addUuid(self, uuid):
      self.messageMap[uuid] = []

   def addMessage(self, message):
      for key in self.messageMap:
         self.messageMap[key].append(message)

   def getMessages(self, uuid):
      messages = self.messageMap[uuid]
      self.messageMap[uuid] = []
      return messages   



      