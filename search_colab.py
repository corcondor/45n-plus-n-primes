"""Colab用探索本体: 候補ファイルを順に処理し、終わったら次を自動で投入する。
状態は Drive (MyDrive/prime45) の done_colab.txt / found_colab.txt に保存され、
再実行時は確認済みを飛ばして続きから始まる。
"""
import os
import time
from multiprocessing import Pool

from gmpy2 import mpz, is_prime

if os.path.exists("/content/drive/MyDrive"):
    BASE = "/content/drive/MyDrive/prime45"
else:
    BASE = "/content/prime45_state"
os.makedirs(BASE, exist_ok=True)
STATE = os.path.join(BASE, "done_colab.txt")
FOUND = os.path.join(BASE, "found_colab.txt")

done = set()
if os.path.exists(STATE):
    done = set(int(x) for x in open(STATE) if x.strip())

REPO = "45n-plus-n-primes"
FILES = ["remaining_candidates.txt", "candidates_over_100k.txt"]
todo = []
for fn in FILES:
    path = os.path.join(REPO, fn)
    if os.path.exists(path):
        todo += [int(x) for x in open(path) if x.strip()]
todo = [n for n in todo if n not in done]
print(f"todo {len(todo)} (done {len(done)}), cpu {os.cpu_count()}", flush=True)


def check(n):
    v = mpz(45) ** n + n
    return n, bool(is_prime(v, 1) and is_prime(v, 25))


t0 = time.time()
count = 0
with Pool(os.cpu_count()) as pool, open(STATE, "a") as sf, open(FOUND, "a") as ff:
    for n, prime in pool.imap_unordered(check, todo, chunksize=1):
        sf.write(f"{n}\n")
        sf.flush()
        count += 1
        if prime:
            ff.write(f"{n}\n")
            ff.flush()
            print(f"PRIME n={n}", flush=True)
        if count % 50 == 0:
            print(f"progress {count}/{len(todo)} elapsed {time.time()-t0:.0f}s", flush=True)
print("ALL DONE", flush=True)
