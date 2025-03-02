from datetime import datetime
import subprocess
import anthropic
import pyperclip
import pyautogui
import whisper
import time
import sys
import os
import warnings

from prompts import P_FACT_EXTRACT_SYSTEM


# Configuration
AUDIO_FILE = '/tmp/quick_capture.wav'
OBSIDIAN_NOTE = os.path.expanduser('~/Obsidian/ZettleKasten/slow_drip - moc.md')
warnings.filterwarnings("ignore", message="Can't initialize NVML") #idk yet

def record_audio():
    """Record audio with arecord and return the process."""
    # Start recording in the background
    record_process = subprocess.Popen([
        'arecord', 
        '-f', 'cd',     # CD quality
        '-t', 'wav',    # WAV format
        '-r', '44100',  # Sample rate
        '-q',           # Quiet mode
        AUDIO_FILE      # Output file
    ])
    
    # Show zenity dialog
    try:
        subprocess.run(['zenity', '--question', 
                       '--text=Recording in progress. Click OK to stop.', 
                       '--title=Recording'])
    except subprocess.CalledProcessError:
        # User clicked Cancel or closed the window
        pass
    
    # Stop the recording process
    record_process.terminate()
    record_process.wait()
    
    return AUDIO_FILE

def get_current_url():
    """Get the URL of the currently active browser window."""
    try:
        pyautogui.hotkey('i')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        pyautogui.hotkey('F6')
        time.sleep(0.1)
        pyautogui.hotkey('Esc')
        return pyperclip.paste().strip()
    except Exception as e:
        print(f"URL capture error: {e}", file=sys.stderr)
        return "URL not found"

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        print(f"Transcription error: {e}", file=sys.stderr)
        return ""

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)

test_text = """
If APIs are inconsistent, developers will need more time to figure out what to do and write more code to mitigate the differences in data, formats, error feedback, or security measures. And constantly writing unnecessary specific code augments the risk of bugs. Also, they will ask more questions and need extended support.

If APIs are consistent—sharing a familiar look and behavior—anyone who has learned how to use one will be able to use another instantly. And if those APIs look like any other outside-world API, that reduces the first learning steps even more. Their consistent design allows developers to reuse client code between different APIs, and combining them will be simplified if those APIs rely on consistent data. If developers don’t have to write specific code to transform data between API calls or interpret the dozens of error feedback structures, they will develop faster with fewer bugs.

And even more important, developers can guess how consistently designed APIs work. That not only reduces the time-to-value, but it also makes them feel brilliant. Such a feeling has no price, especially when the API is a public one they can choose to use or not to use.
"""

message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=20000,
    temperature=1,
    system=P_FACT_EXTRACT_SYSTEM,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": test_text
                }
            ]
        }
    ]
)
print(message.content)
