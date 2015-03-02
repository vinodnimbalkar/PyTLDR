# -*- coding: utf-8 -*-
import unicodedata
from goose import Goose
from ..nlp.tokenizer import Tokenizer


class BaseSummarizer(object):

    def __init__(self, tokenizer=Tokenizer('english')):
        self._tokenizer = tokenizer

    def summarize(self, text, num_sentences=5):
        raise NotImplementedError('This method needs to be implemented in a base class')

    @classmethod
    def parse_input(cls, text):
        if isinstance(text, str) or isinstance(text, unicode):
            if text.startswith('http'):
                # Input is a link - need to extract the text from html
                urlparse = Goose()
                article = urlparse.extract(url=text)
                return cls._unicode_to_ascii(article.cleaned_text)
            elif text.endswith('.txt'):
                # Input is a file - need to read it
                textfile = open(text, 'rb')
                article = textfile.read()
                textfile.close()
                return cls._unicode_to_ascii(article)
            else:
                # Input is a string containing the raw text
                return cls._unicode_to_ascii(text)
        else:
            raise ValueError('Input text must be of type str or unicode.')

    @classmethod
    def _unicode_to_ascii(cls, unicodestr):
        if isinstance(unicodestr, str):
            return unicodestr
        elif isinstance(unicodestr, unicode):
            return unicodedata.normalize('NFKD', unicodestr).encode('ascii', 'ignore')
        else:
            raise ValueError('Input text must be of type str or unicode.')