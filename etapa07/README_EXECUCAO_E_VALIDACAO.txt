UNIVERSIDADE FEDERAL DA PARAÍBA — CENTRO DE INFORMÁTICA
Aprendizagem de Máquina — Lista de Exercícios — Etapa 7
ÁRVORE DE DECISÃO: REPRODUÇÃO E VALIDAÇÃO INDEPENDENTE
========================================================

1. OBJETIVO
-----------
Este pacote permite reproduzir o experimento da Etapa 7 em outro
computador, utilizando os MESMOS 300 pontos gerados na Etapa 1.
O programa treina uma árvore de decisão CART, desenha sua estrutura,
mostra a fronteira de decisão e calcula a matriz de confusão e as
métricas de acurácia, precisão, recall e F1-score.

Este arquivo é um GUIA DE EXECUÇÃO separado do documento acadêmico.

2. ARQUIVOS INCLUÍDOS NO ZIP
---------------------------
Lista_ML_Base_300_Pontos.csv
  Base original: 300 registros; 150 da Classe 1 e 150 da Classe 2.

Lista_ML_Etapa7_Arvore_Decisao.py
  Script completo do experimento, com tabelas de resultados no
  terminal e geração automática de duas imagens PNG.

README_EXECUCAO_E_VALIDACAO.txt
  Estas instruções de instalação, execução e verificação.

A pasta que contém os arquivos deve ter permissão de escrita para
salvar os dois gráficos PNG gerados pelo Python.

3. AMBIENTE DE REFERÊNCIA
------------------------
Python 3.13 e pacotes:
  numpy==2.3.5
  matplotlib==3.10.8
  scikit-learn==1.8.0

Sistemas Linux modernos com Python compatível podem executar o
experimento. As instruções abaixo foram escritas para Debian 13.
Não é necessário Docker, Kubernetes nem acesso root durante o teste.

4. COMO EXECUTAR NO DEBIAN 13 (PASSO A PASSO)
--------------------------------------------
A) Instale Python, venv e a ferramenta de descompactação.

   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip unzip

B) Crie uma pasta para o trabalho e entre nela.

   mkdir -p ~/ufpb-lista-ml/etapa7
   cd ~/ufpb-lista-ml/etapa7

C) Coloque o ZIP baixado nessa pasta e extraia os três arquivos.
   Substitua CAMINHO_DO_ZIP pelo caminho real do arquivo. Exemplo:

   unzip ~/Downloads/UFPB_Etapa_07_Arvore_Decisao_Pacote_Reproducao.zip

   Se você descompactou usando um gerenciador de arquivos, basta
   abrir um terminal na pasta onde estão o CSV, o .py e este README.

D) Crie e ative o ambiente Python isolado:

   python3 -m venv .venv
   source .venv/bin/activate

   Quando ativado, o terminal geralmente mostra (.venv).

E) Instale as dependências do experimento:

   python -m pip install --upgrade pip
   python -m pip install numpy==2.3.5 matplotlib==3.10.8 scikit-learn==1.8.0

F) Confira os arquivos e a assinatura da base de dados:

   ls -l Lista_ML_Base_300_Pontos.csv Lista_ML_Etapa7_Arvore_Decisao.py
   sha256sum Lista_ML_Base_300_Pontos.csv

   O SHA-256 esperado do CSV original é:
   04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5

G) Execute o algoritmo:

   python Lista_ML_Etapa7_Arvore_Decisao.py

O script NÃO modifica o CSV. Ele calcula a assinatura e recusa uma
base diferente, para preservar a comparabilidade com as etapas 1–6.
O treinamento utiliza apenas os pontos de treino; a avaliação utiliza
apenas os 60 pontos separados para teste.

5. RESULTADOS ESPERADOS
----------------------
Total: 300 | Treino: 240 | Teste: 60
Classes no teste: [30, 30]
Profundidade: 3 | Folhas: 5
Acuracia no treino: 99.1667%

