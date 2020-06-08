#!/usr/bin/python3

from argon2 import PasswordHasher
import itertools

words_list = ["Allo","Bruine","Crachin","Dour","Etudiant","Fransez","Gwrizienn","Hacktheplanet","Iliz", \
        "Jablus","Kerez","Lukachenn","Mabig","Nebeut","Oskeg","Postel","Quidditch","Roazhon","Sivi", \
        "Tabut","Ubuntu","Vaksin","Warantugin","Xkcd","Yaek","Zedig"]

permutations = itertools.permutations(words_list, 3)
passwords_list = []
for p in permutations:
    passwords_list.append("".join(pp for pp in p))
ph = PasswordHasher()

#meteo "AlloBruineCrachin"
#h = "$argon2id$v=19$m=102400,t=2,p=8$epXJYKkYSEXDBkRAuKCSig$Bc8YbOHmrOeDiBygKFzkMw"

#chat
s = len(passwords_list)

counter = 1
h = "$argon2id$v=19$m=102400,t=2,p=8$ShgCOIbvVzVKtPEKEQge3g$zZwnq4W8H4LqtwiCSAULQQ"
for password in passwords_list:
    try:
        print(ph.verify(h, password))
        print("WIN !\n")
        print("password: " + password)
        break
    except:
        if (counter % 100) == 0:
            print(str(counter)+str("/")+str(s))
        pass
    counter += 1
