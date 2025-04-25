from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk
import re

# Ensure NLTK tokenizers are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def preprocess_text(text):
    # Clean text before summarization
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'\[.*?\]', '', text)  # Remove [footnotes]
    return text.strip()

def generate_summary(text, algorithm="lexrank", sentences_count=3):
    """
    Generate a summary using Sumy.
    Args:
        text (str): Input text to summarize
        algorithm (str): 'lexrank' (default), 'lsa', or 'luhn'
        sentences_count (int): Number of sentences in summary
    Returns:
        str: Generated summary or error message
    """
    try:
        if not text or len(text.split()) < 10:
            return "Text too short to summarize"
        
        text = preprocess_text(text)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        if algorithm.lower() == "lsa":
            summarizer = LsaSummarizer()
        elif algorithm.lower() == "luhn":
            summarizer = LuhnSummarizer()
        else:
            summarizer = LexRankSummarizer()
        
        summary = summarizer(parser.document, sentences_count)
        return " ".join(str(sentence) for sentence in summary)
    
    except Exception as e:
        return f"Summarization failed: {str(e)}"