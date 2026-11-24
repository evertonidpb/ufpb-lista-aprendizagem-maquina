"""Confere o conjunto de dados e executa os oito experimentos isoladamente."""
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
RELATORIOS = ROOT / "relatorios"
RELATORIOS.mkdir(exist_ok=True)
SHA = "04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5"

PROGRAMAS = {
  1: ("Lista_ML_Etapa1_Reproducao_Exata.py", ["Arquivo idêntico à referência: SIM"]),
  2: ("Lista_ML_Etapa2_KMeans.py", ["ARI=0.960267", "acertos=297/300"]),
  3: ("Lista_ML_Etapa3_Fuzzy_CMeans.py", ["Iteracoes: 15", "FPC: 0.878095"]),
  4: ("Lista_ML_Etapa4_RegressaoLogistica.py", ["Treino: 240 | Teste: 60", "Acuracia=1.000000", "F1=1.000000"]),
  5: ("Lista_ML_Etapa5_RNA.py", ["Treino: 240 | Teste: 60", "Camadas da RNA: 4 | Iterações: 38"]),
  6: ("Lista_ML_Etapa6_SVM.py", ["Acuracia: 1.000000", "F1-score: 1.000000", "Vetores de suporte por classe: [11, 11]"]),
  7: ("Lista_ML_Etapa7_Arvore_Decisao.py", ["Acuracia: 1.000000", "F1-score: 1.000000"]),
  8: ("Lista_ML_Etapa8_KNN.py", ["k selecionado por CV: 5", "TP=30 | FN=0 | FP=0 | TN=30"]),
}

def csv_valido(arquivo: Path) -> bool:
    return arquivo.is_file() and hashlib.sha256(arquivo.read_bytes()).hexdigest() == SHA

falhas = []
for etapa, (script, esperados) in PROGRAMAS.items():
    pasta = ROOT / f"etapa{etapa:02d}"
    dados = pasta / "Lista_ML_Base_300_Pontos.csv"
    if not csv_valido(dados):
        falhas.append(f"Etapa {etapa}: CSV ausente ou SHA-256 diferente")
        print(f"[FALHA] Etapa {etapa}: CSV inválido")
        continue
    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"
    env.setdefault("OPENBLAS_NUM_THREADS", "1")
    try:
        proc = subprocess.run([sys.executable, str(pasta/script)], cwd=pasta,
                              env=env, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=180)
        (RELATORIOS/f"etapa{etapa:02d}.txt").write_text(proc.stdout, encoding="utf-8")
        ausentes = [frase for frase in esperados if frase not in proc.stdout]
        if proc.returncode or ausentes or not csv_valido(dados):
            falhas.append(f"Etapa {etapa}: retorno={proc.returncode}; marcadores ausentes={ausentes}")
            print(f"[FALHA] Etapa {etapa}")
        else:
            print(f"[OK] Etapa {etapa} — {script}")
    except Exception as err:
        falhas.append(f"Etapa {etapa}: {err}")
        print(f"[FALHA] Etapa {etapa}: {err}")

print(f"\nRelatórios: {RELATORIOS}")
if falhas:
    print("Problemas encontrados:")
    for f in falhas:print(" -",f)
    sys.exit(1)
print("SUCESSO: oito etapas executadas e resultados esperados confirmados.")
