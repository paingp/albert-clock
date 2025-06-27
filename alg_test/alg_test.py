import sys
import random


class EquationAlg():

    # TO DO: add am/pm mode later to change HOURS_RANGE
    # TO DO: add feature to so only one of the equations (for hour or min) is mult/div; other one is purely arithmetic
    def __init__(self):
        self.hours_range = list(range(0,23))
        self.mins_range = list(range(0,59))
        self.abs_min_bound = min(min(self.hours_range), min(self.hours_range))
        self.abs_max_bound = max(max(self.hours_range), max(self.hours_range))

        self.prime_nums = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}

        self.val_facs_dict = dict()
        self.val_mults_dict = dict()

        self.max_del = 20                # inclusive (max delta for addition/subtraction)
        self.max_div_val = 99            # inclusive (max bound for division equations)

        self.generateEqns()


    def findFacsOdd(self, val):
        fac1, fac2 = -1, -1

        for pn in self.prime_nums:
            if (val%pn == 0):
                fac1, fac2 = pn, val//pn
                break

        return fac1, fac2


    def findFacs(self, val):
        fac1, fac2 = -1, -1
        
        if (val%2 == 0): fac1, fac2 = 2, val//2
        else: fac1, fac2 = self.findFacsOdd(val)

        return fac1, fac2


    def isPrime(self, val): 
        return (val in self.prime_nums)


    def generateFactors(self, val):
        fac1, fac2 = self.findFacs(val)

        # validate fac1, fac2
        if (fac1 == -1 or fac2 == -1):
            print(f"ERR: finding facs failed for val {val}, returned: {fac1} {fac2}")
            sys.exit(-1)
        # fac1 should ALWAYS be smaller and prime
        if not (self.isPrime(fac1) and fac1 <= fac2):
            print(f"ERR: fac1 not both smaller and prime for val={val}: fac1={fac1}, fac2={fac2}")
            sys.exit(-1) 

        self.val_facs_dict[val] = [(fac1, fac2)]

        if self.isPrime(fac2): return
        if self.val_facs_dict.get(fac2) == None:
            print(f"ERR: {fac2} expected to be prime or in dict")
            sys.exit(-1)

        print(f"val: {val}   fac1: {fac1}   fac2: {fac2}")

        recurse_fac_vals = self.val_facs_dict[fac2]
        for (f1,f2) in recurse_fac_vals:
            cand1_tup, cand2_tup = (f2, fac1*f1), (f1, fac1*f2)
            cand1_tup_rev, cand2_tup_rev = cand1_tup[::-1], cand2_tup[::-1]

            if (not cand1_tup in self.val_facs_dict[val]) and (not cand1_tup_rev in self.val_facs_dict[val]): self.val_facs_dict[val].append(cand1_tup)
            if (not cand2_tup in self.val_facs_dict[val]) and (not cand2_tup_rev in self.val_facs_dict[val]): self.val_facs_dict[val].append(cand2_tup)


    def generateMultiples(self, val):
        counter = 2
        res = val * counter

        while res < self.max_div_val:
            ordered_tup = (res, counter)

            if self.val_mults_dict.get(val) == None: self.val_mults_dict[val] = [ordered_tup]
            else: self.val_mults_dict[val].append(ordered_tup)

            counter += 1
            res = val * counter


    def generateEqns(self):
        for val in range(2, max(self.mins_range)):
            self.generateMultiples(val)		                        # for division
            if not self.isPrime(val): self.generateFactors(val)           # for multiplication


    def getRandomMultEqn(self, val):
        # get bounds based on max delta
        min_bound, max_bound = val-self.max_del, val+self.max_del
        if min_bound < self.abs_min_bound: min_bound = self.abs_min_bound
        if max_bound < self.abs_max_bound: max_bound = self.abs_max_bound

        # randomly select value based on bounds (if value is prime prompt again)
        while not (cand_random_val:=random.randint(min_bound, max_bound)) in self.val_facs_dict:
            cand_random_val = random.randint(min_bound, max_bound)

        # generate delta to be applied and the multiplication equation for randomly selected value
        delta = val - cand_random_val

        val_factors = self.val_facs_dict[cand_random_val]
        factors = random.choice(val_factors)

        # generate equation string
        eqn_string = f"{factors[0]} * {factors[1]} + {delta}"
        if delta < 0: eqn_string = f"{factors[0]} * {factors[1]} - {abs(delta)}"

        # delta will be addition/subtraction of the multiplication result
        return eqn_string


if __name__ == "__main__":
    alg = EquationAlg()
    print(alg.getRandomMultEqn(15))
    print(alg.getRandomMultEqn(20))
    print(alg.getRandomMultEqn(18))
    print(alg.getRandomMultEqn(18))
    print(alg.getRandomMultEqn(18))
    print(alg.getRandomMultEqn(18))
