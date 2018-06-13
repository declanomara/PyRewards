def load_accounts(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

    phrases = {}
    for line in lines:
        if len(line) > 0 and line[0] != '#':
            search, phrase = line.split(';')
            phrases[search] = phrase.strip()

    return(phrases)

def load_names(filename):
    first_names = []
    last_names = []
    lines = []

    with open(filename) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

    for line in lines:
        if len(line) > 0 and line[0] != '#':
            first, last = line.split(' ')
            first_names.append(first)
            last_names.append(last)
    return (first_names, last_names)

def load_list(filename):
    words = []
    lines = []

    with open(filename) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

    for line in lines:
        if len(line) > 0 and line[0] != '#':
            words.append(line)

    return(words)
