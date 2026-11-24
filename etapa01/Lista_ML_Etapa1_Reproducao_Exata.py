"""Reproduz exatamente o CSV da Etapa 1 da lista de Aprendizagem de Máquina.

Dependência testada: NumPy 2.3.5.
Execução: python Lista_ML_Etapa1_Reproducao_Exata.py
"""

import csv
import hashlib
from pathlib import Path

import numpy as np

# A semente fixa torna a sequência de sorteios reproduzível.
rng = np.random.default_rng(42)

# O arquivo será criado na mesma pasta deste script.
saida = Path(__file__).resolve().parent / "Lista_ML_Base_300_Pontos.csv"

# Parâmetros na ordem: classe, quantidade, média X, média Y, variância X, variância Y.
classes = [
    (1, 150, 25, 10, 100, 25),
    (2, 150, 60, 30, 36, 144),
]

with saida.open("w", newline="", encoding="utf-8-sig") as arquivo:
    # LF padronizado para gerar o mesmo CSV tanto no Windows quanto no Linux.
    escritor = csv.writer(arquivo, lineterminator="\n")
    escritor.writerow(["id", "x", "y", "classe"])

    for classe, quantidade, media_x, media_y, var_x, var_y in classes:
        # O NumPy recebe o DESVIO-PADRÃO, não a variância.
        valores_x = rng.normal(media_x, np.sqrt(var_x), quantidade)
        valores_y = rng.normal(media_y, np.sqrt(var_y), quantidade)

        for indice, (x, y) in enumerate(zip(valores_x, valores_y), start=1):
            escritor.writerow([f"C{classe}-{indice:03d}", f"{x:.10f}", f"{y:.10f}", classe])

# Conferência: tamanho do arquivo e assinatura SHA-256 da referência.
sha256 = hashlib.sha256(saida.read_bytes()).hexdigest()
sha256_esperado = "04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5"

print(f"Arquivo gerado: {saida}")
print("Registros: 300 (150 da Classe 1 e 150 da Classe 2)")
print(f"NumPy: {np.__version__}")
print(f"SHA-256: {sha256}")
print("Arquivo idêntico à referência:", "SIM" if sha256 == sha256_esperado else "NÃO")

# Complemento de visualização para reproduzir a Figura 1 da resolução.
# O código original de geração de pontos permanece inalterado.
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

import numpy as np

fig, ax = plt.subplots(figsize=(12.4, 7.2))
fig.patch.set_facecolor("white")
cores = {1: "#2d7eb7", 2: "#1ca89d"}
chi2_95 = 5.991464547107979  # quantil de 95% da distribuição qui-quadrado com 2 g.l.

with saida.open(encoding="utf-8-sig", newline="") as base_csv:
    pontos = list(csv.DictReader(base_csv))

for classe, mx, my, vx, vy in [(1, 25, 10, 100, 25), (2, 60, 30, 36, 144)]:
    dados_classe = np.array([
        [float(linha["x"]), float(linha["y"])]
        for linha in pontos if int(linha["classe"]) == classe
    ])
    ax.scatter(dados_classe[:, 0], dados_classe[:, 1], s=27, alpha=0.77,
               color=cores[classe], label=f"Classe {classe} (150 pontos)")
    ax.scatter([mx], [my], marker="X", s=230, color=cores[classe],
               edgecolor="#14334a", linewidth=1.2, zorder=4)
    elipse = Ellipse((mx, my), width=2*np.sqrt(vx*chi2_95),
                     height=2*np.sqrt(vy*chi2_95), angle=0,
                     fill=False, lw=1.8, ls=(0, (5, 4)), color=cores[classe])
    ax.add_patch(elipse)

ax.set_title("Distribuição dos 300 pontos simulados", fontsize=19,
             fontweight="bold", color="#19334e", pad=14)
ax.text(0.01, 1.015, "150 observações por classe | médias teóricas marcadas com X",
        transform=ax.transAxes, fontsize=10.4, color="#506b80")
ax.set_xlabel("Variável X", fontsize=12, color="#19334e")
ax.set_ylabel("Variável Y", fontsize=12, color="#19334e")
ax.grid(alpha=.19)
ax.legend(loc="upper left", fontsize=10)
ax.set_axisbelow(True)
fig.tight_layout()
grafico = saida.with_name("Lista_ML_Etapa1_Grafico.png")
fig.savefig(grafico, dpi=170, facecolor="white", bbox_inches="tight")
plt.close(fig)
print("Figura da Etapa 1:", grafico.name)
