# -*- coding: utf-8 -*-

import random
import string
import subprocess

#
# str = '123sdalkfjljfw3294879842kjahfdsf'
# ciag = '12a'
# #print(bool(str.find(ciag)))
#
# if ciag in str:
#     print('tak')
#
#
# tel = '+48791366206'
# nowe_haslo = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
#
# bash_command = 'echo ' + nowe_haslo + ' | gnokii --sendsms ' + tel
# print('raw: ' + bash_command)
#
# # shell=True poprawić: http://stackoverflow.com/questions/13332268/python-subprocess-command-with-pipe
# # process = subprocess.Popen(('echo', nowe_haslo, '| gnokii --sendsms', tel), stdout=subprocess.PIPE)
#
# pierwszy = subprocess.Popen(('echo', nowe_haslo), stdout=subprocess.PIPE)
# drugi = subprocess.check_output(('gnokii', '--sendsms', tel), stdin=pierwszy.stdout)
# pierwszy.wait()
#
#
# output, error = pierwszy.communicate()
# print('o:', output)
# print('e:', error)


a = [4, 2, 3, 8, -8]
b = [4, 2, 5]


def answer(x, y):
    z = list(set(x).difference(set(y)))

    return z


n = answer(a, b)
print(n)
