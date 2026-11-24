"""Etapa 5: RNA feedforward e comparação justa com a Regressão Logística."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

BASE = Path(__file__).resolve().parent
with (BASE / 'Lista_ML_Base_300_Pontos.csv').open(encoding='utf-8-sig', newline='') as f:
    registros = list(csv.DictReader(f))
ids = np.array([r['id'] for r in registros])
X = np.array([[float(r['x']), float(r['y'])] for r in registros])
y = np.array([int(r['classe']) for r in registros])
indices = np.arange(len(y))
idx_treino, idx_teste = train_test_split(
    indices, test_size=0.20, stratify=y, random_state=42)
X_treino, X_teste = X[idx_treino], X[idx_teste]
y_treino, y_teste = y[idx_treino], y[idx_teste]

rna = make_pipeline(StandardScaler(), MLPClassifier(
    hidden_layer_sizes=(12, 6), activation='relu', solver='lbfgs',
    alpha=0.01, max_iter=1200, random_state=42))
regressao = make_pipeline(StandardScaler(), LogisticRegression(
    C=1.0, solver='lbfgs', max_iter=1000, random_state=42))
for modelo in (rna, regressao):
    modelo.fit(X_treino, y_treino)

resultados = {}
for nome, modelo in [('RNA', rna), ('Regressão Logística', regressao)]:
    previsoes = modelo.predict(X_teste)
    resultados[nome] = {
        'matriz': confusion_matrix(y_teste, previsoes, labels=[1, 2]),
        'acuracia': accuracy_score(y_teste, previsoes),
        'precisao': precision_score(y_teste, previsoes, pos_label=2),
        'recall': recall_score(y_teste, previsoes, pos_label=2),
        'f1': f1_score(y_teste, previsoes, pos_label=2),
        'erros': ids[idx_teste][previsoes != y_teste].tolist()}
    print(nome, '| matriz:', resultados[nome]['matriz'].tolist())
    for metrica in ('acuracia', 'precisao', 'recall', 'f1'):
        print(' ', metrica, f"{resultados[nome][metrica]:.6f}")
    print(' Divergências no teste:', resultados[nome]['erros'])
print('Treino:', len(idx_treino), '| Teste:', len(idx_teste))
print('Classes no teste:', np.bincount(y_teste, minlength=3)[1:].tolist())
print('Camadas da RNA:', rna[-1].n_layers_, '| Iterações:', rna[-1].n_iter_)

xs = np.linspace(X[:, 0].min()-8, X[:, 0].max()+8, 280)
ys = np.linspace(X[:, 1].min()-9, X[:, 1].max()+9, 240)
xx, yy = np.meshgrid(xs, ys)
malha = np.column_stack((xx.ravel(), yy.ravel()))
fig, eixos = plt.subplots(1, 2, figsize=(12, 4.9), sharex=True, sharey=True)
fig.patch.set_facecolor('white')
fundo = LinearSegmentedColormap.from_list('prob', ['#e2eef6', '#fafbfc', '#d2efe9'])
for ax, (nome, modelo) in zip(eixos, [('Regressão Logística', regressao), ('RNA feedforward', rna)]):
    prob = modelo.predict_proba(malha)[:, 1].reshape(xx.shape)
    ax.contourf(xx, yy, prob, levels=np.linspace(0, 1, 21), cmap=fundo)
    ax.contour(xx, yy, prob, levels=[0.5], colors=['#142c43'], linewidths=2.4)
    for classe, cor in [(1, '#24577b'), (2, '#008f8c')]:
        tr = idx_treino[y_treino == classe]
        te = idx_teste[y_teste == classe]
        ax.scatter(X[tr, 0], X[tr, 1], s=16, color=cor, alpha=0.76,
                   edgecolors='white', linewidths=0.22, label=f'Classe {classe} | treino')
        ax.scatter(X[te, 0], X[te, 1], s=45, facecolors='none', edgecolors=cor,
                   linewidths=1.4, label=f'Classe {classe} | teste')
    ax.set_title(nome, fontsize=12, fontweight='bold', color='#142c43')
    ax.set_xlabel('Variável X')
    ax.grid(alpha=0.13)
    ax.text(0.98, 0.02, 'Fronteira: P(Classe 2) = 0,50', transform=ax.transAxes,
            ha='right', fontsize=8, color='#142c43',
            bbox=dict(facecolor='white', edgecolor='#dce6ea', boxstyle='round,pad=0.3'))
eixos[0].set_ylabel('Variável Y')
eixos[0].legend(fontsize=7.5, loc='upper left', ncol=2, framealpha=0.95)
fig.suptitle('Fronteiras de decisão com os mesmos dados e divisão de teste',
             fontsize=13, fontweight='bold', color='#142c43')
fig.tight_layout(rect=(0, 0, 1, 0.94), w_pad=2)
fig.savefig(BASE / 'Etapa5_RNA_Comparacao_Fronteiras.png', dpi=210, bbox_inches='tight')
plt.close(fig)
