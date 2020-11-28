import pandas as pd
import numpy as np
import string
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def load_dataset(name):
    # Use a breakpoint in the code line below to debug your script.
    bs = pd.read_csv('dataset/bank_statement.csv')
    c = pd.read_csv('dataset/checkout.csv')
    bs_len = len(bs)
    c_len = len(c)

    desc = bs['desc']
    split_x = [i.split('*') for i in desc]

    # count distinct word
    count_word = 0
    for x in split_x:
        for y in x:
            # lower and strip
            word = y.lower().strip()
            # remove punctuation
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word:
                if 'transfer' not in word and 'shopee' not in word and 'tf' not in word:
                    count_word += 1

    print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dataset('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
