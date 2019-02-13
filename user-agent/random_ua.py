import json


with open('ualist.json') as f:
    ua_dict = json.load(f)

# clist = ua_dict['chrome']
# olist = ua_dict['opera']
# flist = ua_dict['firefox']
# ilist = ua_dict['ie']
# slist = ua_dict['safari']


def get_random_ua():
    from random import choice
    return choice(ua_dict.get(choice(
        ['chrome', 'opera', 'firefox', 'ie', 'safari'])))


if __name__ == '__main__':
    print(get_random_ua())
