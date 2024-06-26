Desktop Assistant

This Desktop Assistant is a versatile and interactive application designed to help you manage daily tasks efficiently from your desktop. It offers a wide range of functionalities such as performing web searches, checking emails, managing system info, and even integrating with APIs to fetch news and weather updates.

Features

Open Applications: Open common applications like Notepad, Spotify, VS Code, and web browsers directly from the assistant.

Web Searches: Perform web searches and open websites like Wikipedia and YouTube.

Weather Updates: Fetch the current weather information for predefined locations.

News Headlines: Retrieve the latest news headlines.

System Information: Monitor CPU usage, memory usage, and disk usage.
Email Checker: Check for new emails in your inbox.

Math Evaluations: Solve math expressions and trigonometric calculations.

Spelling Corrections: Check and correct spelling mistakes.

3D Model Viewer: Open a window to display 3D models, specifically configured for Sylvanas Windrunner.

Voice Interaction: Input commands via voice (feature planned).


Installation
Prerequisites
Python 3.6+
pip (Python package installer)
API Keys for OpenAI, Weather API, and News API

Required Libraries--

Install all required Python libraries 
with the following command:

pip install tkinter requests openai wikipedia-api pyspellchecker pyglet psutil imapclient pyzmail subprocess
Environment Variables

Ensure the following environment 
variables are set:

OPENAI_API_KEY: Your OpenAI API key for GPT-3 queries.
WEATHER_API_KEY: API key for weather updates.
NEWS_API_KEY: API key for fetching news headlines.
EMAIL: Your email address for checking new emails.
EMAIL_PASSWORD: Password for your email account.
You can set these variables in your environment or directly in the script if security is not a concern.

To run the desktop assistant Navigate to the directory containing the script.

Run the script using Python:

python desktop_assistant.py
The main window of the Desktop Assistant will open, and you can start interacting with it by typing commands into the input box or using predefined buttons for specific tasks.

Extending Functionality
The application is modular, allowing for easy extension. You can add new features by defining additional functions and linking them to user commands in the register_commands method of the DesktopAssistant class.

Troubleshooting
If you encounter any issues:

Check the Python and library versions to ensure compatibility.
Verify that all API keys are valid and have not expired.
Ensure that environment variables are correctly set.
For further assistance, consult the logging output for error details, which can provide insights into what might be going wrong.

Contributing
Contributions to enhance or expand the application's capabilities are welcome. Please fork the repository, make your changes, and submit a pull request.
