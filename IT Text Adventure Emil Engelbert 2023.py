from tkinter import *
from PIL import ImageTk, Image
import json


#region ----- open files -----

scenes = ""
with open("scenes.json", "r") as file:
    scenes = file.read() # Read file as plaintext
scenes = json.loads(scenes) # Turn plaintext into dictionary

#mainPic = PhotoImage(file = 'Placeholder')

#endregion ----------


#region ----- set up window & gui -----

window = Tk()
window.title("Text Adventure")
window.geometry("777x444")

winTitle = Label(window, text = "hello world\nnewline!!!") # title of the current scene
winCanvas = Canvas(window, width = 80, height = 80, bg = 'white') # space to display images
winImage = ImageTk.PhotoImage(file = "coconut.jpg")
winText = Label(window, text = "hello world\nnewline!!!\nthis is the text field") # main text with the story from the current scene
winEntry = Entry() # text field to input commands
winOptions = Label(text = ">Option1\n>Option2") # list of all possible commands
winConfirm = Button(text = "Enter") # confirm button
winReset = Button(text = "Reset") # reset button

winTitle.grid(row = 0, column = 0, columnspan = 6)
winCanvas.grid(row = 1, column = 0, columnspan = 6)
winCanvas.create_image(0, 0, image = winImage)
winText.grid(row = 2, column = 0, rowspan = 3, columnspan = 4)
winOptions.grid(row = 2, column = 5, columnspan = 2)
winConfirm.grid(row = 3, column = 5)
winReset.grid(row = 3, column = 6)

#endregion ----------


currentScene = "start"
print(scenes[currentScene]["name"])

mainloop()



#region -----  -----


#endregion ----------