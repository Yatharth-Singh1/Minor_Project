import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from flask import Flask, render_template, request, jsonify
import whisper

app = Flask(__name__, static_url_path='/static')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("good morning!")
    elif 12 <= hour < 18:
        speak("good afternoon")
    else:
        speak("good evening!")

    speak("I am your personal assistant. Please tell me how can I help you")

def takecommand():
     r = sr.Recognizer()
     with  sr.Microphone() as source: 
          print ("listening..") 
          r.pause_threshold = 1  
          audio=r.listen(source) 
     
     try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
            print(f"User said: {query}\n")  #User query will be printed.

     except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
     return query

'''def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        # Save the audio data as an MP3 file
        with open("audio.mp3", "wb") as f:
            f.write(audio.get_wav_data())

    try:
        print("Recognizing...")
        model = whisper.load_model("tiny")
        transcript = model.transcribe("audio.mp3", fp16=False)
        query = transcript['text']
        print(f"User said: {query}\n")
    except Exception as e:
        print("Error:", e)
        print("Say that again please...")
        return "None"
    
    return query.lower() if query else "None"'''

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('singhchitwan08@gmail.com', '(#!tw@^@2313')
    server.sendmail('singhchitwan08@gmail.com', to, content)
    server.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def get_command():
    # Simulate speech recognition (replace with your actual logic)
    query = takecommand()
    if 'Wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
    elif 'play music' in query:
        music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
    elif 'open code' in query:
        codePath = "C:\\Users\\Vidyarthi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)
    elif 'email to Chitwan' in query:
        try:
            speak("what should i say ?")
            content = takecommand()
            to = "yatharthsingh051@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry my friend. I am not able to send this email")
    elif 'exit' in query:
        speak("Exiting the program. Goodbye!")
        exit()

    return jsonify({'response': query})

if __name__ == "__main__":
    wishme()
    app.run(debug=True, port=5000)
