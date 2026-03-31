import requests
from youtube_transcript_api import YouTubeTranscriptApi
from translate import Translator
from deep_translator import GoogleTranslator
from os import getenv
from dotenv import load_dotenv
load_dotenv()
import json
import time

def chunk_text(text, max_size=2000):
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_size

        # avoid cutting in middle of word
        if end < len(text):
            while end > start and text[end] != " ":
                end -= 1

        chunks.append(text[start:end])
        start = end
    print(f"chunking :{len(chunks)}")
    return chunks




def get_transcript(link:str):
    yyt = YouTubeTranscriptApi()
    id = link.split("v=")[-1]
    if "=" in id:
        temp = id.split("&")
        id=temp[0]
    reslut = yyt.fetch(id,languages=['hi','en'])
    text = ""
    for snippet in reslut:
            text = text + snippet.text
    return text


def translate_text(text:str):
    translator = GoogleTranslator(source="auto",target="en")
    translator23 = Translator(to_lang="en")
    chunks = chunk_text(text=text)
    for chunk in chunks:
        print(f"translating {chunks.index(chunk)}")
        translated_result = translator.translate(chunk)

        for word in translated_result.split(" ") :
            yield f"data: {word} \n\n" 
            time.sleep(0.05)

def main(link:str):
    text = get_transcript(link=link)
    return translate_text(text=text)






    


