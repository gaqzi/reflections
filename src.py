# import time
# from functools import lru_cache


# @lru_cache
# def slow_add(*args, delay=1):
#     time.sleep(delay)
#     return sum(args)


# s1 = time.perf_counter()

# for i in range(5):
#     print(f"Result of run {i} is: {slow_add(1,2,3)}")

# s2 = time.perf_counter()
# print(f"Total runtime: {s2-s1} seconds.")


# import timeit

# # Implicitly interned dict creation and access.
# implicitly_interned = """
# d = {"#"*4096 : "Interned"}
# d["#"*4096]
# """

# # Explicitly interned dict creation and access.
# explicitly_interned = """
# k = sys.intern("#"*4097)
# d = { k : "Explicitly-interned"}
# d[k]
# """

# # print(f"Interned dict creation & access: {timeit.timeit(interned)} seconds")
# # print(f"Non-interned dict creation & access: {timeit.timeit(non_interned)} seconds")

# print(timeit.timeit(explicitly_interned)/timeit.timeit(implicitly_interned))

import sys
import time

# Implicitly interned.
t0 = time.perf_counter()

for _ in range(10000):
    d = {"#"*4096 : "Interned"}
    d["#"*4096]

t1 = time.perf_counter()


# Explicitly interned.
t2 = time.perf_counter()

k1 = sys.intern("#"*4097)
k2 = sys.intern("#"*4097)
for _ in range(10000):
    d = {k1 : "Interned"}
    d[k2]

t3 = time.perf_counter()


print(t1-t0)
print((t3-t2)/ (t1-t0))
print(f"Implicitly interned dict creation & access: {t1-t0} seconds")
print(f"Explicitly interned dict creation & access: {t3-t2} seconds")
print(f"Explicitly interned creation & access is {(t3-t2)/(t1-t0)} times slower")
