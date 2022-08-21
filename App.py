from curses import meta
from PIL.ExifTags import TAGS
import tkinter as tk
import tkinter.filedialog as fd
import os
import json
from PIL import Image,ExifTags
from datetime import date, datetime
from tkcalendar import Calendar, DateEntry
from tkinter import simpledialog
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
        # ask the dates of the trip
        self.dates = self.ask_dates()
        
        # ask the user for the name of the trip
        self.trip_name = simpledialog.askstring("Trip name", "Enter the name of the trip")
        # create a directory for the trip
        self.user_organized_photo_directory = self.user_organized_photo_directory + "/" + str(self.trip_name)
        # if the directory doesn't exist, create it
        if not os.path.exists(self.user_organized_photo_directory):
            os.makedirs(self.user_organized_photo_directory)
        else:
            # if the directory exists, ask the user if he wants to overwrite it
            self.overwrite_trip_directory = simpledialog.askstring("Overwrite trip directory", "The directory for the trip already exists. Do you want to overwrite it?")
            if self.user_organized_photo_directory == "yes":
                os.removedirs(self.user_organized_photo_directory)
                os.makedirs(self.user_organized_photo_directory)
            else:
                # if the user doesn't want to overwrite it, create a folder whose name is the date of the trip
                self.user_organized_photo_directory = self.user_organized_photo_directory + "/" + str(self.dates[0]+"_"+self.dates[1])
        # organize the images by day
        self.regroup_images_by_day_trip()
        # create a event window to tell the user that the images have been organized
        self.event_window = tk.Tk()
        self.event_window.geometry("200x200")
        self.event_window.title("Images organized")
        self.label = tk.Label(self.event_window, text="Images organized")
        self.label.pack()
        self.button = tk.Button(self.event_window, text="Close", command=self.event_window.destroy)
        self.button.pack()
        self.event_window.mainloop()

        
    def ask_dates(self):
        self.dates = []
        self.dates.append(simpledialog.askstring("Date", "Enter the first date of the trip"))
        self.dates.append(simpledialog.askstring("Date", "Enter the last date of the trip"))
        # format the dates
        for i in range(len(self.dates)):
            self.dates[i] = datetime.strptime(self.dates[i], "%d-%m-%Y")       
        return self.dates

    def regroup_images_by_day_trip(self):
        images=self.images
        dates=self.dates
        # get the images that have been taken between the two dates
        images_during_trip=[]
        for image in images:
            image_date = exifread.process_file(open(self.directory+"/"+image, 'rb'))['EXIF DateTimeOriginal']
            image_date = datetime.strptime(str(image_date), "%Y:%m:%d %H:%M:%S")
            if dates[0]<=image_date<=dates[1]:
                images_during_trip.append(image)
        
        # create a directory for each day of the trip
        for image in images_during_trip:
            image_date = exifread.process_file(open(self.directory+"/"+image, 'rb'))['EXIF DateTimeOriginal']
            image_date = datetime.strptime(str(image_date), "%Y:%m:%d %H:%M:%S")
            image_date = image_date.strftime("%d-%m-%Y")
            date_directory = self.user_organized_photo_directory + "/" + str(image_date)
            if not os.path.exists(date_directory):
                os.makedirs(date_directory)
            os.system("cp " + self.correct_path(self.directory+"/"+image) + " " + self.correct_path(date_directory))




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