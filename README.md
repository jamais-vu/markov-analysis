# markov-analysis
Generates random text in the style of a given corpus.

This code is my solution to Exercise 13.8 of [*Think Python*](https://greenteapress.com/wp/think-python-2e/) 
by Allen Downey, released under the [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/) license.

## Goals

### Exercise 13.8

> 1. Write a program to read a text from a file and perform Markov analysis. The 
>    result should be a dictionary that maps from prefixes to a collection of 
>    possible suffixes.
>   
> 2. Add a function to the previous program to generate random text based on the 
>    Markov analysis.
>
> 3. Once your program is working, you might want to try a mash-up: if you 
>    combine text from two or more books, the random text you generate will blend
>    the vocabulary and phrases from the sources in interesting ways.

### Further Exploration

My solution is likely not the most efficient, and since writing it I have become more familiar with Python.
I would like to develop intuitions for how to determine which algorithms or data structures suit which applications,
and how to efficiently implement these in Python.

Some options:

- Refactor my solution.

- Become familiar with [`timeit`](https://docs.python.org/3/library/timeit.html) 
  or [`cProfile`](https://docs.python.org/3/library/profile.html). Profile my
  code so I know which parts are slowing it down.
  
- Compare my original solution to my refactored solution, or to the 
  [solution provided by the author](http://thinkpython2.com/code/markov.py)
