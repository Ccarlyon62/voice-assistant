import os
import subprocess
import speech_recognition as sr

def speak(text):
    """Passes text to Android's TTS engine via Termux API."""
    if not text:
        return
    print(f"Assistant: {text}")
    # Escape double quotes to prevent shell syntax issues
    safe_text = text.replace('"', '\\"')
    tts_cmd = f'termux-tts-speak "{safe_text}"'
    subprocess.run(tts_cmd, shell=True)

def process_response(user_input):
    """Simple command logic handler (expandable with APIs or LLMs)."""
    text = user_input.lower()
    
    if "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"
    elif "time" in text:
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif "your name" in text:
        return "I am your Termux Python voice assistant."
    else:
        return f"I heard you say: {user_input}"

def listen():
    audio_file = "input.wav"
    
    if os.path.exists(audio_file):
        os.remove(audio_file)
        
    print("\nListening... Speak now!")
    rec_cmd = f"pactl load-module module-sles-source >/dev/null 2>&1; rec -q -r 16000 -c 1 {audio_file} trim 0 4 gain 5"
    
    try:
        subprocess.run(rec_cmd, shell=True)
    except KeyboardInterrupt:
        return "exit"

    if not os.path.exists(audio_file):
        speak("Error: Audio file was not created.")
        return None

    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.record(source)

        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("I couldn't understand what you said.")
        return None
    except Exception as e:
        speak("There was an error processing the audio.")
        return None
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    speak("Voice assistant initialized.")
    try:
        while True:
            cmd = listen()
            if cmd:
                if 'exit' in cmd.lower() or 'stop' in cmd.lower():
                    speak("Goodbye!")
                    break
                
                # Generate and speak the response
                reply = process_response(cmd)
                speak(reply)
                
    except KeyboardInterrupt:
        speak("Exiting assistant.")

