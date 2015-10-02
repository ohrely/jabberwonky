import sys
import os
import twitter
from random import choice


class MarkovMachine(object):

    def read_files(self, filenames):
        """Given a list of files, make chains from them."""

        body = ""

        for filename in filenames:
            text_file = open(filename)
            body = body + text_file.read()
            text_file.close()

        self.make_chains(body)

    def make_chains(self, corpus):
        """Takes input text as string; returns dictionary of markov chains."""

        self.chains = {}

        words = corpus.split()

        for i in range(len(words) - 2):
            key = (words[i], words[i + 1])
            value = words[i + 2]

            if key not in self.chains:
                self.chains[key] = []

            self.chains[key].append(value)

    def make_text(self):
        """Takes dictionary of markov chains; returns random text."""

        key = choice(self.chains.keys())
        words = [key[0], key[1]]

        while key in self.chains:
            # Keep looping until we have a key that isn't in the chains
            # (which would mean it was the end of our original text)
            #
            # Note that for long texts (like a full book), this might mean
            # it would run for a very long time.

            word = choice(self.chains[key])
            words.append(word)
            key = (key[1], word)

        text = " ".join(words)

        # This is the clumsiest way to make sure it's never longer than
        # 140 characters; can you think of better ways?
        return text[:140]


# if __name__ == "__main__":
filenames = sys.argv[1:]

generator = MarkovMachine()
generator.read_files(filenames)
print generator.make_text()



# Begin work with Twitter API via python-twitter

api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# print api.VerifyCredentials()

status = api.PostUpdate(generator.make_text())
# print status.text