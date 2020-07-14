def encrypt(val,key):
    output = []
    for x in val:
        output.append(key[x])
    return ''.join(output)

def decrypt(val,key):
    output = []
    for x in val:
        output.append({k for k,v in key.items() if v == x}.pop())
    return ''.join(output)

def create_cipher():
    import random,string
    bag = list(string.ascii_letters)
    for n in range(10): bag.append(str(n))
    mpd = bag.copy()
    cipher = {}
    for x in bag:
        c = random.choice(mpd);mpd.remove(c)
        cipher[x] = str(c)
    return cipher