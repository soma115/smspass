#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import crypt
import subprocess
import string


# DONE: odbieranie SMS'a
# DONE: generowanie hasła z pythona
# DONE: wysyłanie SMS'a:
# TODO: apache authentication
        # https://www.thomas-krenn.com/pl/wiki/Zabezpieczenie_has%C5%82em_zasob%C3%B3w_serwera_WWW

# TODO: przekierowanie strony z internetu

# TODO: wygasanie hasla
        # cron co godzine
        # chmod a+x foo.py
        # and use full path

# TODO: dodaj nowy numer tel z linii kommend, wyślij od razu hasło żeby user mógł przetestować logowanie.
        # Może od razu instrukcje do logowania na SMS.
        # update("alfa", "haslo123aaass")

# TODO: Usuń numer telefonu z linii kommend
        # delete("jan")

'''
Plan akcji:
1. odczytaj sms - done
2. skasuj sms - done
3. sprawdz numer - done
4. wyslij sms - done
5. Ekspiruj hasła

Dodatkowe funkcje:
1. Dodawania numeru telefonu nowego użytkownika
2. Usuwanie numeru telefonu
'''


# workdir = '/home/rfialek/Documents/py/2fa/'
# workdir = '/etc/smspass/'
workdir = '/opt/bin/smspass/'  # dostosowanie sciezki dynamicznie jest trudne. Dlatego na razie zostawiam na to sztywno.
hasla = "smspass.db"
path_to_gnokii = '/usr/local/bin/gnokii'    # centos 7
# path_to_gnokii = '/usr/bin/gnokii'        # fedora 25


def zczytaj():
    bash_command = path_to_gnokii + ' --getsms ME 0'
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        a = output.split('\n')
        tel = a[2].split()[1]
        tresc = a[4]
        bash_command1 = path_to_gnokii + ' --deletesms ME 0'
        process = subprocess.Popen(bash_command1.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        sprawdz_numer(tel, tresc)


def salt():
    """Returns a string of 2 randome letters"""
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789/.'
    return random.choice(letters) + random.choice(letters)


def load(filename):
    """Read the htpasswd file into memory."""
    # lines = open(os.getcwd()+'/'+hasla, 'r').readlines()
    lines = open(workdir + filename, 'r').readlines()
    linie = []
    for line in lines:
        username, pwhash = line.split(':')
        entry = [username, pwhash.rstrip()]
        linie.append(entry)
    return linie


def save(filename, entries):
    """Write the htpasswd file to disk"""
    open(filename, 'w').writelines(["%s:%s\n" % (entry[0], entry[1]) for entry in entries])


def update(username, password):
    """Replace the entry for the given user, or add it if new.
    usage:
        update(hasla, "felek", "haslo", load(hasla))"""
    pwhash = crypt.crypt(password, salt())
    matching_entries = [entry for entry in entries
                        if entry[0] == username]
    if matching_entries:
        matching_entries[0][1] = pwhash
    else:
        entries.append([username, pwhash])
    save(hasla, entries)


def delete(username):
    """Remove the entry for the given user."""
    entries = load(hasla)
    entries = [entry for entry in entries if entry[0] != username]
    save(hasla, entries)


def wyslij_haslo_jednorazowe(tel):
    nowe_haslo = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    update(tel, nowe_haslo)

    pierwszy = subprocess.Popen(('echo', nowe_haslo), stdout=subprocess.PIPE)
    try:
        drugi = subprocess.check_output((path_to_gnokii, '--sendsms', tel), stdin=pierwszy.stdout)
    except:
        pass
    pierwszy.wait()

    print('Haslo jednorazowe wyslane!')


def sprawdz_numer(tel, tresc):
    '''sprawdza czy haslo jest prawidlowe i czy numer telefonu jest na liscie osob uprawnionych'''

    if tresc.lower() == 'haslo' or tresc.lower() == 'hasło':
        plik = open(workdir + hasla, 'r')
        wpisy = plik.read()

        if wpisy.find(tel):
            print('Tego numeru telefonu nie ma na liscie osob uprawnionych')
            print(tel)
        else:
            wyslij_haslo_jednorazowe(tel)
    else:
        print('Nieprawidlowe haslo')


entries = load(hasla)

while True:
    zczytaj()
