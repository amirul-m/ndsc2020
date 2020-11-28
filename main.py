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
    desc_filtered = []
    for x in split_x:
        line_filtered = []
        for y in x:
            # lower and strip
            word = y.lower().strip()
            # remove punctuation
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word:
                if 'transfer' not in word and 'shopee' not in word and 'tf' not in word and 'instant' not in word and 'to' not in word:
                    count_word += 1
                    line_filtered.append(word)
        desc_filtered.append(' '.join(line_filtered))

    logic_selection = [
        "Statement description “contains” buyer's name.",
        "Statement description does not have to contain every word in buyer’s name.",
        "Order of the words in names does not matter.",
        "The spelling of the words in names are not exactly the same, but very similar."
    ]

    data_0 = [i for i in desc]
    data_1 = [i for i in bs['stmt_amount']]
    data_2 = []
    data_3 = []
    data_4 = []

    for i, v in enumerate(desc_filtered):
        for i2, v2 in enumerate(c['buyer_name']):
            if i2 < 24000:
                if v2.lower() in v and c['ckt_amount'][i] == bs['stmt_amount'][i]:
                    data_2.append(c['buyer_name'][i])
                    data_3.append(c['ckt_amount'][i])
                    data_4.append(logic_selection[0])
            else:
                data_2.append('')
                data_3.append('')

    df = pd.DataFrame({'Statement description': data_0,
                       'Statement amount': data_1,
                       'Buyer name': data_2,
                       'Checkout amount': data_3,
                       'Name match logic': data_4
                       })
    df.to_csv('res.csv', index=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dataset('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
