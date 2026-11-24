"""Etapa 8: KNN com a base fixa de 300 pontos da Lista de ML/UFPB."""
from pathlib import Path
import csv
import hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Gera os graficos tambem em servidores sem tela.
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

BASE = Path(__file__).resolve().parent
ARQUIVO = BASE / 'Lista_ML_Base_300_Pontos.csv'
HASH_ESPERADO = '04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5'
assert ARQUIVO.is_file(), f'CSV ausente: {ARQUIVO}'
hash_obtido = hashlib.sha256(ARQUIVO.read_bytes()).hexdigest()
assert hash_obtido == HASH_ESPERADO, 'CSV difere da base original: confira o pacote.'
with ARQUIVO.open(encoding='utf-8-sig', newline='') as f:
    registros = list(csv.DictReader(f))
ids = np.array([r['id'] for r in registros])
X = np.array([[float(r['x']), float(r['y'])] for r in registros])
y = np.array([int(r['classe']) for r in registros])
assert X.shape == (300, 2) and np.bincount(y)[1:].tolist() == [150, 150]
indices = np.arange(300)
idx_tr, idx_te = train_test_split(
    indices, test_size=0.20, stratify=y, random_state=42)
X_tr, X_te = X[idx_tr], X[idx_te]
y_tr, y_te = y[idx_tr], y[idx_te]

KS = [1, 3, 5, 7, 9, 15]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
resultado = {}
for k in KS:
    # Padronizador ajustado somente no treino de cada dobra, sem vazamento.
    pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(
        n_neighbors=k, weights='uniform', metric='minkowski', p=2))
    pont_cv = cross_val_score(pipeline, X_tr, y_tr, cv=cv, scoring='accuracy')
    pipeline.fit(X_tr, y_tr)
    pred = pipeline.predict(X_te)
    matriz = confusion_matrix(y_te, pred, labels=[1, 2])
    resultado[k] = {
        'modelo': pipeline, 'cv': pont_cv, 'pred': pred, 'matriz': matriz,
        'acc': accuracy_score(y_te, pred),
        'prec': precision_score(y_te, pred, pos_label=1),
        'rec': recall_score(y_te, pred, pos_label=1),
        'f1': f1_score(y_te, pred, pos_label=1),
    }
# A selecao do hiperparametro ocorre so com a validacao cruzada do treino.
k_escolhido = max(KS, key=lambda k: (resultado[k]['cv'].mean(), -k))
r = resultado[k_escolhido]
tp, fn = r['matriz'][0]
fp, tn = r['matriz'][1]
print('SHA-256:', hash_obtido)
print('Total: 300 | Treino:', len(idx_tr), '| Teste:', len(idx_te))
print('Classes de teste:', np.bincount(y_te)[1:].tolist())
print('k | CV media | Acuracia | Precisao | Recall | F1 | Erros (IDs)')
for k in KS:
    a = resultado[k]
    erros = ids[idx_te][a['pred'] != y_te].tolist()
    print(f"{k:2d} | {a['cv'].mean():.6f} | {a['acc']:.6f} | "
          f"{a['prec']:.6f} | {a['rec']:.6f} | {a['f1']:.6f} | {erros}")
print('k selecionado por CV:', k_escolhido)
print('Matriz [real x prevista], labels=[1,2]:\n', r['matriz'])
print(f'TP={tp} | FN={fn} | FP={fp} | TN={tn} (Classe 1 positiva)')

NAVY, TEAL = '#254f73', '#008b89'
XGRID, YGRID = np.meshgrid(
    np.linspace(X[:, 0].min()-7, X[:, 0].max()+7, 340),
    np.linspace(X[:, 1].min()-9, X[:, 1].max()+9, 280))
