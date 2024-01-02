from tkinter import *
from PIL import ImageTk, Image
import json

CANVAS_SIZE = (300, 300)
FIRST_SCENE = "start"

#region ----- Open files -----

print("Loading game files")

scenes = ""
with open("scenes.json", "r") as file:
    scenes = file.read() # Read file as plaintext
scenes = json.loads(scenes) # Turn plaintext into dictionary

print("Game files loaded")

#endregion ----------

#region ----- Button Commands -----

def validateCommand(event = None): # event is apparently needed for the Return keybind to work...
    command = winEntry.get()
    winEntry.configure(text = "")

    for option in scenes[currentScene]["options"]:
        if option["action"].lower() == command.lower():
            print("Loading scene: {}".format(option["link"]))
            loadScene(option["link"])

def reset():
    print("Progress reset")
    loadScene(FIRST_SCENE)

#endregion ----------

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
    wraplength = 300,
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
window.bind('<Return>', validateCommand) # when Return is pressed, run validateCommand

winConfirm = Button(
    text = "Enter",
    command = validateCommand
)
winRestart = Button(
    text = "Restart",
    command = reset
)
winSave = Button(text = "Save & Exit")

#endregion ----------

#region ----- Place GUI -----

window.columnconfigure(
    0,
    weight = 3 # makes column 0 be as wide as X columns
)
window.columnconfigure(
    1,
    weight = 3
)
window.columnconfigure(
    2,
    weight = 2
)
window.rowconfigure(
    1,
    weight = 2
)

winSceneTitle.grid(
    row = 0,
    column = 0,
    sticky = N
)
winSceneText.grid(
    row = 1,
    column = 0,
    sticky = NW
)
winSceneOptionsTitle.grid(
    row = 2,
    column = 0,
    sticky = SW
)
winSceneOptions.grid(
    row = 3,
    column = 0,
    sticky = SW
)
winEntry.grid(
    row = 4,
    column = 0,
    columnspan = 2,
    sticky = EW
)
winConfirm.grid(
    row = 4,
    column = 2,
    sticky = EW,
)
winSave.grid(
    row = 4,
    column = 3,
    sticky = EW
)
winRestart.grid(
    row = 4,
    column = 4,
    sticky = EW
)
winCanvas.grid(
    row = 0,
    rowspan = 4,
    column = 1,
    columnspan = 4,
    sticky = E
)

#endregion ----------

frame_index = 0
def updateFrames():
    global frame_index
    frame = sceneFramesTk[frame_index]
    frame_index += 1
    if frame_index >= sceneFramesTk.__len__():
        frame_index = 0
    
    winCanvas.create_image( # place the image on the canvas
        CANVAS_SIZE[0] / 2,
        CANVAS_SIZE[1] / 2,
        image = frame
    )

    window.after(100, updateFrames) # to keep the cycle going
window.after(100, updateFrames) # to begin the cycle

def loadImage(path: str):
    sceneImage = Image.open(path)

    global sceneFramesTk # sceneFramesTk has to be declared globally so the memory isn't freed after this function ends, resulting in the image to disappear
    sceneFramesTk = [] # a list of all the frames in the gif

    keyframes = 1
    if path[path.__len__() - 3:] == "gif": # since it's not guaranteed that the file type is a gif and has the n_frames attribute
        keyframes = sceneImage.n_frames

    for i in range(keyframes):
        frame = sceneImage
        frame.seek(keyframes // keyframes * i)
        frame = frame.resize((CANVAS_SIZE[0], CANVAS_SIZE[1]), Image.NEAREST)
        # global sceneFrameTk
        sceneFrameTk = ImageTk.PhotoImage(frame)
        sceneFramesTk.append(sceneFrameTk)
    
    global frame_index
    frame_index = 0

def loadScene(scene: str): # force input type to be a string to avoid shenanigans
    global currentScene
    currentScene = scene

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
    loadImage(sceneImagePath)

loadScene(FIRST_SCENE)

mainloop()



#region -----  -----


#endregion ----------