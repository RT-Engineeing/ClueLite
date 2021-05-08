from GameOperations import Players, Weapons, Weapdeck, Roomsdeck, Chardeck


class Node:
    def __init__(self, dataval=None, uid=None, player=None):
        self.dataval = dataval
        self.uid = uid
        self.player = player
        self.nextval = None
        self.ready = False

    def getdataval(self):
        return self.dataval

    def getuid(self):
        return self.uid

    def getplayer(self):
        return self.player

    def getready(self):
        return self.ready

    def setdataval(self, temp):
        self.dataval = temp

    def setuid(self, temp):
        self.uid = temp

    def setplayer(self, temp):
        self.player = temp

    def setready(self, temp):
        self.ready = temp


class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        while printval is not None:
            print(printval.dataval)
            printval = printval.nextval

    def RemoveNode(self, Removekey):
        HeadVal = self.headval
        if (HeadVal is not None):
            if (HeadVal.data == Removekey):
                self.headval = HeadVal.next
                HeadVal = None
                return
        while (HeadVal is not None):
            if HeadVal.data == Removekey:
                break
            prev = HeadVal
            HeadVal = HeadVal.next
        if (HeadVal == None):
            return
        prev.next = HeadVal.next
        HeadVal = None

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        laste = self.headval
        while (laste.nextval):
            laste = laste.nextval
        laste.nextval = NewNode

    def listlength(self):
        counter = 0
        HeadVal = self.headval
        while HeadVal is not None:
            counter += 1
            HeadVal = HeadVal.nextval
        return counter

    def checkready(self):
        checkready = False
        printval = self.headval
        while printval is not None:
            if not printval.getready():
                return checkready
            printval = printval.nextval
        return True
