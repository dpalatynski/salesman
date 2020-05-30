import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
Config.set('graphics', 'resizable', True)
import os
import sys
import TSP

global method_of_calculating
method_of_calculating = None

if os.path.isfile("results.txt"):
    with open("results.txt", "w") as f:
        f.truncate()

if os.path.isfile("addresses.txt"):
    with open("addresses.txt", "w") as f:
        f.truncate()

if os.path.isfile("distance.txt"):
    with open("distance.txt", "w") as f:
        f.truncate()


class SalesmanApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.entry_page = EntryPage()
        screen = Screen(name = "Entry")
        screen.add_widget(self.entry_page)
        self.screen_manager.add_widget(screen)

        self.writing_rows = Writingrows()
        screen = Screen(name = "Writing_rows")
        screen.add_widget(self.writing_rows)
        self.screen_manager.add_widget(screen)

        self.loading = Loading()
        screen = Screen(name = "Loading")
        screen.add_widget(self.loading)
        self.screen_manager.add_widget(screen)

        self.results = Results()
        screen = Screen(name = "Results")
        screen.add_widget(self.results)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

class EntryPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 5

        if os.path.isfile("addresses.txt"):
            with open("addresses.txt", "w") as f:
                f.truncate()

        lbl1 = Label(text = "Choose the method of calculating the route:", font_size = 35)
        self.add_widget(lbl1)

        btn1 = Button(text = "Brute Force")
        btn1.bind(on_press=self.choosing_brute_force)
        self.add_widget(btn1)

        btn2 = Button(text = "Repetitive Nearest Neighbour")
        btn2.bind(on_press=self.choosing_nearest_neigbour)
        self.add_widget(btn2)

        btn3 = Button(text = "Held-Karp algorithm")
        btn3.bind(on_press=self.choosing_held_karp)
        self.add_widget(btn3)

        btn4 = Button(text = "Exit")
        btn4.bind(on_press=self.exitbutton)
        self.add_widget(btn4)

    def choosing_brute_force(self, instance):
        print("You've chosen brute force method")
        global method_of_calculating
        method_of_calculating = 1
        salesman.screen_manager.current = "Writing_rows"

    def choosing_nearest_neigbour(self, instance):
        print("You've chosen nearest neighbour method")
        global method_of_calculating
        method_of_calculating = 2
        salesman.screen_manager.current = "Writing_rows"

    def choosing_held_karp(self, instance):
        print("You've chosen Held-Karp algorithm")
        global method_of_calculating
        method_of_calculating = 3
        salesman.screen_manager.current = "Writing_rows"

    def exitbutton(self, instance):
        App.get_running_app().stop()
        Window.close()

class Writingrows(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 7

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.lbl1 = Label(text = "Country: ")
        self.country = TextInput(text = 'Polska', multiline=False, font_size = 35)
        self.mybox.add_widget(self.lbl1)
        self.mybox.add_widget(self.country)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.lbl1 = Label(text = "City: ")
        self.city = TextInput(multiline=False, font_size = 35)
        self.mybox.add_widget(self.lbl1)
        self.mybox.add_widget(self.city)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal',height = Window.size[1]*0.1, size_hint_y = None)
        self.lbl1 = Label(text = "Address: ")
        self.address = TextInput(multiline=False, font_size = 35)
        self.mybox.add_widget(self.lbl1)
        self.mybox.add_widget(self.address)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.button1 = Button(text="Go to Menu")
        self.button1.bind(on_press=self.backtomenu)
        self.button2 = Button(text="Add")
        self.button2.bind(on_press=self.addbutton)
        self.save = Button(text="Next")
        self.save.bind(on_press=self.next)
        self.mybox.add_widget(self.button1)
        self.mybox.add_widget(self.button2)
        self.mybox.add_widget(self.save)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.button1 = Button(text="Clear all")
        self.button1.bind(on_press=self.clear_all)
        self.button2 = Button(text="Delete the last one")
        self.button2.bind(on_press=self.delete_the_last_one)
        self.save = Button(text="Example 1")
        self.save.bind(on_press=self.example1)
        self.mybox.add_widget(self.button1)
        self.mybox.add_widget(self.button2)
        self.mybox.add_widget(self.save)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.lbl1 = Label(text = "List of places to visit: ")
        self.mybox.add_widget(self.lbl1)
        self.add_widget(self.mybox)

        self.scroll = ScrollableLabel(height = Window.size[1]*0.4, size_hint_y = None)
        self.add_widget(self.scroll)

        f = open("addresses.txt", "r")
        lines = f.readlines()

        self.scroll.update()

    def addbutton(self, instnace):
        country = self.country.text
        city = self.city.text
        address = self.address.text

        f = open("addresses.txt", 'a+')
        if address == '':
            f.write(f"{country}, {city} \n")
        elif address != '':
            f.write(f"{country}, {city}, {address} \n")
        f.close()

        self.country.text = 'Polska'
        self.city.text = ''
        self.address.text = ''

        f = open("addresses.txt", "r")
        lines = f.readlines()

        ScrollableLabel.update(self.scroll)

    def backtomenu(self, instance):
        salesman.screen_manager.current = "Entry"

    def delete_the_last_one(self, instance):
        f = open("addresses.txt", "r")
        lines = f.readlines()

        lines = lines[:-1]

        f.close()

        if os.path.isfile("addresses.txt"):
            with open("addresses.txt", "w") as f:
                f.truncate()

        f = open("addresses.txt", 'a+')
        for i in range(len(lines)):
            f.write(lines[i])
        f.close()

        ScrollableLabel.update(self.scroll)

    def clear_all(self, instance):
        if os.path.isfile("addresses.txt"):
            with open("addresses.txt", "w") as f:
                f.truncate()
        lines = ''
        ScrollableLabel.update(self.scroll)

    def next(self, instance):
        if os.path.isfile("results.txt"):
            with open("results.txt", "w") as f:
                f.truncate()
        if os.path.isfile("distance.txt"):
            with open("distance.txt", "w") as f:
                f.truncate()

        salesman.screen_manager.current = "Loading"
        Clock.schedule_once(self.calculate, 5)


    def calculate(self, instance):
        if method_of_calculating == 1:
            TSP.TSP_brute_force("addresses.txt")
        elif method_of_calculating == 2:
            TSP.TSP_rnn("addresses.txt")
        elif method_of_calculating == 3:
            TSP.TSP_held_karp("addresses.txt")
        if os.path.isfile("addresses.txt"):
            with open("addresses.txt", "w") as f:
                f.truncate()
        ScrollableLabel.update(self.scroll)
        salesman.screen_manager.current = "Results"


    def example1(self, instance):
        if os.path.isfile("addresses.txt"):
            with open("addresses.txt", "w") as f:
                f.truncate()

        f = open("addresses.txt", 'a+')

        f.write('''Polska, Wrocław, Królewiecka
Polska, Warszawa, Łazienkowska
Polska, Poznań, Bułgarska
Polska, Gdańsk, Traugutta
Polska, Kraków, Reymonta
Polska, Kraków, Kałuży
Polska, Chorzów, Katowicka
Polska, Warszawa, Poniatowskiego''')
        f.close()

        f = open("addresses.txt", "r")
        lines = f.readlines()

        ScrollableLabel.update(self.scroll)


class ScrollableLabel(ScrollView):
    def update(self):
        f = open("addresses.txt", "r")
        lines = f.readlines()
        self.ids.lines.text = '\n'
        for i in range(len(lines)):
            self.ids.lines.text += '\n ' +str(i+1) + ". " + lines[i]

class Loading(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 2
        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.3, size_hint_y = None)
        lbl1 = Label(text = "Loading", font_size = 40, size = (0.95,1))
        self.mybox.add_widget(lbl1)
        self.add_widget(self.mybox)

        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.7, size_hint_y = None)
        self.img = Image(source ='gif2.gif', size = (0.5, 0.5))

        self.img.allow_stretch = True
        self.img.keep_ratio = False

        self.img.size_hint_x = 1
        self.img.size_hint_y = 1

        self.img.pos = (Window.size[0]/2 - 50,Window.size[1]/2 - 50)

        self.img.opacity = 1
        self.mybox.add_widget(self.img)

        self.add_widget(self.mybox)


