from tkinter import *
from PIL import ImageTk, Image
from os.path import exists
import json

CANVAS_SIZE = (300, 300)
FIRST_SCENE = "start"

#region ----- Open game files -----

print("Loading story file...")

file = open("scenes.json", "r")
scenes = file.read() # Read file as plaintext
scenes = json.loads(scenes) # Turn plaintext into dictionary

print("Game files loaded.")

print("Loading save file...")

if not exists("save.txt"):
    save_file = open("save.txt", "w")
    save_file.writelines([FIRST_SCENE])
save_file = open("save.txt", "r")
current_scene = save_file.read().strip()

print("Progress loaded.")

#endregion ----------

#region ----- Button Commands -----

def validate_command(event = None): # event is apparently needed for the Return keybind to work...
    command = win_entry.get()
    win_entry.configure(text = "")

    for option in scenes[current_scene]["options"]:
        if option["action"].lower() == command.lower():
            load_scene(option["link"])

def reset():
    print("Progress reset")
    load_scene(FIRST_SCENE)

def save_and_exit():
    print()
    save_progress()
    print("Exiting program...")
    exit()

def save_progress():
    print("Saving progress...")
    save_file = open("save.txt", "w")
    save_file.writelines([current_scene])
    print("Progress saved")

#endregion ----------

#region ----- Set up window & GUI -----

window = Tk()
window.title("Text Adventure")

win_scene_title = Label( 
    window,
    anchor = "w",
    justify = "left"
)
win_scene_text = Label( 
    window,
    wraplength = 300,
    anchor = "w",
    justify = "left"
)
win_scene_options_title = Label(
    window,
    text = "Options:",
    anchor = "w",
)
win_scene_options = Label(
    window,
    anchor = "w",
    justify = "left"
)

# canvas to display images
win_canvas = Canvas( 
    window,
    width = CANVAS_SIZE[0],
    height = CANVAS_SIZE[1],
    bg = "white"
)

win_entry = Entry()
window.bind('<Return>', validate_command) # when Return is pressed, run validateCommand

win_confirm = Button(
    text = "Enter",
    command = validate_command
)
win_restart = Button(
    text = "Restart",
    command = reset
)
win_save = Button(
    text = "Save & Exit",
    command = save_and_exit
)

#endregion ----------

#region ----- Place GUI -----

window.rowconfigure(
    1,
    weight = 2 # makes row X be as wide as Y rows
)

win_scene_title.grid(
    row = 0,
    column = 0,
    sticky = N
)
win_scene_text.grid(
    row = 1,
    column = 0,
    sticky = NW
)
win_scene_options_title.grid(
    row = 2,
    column = 0,
    sticky = SW
)
win_scene_options.grid(
    row = 3,
    column = 0,
    sticky = SW
)
win_entry.grid(
    row = 4,
    column = 0,
    sticky = EW
)
win_confirm.grid(
    row = 4,
    column = 1,
    sticky = EW,
)
win_save.grid(
    row = 4,
    column = 2,
    sticky = EW
)
win_restart.grid(
    row = 4,
    column = 3,
    sticky = EW
)
win_canvas.grid(
    row = 0,
    rowspan = 4,
    column = 1,
    columnspan = 3,
    sticky = E
)

#endregion ----------

#region ----- Scene utility functions -----

frame_index = 0
def update_frames():
    global frame_index
    frame = scene_frames_tk[frame_index]
    frame_index += 1
    if frame_index >= scene_frames_tk.__len__():
        frame_index = 0
    
    win_canvas.create_image( # place the image on the canvas
        CANVAS_SIZE[0] / 2,
        CANVAS_SIZE[1] / 2,
        image = frame
    )

    window.after(50, update_frames) # to keep the cycle going
window.after(0, update_frames) # to begin the cycle

def load_image(path: str):
    print("Loading image: {}".format(path))

    scene_image = Image.open(path)

    global scene_frames_tk # sceneFramesTk has to be declared globally so the memory isn't freed after this function ends, resulting in the image to disappear
    scene_frames_tk = [] # a list of all the frames in the gif

    keyframes = 1
    if path[path.__len__() - 3:] == "gif": # since it's not guaranteed that the file type is a gif and has the n_frames attribute
        keyframes = scene_image.n_frames

    for i in range(keyframes):
        frame = scene_image
        frame.seek(keyframes // keyframes * i)
        frame = frame.resize((CANVAS_SIZE[0], CANVAS_SIZE[1]), Image.NEAREST)
        # global scene_frame_tk
        scene_frame_tk = ImageTk.PhotoImage(frame)
        scene_frames_tk.append(scene_frame_tk)
    
    print("Loaded {} frames.".format(keyframes))
    
    global frame_index
    frame_index = 0

def load_scene(scene: str): # force input type to be a string to avoid shenanigans
    print()
    print("Loading scene: {}".format(scene))

    global current_scene
    current_scene = scene

    # load title
    scene_title = scenes[scene]["name"]
    win_scene_title.configure(text = scene_title)

    # load text
    scene_text = scenes[scene]["text"]
    win_scene_text.configure(text = scene_text)

    # load options
    scene_options = scenes[scene]["options"]
    scene_options_text = ""
    for option in scene_options:
        scene_options_text += ">" + option["action"] + "\n"
    win_scene_options.configure(text = scene_options_text)

    # load image (and resize it to fit the canvas)
    scene_image_path = "Images" + "\\" + scenes[scene]["image"]
    load_image(scene_image_path)

    print("Scene loaded.")

#endregion ----------

load_scene(current_scene)
mainloop()

#region ----- TEMPLATE -----
#endregion ----------