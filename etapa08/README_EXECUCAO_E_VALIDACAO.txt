UNIVERSIDADE FEDERAL DA PARAÍBA — APRENDIZAGEM DE MÁQUINA
ETAPA 8 — K-VIZINHOS MAIS PRÓXIMOS (KNN)
PACOTE DE REPRODUÇÃO E VALIDAÇÃO INDEPENDENTE
========================================================

1. CONTEÚDO DESTE ARQUIVO ZIP
----------------------------
  Lista_ML_Base_300_Pontos.csv      Os 300 pontos originais, 150 por classe
  Lista_ML_Etapa8_KNN.py           Código-fonte integral do experimento
  README_EXECUCAO_E_VALIDACAO.txt  Este tutorial

O script lê EXATAMENTE o CSV fornecido. Ele não sorteia outra base.
A semente 42 é utilizada para a divisão treino/teste e a validação cruzada.

2. REQUISITOS
-------------
Testado em ambiente Python com as versões:
  NumPy: 2.3.5
  Matplotlib: 3.10.8
  scikit-learn: 1.8.0

Sistema sugerido: Debian 13 (Linux, arquitetura x86-64) e Python 3.
Precisa de acesso à internet somente para instalar bibliotecas inicialmente.
Nenhuma conexão é necessária durante a execução dos experimentos.

3. PASSO A PASSO NO DEBIAN 13
-----------------------------
Abra um terminal; os comandos abaixo pressupõem um usuário comum com sudo.
Caso use root, remova o prefixo sudo dos comandos.

A) Instale o Python e o suporte a ambientes virtuais:

    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip unzip

B) Crie uma pasta isolada para o exercício:

    mkdir -p ~/ufpb-lista-ml/etapa8
    cd ~/ufpb-lista-ml/etapa8

C) Extraia o pacote ZIP que foi baixado para ~/Downloads:

    unzip ~/Downloads/UFPB_Etapa_08_KNN_Pacote_Reproducao.zip

   Se o arquivo estiver em outro local, substitua o caminho de ~/Downloads.
   Confira se existem os três arquivos (ls -lah).

D) Crie e ative um ambiente virtual:

    python3 -m venv .venv
    source .venv/bin/activate

E) Instale as versões utilizadas na validação:

    python -m pip install --upgrade pip
    python -m pip install numpy==2.3.5 matplotlib==3.10.8 scikit-learn==1.8.0

F) Confira a integridade do arquivo de dados:

    sha256sum Lista_ML_Base_300_Pontos.csv

   Resultado SHA-256 esperado:
    04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5

   O próprio script também verifica esta assinatura e interrompe a execução
   se detectar um CSV divergente da base original da Etapa 1.

G) Execute o código:

    python Lista_ML_Etapa8_KNN.py

   Para registrar também a saída em um arquivo de texto, pode utilizar:

    python Lista_ML_Etapa8_KNN.py | tee resultado_etapa8.txt

4. RESULTADOS QUE DEVEM APARECER
--------------------------------
  Total: 300 | Treino: 240 | Teste: 60
  Classes de teste: [30, 30]

       k    Média CV       Acurácia teste   Precisão  Recall   F1
       1    0.975000       0.983333         0.967742  1.000000 0.983607
       3    0.983333       1.000000         1.000000  1.000000 1.000000
       5    0.991667       1.000000         1.000000  1.000000 1.000000
       7    0.987500       1.000000         1.000000  1.000000 1.000000
       9    0.987500       1.000000         1.000000  1.000000 1.000000
      15    0.987500       1.000000         1.000000  1.000000 1.000000

  k selecionado por CV: 5
  Matriz (ordem das classes reais e previstas: [1, 2]):
  [[30  0]
   [ 0 30]]
  TP = 30  FN = 0  FP = 0  TN = 30

  Atenção: Classe 1 foi declarada POSITIVA e Classe 2 NEGATIVA.
  k = 1 erra um único registro no teste: C2-134.
  Os outros k avaliados acertam os 60 casos reservados para teste.

A escolha de k foi realizada SOMENTE pela validação cruzada 5-fold nos
240 pontos de treino. As métricas de teste não foram usadas para escolher k.
O escalonamento é ajustado somente em dados de treino, inclusive dentro
cada dobra de validação cruzada, evitando vazamento de dados.

5. FIGURAS GERADAS AUTOMATICAMENTE
-----------------------------------
Ao executar o script, dois novos arquivos PNG aparecerão na pasta:

  Etapa8_KNN_Fronteiras_Por_K.png
     Seis painéis de fronteiras de decisão para k = 1, 3, 5, 7, 9 e 15.
     Pontos preenchidos: treino; círculos vazados: teste.

  Etapa8_KNN_Selecao_Matriz.png
     Comparação da acurácia média de validação cruzada e acurácia no teste;
     matriz de confusão do k selecionado com TP, FN, FP, TN dentro das células.

Para visualizar no ambiente gráfico do Debian:

    xdg-open Etapa8_KNN_Fronteiras_Por_K.png
    xdg-open Etapa8_KNN_Selecao_Matriz.png

Se não houver interface gráfica, os PNGs ainda serão gravados. Copie-os
para um computador com visualizador de imagens.

6. REEXECUÇÃO FUTURA
--------------------
    cd ~/ufpb-lista-ml/etapa8
    source .venv/bin/activate
    python Lista_ML_Etapa8_KNN.py
    deactivate

7. CONFERÊNCIA DE REPRODUTIBILIDADE
-----------------------------------
  [ ] O SHA-256 corresponde ao valor apresentado acima.
  [ ] O script não gerou erro Python.
  [ ] Há 240 pontos de treino e 60 de teste, 30 de cada classe no teste.
  [ ] O k escolhido por CV é 5.
  [ ] A matriz do k = 5 é [[30,0],[0,30]].
  [ ] As quatro métricas do k selecionado são 1.000000 (100%).
  [ ] As duas imagens PNG foram geradas.

8. PROBLEMAS FREQUENTES
-----------------------
- "python3: command not found": instalar python3 com apt.
- "No module named sklearn" ou "No module named matplotlib": ativar .venv
  e executar o comando de instalação das bibliotecas (seção 3E).
- "externally-managed-environment": não instalar pip no Python global;
  usar o ambiente .venv indicado na seção 3D (PEP 668).
- "CSV difere da base original": o CSV pode ter sido alterado por editor
  ou planilha; extrair novamente o pacote original.
- "FileNotFoundError": manter o .py e o .csv na mesma pasta.
- "xdg-open: command not found": instalar xdg-utils ou abrir os PNGs por
  um gerenciador de arquivos; visualização não é necessária ao cálculo.
- CSV sem alteração, mas pequenas diferenças de ponto flutuante em outra
  versão de bibliotecas: reinstalar versões da seção 2 e conferir o Python.

9. OBSERVAÇÃO ACADÊMICA
------------------------
O KNN é um algoritmo supervisionado: utiliza os rótulos dos pontos de treino.
Acurácia de 100% em um conjunto específico não representa garantia de
100% em dados externos. Um único caso de teste equivale a 1,67 ponto
percentual de acurácia nessa amostra de 60 observações.

Arquivos de código e dados podem ser livremente verificados localmente.
Este guia é separado do DOCX acadêmico da Etapa 8, conforme solicitado.
