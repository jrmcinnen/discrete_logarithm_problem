# author: Jere Mäkinen

import math
import time

TEST_PRIMES = [31]
TEST_GENERATORS = [3]

PRIMES = [331777, 16785407, 54018521, 214748357, 342999977, 788748341, 988748323, 2147483647,
          4347483557, 6547483043, 8547483037, 16148168401]

GENERATORS = [5, 5, 6, 2, 3, 2, 3, 7, 5, 2, 2, 22]

# Maksimisuoritusaika ratkaisualgoritmeille.

# Max time for algorithms to run.
MAX_RUNNING_TIME = 7200

# h yhtälöön h = p^x mod p

# h for the equation h = p^x mod p
H = 2021


# Tarkistaa alkion (g) kertaluvun

# Checks element's (g) order in set integers modulo p
def checkOrder(p, g):
    new_value = 1
    for i in range(1,p):
        new_value = (new_value * g) % p
        if new_value == 1:
            return i
    return 0


# Etsii pienimmän mahdollisen virittäjän joukolle kokonaisluvut modulo p.

# Find the smallest possible generator for integers modulo p, where p is a prime number
def findSmallestGenerator(p):
    g = 2
    while g < p:
        if checkOrder(p,g) == p-1:
            print(g)
            return g
        g += 1
    return 0


# Shankin algoritmi. Ratkaisee yhtälön h = p^x mod p, missä p on alkuluku
# Palauttaa ratkaisun x, tehtyjen vertailuiden lukumäärän ja suoritusajan.

# Shank's algorithm. Solves the equation h = p^x mod p, where p is a prime number.
# Returns the solution x, the amount of made comparisons and the running time of the algorithm.
def solveDLP_shank(p, g, h):
    start_time = time.time()
    n = 1 + math.floor(math.sqrt(p-1))
    l1 = {1:  0}
    new_g = 1
    u = pow(g, p - 2, p) ** n % p
    for i in range(1, n+1):
        new_g = (g*new_g) % p
        if not new_g in l1:
            l1[new_g] = i
    if h in l1:
        solution = l1[h]
        print("Solution is ", solution)
        run_time = time.time() - start_time
        print("--- %s seconds ---" % run_time)
        return [solution, run_time]
    else:
        new_u = u
        for i in range(1, n+1):
            new_h = (h*new_u) % p
            if new_h in l1:
                solution = l1[new_h]+n*i
                print("Solution is ", solution)
                run_time = time.time() - start_time
                print("--- %s seconds ---" % run_time)
                return [solution, run_time]
            if time.time() - start_time > MAX_RUNNING_TIME:
                print('Solving took too much time')
                return [-1, MAX_RUNNING_TIME]
            new_u = (u*new_u) % p
    print("no result")



# Suoraviivainen raa'an voiman menetelmä yhtälön h = p^x mod p ratkaisuun, missä p on alkuluku

# Brute force method to solve equation h = p^x mod p, where p is a prime number.
def solveDLP_bruteforce(p, g, h):
    start_time = time.time()
    solution = 0
    new_g = 1
    for i in range(1, p):
        if g*new_g % p == h:
            solution = i
            break
        if time.time() - start_time > MAX_RUNNING_TIME:
            print('Solving took too much time')
            return [-1, MAX_RUNNING_TIME]
        new_g = g * new_g % p
    print('Solution is', solution)
    run_time = time.time() - start_time
    print("--- %s seconds ---" % run_time)
    return [int(solution), run_time]


def give_primes():
    return [PRIMES, GENERATORS]


def main():
    file_shank = open('results_shank.csv', 'a')
    file_bruteforce = open('results_bruteforce.csv', 'a')
    file_check_result = open('results_check.csv', 'a')
    primes_and_generators = give_primes()
    primes = primes_and_generators[0]
    generators = primes_and_generators[1]
    for i in range(0, len(primes)):
        print("Let's solve the following equation: {} = {}^x mod {}".format(H, GENERATORS[i], PRIMES[i]))
        print("")
        print("Shank's algorithm:")
        solution_shank = solveDLP_shank(primes[i], generators[i], H)
        print("")
        print("Brute force:")
        solution_bruteforce = solveDLP_bruteforce(primes[i], generators[i], H)
        start_time = time.time()
        print("")
        if solution_shank[1] < MAX_RUNNING_TIME:
            print('Check result (shank): ', pow(generators[i], solution_shank[0], primes[i]))
        else:
            print("Shank's algorithm ran out of time.")

        if solution_bruteforce[1] < MAX_RUNNING_TIME:
            print('Check result (brute force): ', pow(generators[i], solution_bruteforce[0], primes[i]))
        else:
            print("Brute force run out of time.")
        check_time = time.time() - start_time
        print("--- %s seconds ---" % check_time)
        file_shank.write(str(primes[i]) + ';' + str(solution_shank[0]) + ';' + str(solution_shank[1]) +'\n')
        file_bruteforce.write(str(primes[i]) + ';' + str(solution_bruteforce[0]) + ';' +
                              str(solution_bruteforce[1]) + '\n')
        file_check_result.write(str(primes[i]) + ';' + str(solution_shank[0]) + ';' + str(check_time) + '\n')
        print("")
        print("")
    file_shank.close()
    file_bruteforce.close()
    file_check_result.close()


main()
