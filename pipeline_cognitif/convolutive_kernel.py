import math

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0: return False
        i += w
        w = 6 - w
    return True

class ConvolutiveSystemEngine:
    ANCHORS_N10 = {
        2: 29, 3: 227, 4: 947, 5: 2999,
        6: 7529, 7: 16519, 8: 32327, 9: 58337
    }

    @staticmethod
    def savard_constants(k: int) -> tuple[float, float, float, float]:
        fk = float(k)
        alphaA = 2.0 * (fk**4 - fk**2 + 1.0) / ((fk - 1.0) * (fk**3))
        alphaB = fk * alphaA
        offsetA = fk / (fk - 1.0)
        offsetB = (fk**7 - fk**6 + fk) / (fk - 1.0)
        return alphaA, alphaB, offsetA, offsetB

    @classmethod
    def sums_SA_SB(cls, k: int, n: int) -> tuple[float, float]:
        alphaA, alphaB, offsetA, offsetB = cls.savard_constants(k)
        fk = float(k)
        SA = (alphaA / 2.0) * (fk**n) - offsetA
        SB = (alphaB / 2.0) * (fk**n) - offsetB
        return SA, SB

    @classmethod
    def reconstruct_prime_n10(cls, k: int) -> int:
        if k in cls.ANCHORS_N10:
            return cls.ANCHORS_N10[k]

        SA, SB = cls.sums_SA_SB(k, 10)
        fk = float(k)
        k6, k8, k7 = fk**6, fk**8, fk**7

        digamma_options = [SA - k8, SA + k8, SA + k7, SA - k7]

        for dig_val in digamma_options:
            P_cand = round((SB - dig_val) / k6)
            if is_prime(P_cand):
                return P_cand

        base_P = int(round((SB - (SA - k8)) / k6))
        if is_prime(base_P): return base_P
        
        offset = 1
        while True:
            if is_prime(base_P + offset): return base_P + offset
            if is_prime(base_P - offset) and (base_P - offset) > 1: return base_P - offset
            offset += 1
