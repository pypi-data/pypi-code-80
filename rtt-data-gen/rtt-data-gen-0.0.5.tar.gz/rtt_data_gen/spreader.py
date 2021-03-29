#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import binascii
import sys
import math
import time
import random
import logging
import coloredlogs
import itertools
from typing import Optional
from bitarray import bitarray
from numpy.random import Generator, PCG64
from randomgen.aes import AESCounter
from randomgen.chacha import ChaCha


logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO)


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def randbytes(x):
    osize = 0
    r = bytearray(x)
    while osize < x:
        rest = x - osize
        ssize = 8 if rest >= 8 else rest
        z = random.getrandbits(ssize << 3)
        zb = z.to_bytes(ssize, 'big')
        for i in range(ssize):
            r[osize + i] = zb[i]
        osize += ssize
    return bytes(r)


def counter(offset=0, mod=None):
    ctr = offset
    while True:
        yield ctr
        ctr += 1
        if mod:
            ctr %= mod


def number_streamer(gen, osize, nbytes):
    osize_b = int(math.ceil(osize/8.))
    b = bitarray(endian='big')
    btmp = bitarray(endian='big')
    for x in itertools.islice(gen, nbytes*8 // osize):
        xb = int(x).to_bytes(osize_b, 'big')
        btmp.clear()
        btmp.frombytes(xb)
        b += btmp[osize_b*8 - osize:]
    return b.tobytes()


class RGenerator:
    def __init__(self):
        pass

    def randint(self, low, high, size=None):
        raise ValueError()

    def randbytes(self, length):
        raise ValueError()

    def randbits(self, bits):
        raise ValueError()

    def uniform(self, low, high, size=None):
        raise ValueError()


class RGeneratorRandom(RGenerator):
    def __init__(self, seed=None):
        super().__init__()
        if seed:
            random.seed(seed)

    def randint(self, low, high, size=None):
        if size is None:
            return random.randint(low, high)
        return [random.randint(low, high) for _ in range(size)]

    def randbytes(self, length):
        return randbytes(length)

    def randbits(self, bits):
        return random.getrandbits(bits)

    def uniform(self, low, high, size=None):
        if size is None:
            return random.uniform(low, high)
        return [random.uniform(low, high) for _ in range(size)]


class RGeneratorPCG(RGenerator):
    def __init__(self, seed=None, cls=None, cls_kw=None):
        super().__init__()
        seedx = int.from_bytes(bytes=seed, byteorder='big') if seed else None
        self.rand = PCG64(seedx) if cls is None else cls(seedx, **(cls_kw or {}))
        self.gen = Generator(self.rand)

    def randint(self, low, high, size=None):
        return self.gen.integers(low, high, size=size, endpoint=True)

    def randbytes(self, length):
        return self.gen.bytes(length)

    def randbits(self, bits):
        return self.randint(0, (2 << bits)-1)

    def uniform(self, low, high, size=None):
        return self.gen.uniform(low, high, size=size)


def rand_moduli(mod=None, gen: Optional[RGenerator] = None):
    if gen is None:
        while True:
            yield random.randint(0, mod - 1)

    while True:
        yield from gen.randint(0, mod - 1, 2048)


def rand_gen_randint(low, high, gen: RGenerator, chunk=2048):
    while True:
        yield from gen.randint(low, high, chunk)


def rand_gen_uniform(low, high, gen: RGenerator, chunk=2048):
    while True:
        yield from gen.uniform(low, high, chunk)


def rand_moduli_bias_frac(mod, gen: Optional[RGenerator], p=0.001, frac=10):
    gen_p = rand_gen_uniform(0, 1, gen)
    gen_uni = rand_gen_randint(0, mod - 1, gen)
    gen_bias = rand_gen_randint(int(mod/frac), int(mod*(frac-1)/frac), gen)  # 1/10 ... 9/10 of the mod
    while True:
        cp = next(gen_p)
        if cp <= p:
            yield next(gen_bias)
        else:
            yield next(gen_uni)


class ModSpreader:
    def __init__(self, m=None, osize=None, gen: Optional[RGenerator] = None):
        self.m = m
        self.osize = osize
        self.gen = gen

        self.max = (2 ** osize)
        self.max_mask = self.max - 1
        self.tp = self.max // m
        self.bp = self.max / m
        self.rm = self.max - self.tp * self.m
        self.msize = int(math.ceil(math.log2(m)))

        self.gen_randint_0_tp = rand_gen_randint(0, self.tp, gen)
        self.gen_randint_0_maxm1 = rand_gen_randint(0, self.max - 1, gen)
        self.gen_uniform_0_bp = rand_gen_uniform(0, self.bp, gen)

    def spread(self, z):
        """Spread number z inside range (0 ... m) to osize"""
        z %= self.m
        return (self.m * self.gen.randint(0, self.tp if z < self.rm else self.tp - 1)) + z

    def spread_weak(self, z):
        """Spreads number inside range (0 ... m) to osize, with bias on lower moduli range"""
        z %= self.m
        return z + (self.gen.randbits(self.osize - self.msize) << self.msize)

    def spread_weak_minus(self, z):
        """Spreads number inside range (0 ... m) to osize, with bias - upper moduli is not covered"""
        z %= self.m
        y = self.gen.randbits(self.osize)
        return (y - (y % self.m)) + z

    def spread_weak_weird(self, z):
        """For testing, generates highly non-uniform distribution (resembles a company logo)"""
        z %= self.m
        y = self.gen.randbits(self.osize)
        return (y - self.m if y >= self.m else y) + z

    def spread_flat(self, z):
        """For testing, introducing significant bias by masking random positions in moduli to zero"""
        p = self.gen.randbits(self.gen.randint(0, 8))
        z &= ~p
        return self.spread(z)

    def spread_reject(self, z):
        """Rejection sampling, smaller data size, works!"""
        x = (self.m * next(self.gen_randint_0_tp)) + z
        return x if x < self.max else None

    def spread_gen(self, z):
        """Rejection sampling, with aux gen, works also!"""
        x = (self.m * next(self.gen_randint_0_tp)) + z
        return x if x < self.max else next(self.gen_randint_0_maxm1)

    def spread_wider(self, z):
        """Cannot detect biases, z is basically ignored"""
        z %= self.m
        return int(next(self.gen_uniform_0_bp) * self.m + z) & self.max_mask

    def spread_wider_reject(self, z):
        """Cannot detect biases, z is basically ignored"""
        z %= self.m
        x = int(next(self.gen_uniform_0_bp) * self.m + z)
        return x if x < self.max else None


class DataGenerator:
    def __init__(self):
        self.args = None
        self.rng = None

    def main(self):
        parser = self.argparser()
        self.args = parser.parse_args()

        if self.args.debug:
            coloredlogs.install(level=logging.DEBUG)

        seed = binascii.unhexlify(self.args.seed) if self.args.seed else None
        if self.args.rgen in ['pcg', 'pcg32', 'pcg64', 'numpy', 'np']:
            self.rng = RGeneratorPCG(seed)
        elif self.args.rgen in ['aes'] or self.args.rgen is None:
            self.rng = RGeneratorPCG(seed, cls=AESCounter, cls_kw={'mode': 'sequence'})
        elif self.args.rgen in ['chacha'] or self.args.rgen is None:
            self.rng = RGeneratorPCG(seed, cls=ChaCha, cls_kw={'mode': 'sequence'})
        elif self.args.rgen in ['sys', 'py', 'random'] or self.args.rgen is None:
            self.rng = RGeneratorRandom(seed)
        else:
            raise ValueError('Unknown generator: %s' % (self.args.rgen, ))

        mod = int(self.args.mod, 16) if self.args.mod else None
        mod_size = int(math.ceil(math.log2(mod))) if mod else None

        osize = self.args.osize
        isize = self.args.isize
        if not isize and mod:
            isize = mod_size
        if not mod_size and isize:
            mod_size = isize
        if not osize and isize:
            osize = isize
        if not osize and mod_size:
            osize = mod_size

        osize_b = int(math.ceil(osize / 8.))
        isize_b = int(math.ceil(isize / 8.))

        read_multiplier = 8 / gcd(isize, 8)
        read_chunk_base = int(isize * read_multiplier)
        read_chunk = read_chunk_base * max(1, 8192 // read_chunk_base)  # expand a bit
        max_len = self.args.max_len
        max_out = self.args.max_out
        cur_len = 0
        cur_out = 0

        spreader = ModSpreader(m=mod, osize=osize, gen=self.rng) if mod else None
        spread_func = lambda x: x  # identity by default
        output_fh = sys.stdout.buffer if not self.args.ofile else open(self.args.ofile, 'w+b')

        if spreader:
            st = self.args.strategy
            if st == 0:
                pass  # identity
            elif st == 1:
                spread_func = spreader.spread
            elif st == 2:
                spread_func = spreader.spread_weak
            elif st == 3:
                spread_func = spreader.spread_weak_minus
            elif st == 4:
                spread_func = spreader.spread_weak_weird
            elif st == 5:
                spread_func = spreader.spread_flat
            elif st == 6:
                spread_func = spreader.spread_reject
            elif st == 7:
                spread_func = spreader.spread_gen
            elif st == 8:
                spread_func = spreader.spread_wider
            elif st == 9:
                spread_func = spreader.spread_wider_reject
            else:
                raise ValueError('No such strategy')

        gen_ctr = counter(self.args.inp_ctr_off, mod) if self.args.inp_ctr else None
        gen_moduli = rand_moduli(mod, self.rng) if self.args.rand_mod else None

        b = bitarray(endian='big')
        bout = bitarray(endian='big')
        b_filler = bitarray(isize_b*8 - isize, endian='big')
        b_filler.setall(0)
        btmp = bitarray(endian='big')
        osize_mask = (2 ** (osize_b * 8)) - 1
        nrejects = 0
        noverflows = 0
        time_start = time.time()
        logger.info("Generating data")

        while True:
            if self.args.stdin:
                data = sys.stdin.buffer.read(read_chunk)
            elif gen_ctr:
                data = number_streamer(gen_ctr, isize, read_chunk)
            elif gen_moduli:
                data = number_streamer(gen_moduli, isize, read_chunk)
            elif self.args.rand_mod_bias1:
                gg = rand_moduli_bias_frac(mod, self.rng, 0.0001, 10)
                data = number_streamer(gg, isize, read_chunk)
            elif self.args.rand_mod_bias2:
                gg = rand_moduli_bias_frac(mod, self.rng, 0.01, 7)
                data = number_streamer(gg, isize, read_chunk)
            elif self.args.rand_mod_bias3:
                gg = rand_moduli_bias_frac(mod, self.rng, 0.01, 4)
                data = number_streamer(gg, isize, read_chunk)
            else:
                data = self.rng.randbytes(read_chunk)

            if not data:
                break

            # Manage output size constrain in bits
            cblen = len(data) * 8
            if max_len is not None and cur_len + cblen > max_len:
                rest = max_len - cur_len
                data = data[:rest//8]
                cblen = rest

            cur_len += cblen
            elems = cblen // isize

            b.clear()
            b.frombytes(data)

            # Parse on ints
            for i in range(elems):
                cbits = b_filler + b[i * isize: (i+1) * isize]

                cbytes = cbits.tobytes()
                celem = int.from_bytes(bytes=cbytes, byteorder='big')
                spreaded = spread_func(celem)
                if spreaded is None:
                    nrejects += 1
                    continue
                if spreaded > osize_mask:
                    noverflows += 1

                oelem = int(spreaded) & osize_mask
                oelem_b = oelem.to_bytes(osize_b, 'big')
                btmp.clear()
                btmp.frombytes(oelem_b)
                bout += btmp[osize_b * 8 - osize:]
                cur_out += osize
                if max_out is not None and cur_out >= max_out:
                    break

            finishing = data is None \
                        or (max_len is not None and max_len <= cur_len) \
                        or (max_out is not None and max_out <= cur_out)
            if (len(bout) % 8 == 0 and len(bout) >= 2048) or finishing:
                tout = bout.tobytes()
                if self.args.ohex:
                    tout = binascii.hexlify(tout)

                output_fh.write(tout)
                bout = bitarray(endian='big')

            if finishing:
                output_fh.flush()
                break

        time_elapsed = time.time() - time_start
        logger.info("Number of rejects: %s, overflows: %s, time: %s s" % (nrejects, noverflows, time_elapsed, ))
        if self.args.ofile:
            output_fh.close()

    def argparser(self):
        parser = argparse.ArgumentParser(description='Data spreader - for moduli functions')

        parser.add_argument('--debug', dest='debug', action='store_const', const=True,
                            help='enables debug mode')
        parser.add_argument('-i', '--stdin', dest='stdin', action='store_const', const=True,
                            help='Read input stdin')
        parser.add_argument('-r', '--rand', dest='rand', action='store_const', const=True,
                            help='Generate randomness internally')
        parser.add_argument('--rgen', dest='rgen',
                            help='Random number generator implementation (pcg32)')
        parser.add_argument('--inp-rand-mod', dest='rand_mod', action='store_const', const=True,
                            help='Generate randomness internally, generating random integer in mod range')
        parser.add_argument('--inp-rand-mod-bias1', dest='rand_mod_bias1', action='store_const', const=True,
                            help='Generate randomness internally, generating random integer in mod range, bias1')
        parser.add_argument('--inp-rand-mod-bias2', dest='rand_mod_bias2', action='store_const', const=True,
                            help='Generate randomness internally, generating random integer in mod range, bias2')
        parser.add_argument('--inp-rand-mod-bias3', dest='rand_mod_bias3', action='store_const', const=True,
                            help='Generate randomness internally, generating random integer in mod range, bias3')
        parser.add_argument('--inp-ctr', dest='inp_ctr', action='store_const', const=True,
                            help='Input counter generator')
        parser.add_argument('--inp-ctr-off', dest='inp_ctr_off', type=int, default=0,
                            help='Input counter generator offset')
        parser.add_argument('-s', '--seed', dest='seed',
                            help='Seed for random generator')
        parser.add_argument('-m', '--mod', dest='mod',
                            help='Hex-coded modulus to spread')
        parser.add_argument('--ib', dest='isize', type=int,
                            help='Input block size in bits (when using on stdin)')
        parser.add_argument('--ob', dest='osize', type=int,
                            help='Output block size in bits (to spread)')
        parser.add_argument('--st', dest='strategy', type=int, default=0,
                            help='Strategy to use for spreading')
        parser.add_argument('--max-len', dest='max_len', type=int,
                            help='Maximum length in bits when working with generator')
        parser.add_argument('--max-out', dest='max_out', type=int,
                            help='Maximum length in bits for output')
        parser.add_argument('--ohex', dest='ohex', action='store_const', const=True,
                            help='Output hex-coded')
        parser.add_argument('--ofile', dest='ofile',
                            help='Dump to output file')
        return parser


def main():
    br = DataGenerator()
    return br.main()


if __name__ == '__main__':
    main()
