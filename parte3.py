"""
Laboratorio 4
Cifrado de información
#Maria Jose Castro 181202
#Diana de Leon 18607
#Camila Gonzalez 18398
#Maria Ines Vasquez 18250
"""

#Parte Diffie-Helman
#Codigo extraido de: https://sublimerobots.com/2015/01/simple-diffie-hellman-example-python/
import random

#Aqui se colcan los numeros primos
#Este numero es de conocimiento de Alice y Bob
num_compartido = 71
#Numero usado en el modulo 
generador = 69

#Se utiliza un generador para seleccionar los numeros al azar entre 0 y 20
priv_alice = random.randint(0,20)
priv_bob = random.randint(0,20)
 
# Aqui imprimimos la informacion que es publica y 
#compartida por ambos
print( "Variables Compartidas Publicas:")
print( "    Llave primaria: " , num_compartido )
print( "    Llave base:  " , generador )
 
# Alice calcula lo siguiente y lo envia a Bob 
# en un canal inseguro
# A = g^a mod p

A = (generador**priv_alice) % num_compartido
print( "\n  Alice envia a Bob : " , A )
 
# Bob calcula lo siguiente y se lo envia a alice 
# en un canal inseguro
# B = g^b mod p
B = (generador ** priv_bob) % num_compartido
print( " Bob envia a Alice: ", B )
 
print( "\n------------\n" )
print( "Privately Calculated Shared Secret:" )
# Alice utiliza B para poder obtener el numero
# secreto compartido con Bob
#  s = B^a mod p
alice_ss = (B ** priv_alice) % num_compartido
print( "    La llave secreta y compartida que calculo Alice: ", alice_ss )
 
# Bob utiliza A para poder obtener el numero
# secreto compartido con Alice
# s = A^b mod p
bob_ss = (A**priv_bob) % num_compartido
print( "    La llave secreta y compartida que calculo Bob: ", bob_ss )