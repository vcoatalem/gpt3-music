import os
import re
from dotenv import load_dotenv

import openai

load_dotenv()

def get_chord_progression(track_description="melancholic song", nb_chords=4, base_scale="C"):
    
    prompt = f"Write me a {nb_chords}-chords harmonic progression in {base_scale} scale for a {track_description}."

    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    # Initialize the OpenAI API
    openai.api_key = open_ai_api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0
    )
    print(response.choices[0])
    note_parsed = parse_notes(response.choices[0].text)
    return note_parsed

def parse_notes(string):
    notes = re.findall(r'[A-G](?:#|b)?(?:min|maj|minor|major|m|M)?[0-9]?', string)
    return notes



