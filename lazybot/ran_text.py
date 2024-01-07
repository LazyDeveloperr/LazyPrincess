# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...

import random
import string

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

ran = (random_char(5))
