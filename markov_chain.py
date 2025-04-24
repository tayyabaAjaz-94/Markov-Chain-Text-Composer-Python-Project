import random
from collections import defaultdict

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.model = defaultdict(list)

    def train(self, text):
        """Train the Markov Chain with the provided text."""
        words = text.split()
        for i in range(len(words) - self.order):
            current_tuple = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.model[current_tuple].append(next_word)

    def generate(self, length=50):
        """Generate a sequence of words based on the trained Markov model."""
        if not self.model:
            return "Model is empty. Please train with valid text data."

        # Start with a random key
        current_tuple = random.choice(list(self.model.keys()))
        generated_words = list(current_tuple)

        for _ in range(length):
            next_word = random.choice(self.model[current_tuple])
            generated_words.append(next_word)
            current_tuple = tuple(generated_words[-self.order:])

        return ' '.join(generated_words)
