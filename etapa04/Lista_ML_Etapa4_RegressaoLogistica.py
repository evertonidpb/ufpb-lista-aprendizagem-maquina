"""Etapa 4: regressao logistica sobre os 300 pontos da Etapa 1."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

BASE = Path(__file__).resolve().parent
with (BASE / "Lista_ML_Base_300_Pontos.csv").open(encoding="utf-8-sig", newline="") as f:
    registros = list(csv.DictReader(f))
ids = np.array([r["id"] for r in registros])
X = np.array([[float(r["x"]), float(r["y"])] for r in registros])
y = np.array([int(r["classe"]) for r in registros])
indices = np.arange(len(y))

idx_treino, idx_teste = train_test_split(
    indices, test_size=0.20, random_state=42, stratify=y
)
X_treino, X_teste = X[idx_treino], X[idx_teste]
y_treino, y_teste = y[idx_treino], y[idx_teste]
modelo = make_pipeline(
    StandardScaler(),
    LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000,
                       random_state=42)
)
modelo.fit(X_treino, y_treino)
previstos = modelo.predict(X_teste)
matriz = confusion_matrix(y_teste, previstos, labels=[1, 2])
acuracia = accuracy_score(y_teste, previstos)
precisao = precision_score(y_teste, previstos, pos_label=2)
revocacao = recall_score(y_teste, previstos, pos_label=2)
f1 = f1_score(y_teste, previstos, pos_label=2)

padronizador, regressao = modelo.steps[0][1], modelo.steps[1][1]
pesos = regressao.coef_[0] / padronizador.scale_
intercepto = regressao.intercept_[0] - np.dot(pesos, padronizador.mean_)
print("Treino:", len(idx_treino), "| Teste:", len(idx_teste))
print("Classes no teste:", np.bincount(y_teste, minlength=3)[1:].tolist())
print("Matriz de confusao (verdadeira x prevista):\n", matriz)
print(f"Acuracia={acuracia:.6f}; Precisao={precisao:.6f}")
print(f"Recall={revocacao:.6f}; F1={f1:.6f}")
print(f"Logit classe 2 = {intercepto:.6f} + {pesos[0]:.6f}*X + {pesos[1]:.6f}*Y")
print("Erros no teste:", ids[idx_teste][previstos != y_teste].tolist())

x_grade = np.linspace(X[:, 0].min() - 8, X[:, 0].max() + 8, 260)
y_grade = np.linspace(X[:, 1].min() - 9, X[:, 1].max() + 9, 230)
xx, yy = np.meshgrid(x_grade, y_grade)
malha = np.column_stack([xx.ravel(), yy.ravel()])
p_classe2 = modelo.predict_proba(malha)[:, 1].reshape(xx.shape)
fig, (ax, cm_ax) = plt.subplots(1, 2, figsize=(12, 5),
                                gridspec_kw={"width_ratios": [1.65, 1]})
fig.patch.set_facecolor("white")
cores = ["#24577b", "#008f8c"]
fundo = LinearSegmentedColormap.from_list("probabilidade", ["#e6eef7", "#f7f9fb", "#d4f3ed"])
ax.contourf(xx, yy, p_classe2, levels=np.linspace(0, 1, 21), cmap=fundo, alpha=0.95)
ax.contour(xx, yy, p_classe2, levels=[0.5], colors=["#102c43"], linewidths=2.6)
for classe, cor in zip([1, 2], cores):
    treino = idx_treino[y_treino == classe]
    teste = idx_teste[y_teste == classe]
    ax.scatter(X[treino, 0], X[treino, 1], s=24, color=cor, alpha=0.76,
               edgecolors="white", linewidths=0.3, label=f"Classe {classe} · treino")
    ax.scatter(X[teste, 0], X[teste, 1], s=55, facecolors="none", edgecolors=cor,
               linewidths=1.6, label=f"Classe {classe} · teste")
ax.set_title("Fronteira de decisão da Regressão Logística", fontsize=12, fontweight="bold", color="#142c43")
ax.set_xlabel("Variável X")
ax.set_ylabel("Variável Y")
ax.grid(alpha=0.15)
ax.legend(loc="upper left", fontsize=7.7, framealpha=0.96, ncol=2)
ax.text(0.98, 0.02, "Linha escura: P(Classe 2) = 0,50", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8, color="#142c43",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#d8e4e9"})
cm_ax.imshow(matriz, cmap=LinearSegmentedColormap.from_list("cm", ["#eef4f8", "#167c82"]), vmin=0, vmax=max(30, matriz.max()))
cm_ax.set_title("Matriz de confusão · teste", fontsize=12, fontweight="bold", color="#142c43")
cm_ax.set_xticks([0, 1], ["Classe 1", "Classe 2"])
cm_ax.set_yticks([0, 1], ["Classe 1", "Classe 2"])
cm_ax.set_xlabel("Classe prevista")
cm_ax.set_ylabel("Classe verdadeira")
for i in range(2):
    for j in range(2):
        cm_ax.text(j, i, str(matriz[i, j]), ha="center", va="center", fontsize=21,
                   fontweight="bold", color="white" if matriz[i, j] > 20 else "#142c43")
cm_ax.set_xticks(np.arange(-0.5, 2, 1), minor=True)
cm_ax.set_yticks(np.arange(-0.5, 2, 1), minor=True)
cm_ax.grid(which="minor", color="white", linewidth=2)
cm_ax.tick_params(which="minor", bottom=False, left=False)
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "Etapa4_RegressaoLogistica_Fronteira.png", dpi=210, bbox_inches="tight")
plt.close(fig)
