import csv
import wx

class CardCreator(wx.Frame):

    def __init__(self, characters, title):
        super(CardCreator, self).__init__(parent=None, title=title)

        self.characters = characters
        self.numbers = [i+1 for i in range(len(self.characters))]
        self.keywords = dict()
        self.lessons = dict()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)
        self.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.currentNum = 0
        self.initUI()
    
    def initUI(self):
        self.field1 = wx.TextCtrl(self, -1, value='')
        self.field2 = wx.TextCtrl(self, -1, value=self.characters[0])
        self.field2.SetFont(wx.Font(wx.FontInfo(24)))
        self.field3 = wx.TextCtrl(self, -1, value=str(self.numbers[0]))
        self.field4 = wx.TextCtrl(self, -1, value='')

        self.nextButton = wx.Button(self, label=">")
        self.prevButton = wx.Button(self, label="<")
        self.numJump = wx.TextCtrl(self, -1, value=str(self.currentNum+1))
        self.jumpButton = wx.Button(self, label='...')
        self.jumpBox = wx.BoxSizer(wx.HORIZONTAL)
        self.jumpBox.Add(self.prevButton)
        self.jumpBox.Add(self.numJump)
        self.jumpBox.Add(self.jumpButton)
        self.jumpBox.Add(self.nextButton)

        self.saveButton = wx.Button(self, label="save")

        self.mainSizer.Add(self.field1)
        self.mainSizer.Add(self.field2)
        self.mainSizer.Add(self.field3)
        self.mainSizer.Add(self.field4)
        self.mainSizer.Add(self.jumpBox)
        self.mainSizer.Add(self.saveButton)

        self.nextButton.Bind(wx.EVT_BUTTON, self.nextCard)
        self.prevButton.Bind(wx.EVT_BUTTON, self.prevCard)
        self.jumpButton.Bind(wx.EVT_BUTTON, self.jumpCard)

        self.saveButton.Bind(wx.EVT_BUTTON, self.save)

        self.Bind(wx.EVT_KEY_UP, self.keypress)
        self.field1.Bind(wx.EVT_KEY_UP, self.keypress)

        self.Layout()
        self.Refresh()

    def nextCard(self, evt):
        if self.field1.Value != "":
            self.keywords[self.currentNum + 1] = self.field1.Value
        if self.field1.Value != "":
            self.lessons[self.currentNum + 1] = self.field4.Value

        if self.currentNum < len(self.characters):
            self.currentNum += 1
        
        if self.currentNum + 1 in self.keywords:
            self.field1.ChangeValue(self.keywords[self.currentNum + 1])
        else:
            self.field1.ChangeValue("")
        self.field2.ChangeValue(self.characters[self.currentNum])
        self.field3.ChangeValue(str(self.numbers[self.currentNum]))
        
        if self.currentNum + 1 in self.lessons:
            self.field4.ChangeValue(self.lessons[self.currentNum + 1])

        self.field1.SetFocus()

        self.numJump.ChangeValue(str(self.currentNum+1))

    def prevCard(self, evt):
        if self.field1.Value != "":
            self.keywords[self.currentNum + 1] = self.field1.Value
        if self.field1.Value != "":
            self.lessons[self.currentNum + 1] = self.field4.Value
        if self.currentNum > 0:
            self.currentNum -= 1
        if self.currentNum + 1 in self.keywords:
            self.field1.ChangeValue(self.keywords[self.currentNum + 1])
        else:
            self.field1.ChangeValue("")

        self.field2.ChangeValue(self.characters[self.currentNum])
        self.field3.ChangeValue(str(self.numbers[self.currentNum]))

        if self.currentNum + 1 in self.lessons:
            self.field4.ChangeValue(self.lessons[self.currentNum + 1])

        self.field1.SetFocus()

        self.numJump.ChangeValue(str(self.currentNum+1))

    def jumpCard(self, evt):
        if self.field1.Value != "":
            self.keywords[self.currentNum + 1] = self.field1.Value
        if self.field1.Value != "":
            self.lessons[self.currentNum + 1] = self.field4.Value
        try:
            self.currentNum = int(self.numJump.Value) - 1
        except:
            return
        if self.currentNum + 1 in self.keywords:
            self.field1.ChangeValue(self.keywords[self.currentNum + 1])
        else:
            self.field1.ChangeValue("")

        self.field2.ChangeValue(self.characters[self.currentNum])
        self.field3.ChangeValue(str(self.numbers[self.currentNum]))

        if self.currentNum + 1 in self.lessons:
            self.field4.ChangeValue(self.lessons[self.currentNum + 1])

        self.field1.SetFocus()

        self.numJump.ChangeValue(str(self.currentNum+1))

    def keypress(self, evt):
        if evt.GetKeyCode() == 13:
            self.nextCard(None)

    def save(self, evt):
        outputpath = "./cards.csv"
        with open(outputpath, 'w', newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in self.numbers:
                if i in self.keywords:
                    writer.writerow([self.keywords[i], self.characters[i-1], i, self.lessons[i]])

    
if __name__ == '__main__':
    characters = []
    with open("./characters.txt", "r", encoding="utf-8") as rtk_characters:
        ch = rtk_characters.read()
        characters = ch.split()
    app = wx.App()
    frm = CardCreator(characters, title="Card Creator")
    frm.Show()
    app.MainLoop()