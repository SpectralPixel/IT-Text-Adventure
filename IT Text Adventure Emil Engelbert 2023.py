from tkinter import *
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
window.geometry("300x350")

#endregion ----------

currentScene = "start"
print(scenes[currentScene]["name"])

mainloop()



#region -----  -----


#endregion ----------