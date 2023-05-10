from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '864')

import pickle
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import os
import csv
from kivy.uix.filechooser import FileChooserIconView





def load_medications():
    try:
        with open('medications.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def save_medications(medications):
    with open('medications.pkl', 'wb') as f:
        pickle.dump(medications, f)

class LoginScreen(Screen):
    name_input = ObjectProperty()
    password_input = ObjectProperty()

    def login(self):
        self.manager.current = 'home'
        self.manager.get_screen('home').greet_user(self.name_input.text)

class HomeScreen(Screen):
    greeting = StringProperty()

    def greet_user(self, name):
        self.greeting = f"Hello {name}!"

class AddMedicationScreen(Screen):
    name_input = ObjectProperty()
    time_input = ObjectProperty()
    popup = None  # define popup attribute


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None  # initialize popup attribute

    def add_medication(self, name=None, time=None):
        if name is None and time is None:
            name = self.name_input.text
            time = self.time_input.text
        self.save_data(name, time)
        self.show_popup("Medication added successfully!")

    def save_data(self, name, time):
        # Load existing medications
        medications = load_medications()
        # Append new medication
        medications.append((name, time))
        # Save the updated medications list
        save_medications(medications)



    def show_popup(self, message):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=message))
        button = Button(text="Close", size_hint=(1, 0.2))
        box.add_widget(button)
        popup = Popup(title="Success", content=box, size_hint=(0.8, 0.4))
        button.bind(on_release=popup.dismiss)  # dismiss the popup when the button is pressed
        popup.open()



    def upload_prescription(self):
        # Create a BoxLayout to hold the FileChooser and the Upload button
        box = BoxLayout(orientation='vertical')

        # Create the FileChooser and bind its on_selection event to a method that saves the selection
        self.filechooser = FileChooserIconView(path='.', filters=['*.csv'])
        box.add_widget(self.filechooser)

        # Create a BoxLayout to hold the Upload and Back buttons
        button_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        # Create the Upload button and bind its on_press event to the load_csv method
        upload_button = Button(text="Upload")
        upload_button.bind(on_press=self.load_csv)
        button_box.add_widget(upload_button)

        # Create the Back button and bind its on_press event to a method that closes the popup
        popup = self.popup  # define popup as a local variable
        back_button = Button(text="Back")
        back_button.bind(on_press=lambda _: self.popup.dismiss())
        button_box.add_widget(back_button)

        # Add the button_box to the main box
        box.add_widget(button_box)

        # Create the popup with the box as its content
        self.popup = Popup(title="Choose a CSV file", content=box)
        self.popup.open()



    def load_csv(self, instance):
        # Get the selected file
        selected_file = self.filechooser.selection[0]

        # Load the CSV file
        with open(selected_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # Assume that the first column is the medicine name and the second column is the time
                name, time = row
                # Add the medication
                self.add_medication(name, time)
    
        # Close the popup
        self.popup.dismiss()

    



class ViewMedicationsScreen(Screen):

    def populate_medicine_list(self):
        # Load the medicines
        medicines = load_medications()
        # Get the medicine_list BoxLayout
        medicine_list = self.ids['medicine_list']
        # Remove all current children
        medicine_list.clear_widgets()
        # Add a BoxLayout for each medicine
        for i, (name, time) in enumerate(medicines):
            box = BoxLayout(size_hint_y=None, height='30dp')
            box.add_widget(Label(text=name))
            box.add_widget(Label(text=time))
            view_button = Button(text='View')
            view_button.bind(on_press=lambda instance, i=i: self.view_medicine(i))
            box.add_widget(view_button)
            delete_button = Button(text='Delete')
            delete_button.bind(on_press=lambda instance, i=i: self.delete_medicine(i))
            box.add_widget(delete_button)
            medicine_list.add_widget(box)

    def view_medicine(self, index):
        # Show a popup with the medicine details
        medicine = load_medications()[index]
        self.show_popup(f'Medicine Name: {medicine[0]}\nTime: {medicine[1]}')

    def delete_medicine(self, index):
        # Delete the medicine
        medicines = load_medications()
        del medicines[index]
        save_medications(medicines)
        # Refresh the medicine list
        self.populate_medicine_list()

    def show_popup(self, message):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=message))
        button = Button(text="Close", size_hint=(1, 0.2))
        box.add_widget(button)
        popup = Popup(title="Medicine Details", content=box, size_hint=(0.8, 0.4))
        button.bind(on_release=popup.dismiss)
        popup


class ScreenManagement(ScreenManager):
    pass



class MedicationTrackerApp(App):
    def build(self):
        return Builder.load_file('medicationtracker.kv')

if __name__ == '__main__':
    MedicationTrackerApp().run()

