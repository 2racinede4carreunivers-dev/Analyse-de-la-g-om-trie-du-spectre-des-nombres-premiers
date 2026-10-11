;import math


def suiteA(n, t, k):
    base = [math.hypot(1.0, t ** 1)]
    base += [math.hypot(t ** i, t ** (i + 1)) for i in range(1, n - 1)]
    base.append(math.hypot(t ** (n - 2) - t ** (n - 4), t ** (n - 1) - t ** (n - 3)))
    base.append(math.hypot(t ** (n - 1) - t ** (n - 3), t ** n - t ** (n - 2)))
    return sum(base), base


for k in (7, 2, 3):
    for label, t in (("t=1/k", 1.0 / k), ("t=k", float(k))):
        s10, t10 = suiteA(10, t, k)
        s9, t9 = suiteA(9, t, k)
        print(f"k={k:2d} {label:6s} S10={s10:18.6f} S9={s9:18.6f} "
              f"diff={s10 - s9:16.6f} diff/k^8={(s10 - s9) / k ** 8:16.8f} "
              f"nb_termes={len(t10)}/{len(t9)}")
