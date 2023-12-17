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
#window.geometry("777x444")

winSceneTitle = Label( 
    window,
    text = "hello world",
    anchor = "w",
    justify = "left"
)
winSceneText = Label( 
    window,
    text = "hello world\nnewline!!!\nthis is the text field",
    anchor = "w",
    justify = "left"
)
winOptionsTitle = Label(
    window,
    text = "Options:",
    anchor = "w",
)
winAllOptions = Label(
    window,
    text =
        ">Option1\n" + 
        ">Option2",
    anchor = "w",
    justify = "left"
)

# canvas to display images
winCanvas = Canvas( 
    window,
    width = 400,
    height = 400,
    bg = "white"
)

winEntry = Entry()
winConfirm = Button(text = "Enter")
winRestart = Button(text = "Restart")

window.columnconfigure(
    0,
    weight = 4 # makes column 0 be as wide as 4 columns
)

winSceneTitle.grid(
    row = 0,
    column = 0,
    columnspan = 3
)
winCanvas.grid(
    row = 1,
    column = 0,
    columnspan = 3
)
winSceneText.grid(
    row = 2,
    column = 0,
    rowspan = 4,
    sticky = NW
)
winOptionsTitle.grid(
    row = 2,
    column = 1,
    columnspan = 2,
    sticky = EW
)
winAllOptions.grid(
    row = 3,
    column = 1,
    columnspan = 2,
    sticky = W
)
winEntry.grid(
    row = 4,
    column = 1,
    columnspan = 2
)
winConfirm.grid(
    row = 5,
    column = 1,
    sticky = EW
)
winRestart.grid(
    row = 5,
    column = 2,
    sticky = EW
)

# place the image on the canvas
winImage = ImageTk.PhotoImage(file = "coconut.jpg")
winCanvas.create_image(200, 200, image = winImage)

#endregion ----------


currentScene = "start"
print(scenes[currentScene]["name"])

mainloop()



#region -----  -----


#endregion ----------