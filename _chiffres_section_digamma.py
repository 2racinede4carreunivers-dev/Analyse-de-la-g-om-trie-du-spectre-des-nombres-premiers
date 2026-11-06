from fractions import Fraction as F
OUT = r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_out_chiffres.txt"
L=[]; P=L.append
def SA_ferme(k,n):
    aA=F(2)*(k**4-k**2+1)/F((k-1)*k**3); aB=k*aA
    return aA/2*k**n-F(k,k-1), aB/2*k**n-F(k**7-k**6+k,k-1)
def B0(k): return k**5-k**3+k-1
BR=[("A(8)-","k2",+1),("A(8)+","k2",-1),("A(7)+","k",-1),("A(7)-","k",+1)]
P("A. SUITES A ET B DU RAPPORT TYPIQUE t=1/2 (k=2)")
P(f"{'n':>3} {'S_A':>12} {'S_B':>12} {'S_B-S_A':>12} {'/64':>12}")
for n in range(8,17):
    sa,sb=SA_ferme(2,n)
    P(f"{n:>3} {str(sa):>12} {str(sb):>12} {str(sb-sa):>12} {str(F(sb-sa,64)):>12}")
P("")
P("B. ANCRES DE REFERENCE 29,31,37,41 (k=2)")
P(f"{'n':>3} {'P':>4} {'S_A':>10} {'S_B':>10} {'D':>7} {'Dig calc':>10} {'(S_B-D)/64':>13} {'branche':>8}")
for n,p,d,br in ((10,29,256,"A(8)-"),(11,31,1280,"A(8)+"),(12,37,4224,"A(8)+"),(13,41,10624,"A(8)+")):
    sa,sb=SA_ferme(2,n); calc=sa+d
    P(f"{n:>3} {p:>4} {str(sa):>10} {str(sb):>10} {d:>7} {str(calc):>10} {str(F(sb-calc,64)):>13} {br:>8}")
P("")
P("C. RECURRENCE EMPIRIQUE (coeffs 1,5,9,13)")
co=[1,5,9,13]; base=[256,384,768]
for n,d in ((10,256),(11,1280),(12,4224),(13,10624)):
    reste=d; parts=[]
    for j in range(3):
        if co[j]*base[j]<=reste: reste-=co[j]*base[j]; parts.append(f"{co[j]}x{base[j]}")
    P(f"   n={n}: {d} = "+" + ".join(parts)+f"   (reste {reste})")
P("")
P("D. BRANCHES REDUITES A UN POLYNOME (B0 = k^5-k^3+k-1)")
P(f"   B0(2)={B0(2)} B0(3)={B0(3)} B0(4)={B0(4)} B0(5)={B0(5)}")
P(f"{'branche':>9} {'candidat':>12} {'k=2':>8} {'k=3':>8} {'k=4':>8}")
for br,g,m in BR:
    cand="B0"+("+" if m>0 else "-")+("k^2" if g=="k2" else "k")
    cs=[B0(k)+m*(k**2 if g=="k2" else k) for k in (2,3,4)]
    P(f"{br:>9} {cand:>12} {cs[0]:>8} {cs[1]:>8} {cs[2]:>8}")
P("")
P("E. SUITES A ET B TYPIQUES (n=10 termes)")
A10=[2,4,8,16,32,64,128,256,384,768]; B10=[2,4,8,16,32,128,256,512,768,1536]
P("   A = "+" + ".join(map(str,A10))+f"  = {sum(A10)}")
P("   B = "+" + ".join(map(str,B10))+f"  = {sum(B10)}")
P(f"   6e position suite A = 64 ; S_B-S_A = {sum(B10)-sum(A10)}")
P(f"   (3262-1406)/64 = {F(3262-1406,64)}")
open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n")
print("\n".join(L))
