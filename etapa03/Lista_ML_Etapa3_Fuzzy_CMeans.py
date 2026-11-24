"""Etapa 3: Fuzzy C-means reproduzivel sobre o CSV da Etapa 1."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import adjusted_rand_score, confusion_matrix

BASE = Path(__file__).resolve().parent
ENTRADA = BASE / "Lista_ML_Base_300_Pontos.csv"
SAIDA = BASE / "Etapa3_Pertinencias_FCM.csv"
IMAGEM = BASE / "Etapa3_FuzzyCMeans_Graficos.png"
C, M, TOL, MAX_ITER, SEED = 2, 2.0, 1e-7, 1000, 42

with ENTRADA.open(encoding="utf-8-sig", newline="") as arq:
    linhas = list(csv.DictReader(arq))
ids = [r["id"] for r in linhas]
X = np.array([[float(r["x"]), float(r["y"])] for r in linhas])
y = np.array([int(r["classe"]) for r in linhas])
assert X.shape == (300, 2) and set(y) == {1, 2}

rng = np.random.default_rng(SEED)
U = rng.random((C, len(X)))
U /= U.sum(axis=0, keepdims=True)
for it in range(1, MAX_ITER + 1):
    pesos = U ** M
    centros = (pesos @ X) / pesos.sum(axis=1, keepdims=True)
    dist = np.linalg.norm(X[None, :, :] - centros[:, None, :], axis=2)
    dist = np.maximum(dist, 1e-12)
    inversos = dist ** (-2.0 / (M - 1.0))
    novo_U = inversos / inversos.sum(axis=0, keepdims=True)
    diferenca = np.max(np.abs(novo_U - U))
    U = novo_U
    if diferenca < TOL:
        break

# Os indices dos clusters sao arbitrarios; ordenar pela coordenada X.
ordem = np.argsort(centros[:, 0])
centros, U = centros[ordem], U[ordem]
pert_1, pert_2 = U[0], U[1]
rotulos = np.argmax(U, axis=0) + 1
conf = confusion_matrix(y, rotulos, labels=[1, 2])
ari = adjusted_rand_score(y, rotulos)
fpc = float(np.sum(U * U) / len(X))
objetivo = float(np.sum((U ** M) * (dist[ordem] ** 2)))

with SAIDA.open("w", encoding="utf-8-sig", newline="") as arq:
    gravador = csv.writer(arq)
    gravador.writerow(["id", "x", "y", "classe_verdadeira", "membership_classe_1", "membership_classe_2", "cluster_fcm"])
    for k, registro in enumerate(linhas):
        gravador.writerow([ids[k], registro["x"], registro["y"], y[k],
                           f"{pert_1[k]:.10f}", f"{pert_2[k]:.10f}", rotulos[k]])

cores = LinearSegmentedColormap.from_list("ufpb", ["#142c43", "#e9f1f3", "#07958a"])
fig, eixos = plt.subplots(1, 2, figsize=(12.8, 5.2))
pontos = eixos[0].scatter(X[:, 0], X[:, 1], c=pert_1, cmap=cores,
                         vmin=0, vmax=1, s=29, edgecolor="white", linewidth=0.3)
eixos[0].scatter(centros[:, 0], centros[:, 1], marker="X", s=195,
                c=["#07958a", "#142c43"], edgecolor="white", linewidth=1.6)
eixos[0].set(title="Pertinencia fuzzy a Classe 1", xlabel="Variavel X", ylabel="Variavel Y")
barra = fig.colorbar(pontos, ax=eixos[0], fraction=0.046, pad=0.02)
barra.set_label("Membership de Classe 1 (0 a 1)")
eixos[1].hist(pert_1[y == 1], bins=np.linspace(0, 1, 21), alpha=0.72,
              color="#07958a", label="Classe verdadeira 1", edgecolor="white")
eixos[1].hist(pert_1[y == 2], bins=np.linspace(0, 1, 21), alpha=0.66,
              color="#142c43", label="Classe verdadeira 2", edgecolor="white")
eixos[1].axvline(0.5, color="#d47e41", linewidth=1.5, linestyle="--")
eixos[1].set(title="Distribuicao dos graus de pertinencia", xlabel="Membership de Classe 1", ylabel="Numero de pontos")
eixos[1].legend(fontsize=8)
for eixo in eixos:
    eixo.grid(alpha=0.14)
fig.tight_layout()
fig.savefig(IMAGEM, dpi=190, bbox_inches="tight")
plt.close(fig)

print("Iteracoes:", it, "| Variacao maxima:", f"{diferenca:.2g}")
print("Centroides:", np.round(centros, 6))
print("Matriz de confusao:\n", conf)
print("ARI:", round(ari, 6), "| FPC:", round(fpc, 6), "| Objetivo:", round(objetivo, 6))
print("Membr. Classe 1 >= 0.9:", int(np.sum(pert_1 >= 0.9)))
print("Membr. Classe 1 <= 0.1:", int(np.sum(pert_1 <= 0.1)))
print("0.4 <= Membr. Classe 1 <= 0.6:", int(np.sum((pert_1 >= 0.4) & (pert_1 <= 0.6))))
print("CSV salvo:", SAIDA.name, "| Grafico:", IMAGEM.name)
