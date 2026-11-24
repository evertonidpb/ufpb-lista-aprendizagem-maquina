"""Etapa 6: SVM RBF nos 300 pontos fixos da Etapa 1."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

BASE = Path(__file__).resolve().parent
with (BASE / 'Lista_ML_Base_300_Pontos.csv').open(
        encoding='utf-8-sig', newline='') as arquivo:
    registros = list(csv.DictReader(arquivo))
ids = np.array([r['id'] for r in registros])
X = np.array([[float(r['x']), float(r['y'])] for r in registros])
y = np.array([int(r['classe']) for r in registros])
assert len(y) == 300 and np.bincount(y)[1:].tolist() == [150, 150]
indices = np.arange(len(y))
idx_treino, idx_teste = train_test_split(
    indices, test_size=0.20, stratify=y, random_state=42)
X_treino, X_teste = X[idx_treino], X[idx_teste]
y_treino, y_teste = y[idx_treino], y[idx_teste]

modelo = make_pipeline(StandardScaler(), SVC(
    kernel='rbf', C=1.0, gamma='scale', tol=1e-3,
    shrinking=True, cache_size=200, random_state=42))
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)
matriz = confusion_matrix(y_teste, previsoes, labels=[1, 2])
metricas = {
    'Acuracia': accuracy_score(y_teste, previsoes),
    'Precisao': precision_score(y_teste, previsoes, pos_label=1),
    'Recall': recall_score(y_teste, previsoes, pos_label=1),
    'F1-score': f1_score(y_teste, previsoes, pos_label=1),
}
print('Conjunto: 300 pontos | Treino:', len(idx_treino),
      '| Teste:', len(idx_teste))
print('Classes no teste:', np.bincount(y_teste)[1:].tolist())
print('Matriz de confusao (real x prevista):\n', matriz)
for nome, valor in metricas.items():
    print(f'{nome}: {valor:.6f} ({valor:.2%})')
print('Vetores de suporte por classe:', modelo[-1].n_support_.tolist())
print('Identificadores incorretos:',
      ids[idx_teste][previsoes != y_teste].tolist())

x_grade = np.linspace(X[:, 0].min()-8, X[:, 0].max()+8, 260)
y_grade = np.linspace(X[:, 1].min()-9, X[:, 1].max()+9, 240)
xx, yy = np.meshgrid(x_grade, y_grade)
malha = np.column_stack((xx.ravel(), yy.ravel()))
funcao = modelo.decision_function(malha).reshape(xx.shape)
fig, (ax, ax_cm) = plt.subplots(
    1, 2, figsize=(12, 4.95),
    gridspec_kw={'width_ratios': [1.7, 1]})
fig.patch.set_facecolor('white')
fundo = LinearSegmentedColormap.from_list(
    'regioes', ['#dceaf5', '#f7fafb', '#d2ede9'])
limite = max(1.0, np.percentile(np.abs(funcao), 95))
ax.contourf(xx, yy, funcao, levels=np.linspace(-limite, limite, 25),
            cmap=fundo, extend='both')
ax.contour(xx, yy, funcao, levels=[0], colors=['#142c43'],
           linewidths=2.6)
for classe, cor in [(1, '#24577b'), (2, '#008f8c')]:
    treino = idx_treino[y_treino == classe]
    teste = idx_teste[y_teste == classe]
    ax.scatter(X[treino, 0], X[treino, 1], s=23, c=cor,
               alpha=0.77, edgecolors='white', linewidths=0.25,
               label=f'Classe {classe} | treino')
    ax.scatter(X[teste, 0], X[teste, 1], s=55,
               facecolors='none', edgecolors=cor, linewidths=1.5,
               label=f'Classe {classe} | teste')
suportes = X_treino[modelo[-1].support_]
ax.scatter(suportes[:, 0], suportes[:, 1], s=105,
           facecolors='none', edgecolors='#172c40',
           linewidths=1.1, marker='s', label='Vetores de suporte')
ax.set(title='Fronteira de decisao do SVM (RBF)',
       xlabel='Variavel X', ylabel='Variavel Y')
ax.grid(alpha=0.13)
ax.legend(fontsize=7.4, loc='upper left', ncol=2)
mapa_cm = LinearSegmentedColormap.from_list(
    'matriz', ['#eaf2f8', '#187c82'])
ax_cm.imshow(matriz, cmap=mapa_cm, vmin=0, vmax=30)
ax_cm.set(title='Matriz de confusao | teste\nClasse 1 = positiva',
          xlabel='Classe prevista', ylabel='Classe verdadeira')
ax_cm.set_xticks([0, 1], ['Classe 1', 'Classe 2'])
ax_cm.set_yticks([0, 1], ['Classe 1', 'Classe 2'])
for i in range(2):
    for j in range(2):
        ax_cm.text(j, i, f'{(("TP", "FN"), ("FP", "TN"))[i][j]}\n{matriz[i, j]}', ha='center',
                   va='center', fontsize=16, fontweight='bold',
                   color='white' if matriz[i, j] >= 16 else '#142c43')
fig.tight_layout(pad=1.8)
fig.savefig(BASE / 'Etapa6_SVM_Fronteira_Matriz.png',
            dpi=210, bbox_inches='tight')
plt.close(fig)
