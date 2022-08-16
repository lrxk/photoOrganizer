import tkinter as tk
import tkinter.filedialog as fd
import os
class App:
    # create a gui window
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        # set width and height of the window
        self.master.geometry("800x800")
        self.master.title("Photo Organizer")
        global filepath_to_images
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Welcome to photo organizer !")
        self.label.pack()
        # create a button to quit the application
        self.button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.button.pack()
        # create a button to select a directory
        self.button = tk.Button(self.frame, text="Select a directory and organize", command=lambda:self.select_directory_and_organize())
        self.button.pack()
    def select_directory_and_organize(self):
        self.directory = fd.askdirectory(title="Select your photos directory")
        filepath_to_images = self.directory
        # get all the images in the directory
        self.images = [f for f in os.listdir(filepath_to_images) if f.endswith('.jpg')]
        # ask the user to select a directory to put the images in
        self.user_organized_photo_directory = fd.askdirectory(title="Select a directory to put your images in")
        # loop through the images and copy them to the user selected directory
        for image in self.images:
            os.system("cp " + filepath_to_images + "/" + image + " " + self.user_organized_photo_directory)
        # create a event window to tell the user that the images have been organized
        self.event_window = tk.Tk()
        self.event_window.geometry("200x200")
        self.event_window.title("Images organized")
        self.label = tk.Label(self.event_window, text="Images organized")
        self.label.pack()
        self.button = tk.Button(self.event_window, text="Close", command=self.event_window.destroy)
        self.button.pack()
        self.event_window.mainloop()
    
        
    def quit(self):
        self.master.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()