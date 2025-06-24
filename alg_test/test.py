import sys
from collections import deque


def findFacsOdd(val):
    global PRIME_NUMS
    fac1, fac2 = -1, -1

    for pn in PRIME_NUMS:
        if (val%pn == 0):
            fac1, fac2 = pn, val//pn
            break

    return fac1, fac2


def findFacs(val):
    fac1, fac2 = -1, -1
    
    if (val%2 == 0): fac1, fac2 = 2, val//2
    else: fac1, fac2 = findFacsOdd(val)

    return fac1, fac2


def generateDivisorTree(val):
    global VAL_FACS_DICT

    fac1, fac2 = findFacs(val)

    # validate fac1, fac2
    if (fac1 == -1 or fac2 == -1):
        print(f"ERR: finding facs failed for val {val}, returned: {fac1} {fac2}")
        sys.exit(-1)
    # fac1 should ALWAYS be smaller and prime
    if not (isPrime(fac1) and fac1 <= fac2):
        print(f"ERR: fac1 not both smaller and prime for val={val}: fac1={fac1}, fac2={fac2}")
        sys.exit(-1) 

    VAL_FACS_DICT[val] = [(fac1, fac2)]

    if isPrime(fac2): return
    if VAL_FACS_DICT.get(fac2) == None:
        print(f"ERR: {fac2} expected to be prime or in dict")
        sys.exit(-1)

    print(f"val: {val}   fac1: {fac1}   fac2: {fac2}")

    recurse_fac_vals = VAL_FACS_DICT[fac2]
    for (f1,f2) in recurse_fac_vals:
        cand1_tup, cand2_tup = (f2, fac1*f1), (f1, fac1*f2)
        cand1_tup_rev, cand2_tup_rev = cand1_tup[::-1], cand2_tup[::-1]

        if (not cand1_tup in VAL_FACS_DICT[val]) and (not cand1_tup_rev in VAL_FACS_DICT[val]): VAL_FACS_DICT[val].append(cand1_tup)
        if (not cand2_tup in VAL_FACS_DICT[val]) and (not cand2_tup_rev in VAL_FACS_DICT[val]): VAL_FACS_DICT[val].append(cand2_tup)


def isPrime(val): 
    global PRIME_NUMS
    return (val in PRIME_NUMS)


def generateMultEqns(val):
    if not isPrime(val): 
        generateDivisorTree(val)

def getRandomMultEqn(val):
    # get bounds based on max delta
    # randomly select value based on bounds
    # check if value is prime and just add or subtract
    # generate multiplication equation for that value
    # delta will be addition/subtraction of the multiplication result
    return
    
if __name__ == "__main__":
    HOURS_RANGE = list(range(0,23))
    MINS_RANGE = list(range(0,59))

    PRIME_NUMS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}
    VAL_FACS_DICT = dict()

    for m in MINS_RANGE:
        if (m > 1):
            generateMultEqns(m)
            # generateDivEqns(m)

    for key, val in VAL_FACS_DICT.items():
        print(f"{key}: {val}")
    input("HERE")

    MAX_DEL = 20

    OPERANDS_SET = set(range(1,100))

    addition_f = lambda x,y: x+y
    subtraction_f = lambda x,y: x-y
    OPERATORS_SET = [add_f, sub_f, mult_f, div_f]
