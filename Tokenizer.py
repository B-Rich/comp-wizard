# Tokenizer
# Taken from Homework 1
# Used to do tf-idf


import PorterStemmer


    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
def tokenize(text):
       import re
       clean_string = re.sub('[^a-z0-9]', ' ', text.lower())
       tokens = clean_string.split()
       return tokens






def stemming(tokens):
       p = PorterStemmer.PorterStemmer()
       stemmed_tokens = []
       for t in tokens:
           stemmed_token = p.stem(t, 0,len(t)-1)
           stemmed_tokens.append(stemmed_token)
       return stemmed_tokens       
   



# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
   import sys
   main(sys.argv)
