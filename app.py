from flask import Flask, render_template, url_for, request

# NLP Packages
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
from gensim.summarization import summarize

# Extra Packages
import spacy 
import time
nlp = spacy.load('en_core_web_sm')

# Web Scrapping Packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Summarization Packages 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer 

# Sumy 
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer('english'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence)for sentence in summary]
    result = ' '.join(summary_list)
    return result

app = Flask(__name__)

# Home Route 
@app.route('/')
def index():
    return render_template('index.html')
# Compare Route
@app.route('/compare_summary')
def compare_summary():
    return render_template('compare_summary.html')

@app.route('/comparer', methods=['GET', 'POST'])
def comparer():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary_spacy)
        # Gensim Summarizer
        final_summary_gensim = summarize(rawtext)
        summary_reading_time_gensim = readingTime(final_summary_gensim)
        # NLTK
        final_summary_nltk = nltk_summarizer(rawtext)
        summary_reading_time_nltk = readingTime(final_summary_nltk)
        # Sumy
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)
        end = time.time()
        final_time = end-start
    return render_template('compare_summary.html', ctext=rawtext, final_time=final_time, final_summary_spacy=final_summary_spacy, summary_reading_time=summary_reading_time, summary_reading_time_gensim=summary_reading_time_gensim, final_summary_gensim=final_summary_gensim, summary_reading_time_nltk=summary_reading_time_nltk, final_summary_nltk=final_summary_nltk,final_summary_sumy=final_summary_sumy, summary_reading_time_sumy=summary_reading_time_sumy)

# Grab ReadingTime Function
def readingTime(mytext):
    total_words = len([ token.text for token in nlp(mytext)]) # grab length of token 
    estimated_time = total_words/200.0
    return estimated_time

# Fetch Data From Url's
def get_text(url):
    page = urlopen(url)
    # uses beautiful soup
    soup = BeautifulSoup(page, 'html.parser') # "html.parser", features='xml'
    new = soup.find_all('p')[0].get_text()
    return str(new)
    # fetched_text = ' '.join(map(lambda p:p.text.soup.find_all('p')))
    # return fetched_text


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext'] # stores everything into rawtext
        final_readingtime = readingTime(rawtext)
        # Summarization
        final_summary = text_summarizer(rawtext) #pass rawtext into text summarizer function
        # Get ReadingTime   
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end - start 
    return render_template('index.html', ctext=rawtext,final_summary=final_summary, final_time=final_time,final_reading_time=final_readingtime, summary_reading_time=summary_reading_time)

@app.route('/analyze_url', methods=['GET', 'POST'])
def analyze_url():
    start = time.time()
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url) # stores everything into rawtext
        final_readingtime = readingTime(rawtext)
        # Summarization
        final_summary = text_summarizer(rawtext) #pass rawtext into text summarizer function
        # Get ReadingTime   
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end - start 
    return render_template('index.html', final_summary=final_summary, final_time=final_time,final_reading_time=final_readingtime, summary_reading_time=summary_reading_time)

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)