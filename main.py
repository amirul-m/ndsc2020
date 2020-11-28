import pandas as pd
import numpy as np
import string
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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

    limit = 40

    data_i1 = [i for i in bs['stmt_id']]
    data_0 = [i for i in desc]
    data_1 = [i for i in bs['stmt_amount']]
    data_2 = ['' for i in range(len(desc))]
    data_3 = ['' for i in range(len(desc))]
    data_4 = ['' for i in range(len(desc))]
    data_5 = ['' for i in range(len(desc))]

    matched_count = 0
    no_matched_count = 0
    for i2, v2 in enumerate(c['buyer_name'][:1000]):
        print(i2, v2)
        matching = [i for i, s in enumerate(bs['desc']) if v2.lower() in s.lower()]
        if matching:
            for i, v in enumerate(matching):
                # print(desc_filtered[v], bs['stmt_amount'][v], v2.lower(), c['ckt_amount'][v])
                if c['ckt_amount'][i2] == bs['stmt_amount'][v]:
                    data_2[v] = v2
                    data_3[v] = c['ckt_amount'][i2]
                    data_4[v] = logic_selection[0]
                    data_5[v] = i2
                    print('matched')
                    matched_count += 1
                elif i == len(matching) - 1:
                    print('not match')
                    no_matched_count += 1
        else:
            print('not match')
            no_matched_count += 1

    df = pd.DataFrame({'stmt_id': data_i1,
                       # 'stmt_amount': data_1,
                       # 'description': data_0,
                       'ckt_id': data_5,
                       # 'ckt_amount': data_3,
                       # 'buyer_name': data_2,
                       # 'Name match logic': data_4
                       })
    df.to_csv('res4.csv', index=False)

    print(matched_count, no_matched_count)


def compare_fuzzy(desc,buyer_name):
    return fuzz.partial_ratio(desc,buyer_name)


def rank3_ndsc(name):
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    bank = pd.read_csv('dataset/bank_statement.csv')
    checkout = pd.read_csv('dataset/checkout.csv')

    def find_match(stmt_amount, desc):
        potential_match = checkout[checkout['ckt_amount'] == stmt_amount]
        result = []
        for ckt_id, buyer_name in zip(potential_match['ckt_id'], potential_match['buyer_name']):
            score = compare_fuzzy(desc, buyer_name)
            if score > 0:
                result.append((ckt_id, score))
        return result

    def get_max(list_of_tuple):
        max_score = 0
        final_id = -1
        for stmt_id, score in list_of_tuple:
            if score > max_score:
                max_score = score
                final_id = stmt_id
        return final_id

    final_result = []
    for stmt_id, stmt_amount, desc in zip(bank['stmt_id'], bank['stmt_amount'], bank['desc']):
        print(stmt_id)
        ckt_id = get_max(find_match(stmt_amount, desc))
        final_result.append((stmt_id, ckt_id))

    stmt_id = [a for a, b in final_result]
    ckt_id = [b for a, b in final_result]
    df = pd.DataFrame({'stmt_id': stmt_id, 'ckt_id': ckt_id})

    df.to_csv('final_fuzzy.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # load_dataset('PyCharm')
    rank3_ndsc('Rank 3')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
