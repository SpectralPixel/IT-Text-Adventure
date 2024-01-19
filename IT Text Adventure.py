from tkinter import *
from PIL import ImageTk, Image
from os.path import exists
from pyglet.font import add_directory
import json

CANVAS_SIZE = (300, 300)
FIRST_SCENE = "start"
BG_COLOR = "#e6e6ff"

#region ----- Open game files -----

print("Loading fonts...")
add_directory("Fonts")

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

restart_warning_triggered = False
def reset():
    global restart_warning_triggered # get the variable into this scope, otherwise python gets confused (WHY IS PYTHON SO ANNOYING??????)

    if not restart_warning_triggered:
        win_restart.configure(text = "Are you sure?")
        restart_warning_triggered = True
        return

    win_restart.configure(text = "Back to start")
    restart_warning_triggered = False
    print("Sent back to beginning.")
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
window.configure(background = BG_COLOR)

win_scene_title = Label( 
    window,
    anchor = "w",
    justify = "left",
    font = ("Quicksand-Bold", 20),
    background = BG_COLOR
)
win_scene_text = Label( 
    window,
    wraplength = 300,
    anchor = "w",
    justify = "left",
    font = ("Quicksand-Regular", 10),
    background = BG_COLOR
)
win_scene_options_title = Label(
    window,
    text = "Options:",
    anchor = "w",
    font = ("Quicksand-Bold", 15),
    background = BG_COLOR
)
win_scene_options = Label(
    window,
    anchor = "w",
    justify = "left",
    font = ("Quicksand-Regular", 10),
    background = BG_COLOR
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
    text = "Act!",
    command = validate_command,
    font = ("Quicksand-Regular", 10),
    background = "#ccffcc"
)
win_restart = Button(
    text = "Back to start",
    command = reset,
    font = ("Quicksand-Regular", 10),
    background = "#ffcccc"
)
win_save = Button(
    text = "Save & Exit",
    command = save_and_exit,
    font = ("Quicksand-Regular", 10),
    background = "#ccccff"
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
frame_durations = []
def update_frames():
    global frame_index
    frame = scene_frames_tk[frame_index]
    frame_duration = frame_durations[frame_index]
    frame_index += 1
    if frame_index >= scene_frames_tk.__len__():
        frame_index = 0
    
    win_canvas.create_image( # place the image on the canvas
        CANVAS_SIZE[0] / 2,
        CANVAS_SIZE[1] / 2,
        image = frame
    )

    print(frame_duration)
    window.after(frame_duration, update_frames) # to keep the cycle going
window.after(0, update_frames) # to begin the cycle

def load_image(path: str):
    print("Loading image: {}".format(path))

    scene_image = Image.open(path)

    global scene_frames_tk # sceneFramesTk has to be declared globally so the memory isn't freed after this function ends, resulting in the image to disappear
    scene_frames_tk = [] # a list of all the frames in the gif

    keyframes = 1
    if path[path.__len__() - 3:] == "gif": # since it's not guaranteed that the file type is a gif and has the n_frames attribute
        keyframes = scene_image.n_frames

    global frame_durations
    if len(frame_durations) > 0:
        frame_durations = []

    for i in range(keyframes):
        frame = scene_image
        frame.seek(keyframes // keyframes * i)

        if 'duration' in frame.info:
            frame_durations.append(frame.info['duration'])
            print(f"Frame {i} displays for {frame.info['duration']}ms.")
        else:
            frame_durations.append(50)

        frame = frame.resize((CANVAS_SIZE[0], CANVAS_SIZE[1]), Image.NEAREST)
        # global scene_frame_tk
        scene_frame_tk = ImageTk.PhotoImage(frame)
        scene_frames_tk.append(scene_frame_tk)
    
    global frame_index
    frame_index = 0
    
    print("Loaded {} frames.".format(keyframes))

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
    if len(scene_options) == 0:
        win_scene_options_title.configure(text = "NO OPTIONS AVAILIBLE.")
        win_scene_options.configure(text = "PRESS [Back to start].")
    else:
        win_scene_options_title.configure(text = "Options:")
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