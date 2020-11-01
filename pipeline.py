from sklearn.feature_extraction.text import CountVectorizer
import pickle
import re


class NLPPipe:
    def __init__(
        self,
        vectorizer=CountVectorizer(),
        tokenizer=None,
        cleaning_function=None,
        stemmer=None,
        model=None,
    ):
        """
        A class for pipelining our data in NLP problems.
        The user provides a series of tools, and this class
        manages all of the training, transforming, and modification
        of the text data.
        ---
        Inputs:
        vectorizer: the model to use for vectorization of text data
        tokenizer: The tokenizer to use, if none defaults to split on spaces
        cleaning_function: how to clean the data,
            if None, defaults to the in built class
        """
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False

    def splitter(self, text):
        """
        Default tokenizer that splits on spaces naively
        """
        return text.split(" ")

    def clean_text(self, text, tokenizer, stemmer):
        """
        A naive function to lowercase all works can clean them quickly.
        This is the default behavior if no other cleaning function is specified
        """
        cleaned_text = []
        for post in text:
            cleaned_words = []
            for word in tokenizer(post):
                low_word = word.lower()
                if stemmer:
                    low_word = stemmer.stem(low_word)
                cleaned_words.append(low_word)
            cleaned_text.append(" ".join(cleaned_words))
        return cleaned_text

    def fit(self, text):
        """
        Cleans the data and then fits the vectorizer with
        the user provided text
        """
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        self.vectorizer.fit(clean_text)
        self._is_fit = True

    def transform(self, text):
        """
        Cleans any provided data and then transforms the data into
        a vectorized format based on the fit function. Returns the
        vectorized form of the data.
        """
        if not self._is_fit:
            raise ValueError("Must fit the models before transforming!")
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        return self.vectorizer.transform(clean_text)

    def save_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        pickle.dump(self.__dict__, open(filename + ".mdl", "wb"))

    def load_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        if filename[-4:] != ".mdl":
            filename += ".mdl"
        self.__dict__ = pickle.load(open(filename, "rb"))


def hasNumbers(inputString):
    """
    Tests if a string has numbers in it.

    Args:
        inputString: a string

    Returns:
        A boolean. True if it has numbers, False otherwise.
    """
    return any(char.isdigit() for char in inputString)


def tweet_clean1(text, tokenizer, stemmer):
    """
    Build upon the naive function in the NLPPipe class to
    also remove tokens containing numbers.
    """
    cleaned_text = []
    for post in text:
        cleaned_words = []
        for word in tokenizer(post):
            low_word = word.lower()
            low_word = re.sub(r"[^\w\s]", "", low_word)
            low_word = re.sub(r"_", "", low_word)
            if stemmer:
                low_word = stemmer.stem(low_word)
            if not hasNumbers(low_word):
                cleaned_words.append(low_word)
        cleaned_text.append(" ".join(cleaned_words))
    return cleaned_text
