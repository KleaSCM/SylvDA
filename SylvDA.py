import tkinter as tk
from tkinter import scrolledtext
import subprocess
import openai
import wikipediaapi
from spellchecker import SpellChecker
import threading
import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import os
import logging
import requests
import psutil
import imapclient
import pyzmail

# Set fake environment variables for testing purposes
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
os.environ['WEATHER_API_KEY'] = 'your_weather_api_key'
os.environ['NEWS_API_KEY'] = 'your_news_api_key'
os.environ['EMAIL'] = 'your_email@example.com'
os.environ['EMAIL_PASSWORD'] = 'your_email_password'
os.environ['SYLVANAS_MODEL_PATH'] = 'path_to_sylvanas_model.obj'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")
openai.api_key = api_key

# Initialize Wikipedia API and spell checker
wiki_wiki = wikipediaapi.Wikipedia('en')
spell = SpellChecker()

def query_gpt3(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logging.error(f"Error querying OpenAI: {str(e)}")
        return f"Error querying OpenAI: {str(e)}"

def search_wikipedia(query):
    page = wiki_wiki.page(query)
    return page.summary if page.exists() else "No information found."

def check_spelling(query):
    misspelled = spell.unknown(query.split())
    if misspelled:
        word = misspelled.pop()
        return f"The correct spelling of {word} is {spell.correction(word)}."
    return "No spelling mistakes found."

def evaluate_math_expression(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        logging.error(f"Error evaluating math expression: {str(e)}")
        return f"Error: {str(e)}"

def evaluate_trigonometry(expression):
    try:
        angle = float(expression.split()[-1])
        if "sin" in expression:
            result = math.sin(math.radians(angle))
        elif "cos" in expression:
            result = math.cos(math.radians(angle))
        elif "tan" in expression:
            result = math.tan(math.radians(angle))
        return f"{expression} = {result}"
    except ValueError:
        logging.error("Invalid input for trigonometric function.")
        return "Invalid input for trigonometric function."
    except Exception as e:
        logging.error(f"Error evaluating trigonometric function: {str(e)}")
        return f"Error: {str(e)}"

def get_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    location = 'New York'  # Change as needed
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        data = response.json()
        current = data['current']
        return f"Weather in {location}: {current['temp_c']}°C, {current['condition']['text']}"
    except Exception as e:
        logging.error(f"Error getting weather: {str(e)}")
        return "Error getting weather information."

def get_news():
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        articles = response.json().get('articles', [])
        headlines = [article['title'] for article in articles[:5]]
        return "Top news headlines:\n" + "\n".join(headlines)
    except Exception as e:
        logging.error(f"Error getting news: {str(e)}")
        return "Error getting news updates."

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (f"CPU Usage: {cpu_usage}%\n"
            f"Memory Usage: {memory.percent}%\n"
            f"Disk Usage: {disk.percent}%")

def check_email():
    email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    try:
        server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        server.login(email, password)
        server.select_folder('INBOX')
        messages = server.search(['UNSEEN'])
        if messages:
            return f"You have {len(messages)} new emails."
        else:
            return "No new emails."
    except Exception as e:
        logging.error(f"Error checking email: {str(e)}")
        return "Error checking email."

class ApplicationOpener:
    @staticmethod
    def open_application(command, app_name, shell=False):
        try:
            subprocess.Popen(command, shell=shell)
            return f"Opening {app_name}..."
        except FileNotFoundError:
            logging.error(f"{app_name} not found.")
            return f"{app_name} not found."
        except Exception as e:
            logging.error(f"Error opening {app_name}: {str(e)}")
            return f"Error opening {app_name}: {str(e)}"

class DesktopAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Assistant")

        self.create_widgets()
        self.register_commands()

    def create_widgets(self):
        self.input_box = tk.Entry(self.root, width=50)
        self.input_box.pack(pady=10)
        self.input_box.bind("<Return>", self.process_input)

        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.output_box.pack(pady=10)

        self.model_button = tk.Button(self.root, text="Show Sylvanas", command=self.show_model)
        self.model_button.pack(pady=10)

        self.speak_button = tk.Button(self.root, text="Speak", command=self.speak_input)
        self.speak_button.pack(pady=10)

        self.reminder_button = tk.Button(self.root, text="Set Reminder", command=self.set_reminder)
        self.reminder_button.pack(pady=10)

    def register_commands(self):
        self.commands = {
            "open notepad": lambda: ApplicationOpener.open_application(["notepad.exe"], "Notepad"),
            "open spotify": lambda: ApplicationOpener.open_application(["spotify.exe"], "Spotify"),
            "open word": lambda: ApplicationOpener.open_application(["start", "winword"], "Word", shell=True),
            "open excel": lambda: ApplicationOpener.open_application(["start", "excel"], "Excel", shell=True),
            "open browser": lambda: ApplicationOpener.open_application(["start", "chrome"], "Web Browser", shell=True),
            "open vs code": lambda: ApplicationOpener.open_application(["code"], "VS Code"),
            "open paint": lambda: ApplicationOpener.open_application(["mspaint.exe"], "MS Paint"),
            "open battle.net": lambda: ApplicationOpener.open_application(["Battle.net.exe"], "Battle.net"),
            "open curseforge": lambda: ApplicationOpener.open_application(["CurseForge.exe"], "CurseForge"),
            "open youtube": lambda: ApplicationOpener.open_application(["start", "https://www.youtube.com"], "YouTube", shell=True),
            "open wikipedia": lambda: ApplicationOpener.open_application(["start", "https://www.wikipedia.org"], "Wikipedia", shell=True),
            "weather": get_weather,
            "news": get_news,
            "system info": get_system_info,
            "check email": check_email,
        }

    def process_input(self, event=None):
        user_input = self.input_box.get()
        self.output_box.insert(tk.END, f"User: {user_input}\n")
        self.input_box.delete(0, tk.END)

        response = self.handle_command(user_input.lower())
        self.output_box.insert(tk.END, f"Assistant: {response}\n")

    def handle_command(self, command):
        for cmd, func in self.commands.items():
            if cmd in command:
                return func()

        if "who is" in command:
            return search_wikipedia(command.replace("who is ", ""))
        elif "how do you spell" in command:
            return check_spelling(command.replace("how do you spell ", ""))
        elif any(op in command for op in ['+', '-', '*', '/']):
            return evaluate_math_expression(command)
        elif any(trig in command for trig in ['sin', 'cos', 'tan']):
            return evaluate_trigonometry(command)
        else:
            return query_gpt3(command)

    def show_model(self):
        threading.Thread(target=self.run_model_viewer).start()

    def run_model_viewer(self):
        model_path = os.getenv('SYLVANAS_MODEL_PATH', 'path_to_sylvanas_model.obj')

        class ModelViewerWindow(pyglet.window.Window):
            def __init__(self, width, height, title=''):
                super().__init__(width, height, title)
                pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
                try:
                    self.model = pyglet.model.load(model_path)
                except Exception as e:
                    logging.error(f"Error loading model: {str(e)}")
                    self.close()

            def on_draw(self):
                self.clear()
                glEnable(GL_DEPTH_TEST)
                glLoadIdentity()
                gluPerspective(45.0, self.width / self.height, 0.1, 100.0)
                glTranslatef(0.0, 0.0, -5.0)
                self.model.draw()

            def on_key_press(self, symbol, modifiers):
                if symbol == key.ESCAPE:
                    self.close()

        try:
            window = ModelViewerWindow(800, 600, 'Sylvanas Windrunner')
            pyglet.app.run()
        except Exception as e:
            logging.error(f"Error running model viewer: {str(e)}")

    def speak_input(self):
        user_input = self.input_box.get()
        speak(user_input)

    def set_reminder(self):
        reminder_time = self.input_box.get()
        try:
            reminder_time = datetime.strptime(reminder_time, "%H:%M")
            current_time = datetime.now()
            delay = (reminder_time - current_time).total_seconds()
            if delay > 0:
                self.root.after(int(delay * 1000), lambda: self.output_box.insert(tk.END, "Reminder: Time's up!\n"))
                self.output_box.insert(tk.END, f"Reminder set for {reminder_time.strftime('%H:%M')}\n")
            else:
                self.output_box.insert(tk.END, "Invalid time. Please enter a future time in HH:MM format.\n")
        except ValueError:
            self.output_box.insert(tk.END, "Invalid time format. Please enter time in HH:MM format.\n")

# Create the main Tkinter window and run the desktop assistant
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DesktopAssistant(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error starting the desktop assistant: {str(e)}")
        print(f"Error starting the desktop assistant: {str(e)}")

