UNIVERSIDADE FEDERAL DA PARAÍBA — CENTRO DE INFORMÁTICA
APRENDIZAGEM DE MÁQUINA — ETAPA 6: SVM (KERNEL RBF)
PACOTE DE REPRODUÇÃO E VALIDAÇÃO — DEBIAN 13 / LINUX
======================================================

1. FINALIDADE

Este pacote permite que outra pessoa execute, em sua própria máquina,
o experimento descrito na resolução acadêmica da Etapa 6. O código lê a
mesma base fixa de 300 observações da Etapa 1, separa 80% dos dados para
ajuste do SVM e 20% para teste, calcula as métricas e desenha a fronteira
de decisão e uma matriz de confusão identificada com TP, FN, FP e TN.

O pacote contém EXATAMENTE estes três arquivos:

  Lista_ML_Base_300_Pontos.csv
  Lista_ML_Etapa6_SVM.py
  README_EXECUCAO_E_VALIDACAO.txt

O gráfico Etapa6_SVM_Fronteira_Matriz.png NÃO está dentro do ZIP: será
produzido automaticamente durante a execução.

2. REQUISITOS

- Debian 13 (ou distribuição Linux equivalente com Python 3.11 ou superior).
- Terminal e acesso para instalar pacotes Python.
- Conexão com a internet apenas para instalar pacotes que ainda faltarem.
- Não é necessário usar GPU, Docker, Jupyter ou VS Code.

Versões das bibliotecas usadas nesta reprodução:

  NumPy          2.3.5
  Matplotlib     3.10.8
  scikit-learn   1.8.0

3. INSTALAÇÃO NO DEBIAN 13 (UMA ÚNICA VEZ)

Abra o terminal. Se o usuário possuir sudo, execute:

  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip unzip

Se estiver conectado como root, remova "sudo" dos comandos acima.

Confirme a instalação:

  python3 --version

4. EXTRAÇÃO DO ZIP E PREPARO DA PASTA

Exemplo: supondo que o ZIP esteja em ~/Downloads, execute:

  mkdir -p ~/ufpb-lista-ml/etapa6
  cd ~/ufpb-lista-ml/etapa6
  unzip ~/Downloads/UFPB_Etapa_06_SVM_Pacote_Reproducao.zip

Caso o ZIP esteja em outra pasta, substitua o caminho no comando unzip.

Verifique os arquivos extraídos:

  ls -lh

Devem aparecer os três arquivos listados na seção 1.

5. CRIAÇÃO DO AMBIENTE VIRTUAL E INSTALAÇÃO DAS DEPENDÊNCIAS

Na pasta do exercício, execute:

  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install numpy==2.3.5 matplotlib==3.10.8 scikit-learn==1.8.0

Você verá "(.venv)" no início da linha de comando após a ativação.
O ambiente virtual evita alterar a instalação global do Debian.

6. VERIFICAÇÃO DA BASE DE DADOS ORIGINAL

Antes de executar o algoritmo, confira se o CSV não foi modificado:

  sha256sum Lista_ML_Base_300_Pontos.csv

O SHA-256 esperado é:

  04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5

A base contém 300 linhas de observações além do cabeçalho:
150 registros da Classe 1 e 150 registros da Classe 2. O CSV utiliza
ponto como separador decimal e vírgula como separador de campos.
Não reordene os registros nem altere os valores.

7. EXECUÇÃO DO EXPERIMENTO

Execute o código com o ambiente virtual ativo:

  MPLBACKEND=Agg python Lista_ML_Etapa6_SVM.py

A variável MPLBACKEND=Agg permite salvar a figura inclusive em
servidores sem ambiente gráfico. O script não altera o CSV.

8. SAÍDA ESPERADA

A saída esperada é:

  Conjunto: 300 pontos | Treino: 240 | Teste: 60
  Classes no teste: [30, 30]
  Matriz de confusao (real x prevista):
   [[30  0]
    [ 0 30]]
  Acuracia: 1.000000 (100.00%)
  Precisao: 1.000000 (100.00%)
  Recall: 1.000000 (100.00%)
  F1-score: 1.000000 (100.00%)
  Vetores de suporte por classe: [11, 11]
  Identificadores incorretos: []

Interpretação da matriz (linhas = real; colunas = previsto):

                       Prevista Classe 1   Prevista Classe 2
  Real Classe 1        TP = 30             FN = 0
  Real Classe 2        FP = 0              TN = 30

  Classe 1 = POSITIVA; Classe 2 = NEGATIVA.
  TP = verdadeiro positivo; FN = falso negativo;
  FP = falso positivo; TN = verdadeiro negativo.

Resultados de classificação se referem SOMENTE aos 60 pontos de teste.
O teste foi separado antes do ajuste do StandardScaler e do SVM.
O SVM foi ajustado exclusivamente com os 240 pontos de treinamento.

9. GRÁFICO GERADO

Ao terminar, será criado na mesma pasta:

  Etapa6_SVM_Fronteira_Matriz.png

A imagem mostra: (a) pontos de treino e teste; (b) fronteira de decisão
do SVM RBF; (c) vetores de suporte; (d) matriz de confusão com TP/FN/FP/TN.

Em um Debian com interface gráfica, abra com:

  xdg-open Etapa6_SVM_Fronteira_Matriz.png

Em um servidor sem interface gráfica, copie o arquivo PNG para outro
computador. Não é necessário abrir o gráfico para validar as métricas.

10. NOVAS EXECUÇÕES

Nas próximas sessões, basta executar:

  cd ~/ufpb-lista-ml/etapa6
  source .venv/bin/activate
  MPLBACKEND=Agg python Lista_ML_Etapa6_SVM.py

Para encerrar o ambiente virtual:

  deactivate

11. INFORMAÇÕES PARA REPRODUTIBILIDADE

- Arquivo de dados: 300 pontos fixos gerados com semente 42 na Etapa 1.
- Atributos de entrada: X e Y, sem uso dos rótulos como entrada.
- Divisão treino/teste: estratificada; 80% / 20%; random_state=42.
- Pré-processamento: StandardScaler dentro de um Pipeline.
- Modelo: sklearn.svm.SVC(kernel='rbf', C=1.0, gamma='scale',
  tol=0.001, shrinking=True, random_state=42).
- Matriz: confusion_matrix(..., labels=[1,2]).
- Métricas binárias: pos_label=1 (Classe 1 positiva).
- Teste observado: 60 acertos em 60 pontos, 22 vetores de suporte.

Esses resultados demonstram o comportamento para a divisão especificada;
não representam garantia de desempenho perfeito em outras amostras.

12. RESOLUÇÃO DE PROBLEMAS FREQUENTES

"python3: command not found": instale python3 pelo apt.
"No module named venv": instale python3-venv pelo apt.
"externally-managed-environment": crie e ative o .venv antes de pip.
"No module named sklearn": ative o .venv e instale as dependências.
"FileNotFoundError": confirme que CSV e script estão na MESMA pasta.
"unzip: cannot find": confira o caminho do ZIP baixado.
Se o gráfico não abrir (servidor), procure o PNG gerado com "ls -lh *.png".

IMPORTANTE: se o SHA-256 do CSV for diferente do esperado,
interrompa a validação e obtenha novamente a cópia original do pacote.

FIM DAS INSTRUÇÕES
