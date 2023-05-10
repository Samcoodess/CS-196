from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image

# Set window size and disable resizing
Config.set('graphics', 'resizable', False)
Window.size = (360, 640)

# Define the KV language string that defines the app's user interface
kv = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    UserDetailsScreen:
    MainScreen:
    AppointmentScreen:
    HospitalsScreen:
    DatasetScreen:

<UserDetailsScreen>:
    name: 'details'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'bg.jpg'
    BoxLayout:
        orientation: 'vertical'
        spacing: 50
        padding: 150
        TextInput:
            id: name_input
            hint_text: 'Name'
            multiline: False
            size_hint_y: None
            height: 50
        TextInput:
            id: password
            hint_text: 'Password'
            multiline: False
            size_hint_y: None
            height: 50
        Button:
            text: 'Submit'
            size_hint_y: None
            height: 50
            on_press:
                root.submit()
                root.manager.current = 'main'

<MainScreen>:
    name: 'main'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'bg.jpg'
    Label:
        id: greeting_label
        text: 'Welcome!'
        font_size: 30
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        color: (0, 0, 0, 1)
    MyBoxLayout:
        size_hint: 1, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}


<AppointmentScreen>:
    name: 'appointment'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Scheduling an appointment...'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'

<HospitalsScreen>:
    name: 'hospitals'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Finding hospitals nearby...'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'

<DatasetScreen>:
    name: 'datasets'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Viewing previous datasets...'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'
'''

class UserDetailsScreen(Screen):
    '''screen for user Details input. 
      Allows the user to input their name and password and submit the form.
      '''
    def submit(self):
        """
        Submit the user details form.

        Updates the greeting label on the main screen with the user's name.
        """
        app = App.get_running_app()
        app.root.get_screen('main').ids.greeting_label.text=text=f'Hello, {self.ids.name_input.text}!'


class MainScreen(Screen):
    """
    Main screen of the app.
    
    Displays a greeting label and three buttons for scheduling an appointment, 
    finding hospitals nearby, and viewing previous datasets.
    """

    pass

class AppointmentScreen(Screen):
    '''screen for scheduling an appointment'''
    pass

class HospitalsScreen(Screen):
    '''screen for vieweing hospitals nearby'''
    pass

class DatasetScreen(Screen):
    '''screen for viewing previius datasets'''
    pass

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20

        self.appointment_button = Button(text='Schedule an appointment')
        self.appointment_button.bind(on_press=self.schedule_appointment)
        self.add_widget(self.appointment_button)

        self.hospitals_button = Button(text='Hospitals nearby')
        self.hospitals_button.bind(on_press=self.show_hospitals)
        self.add_widget(self.hospitals_button)

        self.datasets_button = Button(text='See previous datasets')
        self.datasets_button.bind(on_press=self.view_datasets)
        self.add_widget(self.datasets_button)

    def schedule_appointment(self, instance):
        """
        Callback function for the 'Schedule an appointment' button.

        Switches to the appointment screen.
        """
        app = App.get_running_app()
        app.root.current = 'appointment'

    def show_hospitals(self, instance):
        """
        Callback function for the 'Hospitals nearby' button.

        Switches to the hospitals screen.
        """
        app = App.get_running_app()
        app.root.current = 'hospitals'

    def view_datasets(self, instance):
        """
        Callback function for the 'See previous datasets' button.

        Switches to the datasets screen.
        """
        app = App.get_running_app()
        app.root.current = 'datasets'


class MyApp(App):
    '''Main Application class'''
    def build(self):
        """
        Build the app's user interface using the KV language string.
        """
        return Builder.load_string(kv)


if __name__ == '__main__':
    MyApp().run()
