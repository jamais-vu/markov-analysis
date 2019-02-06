"""
 Exercise 13.8. Markov analysis:

 1. Write a program to read a text from a file and perform Markov analysis. The 
    result should be a dictionary that maps from prefixes to a collection of 
    possible suffixes. The collection might be a list, tuple, or dictionary; it 
    is up to you to make an appropriate choice. You can test your program with 
    prefix length two, but you should write the program in a way that makes it 
    easy to try other lengths.

 2. Add a function to the previous program to generate random text based on the 
   Markov analysis. Here is an example from Emma with prefix length 2:
    He was very clever, be it sweetness or be angry, ashamed or only amused, at 
    such a stroke. She had never thought of Hannah till you were never meant for
    me?" "I cannot make speeches, Emma:" he soon cut it all himself.

    For this example, I left the punctuation attached to the words. The result 
    is almost syntactically correct, but not quite. Semantically, it almost 
    makes sense, but not quite.
    What happens if you increase the prefix length? Does the random text make 
    more sense?

 3. Once your program is working, you might want to try a mash-up: if you 
    combine text from two or more books, the random text you generate will blend
    the vocabulary and phrases from the sources in interesting ways.

 Credit: This case study is based on an example from Kernighan and Pike, The 
 Practice of Programming, Addison-Wesley, 1999.

 You should attempt this exercise before you go on; then you can can download my
 solution from http://thinkpython2.com/code/markov.py. You will also need http:
 //thinkpython2.com/code/emma.txt.
"""

import random
import funcy
import collections
import string

def mashup(n, text_length, use_words, *files):
    """Generates a string of random words in the style of some given text files.

    Generates a string of random text of text_length words from user-specified 
    text files. Words are generated one by one, and each subsequent word is 
    randomly chosen from a probability distribution of which words in the source
    texts tend to follow the previous n words (referred to as an n-gram).

    Parameters:
        n : int
            The n-gram length (i.e., the number of preceding words to consider).
        text_length : int
            The number of words of random text to generate.
        use_words : bool
            Whether to use words or characters as the basic unit of the n-grams.
            True will use words, False will use characters. 
        files: str
            The filename(s) of the source text(s).
    
    Returns:
        str
            The generated random text.
    """
    word_list = []
    for file in files:
        # WARNING: skip_header only works for emma.txt, Project Gutenberg books
        #          do NOT have a standard header format
        word_list = word_list + file_to_list(file, skip_header=False)
    ngrams = make_ngram_map(word_list, n)
    return generate_random_string(ngrams, n, text_length)

def generate_random_string(ngram_map, n, text_length):
    """Creates a string of words randomly chosen based on their preceding n-gram.

    Parameters
        ngram_map : dict[tuple[str], Counter[str]]
            A dict of n-gram tuples to suffix Counters.
        n : int
            The length of the n-grams to consider.
        text_length : int
            The length (in words) of the list of random words

    dict, int, int -> list
    """
    # Initialize text of length n with a random n-gram
    random_text = list(random.choice(list(ngram_map.keys()))) 

    while len(random_text) < text_length:
        ngram = tuple(random_text[-n:]) # n-gram is last n items
        suffix_counter = ngram_map[ngram] # Counter of suffix frequencies
        # get zeroth item since random.choices() returns list even k=1 choices
        random_suffix = random.choices(population=list(suffix_counter.keys()), 
                                       weights=list(suffix_counter.values()))[0]
        random_text.append(random_suffix)

    random_text = ' '.join(random_text) + '.' # Space between words, period end.
    return random_text

def make_ngram_map(word_list, n):
    """Creates a dict of n-gram tuples to suffix counters.

    The word_list is broken into partitions of length n+1. The first n words are
    the n-gram, and the last word is the suffix. 

    Parameters:
        word_list : list[str]
            The list of words from which to get n-grams.
        n: int
            Length of the n-grams (number of words).
    
    Returns:
        dict[tuple[str], Counter[str]]
            A mapping of n-gram tuples to a collection of subsequent words.  
    """
    ngram_map = {}
    
    for part in funcy.partition(n + 1, 1, word_list):
        ngram = tuple(part[0:-1])
        suffix = part[-1]
        suffix_map = (ngram_map.get(ngram, collections.Counter()))
        suffix_map[suffix] += 1 # TODO: Don't like the mutation here
        ngram_map[ngram] = suffix_map

    return ngram_map

def file_to_string(filename):
    """Returns the given text file as a string, with no newlines.

    Parameters:
        filename : str
            The name of the text file to get words from.
    
    Returns:
        str
            A string of the text file.
    """
    filestring = ''

    fp = open(filename)

    for line in fp:
        filestring = filestring + line

    return filestring

# WARNING: skip_header=True only known to work with emma.txt
def file_to_list(filename, use_words=True,  strip_line=True, skip_header=False):
    """Creates a list of all words or characters in a file, in the same order.
    
    Parameters:
        filename : str
            The name of the text file to get words from.
        use_words : bool
            Whether to break the file up by word. If False, the file is broken 
            up by character instead (default: True).
        strip_line :
            Whether to strip certain punctuation from the line before 
            processing (default: True). Currently the only change by setting
            this to False is that hyphen ("-") is not replaced by space (" "). 
        skip_header : bool
            Whether to skip the Gutenberg header (default: False).
   
    Returns: 
        list[str]
            A list of all words in the file in order of appearance.
    """
    word_list = []
    fp = open(filename) 
    # TODO: Should i be using the with keyword instead? Do i need fp.close()?
    # https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

    if skip_header:
        skip_gutenberg_header(fp)

    for line in fp:
        word_list = word_list + line_to_list(line, use_words, strip_line)

    return word_list

def line_to_list(line, use_words=True, strip_line=True):
    """Converts a line in a text file to a list of words, using str.split(). 

    Taken from chapter 13 of ThinkPython.
    I removed string.punctuation from strippables for the purpose of the Markov
    analysis.

    Parameters:
        line : str
            A string representing a line from a text file.
        use_words : bool
            Whether to break the line up by word. If False, the line is broken 
            up by character instead (default: True).
        strip_line :
            Whether to strip certain punctuation from the line before 
            processing (default: True). Currently the only change by setting
            this to False is that hyphen ('-') is not replaced by space (' '). 

    Returns:
        list[str]
            A list of words.
    """
    strippables = string.whitespace
    line_list = []
    
    if strip_line:
        line = line.replace('-', ' ')
        strippables = string.whitespace # TODO: Can put more punctuation options

    if use_words:
        for word in line.split():
            word = word.strip(strippables) # Remove punctuation
            word = word.lower()
            line_list = line_list + [word]
    else:
        line_list = list(line)

    return line_list

# WARNING: This is only known to work with emma since Project Gutenberg books
#          do NOT have a standard header format.
def skip_gutenberg_header(fp):
    """
    (Taken from chapter 13 of ThinkPython)
    Reads from fp until it finds the line that ends the header.

    TODO: Project Gutenberg books do not have a standard header. Figure out how 
          to skip the header in general.
    TODO: Some Project Gutenberg books have additional material after the book.
          Figure out how to skip that.

    Parameters:
        fp : _io.TextIOWrapper
            The text stream of the file we are reading.
    """
    for line in fp:
        if line.startswith("*END*THE SMALL PRINT!"):
            break
