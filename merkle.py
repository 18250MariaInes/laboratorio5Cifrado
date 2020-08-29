"""
Laboratorio 5
Cifrado de información
#Maria Jose Castro 181202
#Diana de Leon 18607
#Camila Gonzalez 18398
#Maria Ines Vasquez 18250

"""
#Extraído de: https://medium.com/100-days-of-algorithms/day-75-merkles-puzzles-d9f0e8f9c9d0
from os import urandom
from hashlib import sha1
from random import shuffle, choice

puzzle_size = 2 ** 16

#función en la cual Alice genera N secretos, con N indices y cada par lo inserta en un rompecabezas
#el cual solo Bob puede resolver, esto se logra en un tiempo O(n), y este es mandado a Bob
def merkles_puzzle():
    print("ALICE HACE LOS ROMPECABEZAS:")
    #se inicializa las listas para los N secretos y para los rompecabezas que serán enviados a Bob
    secrets = [None] * puzzle_size
    puzzles = [None] * puzzle_size

    print("Se calculan los secreto de Alice")
    print("Los rompecabezas son computados por Alice")
    for i in range(puzzle_size):
        # se genera secreto
        secrets[i] = urandom(16)


        # se genera el par de [secret, index] con el cual Bob resolverá el rompecabezas
        pair = secrets[i] + int.to_bytes(i, 4, 'big')
        # variable donde se guarda la pareja de secreto|index concatenado con el hash producido de él
        plaintext = pair + sha1(pair).digest()

        # operaciones para encriptar el mensaje con la llave definida de forma aleatorio
        key = urandom(10) #se inicializa la llave
        noise = sha1(key).digest()#se le hace un hash a la llave
        noise += sha1(noise).digest()#se concatena con otro hash para alargar la variable
        ciphertext = bytes(i ^ j for i, j in zip(plaintext, noise)) #se encripta el mensaje

        # los rompecabezas se settean con el mensaje ya encriptado y la llave concatenada
        #ignorando sus dos primeros valores de la llave
        
        puzzles[i] = ciphertext + key[2:]

    # se randomiza el orden de los rompecabezas
    shuffle(puzzles)

    #retorna el secrets y los rompezabezas computados
    return secrets, puzzles

#Función en la cual Bob escoge de forma aleatorio un rompecabzas de los que le mandó ALice y por medio
#de una pareja [secret, index] lo puede resolver solo él, de esta forma Bob y Alice tienen un secreto en común
def solve_puzzle(puzzle):
    print("Operación con Bob con los rompecabezas de Alice")
    #se inicializan el mensaje a decifrar y la llave para hacerlo en base al rompecabezas random que Bob haya seleccionado
    ciphertext = puzzle[:40] #el mensaje cifrado se encuentra desde el inicio a la posición 40 del rompecabezas
    key = puzzle[40:]#La llave se encuentra desde la posición 40 al final del rompecabezas

    #recorre todo el rompecabeza
    print("Bob calcula la llave en base al rompecabezas enviado de Alice")
    for i in range(puzzle_size):
        # obtiene la llave para decifrar el mensaje
        noise = sha1(int.to_bytes(i, 2, 'big') + key).digest()
        noise += sha1(noise).digest()

        # desencripta el mensaje cifrado con la llave obtenida en el paso anterior
        plaintext = bytes(i ^ j for i, j in zip(ciphertext, noise))

        pair = plaintext[:20] #la llave y el index del rompecabezas
        digest = plaintext[20:] #la pareja de [secret|index] hasheada

        # si el hash de la llave encontrada con el index es igual al hash de la llave y el index que provienen de Alice
        if sha1(pair).digest() == digest:
            print("----------El mensaje de Alice ha sido encontrado por Bob por medio de los rompecabezas---------")
            return i, pair[:16], int.from_bytes(pair[16:], 'big')

            #significa que si hubo una comunicación exitosa entre Alice y Bob



alice_secrets, public_puzzles = merkles_puzzle()

bob_time, bob_secret, public_index = solve_puzzle(choice(public_puzzles))

print('Bob obtiene secreto e index de Alice')
print('Llave calculada:', bob_secret)
print('Index:', public_index)
print('Tiempo ejecutado:', bob_time)

print('Alice tiene un secreto')
print('Llave original:', alice_secrets[public_index])
print("Como se puede ver, Bob obtiene la llave de Alice en base a los rompezabezas computados")
print("OPERACIÓN EXITOSA")