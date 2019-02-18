"""
Tokenizer class
To add a tokenizer, add to the below inherting from
main Tokenizer class.

"""
import os

from ..openai_transformer_lm.tf_original import utils as openai_utils
from ..openai_transformer_lm.tf_original.text_utils import TextEncoder
from nltk.tokenize.moses import MosesTokenizer as NLTKMosesTokenizer, MosesDetokenizer

"""Global task registry.

Import this to use @register_task when defining new tasks,
then access the registry as registry.REGISTRY.
"""

AVAILABLE_TOKENIZERS = ["MosesTokenizer" , "OpenAI.BPE"]

class Tokenizer(object):

    def tokenize(self, sentence):
        raise NotImplementedError

class OpenAIBPETokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        OPENAI_DATA_DIR = os.path.join(os.path.dirname(openai_utils.__file__),
                                       "model")
        ENCODER_PATH = os.path.join(OPENAI_DATA_DIR, "encoder_bpe_40000.json")
        BPE_PATH = os.path.join(OPENAI_DATA_DIR, "vocab_40000.bpe")
        self._tokenizer = TextEncoder(ENCODER_PATH, BPE_PATH)
        self._encoder_dict = self._tokenizer.encoder
        self._reverse_encoder_dict = {v:k for k,v in self._encoder_dict.items()}

    def lookup_ids(self, ids):
        return [self._reverse_encoder_dict[i] for i in ids]

    def encode(self, sentences):
        return self._tokenizer.encode(sentences)

    def tokenize(self, sentence):
        ids = self.encode([sentence])[0]
        return self.lookup_ids(ids)

class MosesTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self._tokenizer = NLTKMosesTokenizer()

    def tokenize(self, sentence):
        return self._tokenizer.tokenize(sentence)

    def detokenize(self, tokens):
        '''Unescape Moses punctuation tokens.

        Replaces escape sequences like &#91; with the original characters
        (such as '['), so they better align to the original text.
        '''
        detokenizer = MosesDetokenizer()
        return [detokenizer.unescape_xml(t) for t in tokens]