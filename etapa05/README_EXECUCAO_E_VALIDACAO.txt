UNIVERSIDADE FEDERAL DA PARAÍBA — CENTRO DE INFORMÁTICA
LISTA DE EXERCÍCIOS — APRENDIZAGEM DE MÁQUINA
ETAPA 5 — REDE NEURAL ARTIFICIAL (FEEDFORWARD)
GUIA DE REPRODUÇÃO E VALIDAÇÃO LOCAL (DEBIAN 13 / LINUX)
========================================================================

1. OBJETIVO E CONTEÚDO

Este pacote foi elaborado para que qualquer pessoa reproduza o experimento
acadêmico em uma máquina Linux independente. Contém EXATAMENTE 3 arquivos:

  Lista_ML_Base_300_Pontos.csv
  Lista_ML_Etapa5_RNA.py
  README_EXECUCAO_E_VALIDACAO.txt

A base é fixa: 300 pontos gerados por NumPy (150 por classe), semente 42.
O arquivo CSV deve ser mantido com o script na mesma pasta.
O código original do documento usa Classe 2 como classe positiva na avaliação. A arquitetura é MLP (12, 6) com solver L-BFGS, semente 42.

2. REQUISITOS

- Debian 13 (ou Linux equivalente); Python 3.13 recomendado.
- Acesso à internet SOMENTE para instalar os pacotes Python.
- Não exige Docker, WSL, GPU, Jupyter ou acesso ao GitHub.
- Ambiente de conferência: NumPy 2.3.5; scikit-learn 1.8.0;
  Matplotlib 3.10.8; pandas 2.2.3 quando aplicável.
- Evite executar o script diretamente sobre a sua cópia de referência
  sem antes fazer backup: a Etapa 1 regrava o CSV original.

3. INSTALAR FERRAMENTAS DO DEBIAN 13

Abra o terminal e execute (se estiver como root, retire sudo):

  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip unzip
  python3 --version

4. EXTRAIR O PACOTE

Este exemplo pressupõe que o ZIP foi baixado para ~/Downloads.
Se não estiver lá, ajuste o caminho do arquivo.

  mkdir -p ~/ufpb-lista-ml/etapa5
  cd ~/ufpb-lista-ml/etapa5
  unzip ~/Downloads/UFPB_Etapa_05_Rede_Neural_Artificial_Pacote_Reproducao.zip
  ls -lah

Deve listar precisamente os três arquivos do pacote.

5. CRIAR AMBIENTE VIRTUAL E INSTALAR BIBLIOTECAS

  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install numpy==2.3.5 matplotlib==3.10.8 scikit-learn==1.8.0

Confirme as versões instaladas:

  python -m pip list

6. CONFERIR O CSV ANTES DO TESTE

  sha256sum Lista_ML_Base_300_Pontos.csv

SHA-256 esperado:
  04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5

É esperado que apareça esse hash seguido do nome do arquivo.
O arquivo usa UTF-8 com BOM, cabeçalho id,x,y,classe e 300 linhas de dados.

7. EXECUTAR O EXPERIMENTO

  python Lista_ML_Etapa5_RNA.py

RESULTADOS DE REFERÊNCIA:
  RNA e Regressão Logística: matriz [[30, 0], [0, 30]]; acurácia, precisão, recall, F1 = 1.000000; RNA: 38 iterações

ARQUIVOS PRODUZIDOS AO EXECUTAR:
  - Etapa5_RNA_Comparacao_Fronteiras.png

8. ABRIR GRÁFICOS E CONFERIR RESULTADOS

  xdg-open Etapa5_RNA_Comparacao_Fronteiras.png

Para conferir os arquivos gerados:
  ls -lh

Considere que pequenas mudanças na aparência dos gráficos podem ocorrer
entre backends/fontes, mesmo quando valores e previsões não mudam.

9. REPETIR O EXPERIMENTO EM OUTRO DIA

  cd ~/ufpb-lista-ml/etapa5
  source .venv/bin/activate
  python Lista_ML_Etapa5_RNA.py
  deactivate

10. ERROS COMUNS

- 'python: command not found': execute dentro do ambiente .venv ativado.
- 'No module named ...': reinstale as dependências do item 5.
- 'externally-managed-environment': crie/ative o venv; não use pip
  globalmente nem '--break-system-packages'.
- 'No such file ...csv': coloque o CSV na MESMA pasta do script.
- 'unzip: cannot find': confirme o local onde o navegador salvou o ZIP.
- 'xdg-open' não encontra aplicativo: use o gerenciador de arquivos do
  ambiente gráfico do Debian; os PNGs são produzidos de qualquer forma.
- Divergência numérica: confira o hash, as versões e a semente.

11. CRITÉRIO DE REPRODUTIBILIDADE

O experimento é considerado reproduzido quando o arquivo de entrada é
idêntico, os parâmetros permanecem iguais, o código roda sem erro e os
resultados do item 7 são obtidos (ressalvadas variações ambientais raras).
Para a Etapa 1, a versão portátil confirma também o SHA-256 exato.

Documento acadêmico e este tutorial são entregas distintas: este TXT
serve apenas para instalação, execução e auditoria do experimento.
