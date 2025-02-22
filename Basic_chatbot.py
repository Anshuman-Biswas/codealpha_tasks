import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import random

# Load spaCy's English model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    messagebox.showerror("Error", f"Failed to load spaCy model: {e}")
    exit()

# Weather API configuration
API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Predefined intents and responses
intents = {
    "greeting": ["hello", "hi", "hey"],
    "farewell": ["bye", "goodbye", "see you"],
    "weather": ["weather", "temperature", "forecast"],
    "joke": ["joke", "tell me a joke"],
    "thanks": ["thank you", "thanks"],
    "name": ["what is your name", "who are you"]
}

responses = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! How can I help you?"],
    "farewell": ["Goodbye! Have a great day!", "Bye! See you soon!"],
    "weather": ["Let me check the weather for you.", "Here's the weather information."],
    "joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call fake spaghetti? An impasta!"],
    "thanks": ["You're welcome!", "No problem!", "Happy to help!"],
    "name": ["I'm a chatbot. You can call me ChatBot!", "I don't have a name, but you can call me ChatBot."],
    "default": ["I'm not sure I understand. Can you rephrase that?", "Sorry, I didn't get that. Could you clarify?"]
}

# Train a simple intent classification model
training_data = [
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("bye", "farewell"),
    ("goodbye", "farewell"),
    ("what is the weather", "weather"),
    ("tell me a joke", "joke"),
    ("thank you", "thanks"),
    ("what is your name", "name")
]

texts, labels = zip(*training_data)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
clf = MultinomialNB()
clf.fit(X, labels)

def classify_intent(user_input):
    """
    Classify the user's intent using the trained model.
    
    :param user_input: The user's input text.
    :return: The predicted intent.
    """
    X_user = vectorizer.transform([user_input])
    return clf.predict(X_user)[0]

def get_weather(city):
    """
    Fetch the current weather for a given city using the OpenWeatherMap API.
    
    :param city: The name of the city.
    :return: A string containing the weather information.
    """
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
        else:
            return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        return f"Error fetching weather data: {e}"

class ChatbotGUI:
    def __init__(self, root):
        """
        Initialize the Chatbot GUI.
        
        :param root: The root window of the application.
        """
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("500x400")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input area
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        self.user_input = tk.Entry(self.input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key to send_message

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # Display welcome message
        self.display_message("ChatBot: Hello! How can I assist you today?")

    def display_message(self, message):
        """
        Display a message in the chat area.
        
        :param message: The message to display.
        """
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)  # Auto-scroll to the bottom

    def send_message(self, event=None):
        """
        Send the user's message and get the chatbot's response.
        """
        user_input = self.user_input.get().strip()
        if user_input:
            # Display user's message
            self.display_message(f"You: {user_input}")
            self.user_input.delete(0, tk.END)  # Clear the input field

            # Classify the intent
            intent = classify_intent(user_input)

            # Generate a response based on the intent
            if intent == "weather":
                doc = nlp(user_input)
                city = None
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity (e.g., city, country)
                        city = ent.text
                        break
                if city:
                    weather_info = get_weather(city)
                    self.display_message(f"ChatBot: {weather_info}")
                else:
                    self.display_message("ChatBot: Please specify a city for the weather.")
            else:
                response = responses.get(intent, responses["default"])
                self.display_message(f"ChatBot: {random.choice(response)}")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()