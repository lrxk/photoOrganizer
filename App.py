import tkinter as tk
import tkinter.filedialog as fd
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
        # create a button to quit the application
        self.button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.button.pack()
        # create a button to select a directory
        self.button = tk.Button(self.frame, text="Select a directory", command=self.select_directory)
        self.button.pack()
    def select_directory(self):
        self.directory = fd.askdirectory()
        print(self.directory)
        self.label = tk.Label(self.frame, text=self.directory)
        self.label.pack()
    def quit(self):
        self.master.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()