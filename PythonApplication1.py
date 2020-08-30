from tkinter import *
import keyboard
import requests

global lastWord, tempWord
lastWord = ""
tempWord = ""

global posX, posY
posX = -6
posY = -21

global fontText, fontTextBold, currentBold
fontText = "Calibri 12"
fontTextBold = "Calibri 12 bold"
currentBold = -1

global currentList, currentIndex
currentList = [""]
currentIndex = -1

global sugg
sugg = [""]

global GUIvis
GUIvis = False


global ctrl,shift,alt
ctrl = False
shift = False
def ctrlDown(event):
    global ctrl
    ctrl = True

def ctrlUp(event):
    global ctrl
    ctrl = False

def shiftDown(event):
    global shift
    shift = True

def shiftUp(event):
    global shift
    shift = False

def altDown(event):
    global alt
    alt = True

def altUp(event):
    global alt
    alt = False

def arrowKey(event):
    global shift, lastWord
    if shift:
        lastWord = ""
        hideNotification()


def aDown(event):
    global ctrl, lastWord
    if ctrl:
        lastWord = ""
## Create notification window
root = Tk()
Label(root).pack()
root.geometry("+" + str(posX) + "+" + str(posY))

# Remove notification window decorations
root.overrideredirect(1)
root.wm_attributes("-topmost", 1)

posX = 200
posY = 200

def lastTyped(event):
    global lastWord, currentIndex
    name = event.name
    if len(name) > 1:
        if name == "space" or name == "enter":
            lastWord = ""
            hideNotification()
        if name == "backspace":
            lastWord = lastWord[:-1]
            hideNotification()
    else:
        lastWord += name
        hideNotification()
    
def APICall():
    global lastWord, sugg
    if lastWord == "":
        getWords = "https://api.datamuse.com/sug?s='"
    else:
        getWords = "https://api.datamuse.com/sug?s=" + lastWord
    rekwest = requests.get(getWords)

    wordsLeng = len(rekwest.json())

    sugg = [0] * wordsLeng

    for i in range(wordsLeng):
        sugg[i] = rekwest.json()[i].get("word")

def showNotification(event=None):
    global posX, posY, currentBold, currentIndex, currentList, lastWord, tempWord, GUIvis
    GUIvis = True
    if lastWord != tempWord:
        APICall()
    tempWord = lastWord;

    # Removing previous text
    killAllChildren()
    currentList = []
    
    # Gets a set of up to 5 words from the suggestions list, and stores them in a list
    for i in range(currentIndex, len(sugg)):
        if i > currentIndex + 4: break
        if lastWord == "": break
        currentList.append(sugg[i])

    # Set position of notification on screen
    root.geometry("+" + str(posX) + "+" + str(posY))

    # Print the current words
    for i in range(len(currentList)):
        if i == 0:
            Label(root, text=currentList[i], fg="black", font=fontTextBold).pack(side=LEFT)
        else:
            Label(root, text=currentList[i], fg="black", font=fontText).pack(side=LEFT)

def changeWordRight(event=None):
    global currentIndex, currentBold
    currentBold += 1
    currentIndex += 1
    if currentIndex > 9:
        currentIndex = 0
    showNotification()

def changeWordLeft(event=None):
    global currentIndex, currentBold
    currentBold -= 1
    currentIndex -= 1
    if currentIndex < 0:
        currentIndex = 9
    showNotification()

def changeWordRight(event=None):
    global currentIndex, currentBold,alt
    if alt:
        currentBold += 1
        currentIndex += 1
        if currentIndex > 9:
            currentIndex = 0
        showNotification()

def changeWordLeft(event=None):
    global currentIndex, currentBold,alt
    if alt:
        currentBold -= 1
        currentIndex -= 1
        if currentIndex < 0:
            currentIndex = 9
        showNotification()

def overwriteWord(event=None):
    global GUIvis
    def wordFill():
        lenLast = len(lastWord)
        selWord = currentList[0]
        selWord = selWord[lenLast:]
        wordPrint = selWord
        keyboard.write("\b", delay=0, restore_state_after=True, exact=None)
        keyboard.write(wordPrint, delay=0, restore_state_after=True, exact=None)
    if GUIvis:
        wordFill()

def hideNotification(event=None):
    global posX, posY, currentIndex, currentList, currentBold, GUIvis
    GUIvis = False
    # Removing text
    killAllChildren()

    # Resetting variables
    currentIndex = -1
    currentList = []
    currentBold = -1

    # Set position of notification off screen
    root.geometry("+" + str(0) + "+" + str(-25))

# Very important function
def killAllChildren():
    for child in root.winfo_children():
        child.destroy()

# Setting key events
keyboard.on_press_key("right shift", showNotification, suppress=False)
keyboard.on_press_key("ctrl", hideNotification, suppress=False)
keyboard.on_press_key("enter", overwriteWord, suppress=False)
keyboard.on_press_key("right", changeWordRight, suppress=False)
keyboard.on_press_key("left", changeWordLeft, suppress=False)
keyboard.on_press(lastTyped, suppress=False)
keyboard.on_press_key("ctrl", ctrlDown, suppress=False)
keyboard.on_press_key("shift", shiftDown, suppress=False)
keyboard.on_press_key("a", aDown, suppress=False)
keyboard.on_press_key("a", aDown, suppress=False)
keyboard.on_press_key("up", arrowKey, suppress=False)
keyboard.on_press_key("down", arrowKey, suppress=False)
keyboard.on_press_key("left", arrowKey, suppress=False)
keyboard.on_press_key("right", arrowKey, suppress=False)
keyboard.on_press_key("alt", altDown, suppress=False)
keyboard.on_release_key("alt", altUp, suppress=False)
keyboard.on_release_key("ctrl", ctrlUp, suppress=False)
keyboard.on_release_key("shift", shiftUp, suppress=False)
# You don't know what it does, and neither do I. Don't worry about it
root.update_idletasks()
root.mainloop()