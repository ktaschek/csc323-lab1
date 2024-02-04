import time
from random import randint
import base64


def bytes_to_base64(s):
    return base64.b64encode(s).decode('utf-8')

# Mersenne Twister

# w: word size (in number of bits)
# n: degree of recurrence
# m: middle word, an offset used in the recurrence relation defining the series
# r: separation point of one word, or the number of bits of the lower bitmask,
# a: coefficients of the rational normal form twist matrix
# b, c: TGFSR(R) tempering bitmasks
# s, t: TGFSR(R) tempering bit shifts
# u, d, l: additional Mersenne Twister tempering bit shifts/masks


class MersenneTwister:
    def __init__(self, seed):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u = 11
        self.d = 0xFFFFFFFF
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.f = 1812433253

        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = ((1 << self.w) - 1) & (~self.lower_mask)

        self.seed(seed)

    def seed(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = self.f * \
                (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i
            self.MT[i] &= ((1 << self.w) - 1)

    def extract_number(self):
        if self.index >= self.n:
            self.twist()

        y = self.MT[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.index += 1
        return y & ((1 << self.w) - 1)

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + \
                (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0


def oracle():
    # random number between 5 and 60
    wait_time = randint(5, 60)
    time.sleep(wait_time)
    seed = int(time.time())

    mt = MersenneTwister(seed)

    wait_time = randint(5, 60)
    time.sleep(wait_time)

    output = mt.extract_number()

    return bytes_to_base64(output.to_bytes(4, 'little'))


def main():
    mt = MersenneTwister(213697213)
    print(mt.extract_number())

    # oracle_output = oracle()
    # print(oracle_output)


if __name__ == "__main__":
    main()
