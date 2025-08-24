import os

from sio.compilers.common import Compiler
from sio.workers.util import tempcwd


class SpeechToTextCompiler(Compiler):
    sandbox = 'speech_to_text.1_amd64'
    lang = 'speech_to_text'
    output_file = 'a.out'

    def _make_cmdline(self, executor):
        api_key = os.environ.get('SPEECH_TO_TEXT_API_KEY')
        return [
            '/usr/bin/python3',
            '/entrypoint',
            '"' + api_key + '"',
            tempcwd(self.source_file),
            tempcwd(self.output_file),
        ]


def run(environ):
    return SpeechToTextCompiler().compile(environ)