pontos_grid = np.column_stack([XGRID.ravel(), YGRID.ravel()])
fig, eixos = plt.subplots(3, 2, figsize=(11.5, 12.6), facecolor='white')
for ax, k in zip(eixos.flat, KS):
    rr = resultado[k]
    z = rr['modelo'].predict(pontos_grid).reshape(XGRID.shape)
    ax.contourf(XGRID, YGRID, z, levels=[0.5, 1.5, 2.5],
                colors=['#e4eef7', '#d8f0ea'], alpha=0.96)
    ax.contour(XGRID, YGRID, z, levels=[1.5], colors='#20384e',
               linewidths=1.35)
    for classe, cor in [(1, NAVY), (2, TEAL)]:
        ind_t = idx_tr[y_tr == classe]
        ind_v = idx_te[y_te == classe]
        ax.scatter(X[ind_t, 0], X[ind_t, 1], s=12, color=cor, alpha=0.72,
                   edgecolors='white', linewidths=0.25)
        ax.scatter(X[ind_v, 0], X[ind_v, 1], s=27, facecolors='none',
                   edgecolors=cor, linewidths=0.9)
    selecao = '  •  selecionado por CV' if k == k_escolhido else ''
    ax.set_title(f'k = {k}  |  teste: {rr["acc"]:.2%}{selecao}',
                 fontsize=11.5, color='#172d43', fontweight='bold')
    ax.set_xlabel('Variável X', fontsize=9)
    ax.set_ylabel('Variável Y', fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(alpha=0.13)
fig.suptitle('KNN | Fronteiras de decisão por número de vizinhos',
             fontsize=17, color='#162e46', weight='bold', y=0.997)
fig.text(0.5, 0.008, 'Pontos preenchidos: treino   •   círculos vazados: teste   |   ' 
         'Classe 1: azul   •   Classe 2: verde-petróleo',
         ha='center', fontsize=9, color='#486173')
fig.tight_layout(rect=[0, 0.022, 1, 0.975], h_pad=2.0, w_pad=1.0)
fig.savefig(BASE / 'Etapa8_KNN_Fronteiras_Por_K.png', dpi=170,
            bbox_inches='tight', facecolor='white')
plt.close(fig)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2),
                              gridspec_kw={'width_ratios': [1.15, 1]},
                              facecolor='white')
ax1.plot(KS, [resultado[k]['cv'].mean()*100 for k in KS],
         marker='o', lw=2.5, c=NAVY, label='Acurácia CV (treino)')
ax1.plot(KS, [resultado[k]['acc']*100 for k in KS],
         marker='s', lw=2.2, c=TEAL, label='Acurácia teste (descritiva)')
ax1.axvline(k_escolhido, ls='--', alpha=0.55, c='#9a793e')
ax1.set(xticks=KS, ylim=(95, 100.7), xlabel='Número de vizinhos (k)',
        ylabel='Acurácia (%)', title='Seleção por validação cruzada')
ax1.grid(alpha=0.22)
ax1.legend(loc='lower right', fontsize=9)
mat = r['matriz']
ax2.imshow(mat, cmap=ListedColormap(['#e6f0f6', '#087d86']),
           vmin=0, vmax=30)
ax2.set(title=f'Matriz de confusão | k={k_escolhido}',
        xlabel='Classe prevista', ylabel='Classe verdadeira')
ax2.set_xticks([0, 1], ['Classe 1', 'Classe 2'])
ax2.set_yticks([0, 1], ['Classe 1', 'Classe 2'])
for i, linha in enumerate([['TP', 'FN'], ['FP', 'TN']]):
    for j, nome in enumerate(linha):
        cor = 'white' if mat[i, j] >= 16 else '#193b56'
        ax2.text(j, i, f'{nome}\n{mat[i, j]}', ha='center', va='center',
                 fontsize=18, fontweight='bold', color=cor)
fig.suptitle('KNN | Validação do hiperparâmetro e avaliação final',
             fontsize=16, weight='bold', color='#172d43', y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.93], w_pad=3.0)
fig.savefig(BASE / 'Etapa8_KNN_Selecao_Matriz.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close(fig)
print('Figuras: Etapa8_KNN_Fronteiras_Por_K.png e Etapa8_KNN_Selecao_Matriz.png')