Matriz [classe real x prevista], ordem [1,2]:
[[30  0]
 [ 0 30]]

TP=30 | FN=0 | FP=0 | TN=30 (positiva: classe 1)
Acuracia: 1.000000 (100.00%)
Precisao: 1.000000 (100.00%)
Recall: 1.000000 (100.00%)
F1-score: 1.000000 (100.00%)
Erros no teste: []
Importancia dos atributos [X,Y]: [0.99374797 0.00625203]

Os nomes dos arquivos PNG gerados são:
  Etapa7_Arvore_Estrutura.png
  Etapa7_Fronteira_Matriz.png

Valores internos ou formatação de textos podem diferir muito pouco
entre versões de bibliotecas, por isso recomendamos as versões fixadas.

6. COMO INTERPRETAR A MATRIZ DE CONFUSÃO
---------------------------------------
Neste exercício, a Classe 1 é definida como POSITIVA e a Classe 2
como NEGATIVA. As linhas correspondem às classes verdadeiras,
e as colunas às classes previstas.

                 Prevista 1      Prevista 2
Real Classe 1      TP = 30         FN = 0
Real Classe 2      FP = 0          TN = 30

TP = verdadeiro positivo; FN = falso negativo;
FP = falso positivo; TN = verdadeiro negativo.

Acurácia = (TP + TN) / (TP + FN + FP + TN)
Precisão = TP / (TP + FP)
Recall   = TP / (TP + FN)
F1-score = 2 * (Precisão * Recall) / (Precisão + Recall)

7. COMO ABRIR E CONFERIR OS GRÁFICOS
-----------------------------------
Em um ambiente gráfico Linux, execute:

   xdg-open Etapa7_Arvore_Estrutura.png
   xdg-open Etapa7_Fronteira_Matriz.png

Na primeira figura, confira a divisão inicial X <= 45.48 e a árvore
com profundidade 3. Na segunda, verifique a fronteira segmentada e
a matriz de confusão marcada com TP, FN, FP e TN.

Se não tiver interface gráfica, os arquivos PNG ainda serão gerados.
Você pode transferi-los para outro computador e abri-los normalmente.

8. REEXECUÇÃO E LIMPEZA
-----------------------
Para executar novamente depois de fechar o terminal:

   cd ~/ufpb-lista-ml/etapa7
   source .venv/bin/activate
   python Lista_ML_Etapa7_Arvore_Decisao.py

O script sobrescreve as duas imagens PNG com versões atualizadas.
Para sair do ambiente Python:

   deactivate

9. PROBLEMAS FREQUENTES
-----------------------
'No module named sklearn' ou 'No module named matplotlib':
  Ative o ambiente (.venv) e repita o comando de instalação do item 4E.

'CSV diferente da base original da Etapa 1':
  O arquivo CSV foi alterado ou não corresponde à base fornecida.
  Extraia novamente o CSV do ZIP original; não edite as coordenadas.

'No such file or directory':
  Confira se está na mesma pasta dos arquivos com o comando 'pwd'
  e confira seus nomes com 'ls'.

'Permission denied':
  Execute em uma pasta da qual seu usuário seja proprietário, como ~/.

'pip: externally-managed-environment':
  Evite instalar pacotes globalmente no Debian; use o ambiente virtual
  do item 4D, conforme as orientações acima.

10. REPRODUTIBILIDADE E LIMITAÇÕES
---------------------------------
* A divisão estratificada usa test_size=0.20 e random_state=42.
* O modelo CART usa criterion='gini', max_depth=3,
  min_samples_leaf=2, min_samples_split=2, ccp_alpha=0.0.
* Não houve escolha de hiperparâmetros com base no conjunto de teste.
* 100% é o resultado desta partição específica; não garante acertos
  perfeitos em novos conjuntos de dados.
* O ZIP contém exclusivamente os três arquivos descritos no item 2.
* O documento acadêmico DOCX é fornecido separadamente deste ZIP.
