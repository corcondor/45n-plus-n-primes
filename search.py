"""45^n + n が素数となる n を探す。

使い方: python search.py [上限N]   (デフォルト 10000, 要 gmpy2)
手順: 偶数・3・5 の倍数を除外 → 小さい素数でふるう → GMP で確率的素数判定。
"""
import sys
import time

sys.set_int_max_str_digits(2000000)
from gmpy2 import mpz, is_prime


def primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    ps = []
    for i in range(2, limit + 1):
        if sieve[i]:
            ps.append(i)
            sieve[i * i :: i] = b"\x00" * len(sieve[i * i :: i])
    return ps


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    t0 = time.time()
    cand = [n for n in range(2, N + 1) if n % 2 == 0 and n % 3 != 0 and n % 5 != 0]
    print(f"stage1 candidates: {len(cand)}", flush=True)
    for p in primes_upto(5000):
        if p in (2, 3, 5):
            continue
        cand = [n for n in cand if (pow(45, n, p) + n) % p != 0]
    print(f"stage2 survivors: {len(cand)}  elapsed {time.time() - t0:.0f}s", flush=True)
    found = []
    for i, n in enumerate(cand):
        if is_prime(mpz(45) ** n + n, 10):
            found.append(n)
            print(f"PRIME n={n}  ({time.time() - t0:.0f}s)", flush=True)
        if i % 100 == 0:
            print(f"progress {i}/{len(cand)} n={n} found={found}", flush=True)
    print(f"DONE primes <= {N}: {found}", flush=True)


if __name__ == "__main__":
    main()
