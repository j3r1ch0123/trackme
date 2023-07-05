#!/bin/python3.9
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from urllib.request import urlopen
import datetime
import json
import requests
import os

filename = "location.txt"

class TrackMe(App):

    def request_loc(self, dt=1):
        separator = " , "
        url = "https://ipinfo.io/json"
        req = urlopen(url)
        data = json.load(req)

        lat = data['loc'].split(",")[0]
        lon = data['loc'].split(",")[1]

        time = datetime.datetime.now()
        d_time = time.strftime("%X")

        location = lat, separator,  lon
        coordinates = "".join(location)
        print(coordinates)

        with open(filename, "a") as thefile:
            contents = "Location : " + coordinates
            thefile.write(d_time + " " + contents + "\n")
            url = "http://127.0.0.1:5000/add-message" #Change this
            data = open(filename, "rb")
            response = requests.post(url, data=data)
            print("Location sent...")
        
        return coordinates

    def update_gps(self, *args):
        coordinates = self.request_loc()
        self.label.text = coordinates

    def start_gps(self, initialize):
        self.update_gps()
        self.event = Clock.schedule_interval(self.update_gps, 60)

    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.label = Label(text="GPS Coordinates: ")
        self.label.background_color = (0, 1, 0, 1)
        layout.add_widget(self.label)

        button = Button(text="TrackMe")
        button.bind(on_press=self.start_gps)
        layout.add_widget(button)

        self.label.text = self.request_loc()

        return layout

if __name__ == "__main__":
    TrackMe().run()
