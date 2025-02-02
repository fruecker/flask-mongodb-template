import random

def draw_random(sequence, count):
    return random.sample(sequence, min(count, len(sequence)))