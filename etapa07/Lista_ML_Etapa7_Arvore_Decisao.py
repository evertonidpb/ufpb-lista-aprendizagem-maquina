"""Etapa 7: arvore de decisao para os 300 pontos originais da lista."""
from pathlib import Path
import csv
import hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Permite gerar figuras sem interface grafica.
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

BASE = Path(__file__).resolve().parent
CSV = BASE / 'Lista_ML_Base_300_Pontos.csv'
SHA256_REFERENCIA = '04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5'
sha256 = hashlib.sha256(CSV.read_bytes()).hexdigest()
if sha256 != SHA256_REFERENCIA:
    raise ValueError('CSV diferente da base original da Etapa 1. Confira o arquivo.')
with CSV.open(encoding='utf-8-sig', newline='') as arquivo:
    linhas = list(csv.DictReader(arquivo))
identificadores = np.array([linha['id'] for linha in linhas])
X = np.array([[float(r['x']), float(r['y'])] for r in linhas])
y = np.array([int(r['classe']) for r in linhas])
assert X.shape == (300, 2)
assert np.bincount(y)[1:].tolist() == [150, 150]

indices = np.arange(len(y))
idx_treino, idx_teste = train_test_split(
    indices, test_size=0.20, stratify=y, random_state=42)
X_treino, X_teste = X[idx_treino], X[idx_teste]
y_treino, y_teste = y[idx_treino], y[idx_teste]
modelo = DecisionTreeClassifier(
    criterion='gini', splitter='best', max_depth=3,
    min_samples_split=2, min_samples_leaf=2,
    ccp_alpha=0.0, random_state=42)
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)
matriz = confusion_matrix(y_teste, previsoes, labels=[1, 2])
tp, fn = matriz[0]
fp, tn = matriz[1]
metricas = {
    'Acuracia': accuracy_score(y_teste, previsoes),
    'Precisao': precision_score(y_teste, previsoes, pos_label=1),
    'Recall': recall_score(y_teste, previsoes, pos_label=1),
    'F1-score': f1_score(y_teste, previsoes, pos_label=1),
}
print('CSV SHA-256:', sha256)
print('Total: 300 | Treino:', len(idx_treino), '| Teste:', len(idx_teste))
print('Classes no teste:', np.bincount(y_teste)[1:].tolist())
print('Profundidade:', modelo.get_depth(), '| Folhas:', modelo.get_n_leaves())
print('Acuracia no treino:', f'{modelo.score(X_treino, y_treino):.4%}')
print('Matriz [classe real x prevista], ordem [1,2]:\n', matriz)
print(f'TP={tp} | FN={fn} | FP={fp} | TN={tn} (positiva: classe 1)')
for nome, valor in metricas.items():
    print(f'{nome}: {valor:.6f} ({valor:.2%})')
print('Erros no teste:', identificadores[idx_teste][previsoes != y_teste].tolist())
print('Importancia dos atributos [X,Y]:', modelo.feature_importances_)
print('Regras da arvore:\n' + export_text(modelo, feature_names=['X', 'Y']))

# Figura 7: estrutura da arvore de decisao.
fig, ax = plt.subplots(figsize=(12, 5.4), facecolor='white')
no_textos = plot_tree(
    modelo, ax=ax, feature_names=['X', 'Y'],
    class_names=['Classe 1', 'Classe 2'], filled=False,
    rounded=True, impurity=True, proportion=False,
    precision=2, fontsize=10)
for no in no_textos:
    caixa = no.get_bbox_patch()
    if caixa is not None:
        texto = no.get_text()
        fundo = '#e1eff8' if 'class = Classe 1' in texto else '#d7f0ed'
        caixa.set_facecolor(fundo)
        caixa.set_edgecolor('#25485e')
        caixa.set_linewidth(1.1)
ax.set_title('Estrutura da arvore de decisao | CART / Gini',
             fontsize=16, fontweight='bold', color='#142c43', pad=12)
fig.tight_layout(pad=1.2)
fig.savefig(BASE / 'Etapa7_Arvore_Estrutura.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close(fig)

# Figura 8: fronteira de decisao e matriz de confusao identificada.
x_eixo = np.linspace(X[:, 0].min()-8, X[:, 0].max()+8, 320)
y_eixo = np.linspace(X[:, 1].min()-9, X[:, 1].max()+9, 260)
xx, yy = np.meshgrid(x_eixo, y_eixo)
regioes = modelo.predict(np.column_stack([xx.ravel(), yy.ravel()]))
regioes = regioes.reshape(xx.shape)
fig, (ax, ax_cm) = plt.subplots(
    1, 2, figsize=(12.3, 5.2), facecolor='white',
    gridspec_kw={'width_ratios': [1.65, 1]})
ax.contourf(xx, yy, regioes, levels=[0.5, 1.5, 2.5],
            colors=['#e2edf7', '#d5f0eb'], alpha=0.95)
ax.contour(xx, yy, regioes, levels=[1.5], colors='#142c43', linewidths=2)
for classe, cor in [(1, '#24577b'), (2, '#008f8c')]:
    treino = idx_treino[y_treino == classe]
    teste = idx_teste[y_teste == classe]
    ax.scatter(X[treino, 0], X[treino, 1], s=24, c=cor,
               alpha=0.80, edgecolor='white', linewidth=0.3,
               label=f'Classe {classe} | treino')
    ax.scatter(X[teste, 0], X[teste, 1], s=58, facecolors='none',
               edgecolors=cor, linewidths=1.6,
               label=f'Classe {classe} | teste')
ax.set(title='Fronteira de decisao | arvore',
       xlabel='Variavel X', ylabel='Variavel Y')
ax.grid(alpha=0.12)
ax.legend(loc='upper left', fontsize=7.7, ncol=2)
ax_cm.imshow(matriz, cmap=ListedColormap(['#e7f1f6', '#087e86']),
             vmin=0, vmax=30)
ax_cm.set(title='Matriz de confusao | teste',
          xlabel='Classe prevista', ylabel='Classe verdadeira')
ax_cm.set_xticks([0, 1], ['Classe 1', 'Classe 2'])
ax_cm.set_yticks([0, 1], ['Classe 1', 'Classe 2'])
rotulos = [['TP', 'FN'], ['FP', 'TN']]
for i in range(2):
    for j in range(2):
        cor_texto = 'white' if matriz[i, j] >= 16 else '#142c43'
        ax_cm.text(j, i, f'{rotulos[i][j]}\n{matriz[i, j]}',
                   ha='center', va='center', fontsize=17,
                   fontweight='bold', color=cor_texto)
fig.tight_layout(pad=1.8)
fig.savefig(BASE / 'Etapa7_Fronteira_Matriz.png', dpi=210,
            bbox_inches='tight', facecolor='white')
plt.close(fig)
print('Figuras gravadas: Etapa7_Arvore_Estrutura.png e Etapa7_Fronteira_Matriz.png')
