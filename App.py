from curses import meta
from PIL.ExifTags import TAGS
import tkinter as tk
import tkinter.filedialog as fd
import os
import json
from PIL import Image,ExifTags
from datetime import date, datetime
from tkcalendar import Calendar, DateEntry
import exifread
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
        # create a button to select a directory for the trip
        self.button = tk.Button(self.frame, text="Select a directory and organize by trip", command=lambda:self.select_directory_and_organize_by_trip())
        self.button.pack()
    def select_directory_and_organize(self):
        self.directory = fd.askdirectory(title="Select your photos directory")
        filepath_to_images = self.directory
        # get all the images in the directory
        self.images = [f for f in os.listdir(filepath_to_images) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.JPG')]
        # ask the user to select a directory to put the images in
        self.user_organized_photo_directory = fd.askdirectory(title="Select a directory to put your images in")
        # create a event window to tell the user that the images have been organized
        self.regroup_images_by_day()
        self.event_window = tk.Tk()
        self.event_window.geometry("200x200")
        self.event_window.title("Images organized")
        self.label = tk.Label(self.event_window, text="Images organized")
        self.label.pack()
        self.button = tk.Button(self.event_window, text="Close", command=self.event_window.destroy)
        self.button.pack()
        self.event_window.mainloop()
    def correct_path(self, path:str):
        return path.replace(" ", "\\ ").replace("?", "\\?").replace("&", "\\&").replace("(", "\\(").replace(")", "\\)").replace("*", "\\*").replace("<", "\\<").replace(">", "\\>")
    def select_directory_and_organize_by_trip(self):
        self.directory = fd.askdirectory(title="Select your photos directory")
        filepath_to_images = self.directory
        
        # get all the images in the directory
        self.images = [f for f in os.listdir(filepath_to_images) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.JPG')]
        # ask the user to select a directory to put the images in
        self.user_organized_photo_directory = fd.askdirectory(title="Select a directory to put your images in")
        self.select_trip_name()
        
        # create a event window to tell the user that the images have been organized
        self.regroup_images_by_trip()
        
        self.event_window = tk.Tk()
        self.event_window.geometry("200x200")
        self.event_window.title("Images organized")
        self.label = tk.Label(self.event_window, text="Images organized")
        self.label.pack()
        self.button = tk.Button(self.event_window, text="Close", command=self.event_window.destroy)
        self.button.pack()
        self.event_window.mainloop()
    def regroup_images_by_trip(self):
        # get all the images in the directory
        self.images = [f for f in os.listdir(self.user_organized_photo_directory) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.JPG')]
        # create a window to ask the user to select the dates of the trip
        self.calendar_window = tk.Tk()
        self.calendar_window.geometry("200x200")
        self.calendar_window.title("Select the starting date of the trip")
        self.starting_date_calendar = Calendar(self.calendar_window, selectmode='day', year=2020, month=1, day=1)
        self.starting_date_calendar.pack(fill='both', expand=True)
        self.button = tk.Button(self.calendar_window, text="Select", command=self.select_starting_date_of_the_trip)
        self.button.pack()
        self.ending_date_calendar = Calendar(self.calendar_window, selectmode='day', year=2020, month=1, day=1)
        self.ending_date_calendar.pack(fill='both', expand=True)
        self.button = tk.Button(self.calendar_window, text="Select", command=self.select_ending_date_of_the_trip)
        self.button.pack()
        self.calendar_window.mainloop()

        
    def select_ending_date_of_the_trip(self):
        self.ending_date=self.ending_date_calendar.selection_get()
        self.ending_date_calendar.destroy()
        self.calendar_window.destroy()
    def select_starting_date_of_the_trip(self):
        self.starting_date = self.starting_date_calendar.selection_get()
        self.starting_date_calendar.destroy()
    # ask the user the name of the trip
    def select_trip_name(self):
        self.trip_name = tk.Tk()
        self.trip_name.geometry("200x200")
        self.trip_name.title("Select a name for the trip")
        self.label = tk.Label(self.trip_name, text="Enter the name of the trip")
        self.label.pack()
        self.entry = tk.Entry(self.trip_name)
        self.entry.pack()
        self.button = tk.Button(self.trip_name, text="Select", command=self.select_name_of_the_trip)
        self.button.pack()
        self.trip_name.mainloop()

    def copy_images(self):
        self.images = [f for f in os.listdir(self.user_organized_photo_directory) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith('.JPG')]
        images_trip=[]
        for image in self.images:
            image_path=str(self.user_organized_photo_directory)+"/"+str(image)
            image_path=self.correct_path(image_path)
            # check if the image is in the trip date
            if self.is_image_in_the_trip_date(image_path):
                images_trip.append(image_path)
        # copy the images to the trip directory
        for image in images_trip:
            os.system("cp " + image + " " + str(self.trip_directory))
    def is_image_in_the_trip_date(self, image_path:str):
        image_date = self.get_image_date(image_path)
        if image_date >= self.starting_date and image_date <= self.ending_date:
            return True
        else:
            return False
    def get_image_date(self, image_path:str):
        image_date = exifread.process_file(open(image_path, 'rb'))['EXIF DateTimeOriginal']
        return image_date
    def select_name_of_the_trip(self):
        self.trip_name = self.entry.get()
        # create a directory to put the images in
        self.trip_directory = str(self.user_organized_photo_directory)+"/"+str(self.trip_name)
        os.system("mkdir " + str(self.trip_directory))
        # loop through the images and copy them to the user selected directory
        self.copy_images()
    def regroup_images_by_day(self):
        # get all the images
        images=self.images
        images_date=[]
        filepath_to_images = self.directory
        for image in images:
            # get the metadata of the image
            image_path=str(filepath_to_images)+"/"+str(image)
            metadata = Image.open(image_path).getexif()
            for tag, value in metadata.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "DateTime":
                    # get the date of the image
                    date = value
                    # get the year of the image
                    year = date[0:4]
                    # get the month of the image
                    month = date[5:7]
                    # get the day of the image
                    day = date[8:10]
                    # get the hour of the image
                    hour = date[11:13]
                    # get the minute of the image
                    minute = date[14:16]
                    # get the second of the image
                    second = date[17:19]
                    # get the date of the image
                    date = date[0:10]
                    # get the date of the image in the format YYYY-MM-DD
                    date = year + "-" + month + "-" + day
                    # get the time of the image in the format HH:MM:SS
                    time = hour + ":" + minute + ":" + second
                    # get the date and time of the image in the format YYYY-MM-DD HH:MM:SS
                    date_time = date + " " + time
                    # get the date and time of the image in the format YYYY-MM-DD HH:MM:SS
                    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    # get the date of the image
                    date = date_time.date()
                    images_date.append(date)
        # for each date, create a directory and copy the images in it
        for date in images_date:
            os.system("mkdir " + str(self.user_organized_photo_directory) + "/" + str(date))
            for image in images:
                image_path=str(filepath_to_images)+"/"+str(image)
                image_path=self.correct_path(image_path)
                metadata = Image.open(image_path).getexif()
                for tag, value in metadata.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "DateTime":
                        # get the date of the image
                        image_date = value
                        # get the year of the image
                        year = image_date[0:4]
                        # get the month of the image
                        month = image_date[5:7]
                        # get the day of the image
                        day = image_date[8:10]
                        # get the hour of the image
                        hour = image_date[11:13]
                        # get the minute of the image
                        minute = image_date[14:16]
                        # get the second of the image
                        second = image_date[17:19]
                        # get the date of the image
                        image_date = image_date[0:10]
                        # get the date of the image in the format YYYY-MM-DD
                        image_date = year + "-" + month + "-" + day
                        # get the time of the image in the format HH:MM:SS
                        time = hour + ":" + minute + ":" + second
                        # get the date and time of the image in the format YYYY-MM-DD HH:MM:SS
                        image_date_time = image_date + " " + time
                        # get the date and time of the image in the format YYYY-MM-DD HH:MM:SS
                        image_date_time = datetime.strptime(image_date_time, '%Y-%m-%d %H:%M:%S')
                        # get the date of the image
                        image_date = image_date_time.date()
                        if date == image_date:
                            os.system("cp " + image_path + " " + str(self.user_organized_photo_directory) + "/" + str(date))
                            print("Image %s copied",image)
        pass
        
    def quit(self):
        self.master.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()