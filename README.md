# Lista de Exercícios — Aprendizagem de Máquina | UFPB

Códigos Python para reproduzir as **oito etapas** da lista de Aprendizagem de Máquina do Centro de Informática da Universidade Federal da Paraíba (UFPB). Todos os experimentos utilizam a mesma base sintética de **300 observações** (150 por classe), gerada com semente 42.

## Estrutura

| Pasta | Algoritmo | Script |
| --- | --- | --- |
| `etapa01/` | Geração dos dados e gráfico | `Lista_ML_Etapa1_Reproducao_Exata.py` |
| `etapa02/` | K-means | `Lista_ML_Etapa2_KMeans.py` |
| `etapa03/` | Fuzzy C-means | `Lista_ML_Etapa3_Fuzzy_CMeans.py` |
| `etapa04/` | Regressão Logística | `Lista_ML_Etapa4_RegressaoLogistica.py` |
| `etapa05/` | Rede Neural Artificial (MLP) | `Lista_ML_Etapa5_RNA.py` |
| `etapa06/` | SVM com kernel RBF | `Lista_ML_Etapa6_SVM.py` |
| `etapa07/` | Árvore de Decisão | `Lista_ML_Etapa7_Arvore_Decisao.py` |
| `etapa08/` | K-vizinhos Mais Próximos (KNN) | `Lista_ML_Etapa8_KNN.py` |

Cada pasta contém o script da etapa e uma **cópia idêntica** de `Lista_ML_Base_300_Pontos.csv`. As cópias são intencionais: cada script pode ser executado isoladamente, sem modificar caminhos no código.

## Requisitos

- **Python 3.13** (versão usada nos testes).
- Dependências definidas em `requirements.txt`: NumPy, pandas, Matplotlib e scikit-learn.
- **Git**, se optar por clonar o repositório. Também é possível baixar **Code → Download ZIP** no GitHub e extrair a pasta.

## Obter o código

No terminal de sua preferência, com Git instalado:

```bash
git clone https://github.com/evertonidpb/ufpb-lista-aprendizagem-maquina.git
cd ufpb-lista-aprendizagem-maquina
```

Se baixou o ZIP, abra o terminal na pasta extraída e siga as instruções do seu sistema operacional.

## Debian 13 (Linux)

Instale os requisitos do sistema (execute antes de clonar, se ainda não tiver Git):

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

Na **raiz do repositório**, crie um ambiente virtual, instale as dependências e execute todas as etapas:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verificar_tudo.py
```

Para executar apenas uma etapa (exemplo: Etapa 5):

```bash
python etapa05/Lista_ML_Etapa5_RNA.py
```

## Windows 11 (PowerShell)

Instale **Python 3.13** pelo site oficial [python.org](https://www.python.org/downloads/) e, se desejar clonar, instale o [Git para Windows](https://git-scm.com/downloads/win). Verifique se o comando `py -3.13` está disponível.

Abra o **PowerShell** na raiz do repositório e execute:

```powershell
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\verificar_tudo.py
```

Para executar apenas uma etapa (exemplo: Etapa 5):

```powershell
.\.venv\Scripts\python.exe etapa05\Lista_ML_Etapa5_RNA.py
```

Os comandos acima **não exigem ativar o ambiente virtual** no PowerShell, evitando problemas com a política de execução de scripts. Se `py -3.13` não for reconhecido, confira a instalação do Python e do launcher do Windows.

## Como conferir a execução

O comando `scripts/verificar_tudo.py`:

1. Verifica a assinatura SHA-256 de cada CSV;
2. Executa os oito scripts, em ordem;
3. Confere marcadores dos resultados esperados;
4. Grava os logs em `relatorios/etapa01.txt` até `relatorios/etapa08.txt`.

A saída esperada termina com:

```text
SUCESSO: oito etapas executadas e resultados esperados confirmados.
```

Os gráficos PNG são gerados nas pastas das etapas. A Etapa 3 também gera `Etapa3_Pertinencias_FCM.csv`. Esses arquivos de saída e os relatórios não são versionados.

**Resultados de referência:** K-means com ARI = 0,960267; Fuzzy C-means com FPC = 0,878095; classificadores supervisionados com 60/60 acertos nos respectivos conjuntos de teste; KNN seleciona `k = 5` por validação cruzada. São resultados desta **base sintética e desta divisão**, não garantias de desempenho em outros dados.

**Integridade da base:** SHA-256 de `Lista_ML_Base_300_Pontos.csv`:

```text
04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5
```

Não edite ou regrave os CSVs com outro formato de quebras de linha; isso altera o hash. O script da Etapa 1 regenera o CSV original de maneira reprodutível em Debian e Windows.

**Observação:** precisão, recall e F1 usam a Classe 2 como positiva nas Etapas 4 e 5 e a Classe 1 nas Etapas 6 a 8, conforme definido em cada experimento.
