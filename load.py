def load_accounts(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

    phrases = {}
    for line in lines:
        search, phrase = line.split(';')
        phrases[search] = phrase.strip()

    return(phrases)
