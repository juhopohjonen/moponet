from random import randint

# Some words to say when you are very angry.
# Used by swear()

SWEAR_WORDS = [
    'Voi vittu!',
    'Saatanan saatana!',
    'Vittujen saatana!',
    'Vittujen kevät!',
    'Helvetin helvetti!',
    'Saatanoiden helvetti!',
    'Helveteiden saatana!'
]

def getPaskaMopo():
    
    # return one of these as 'shitty moped' when calling this func :D

    mopot= ["Därpi", "Äpriliä", "Hando", "Paegout", "Pösö", "Raeju"]
    i = randint(0, len(mopot) - 1)
    return mopot[i]

def swear():
    i = randint(0, len(SWEAR_WORDS) - 1)
    return SWEAR_WORDS[i]
    