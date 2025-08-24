import os
import requests

from sio.compilers.common import Compiler
from sio.workers.util import tempcwd


class SpeechToTextCompiler(Compiler):
    sandbox = 'compiler-gcc.12_2_0'
    lang = 'speech_to_text'
    output_file = 'a.out'

    dictionary = {
        # Quotes
        (u'cudzysłów',): '"',
        (u'quote',): '"',

        # Parentheses
        (u'otwórz', u'nawias'): '(',
        (u'nawias', u'otwierający'): '(',
        (u'open', u'parenthesis'): '(',
        (u'opening', u'parenthesis'): '(',

        (u'zamknij', u'nawias'): ')',
        (u'nawias', u'zamykający'): ')',
        (u'close', u'parenthesis'): ')',
        (u'closing', u'parenthesis'): ')',

        # Curly braces
        (u'otwórz', u'nawias', u'klamrowy'): '{',
        (u'otwórz', u'klamrę'): '{',
        (u'klamra', u'otwierająca'): '{',
        (u'nawias', u'klamrowy', u'otwierający'): '{',
        (u'klamrowy', u'nawias', u'otwierający'): '{',
        (u'open', u'brace'): '{',

        (u'zamknij', u'nawias', u'klamrowy'): '}',
        (u'zamknij', u'klamrę'): '}',
        (u'klamra', u'zamykająca'): '}',
        (u'nawias', u'klamrowy', u'zamykający'): '}',
        (u'klamrowy', u'nawias', u'zamykający'): '}',
        (u'close', u'brace'): '}',

        # Square brackets
        (u'otwórz', u'nawias', u'kwadratowy'): '[',
        (u'otwórz', u'kwadratowy', u'nawias'): '[',
        (u'nawias', u'kwadratowy', u'otwierający'): '[',
        (u'kwadratowy', u'nawias', u'otwierający'): '[',
        (u'open', u'bracket'): '[',

        (u'zamknij', u'nawias', u'kwadratowy'): ']',
        (u'zamknij', u'kwadratowy', u'nawias'): ']',
        (u'nawias', u'kwadratowy', u'zamykający'): ']',
        (u'kwadratowy', u'nawias', u'zamykający'): ']',
        (u'close', u'bracket'): ']',

        # Arithmetic operators
        (u'plus',): '+',
        (u'dodać',): '+',
        (u'minus',): '-',
        (u'odjąć',): '-',
        (u'razy',): '*',
        (u'multiply',): '*',
        (u'podzielić',): '/',
        (u'divide',): '/',
        (u'równa',): '=',
        (u'equals',): '=',

        (u'slash',): '/',
        (u'ukośnik',): '/',

        (u'backslash',): '\\',
        (u'back', u'slash',): '\\',
        (u'ukośnik', u'wsteczny'): '\\',

        # Comparison operators
        (u'większe', u'niż'): '>',
        (u'greater', u'than'): '>',
        (u'mniejsze', u'niż'): '<',
        (u'less', u'than'): '<',

        # Punctuation
        (u'przecinek',): ',',
        (u'comma',): ',',
        (u'kropka',): '.',
        (u'dot',): '.',
        (u'semicolon',): ';',
        (u'średnik',): ';',
        (u'dwukropek',): ':',
        (u'colon',): ':',

        (u'hashtag',): '#',

        (u'apostrof',): "'",
        (u'apostrophe',): "'",

        (u'enter',): '\n',
        (u'nowa', u'linia'): '\n',
        (u'new', u'line'): '\n',

        (u'c', u'out'): '\n',
        (u'c', u'o', u'u', u't'): 'cout',

        (u's', u't', u'd', u'c'): 'stdc',
    }

    def _transcribe_file(self, api_key, file_path, model_id="scribe_v1"):
        url = "https://api.elevenlabs.io/v1/speech-to-text"

        headers = {
            "xi-api-key": api_key
        }

        files = {
            "file": open(file_path, "rb")
        }

        data = {
            "model_id": model_id
        }

        resp = requests.post(url, headers=headers, files=files, data=data)

        try:
            return resp.json()
        except Exception:
            return {"status_code": resp.status_code, "text": resp.text}

    def _convert_transcription_to_code(self, transcription):
        words = [word["text"].lower().strip(" ,.!") for word in transcription.get("words", []) if
                 word.get("type") == 'word']

        output = []
        skip = 0

        i = 0
        while i < len(words):
            matched = False
            for key_tuple, symbol in self.dictionary.items():
                n = len(key_tuple)
                if words[i:i + n] == list(key_tuple):
                    output.append((symbol, "symbol"))
                    i += n
                    matched = True
                    break
            if not matched:
                output.append((words[i], "word"))
                i += 1

        output_code = ""
        previous_type = None
        for (content, type) in output:
            if previous_type == "word" and type == "word":
                output_code += " "
            output_code += content
            previous_type = type

        return output_code

    def _speech_to_text(self):
        api_key = os.environ.get('SPEECH_TO_TEXT_API_KEY')
        result = self._transcribe_file(api_key, tempcwd(self.source_file))
        code = self._convert_transcription_to_code(result)
        with open(tempcwd("code.cpp"), "w") as f:
            f.write(code)


    def _make_cmdline(self, executor):
        self._speech_to_text()
        return [
            'g++', 'std=c++20', '-O3', '-s',
            tempcwd("code.cpp"),
            '-o',
            tempcwd(self.output_file),
        ]


def run(environ):
    return SpeechToTextCompiler().compile(environ)
