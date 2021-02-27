import math
import time

PRIMES = [331777, 16785407, 54018521, 214748357, 342999977, 788748341, 2147483647,
          6547483043, 16148168401, 80630964769, 1171432692373]

GENERATORS = [5, 5, 6, 2, 3, 2, 7, 2, 22, 17, 2]

MAX_RUNNING_TIME = 7200

H = 2021

# Tarkistaa alkion (g)

# Checks element's (g) order in set integers modulo p
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
    n = 1 + math.floor(math.sqrt(p-1))
    start_time = time.time()
    u = pow(g, p-2, p)**n % p
    l1 = []
    l2 = []
    l1.append(g**0)
    l2.append(h)
    new_g = 1
    new_u = u
    for i in range(1, n+1):
        l1.append((g*new_g) % p)
        new_g = (g*new_g) % p
        l2.append((h*new_u) % p)
        new_u = (u*new_u) % p
    comparison_amount = 0
    for i in range(0, len(l1)):
        for j in range(0, len(l2)):
            comparison_amount += 1
            if l1[i] == l2[j]:
                print('Solution is ', i+j*n)
                run_time = time.time() - start_time
                print("--- %s seconds ---" % run_time)
                return [int(i+j*n), comparison_amount,  run_time]
            if time.time() - start_time > MAX_RUNNING_TIME:
                print('Solving took too much time')
                return [-1, comparison_amount, MAX_RUNNING_TIME]


def solveDLP_bruteforce(p, g, h):
    start_time = time.time()
    solution = 0
    new_g = 1
    comparison_amount = 0
    for i in range(1, p):
        comparison_amount += 1
        if g*new_g % p == h:
            solution = i
            break
        if time.time() - start_time > MAX_RUNNING_TIME:
            print('Solving took too much time')
            return [-1, comparison_amount, MAX_RUNNING_TIME]
        new_g = g * new_g % p
    print('Solution is', solution)
    run_time = time.time() - start_time
    print("--- %s seconds ---" % run_time)
    return [int(solution), comparison_amount, run_time]


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
        print("")
        print("Shank's algorithm:")
        solution_shank = solveDLP_shank(primes[i], generators[i], H)
        print("")
        print("Brute force:")
        solution_bruteforce = solveDLP_bruteforce(primes[i], generators[i], H)
        start_time = time.time()
        print("")
        if solution_shank[2] < MAX_RUNNING_TIME:
            print('Check result (shank): ', pow(generators[i], solution_shank[0], primes[i]))
        else:
            print("Shank's algorithm ran out of time.")

        if solution_bruteforce[2] < MAX_RUNNING_TIME:
            print('Check result (brute force): ', pow(generators[i], solution_bruteforce[0], primes[i]))
        else:
            print("Brute force run out of time.")
        check_time = time.time() - start_time
        print("--- %s seconds ---" % check_time)
        file_shank.write(str(primes[i]) + ';' + str(solution_shank[0]) + ';' + str(solution_shank[1]) + ';' +
                             str(solution_shank[2]) + '\n')
        file_bruteforce.write(str(primes[i]) + ';' + str(solution_bruteforce[0]) + ';' +
                              str(solution_bruteforce[1]) + ';' + str(solution_bruteforce[2]) + '\n')
        file_check_result.write(str(primes[i]) + ';' + str(solution_shank[0]) + ';' + str(check_time))
    file_shank.close()
    file_bruteforce.close()
    file_check_result.close()


main()
