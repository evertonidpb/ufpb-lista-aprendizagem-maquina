"""Etapa 2: K-means nos 300 pontos fixos da Etapa 1."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, confusion_matrix

BASE = Path(__file__).with_name("Lista_ML_Base_300_Pontos.csv")
dados = pd.read_csv(BASE)
X = dados[["x", "y"]].to_numpy(dtype=float)
y = dados["classe"].to_numpy(dtype=int)
assert len(dados) == 300 and set(np.unique(y)) == {1, 2}

modelo = KMeans(n_clusters=2, init="k-means++", n_init=20,
                max_iter=300, tol=1e-4, algorithm="lloyd", random_state=42)
grupos = modelo.fit_predict(X)
contagens = np.array([[np.sum((y == i) & (grupos == j))
                       for j in (0, 1)] for i in (1, 2)])
mapa = ({0: 1, 1: 2} if contagens[0, 0] + contagens[1, 1] >=
        contagens[0, 1] + contagens[1, 0] else {0: 2, 1: 1})
previstos = np.array([mapa[int(g)] for g in grupos])
matriz = confusion_matrix(y, previstos, labels=[1, 2])
ari = adjusted_rand_score(y, grupos)

print("Centroides (rótulos alinhados):")
for j, centro in enumerate(modelo.cluster_centers_):
    print(f"Grupo {mapa[j]}: X={centro[0]:.6f}; Y={centro[1]:.6f}")
print("Matriz de confusão:\n", matriz)
print(f"ARI={ari:.6f}; acertos={np.sum(y == previstos)}/300")
print(f"Inércia={modelo.inertia_:.4f}; iterações={modelo.n_iter_}")
print("Pontos divergentes:", dados.loc[y != previstos, "id"].tolist())

cores = {1: "#2D719D", 2: "#118D83"}
fig, eixos = plt.subplots(1, 2, figsize=(12.4, 5.1), sharex=True, sharey=True)
for eixo, rotulos, titulo in [(eixos[0], y, "Classes verdadeiras"),
                             (eixos[1], previstos, "Grupos obtidos: K-means")]:
    for classe in (1, 2):
        p = X[rotulos == classe]
        eixo.scatter(p[:, 0], p[:, 1], s=30, c=cores[classe],
                     alpha=0.78, edgecolors="white", linewidths=0.28,
                     label=f"Classe / grupo {classe}")
    eixo.set_title(titulo, fontsize=12, weight="bold", color="#142C43")
    eixo.set_xlabel("Variável X")
    eixo.grid(alpha=0.18)
    eixo.legend(loc="upper left", frameon=False, fontsize=8)
eixos[0].set_ylabel("Variável Y")
for j, centro in enumerate(modelo.cluster_centers_):
    eixos[1].scatter(*centro, marker="*", s=360, color=cores[mapa[j]],
                     edgecolors="#162A40", linewidths=1.25, zorder=8)
divergentes = np.flatnonzero(y != previstos)
eixos[1].scatter(X[divergentes, 0], X[divergentes, 1], s=155,
                 facecolors="none", edgecolors="#D14A4A", linewidths=2,
                 zorder=9, label="Divergências (3)")
eixos[1].legend(loc="upper left", frameon=False, fontsize=8)
fig.suptitle("Agrupamento dos 300 pontos — K-means (k = 2)",
             fontsize=15, weight="bold", color="#142C43")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(Path(__file__).with_name("Etapa2_KMeans_Comparacao.png"), dpi=230,
            bbox_inches="tight", facecolor="white")
plt.close(fig)
