'''
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
'''

import random
import string

'''
    idea:
    mapping of n-tuple (of n prefixes) to some collection that has suffixes with 
    their respective frequencies

    e.g. 

    (p_1, p_2, ..., p_n) -> ((s_1, f_1), (s_2, f_2), ..., (s_n, f_n))
    where the order of p matters
    ideally the f_i's would be normalized but iirc doing that to randomly pick a 
    float x between 0 and 1 might result in something not random, so i think i 
    will go with the cumulative sum solution from the preview problem
    another solution might be to just construct a list of each occurrence 

    simple idea:
    don't use word frequencies, just a set of suffixes
    so the dict is a mapping P -> S 
    (p_1, p_2, ..., p_n) -> (s_1, s_2, ..., s_n)

    after finishing:
    not sure why i ever thought of using a set of suffixes instead of a list,
    since that would even preserve relative frequencies!
'''

def mashup(prefix_length, text_length, *titles):
    '''
    Generates random text using two or more books as source material.

    TODO: process_file does not properly skip the Project Gutenberg header
          (see skip_gutenberg_header for more information)

    prefix_length: int, the number of prefix words to use
    text_length: int, the length of the random text
    titles: strings, titles of the source books
    '''
    word_list = []
    for title in titles:
        # WARNING: skip_header only works for emma.txt, Project Gutenberg books
        #          do NOT have a standard header format
        word_list = word_list + process_file(title, skip_header=False)
    prefixes = prefix_map(word_list, prefix_length)
    return list_to_string(random_text(prefixes, prefix_length, text_length))


def generate_text(prefix_length, text_length, title='emma.txt'):
    '''
    Generates random text using the specified number of prefixes.

    prefix_length: int, the number of prefix words to use
    text_length: int, the length of the random text
    title: string, title of the source book

    int, int -> str
    '''
    word_list = process_file(title, skip_header=True)
    prefixes = prefix_map(word_list, prefix_length)
    return list_to_string(random_text(prefixes, prefix_length, text_length))

def list_to_string(word_list):
    '''
    Converts a list of words to a string, with spaces between each word and a 
    period at the end.

    word_list: list

    list -> str
    '''
    s = ''
    for word in word_list:
        s = s + ('%s ' % word)
    return (s.strip() + '.')

def random_text(prefix_map, prefix_length, text_length):
    '''
    Returns a list of words randomly selected by prefix using the given 
    prefix map.

    # TODO: This looks messy, is there a better way than changing so many types?

    prefix_map: dict of tuples to lists
    prefix_length: int, the length (in words) of the sequence of prefixes to use
    m: int, the length (in words) of the list of random words

    dict, int, int -> list
    '''
    random_text = list(random.choice(list(prefix_map.keys())))

    while (len(random_text) < text_length):
        prefix = tuple(random_text[(len(random_text)-prefix_length):len(random_text)])
        random_text.append(random.choice(prefix_map[prefix]))

    return random_text

def prefix_map(word_list, n):
    '''
    Takes a list of words and returns a dict mapping sequences of n words (which
    we call the prefixes) to a list of all next words (which we call the 
    suffixes).

    word_list: list
    n: int, the number of prefixes to consider
    
    list, int -> dict
    '''
    ''' TODO: This doesn't do quite what I want but can't figure out why
        prefix_map = {(''):{word_list[0]}} # First word follows nothing
        if n > 1: # Map starting prefix sequences of length <n
            for i in range(1, n):
                prefix_seq = tuple(word_list[1:i])
                prefix_map[prefix_seq] = {word_list[i]}
    '''
    prefix_map = {}
    # Maps prefix n-tuples to suffix list
    for prefix_start in range(0, len(word_list)-n):
        prefix_seq = tuple(word_list[prefix_start:prefix_start+n]) 
        suffix = word_list[prefix_start+n]
        prefix_map[prefix_seq] = prefix_map.get(prefix_seq, []) + [suffix]
    
    return prefix_map

# WARNING: skip_header=True only known to work with emma.txt
def process_file(filename, skip_header):
    """
    (Taken from chapter 13 of ThinkPython, modified to return list)
    Makes a list that contains the words from a file.

    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
   
    returns: list of all words in the file in order of appearance
    """
    word_list = []
    fp = open(filename)

    if skip_header:
        skip_gutenberg_header(fp)

    for line in fp:
        process_line(line, word_list)

    return word_list

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

    fp: open file object
    """
    for line in fp:
        if line.startswith('*END*THE SMALL PRINT!'):
            break

def process_line(line, word_list):
    """
    (Taken from chapter 13 of ThinkPython)
    Adds the words in the line to the word list.
    I removed string.punctuation from strippables for the purpose of the Markov
    analysis.

    Modifies word_list

    line: string
    word_list: list of words
    """
    line = line.replace('-', ' ') # replace hyphens with spaces before splitting
    strippables = string.whitespace

    for word in line.split():
        # remove punctuation and convert to lowercase
        word = word.strip(strippables)
        word = word.lower()

        # update the histogram
        word_list.append(word)
    