class Results(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 4

        self.lbl1 = Label(text = "The nearest route is: ", font_size = 40)
        self.add_widget(self.lbl1)

        self.scroll = ScrollableLabelResults(height = Window.size[1]*0.75, size_hint_y = None)
        self.add_widget(self.scroll)


        self.mybox = BoxLayout(orientation='horizontal', height = Window.size[1]*0.1, size_hint_y = None)
        self.button2 = Button(text="Go to menu")
        self.button2.bind(on_press=self.backtomenu)
        self.button1 = Button(text="Show results")
        self.button1.bind(on_press=self.update)
        self.button3 = Button(text="Exit")
        self.button3.bind(on_press=self.exitbutton)
        self.mybox.add_widget(self.button2)
        self.mybox.add_widget(self.button1)
        self.mybox.add_widget(self.button3)
        self.add_widget(self.mybox)

        self.scroll.update()
        ScrollableLabelResults.update(self.scroll)

    def update(self, instance):
        ScrollableLabelResults.update(self.scroll)

    def showresults(self):
        self.scroll.update()

    def exitbutton(self, instance):
        App.get_running_app().stop()
        Window.close()

    def backtomenu(self, instance):
        if os.path.isfile("results.txt"):
            with open("results.txt", "w") as f:
                f.truncate()
        if os.path.isfile("distance.txt"):
            with open("distance.txt", "w") as f:
                f.truncate()
        ScrollableLabelResults.update(self.scroll)
        salesman.screen_manager.current = "Entry"


class ScrollableLabelResults(ScrollView):
    def update(self):
        f = open("distance.txt", "r")
        distance = f.readlines()
        f = open("results.txt", "r")
        lines = f.readlines()
        if len(distance) != 0:
            self.ids.lines.text = 'Distance: ' + str(distance[0]) + '\n'
        elif len(distance) == 0:
            self.ids.lines.text = '\n'
        for i in range(len(lines)):
            self.ids.lines.text += '\n ' +str(i+1) + ". " + lines[i]

Builder.load_string('''
<ScrollableLabel>:
    size_hint_y: None
    GridLayout:
        cols: 1
        size_hint_y: None
        height: self.minimum_height
        Label:
            text_size: self.width, None
            id: lines
            size_hint_y: None
            halign: 'left'
            valign: 'top'
            height: self.texture_size[1]

<ScrollableLabelResults>:
    size_hint_y: None
    GridLayout:
        cols: 1
        size_hint_y: None
        height: self.minimum_height
        Label:
            text_size: self.width, None
            id: lines
            size_hint_y: None
            halign: 'left'
            valign: 'top'
            height: self.texture_size[1]
''')



salesman = SalesmanApp()
salesman.run()

