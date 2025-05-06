import tkinter as tk
from PIL import ImageTk, Image
window = tk.Tk()
window.geometry("960x540+480+200")
load = Image.open("icons8-available-updates-30.png")
render = ImageTk.PhotoImage(load)
#img = tk.Label(image=render)
#img.image = render
#img.place(x=450, y=280)
button1=tk.Button(window , text = 'Click Me !', image = render) 
button1.pack(side=tk.LEFT, padx=(10,0))
tk.mainloop()
