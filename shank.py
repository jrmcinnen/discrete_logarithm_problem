import numpy as np
import math
import time

PRIMES = [331777, 16785407, 54018521, 214748357, 342999977, 788748341, 2147483647,
          6547483043, 16148168401, 80630964769, 1171432692373]

GENERATORS = [5, 5, 6, 2, 3, 2, 7,
              2, 22, 17, 2]

X = [math.floor(331777/2), math.floor(16785407/2), math.floor(54018521/2), math.floor(214748357/2),
     math.floor(342999977/2), math.floor(788748341/2), math.floor(2147483647/2),
     math.floor(6547483043/2), math.floor(16148168401/2), math.floor(80630964769/2), math.floor(1171432692373/2)]

H = [331776, 16785406, 54018520, 214748356, 342999976, 788748340, 2147483646,
     6547483042, 16148168400, 80630964768, 1171432692372]

def checkOrder(p,g):
    new_value = 1
    for i in range(1,p):
        new_value = (new_value * g) % p
        if new_value == 1:
            return i
    return 0

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def findSmallestGenerator(p):
    g = 2
    while g < p:
        if checkOrder(p,g) == p-1:
            print(g)
            return g
        g += 1
    return 0

def solveDLP_shank(p, g, h):
    n = 1 + math.floor(math.sqrt(p-1))
    start_time = time.time()
    u = modinv(g, p)**n % p
    L1 = np.array([g**0])
    L2 = np.array([h])
    new_g = 1
    new_u = u
    for i in range(1,n+1):
        L1 = np.append(L1, (g*new_g) % p)
        new_g = (g*new_g) % p
        L2 = np.append(L2, (h*new_u) % p)
        new_u = (u*new_u) % p
    for i in range(0, L1.size):
        for j in range(0, L2.size):
            if L1[i] == L2[j]:
                print('Solution is ', i+j*n)
                run_time = time.time() - start_time
                print("--- %s seconds ---" % run_time)
                return [int(i+j*n), run_time]


def solveDLP_bruteforce(p, g, h):
    start_time = time.time()
    solution = 0
    new_g = 1
    for i in range(1,p):
        if g*new_g % p == h:
            solution = i
            break
        new_g = g * new_g % p
    print('Solution is', solution)
    run_time = time.time() - start_time
    print("--- %s seconds ---" % run_time)
    return [int(solution), run_time]


def main():
    file_shank = open('results_shank.txt', 'a')
    file_bruteforce = open('results_bruteforce.txt', 'a')
    for i in range(0, len(PRIMES)):
        print("")
        print("Shank's algorithm:")
        solution_shank = solveDLP_shank(PRIMES[i], GENERATORS[i], H[i])
        print("")
        print("Brute force:")
        solution_bruteforce = solveDLP_bruteforce(PRIMES[i], GENERATORS[i], H[i])
        start_time = time.time()
        print("")
        print('Check result (shank): ', pow(GENERATORS[i], solution_shank[0], PRIMES[i]))
        print('Check result (brute force): ', pow(GENERATORS[i], solution_bruteforce[0], PRIMES[i]))
        print("--- %s seconds ---" % (time.time() - start_time))
        file_shank.write(str(PRIMES[i]) + ';' + str(solution_shank[0]) + ';' + str(solution_shank[1]) + '\n')
        file_bruteforce.write(str(PRIMES[i]) + ';' + str(solution_bruteforce[0]) + ';' + str(solution_bruteforce[1]) +
                              '\n')
    file_shank.close()
    file_bruteforce.close()


main()
