import time
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import requests

# Decorator to measure the execution time of functions
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} executed in {duration:.4f} seconds")
        return result
    return wrapper

# URL to fetch Shakespeare's text
url = "https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"
response = requests.get(url)
text = response.text

# Function to count words using a dictionary
@timer_decorator
def count_words_with_dict(text):
    word_count = {}
    for word in text.split():
        word = word.lower().strip('.,!?:;-"\'')
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

# Function to count words using a Counter
@timer_decorator
def count_words_with_counter(text):
    words = [word.lower().strip('.,!?:;-"\'') for word in text.split()]
    return Counter(words)

# Lists to store execution times
times_dict = []
times_counter = []

# Measure the execution time of each method and collect data
for _ in range(100):
    start_time = time.time()
    count_words_with_dict(text)
    end_time = time.time()
    times_dict.append(end_time - start_time)

    start_time = time.time()
    count_words_with_counter(text)
    end_time = time.time()
    times_counter.append(end_time - start_time)

# Create a histogram to visualize the distribution of execution times
plt.hist(times_dict, alpha=0.5, label='Dictionary Method')
plt.hist(times_counter, alpha=0.5, label='Counter Method')
plt.vlines(np.mean(times_counter), 0, 100, colors='b', linestyles='solid', label='')
plt.vlines(np.mean(times_dict), 0, 100, colors='b', linestyles='solid', label='')
plt.legend(loc='upper right')
plt.title('Execution Times Distributions')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency')
plt.show()
