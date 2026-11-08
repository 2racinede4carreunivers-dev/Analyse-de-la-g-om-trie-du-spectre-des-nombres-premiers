import os,re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
SPECTRAL_BLEU=(18/255,42/255,90/255);SPECTRAL_AZUR=(41/255,98/255,168/255);SPECTRAL_OR=(196/255,148/255,34/255);SPECTRAL_VIOLET=(96/255,54/255,140/255);SPECTRAL_GRIS=(244/255,246/255,250/255);SPECTRAL_ROUGE=(158/255,42/255,52/255)
OUT_DIR=os.path.dirname(os.path.abspath(__file__))
LISTE_PATH=r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\Liste_Premier_Multi_Rapports_K\liste_k2_k1001_n10.txt"
points=[]
if os.path.exists(LISTE_PATH):
    for line in open(LISTE_PATH,encoding="utf-8"):
        m=re.search(r"1/(\d+)\s*\(.*?\).*P\(n=10\)=([\d]+)",line)
        if m and "PREMIER TROUVE" in line: points.append((int(m.group(1)),int(m.group(2))))
points.sort(key=lambda x:x[0])
typique=[(k,p,1.0/k) for k,p in points if k==2]
non_typique=[(k,p,1.0/k) for k,p in points if k!=2]
all_pts=typique+non_typique
xs=[p for _,p,_ in all_pts]; ys=[r for _,_,r in all_pts]
order=sorted(range(len(xs)),key=lambda i:xs[i]); xs_s=[xs[i] for i in order]; ys_s=[ys[i] for i in order]
fig,ax=plt.subplots(figsize=(11.0,7.0),facecolor=SPECTRAL_GRIS); ax.set_facecolor("white")
ax.plot(xs_s,[0.5]*len(xs_s),color=SPECTRAL_BLEU,linewidth=2.0,linestyle="--",label="Courbe critique s=1/2+it (rapport typique 1/2)")
ax.plot(xs_s,ys_s,color=SPECTRAL_ROUGE,linewidth=1.6,linestyle="-",alpha=0.7,label="Progression 1/k (reconstruction)")
ax.scatter([p for _,p,_ in typique],[r for _,_,r in typique],color=SPECTRAL_OR,s=90,zorder=5,edgecolor=SPECTRAL_BLEU,linewidth=1.2)
ax.scatter([p for _,p,_ in non_typique],[r for _,_,r in non_typique],color=SPECTRAL_AZUR,s=40,zorder=4,edgecolor=SPECTRAL_VIOLET,linewidth=0.6)
for k,p,r in typique: ax.annotate(f"k={k}\nP={p}",(p,r),textcoords="offset points",xytext=(8,8),fontsize=9,color=SPECTRAL_BLEU,fontweight="bold")
for k,p,r in non_typique[:8]: ax.annotate(f"k={k}",(p,r),textcoords="offset points",xytext=(6,-12),fontsize=8,color=SPECTRAL_VIOLET)
ax.set_xscale("log")
ax.set_xlabel("Valeur du nombre premier (ancrage, n = 10)",color=SPECTRAL_BLEU,fontsize=11,fontweight="bold")
ax.set_ylabel("Rapport typique / non typique (1/k)",color=SPECTRAL_BLEU,fontsize=11,fontweight="bold")
ax.set_title("Progression des rapports 1/k pour les ancrages et leurs valeurs premieres (n = 10)\nGeometrie du spectre des nombres premiers",color=SPECTRAL_BLEU,fontsize=12,fontweight="bold",pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"{v:.0e}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"{v:.4f}"))
ax.grid(True,linestyle=":",alpha=0.5,color=SPECTRAL_VIOLET)
for spine in ax.spines.values(): spine.set_color(SPECTRAL_BLEU)
handles=[plt.Line2D([0],[0],marker="o",color="w",markerfacecolor=SPECTRAL_OR,markeredgecolor=SPECTRAL_BLEU,markersize=9,label="Rapport typique 1/k = 1/2"),plt.Line2D([0],[0],marker="o",color="w",markerfacecolor=SPECTRAL_AZUR,markeredgecolor=SPECTRAL_VIOLET,markersize=7,label="Rapport non typique 1/k != 1/2"),plt.Line2D([0],[0],color=SPECTRAL_BLEU,linestyle="--",linewidth=2,label="Courbe : s=0.5+it"),plt.Line2D([0],[0],color=SPECTRAL_ROUGE,linestyle="-",linewidth=1.6,label="Progression reconstruite")]
ax.legend(handles=handles,loc="upper right",fontsize=9,framealpha=0.95,edgecolor=SPECTRAL_BLEU)
note="Regle reconstruction (courbe): analogie s=1/2+it (Zeta Riemann); RsP=Re(s)=1/2 vrai localement. Rapport typique=1/2 droite critique idiomatique. Rapports non typiques 1/k = valeur x (Chebyshev) -> quantite zeros non triviaux. Geometrie spectre: -2 > nombres premiers; valeur infinitesimale premiere negative la plus petite. Premiers negatifs n=-1..-15: -2 a -47 (15 derniers). Tout < -47 correspond aux P positifs. n=10 limite positive jusqu'a k=84000000 (P max); au-dela valeurs > -47. Ex n=10: 1/3->P=227 (49e premier); 1/4->P=947; 1/5->P=2999. n=1: 1/3->P=173 (n=-1 negatif). RsP=Re(s)=1/2 (rapport spectral typique), valide localement par glissement des rapports non typiques."
fig.text(0.5,0.01,note,ha="center",va="bottom",fontsize=7.5,color=SPECTRAL_VIOLET,style="italic",wrap=True)
fig.tight_layout(rect=[0,0.16,1,1])
out_png=os.path.join(OUT_DIR,"graph_ancrages_rapports_n10.png")
fig.savefig(out_png,dpi=150,facecolor=SPECTRAL_GRIS)
plt.close(fig)
print("Graphique genere :",out_png)
print("Points traces :",len(points))