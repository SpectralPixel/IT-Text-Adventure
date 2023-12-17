from tkinter import *
from PIL import ImageTk, Image
import json

CANVAS_SIZE = (400, 400)
FIRST_SCENE = "start"

#region ----- Set up window & GUI -----

window = Tk()
window.title("Text Adventure")

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
winSceneOptionsTitle = Label(
    window,
    text = "Options:",
    anchor = "w",
)
winSceneOptions = Label(
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
    width = CANVAS_SIZE[0],
    height = CANVAS_SIZE[1],
    bg = "white"
)

winEntry = Entry()
winConfirm = Button(text = "Enter")
winRestart = Button(text = "Restart")

#endregion ----------

#region ----- Place GUI -----

window.columnconfigure(
    0,
    weight = 16 # makes column 0 be as wide as 4 columns
)
window.columnconfigure(
    1,
    weight = 4
)
window.columnconfigure(
    2,
    weight = 1
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
winSceneOptionsTitle.grid(
    row = 2,
    column = 1,
    columnspan = 2,
    sticky = EW
)
winSceneOptions.grid(
    row = 3,
    column = 1,
    columnspan = 2,
    sticky = W
)
winEntry.grid(
    row = 4,
    column = 1,
    columnspan = 2,
    sticky = EW
)
winConfirm.grid(
    row = 5,
    column = 1,
    sticky = EW,
)
winRestart.grid(
    row = 5,
    column = 2,
    sticky = EW
)

#endregion ----------

#region ----- Open files -----

scenes = ""
with open("scenes.json", "r") as file:
    scenes = file.read() # Read file as plaintext
scenes = json.loads(scenes) # Turn plaintext into dictionary

#endregion ----------

def loadScene(scene):
    # load title
    sceneTitle = scenes[scene]["name"]
    winSceneTitle.configure(text = sceneTitle)

    # load text
    sceneText = scenes[scene]["text"]
    winSceneText.configure(text = sceneText)

    # load options
    sceneOptions = scenes[scene]["options"]
    sceneOptionsText = ""
    for option in sceneOptions:
        sceneOptionsText += ">" + option["action"] + "\n"
    winSceneOptions.configure(text = sceneOptionsText)

    # load image (and resize it to fit the canvas)
    sceneImagePath = "Images" + "\\" + scenes[scene]["image"]
    sceneImage = Image.open(sceneImagePath)
    sceneImage = sceneImage.resize((CANVAS_SIZE[0], CANVAS_SIZE[1]), Image.NEAREST)
    global sceneImageTk # sceneImageTk has to be declared globally so the memory isn't freed after this funtion ends, resulting in the image to disappear
    sceneImageTk = ImageTk.PhotoImage(sceneImage)
    winCanvas.create_image( # place the image on the canvas
        CANVAS_SIZE[0] / 2,
        CANVAS_SIZE[1] / 2,
        image = sceneImageTk
    )

currentScene = FIRST_SCENE
loadScene(currentScene)

mainloop()



#region -----  -----


#endregion ----------