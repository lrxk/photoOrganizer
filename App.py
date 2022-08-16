import tkinter as tk

class App:
    # create a gui window
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        # set width and height of the window
        self.master.geometry("800x800")
        self.master.title("Photo Organizer")
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Welcome to photo organizer !")
        self.label.pack()
        
        self.button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.button.pack()
    def quit(self):
        self.master.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()