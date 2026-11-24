# Aprendizagem de Máquina — UFPB | Experimentos reproduzíveis

Repositório para reprodução das **8 etapas** da lista de exercícios da disciplina de Aprendizagem de Máquina, Centro de Informática, Universidade Federal da Paraíba (UFPB).

O objetivo é permitir que o professor e outras pessoas executem os experimentos de ponta a ponta usando **a mesma base sintética de 300 observações**, sem acesso a ambientes privados. Os arquivos `README_EXECUCAO_E_VALIDACAO.txt` nas pastas de cada etapa detalham a execução isolada.

## Organização

| Pasta | Experimento | Saídas geradas |
| --- | --- | --- |
| `etapa01/` | Geração de duas classes com NumPy | CSV de 300 pontos (idêntico ao original) |
| `etapa02/` | K-means (`k=2`) | Gráfico comparativo |
| `etapa03/` | Fuzzy C-means (`c=2`) | Gráfico de pertinência e CSV com memberships |
| `etapa04/` | Regressão Logística | Fronteira de decisão e matriz |
| `etapa05/` | RNA feedforward (12 e 6 neurônios) | Comparação com Regressão Logística |
| `etapa06/` | SVM com kernel RBF | Fronteira de decisão e matriz TP/FN/FP/TN |
| `etapa07/` | Árvore de Decisão | Árvore e fronteira de decisão |
| `etapa08/` | KNN (`k` selecionado por validação cruzada) | Seis fronteiras e matriz de confusão |

**Importante:** as oito pastas têm cópias **idênticas** do CSV, para que cada etapa possa ser executada isoladamente. O SHA-256 da base é:

```text
04b7b779052bd13633472299eb6d763a9bfff26fb26213196ed32d131bb0a4a5
```

## Instalação rápida no Debian 13

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip unzip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o terminal estiver como `root`, remova `sudo`. Não use `pip` global nem `--break-system-packages`.

## Verificar os oito experimentos automaticamente

```bash
python scripts/verificar_tudo.py
```

A verificação executa os códigos em ordem, confere a assinatura dos CSVs e os resultados de referência e registra a saída de cada etapa em `relatorios/`. **O arquivo `relatorios/` não é versionado.** Para executar apenas uma etapa, entre na respectiva pasta e use `python NOME_DO_SCRIPT.py` conforme o README local.

## Resultados esperados

| Etapa | Resultado principal |
| --- | --- |
| 1 | 300 registros, semente 42, hash igual à referência |
| 2 | 297 correspondências, ARI = 0,960267 |
| 3 | 297 correspondências, FPC = 0,878095, 15 iterações |
| 4 | 60/60 classificações corretas no teste |
| 5 | 60/60 classificações corretas no teste; RNA com 38 iterações |
| 6 | 60/60 classificações corretas no teste |
| 7 | 60/60 classificações corretas no teste |
| 8 | `k = 5` por validação cruzada; 60/60 corretas no teste |

Os algoritmos supervisionados usam **80% de treino e 20% de teste** com divisão estratificada e `random_state=42`. O pré-processamento que aprende parâmetros utiliza somente o treino. Nas Etapas 2 e 3, as classes verdadeiras são usadas **após** o agrupamento, exclusivamente para avaliação.

> **Nota sobre classe positiva:** os scripts originais das Etapas 4 e 5, extraídos integralmente dos DOCXs, calculam precisão/recall/F1 com a Classe 2 como positiva; os scripts posteriores adotam Classe 1 positiva. Como ambos os modelos classificaram corretamente os 60 testes, as métricas são 100% em ambas as convenções. Ao compilar os documentos acadêmicos, convém uniformizar a legenda da matriz e explicitar o rótulo positivo.

## Código-fonte e equivalência com os documentos

Os scripts das Etapas 2 a 5 foram recuperados **linha por linha** das listagens numeradas nos documentos Word de entrega, sem modificar seus hiperparâmetros. Os scripts das Etapas 6 a 8 são os originais dos pacotes de reprodução correspondentes. A Etapa 1 usa a versão portátil do gerador, com a mesma sequência de sorteios do código acadêmico e com padronização de quebras de linha para garantir SHA-256 idêntico no Linux.

## Inicializar Git e publicar no GitHub

Consulte [GUIA_GIT_GITHUB.md](GUIA_GIT_GITHUB.md). Execute `bash scripts/preparar_git.sh` para criar o repositório `main` e o primeiro commit **usando sua identidade Git configurada**. Nenhum código é enviado automaticamente ao GitHub. Nunca envie tokens, senhas, chaves privadas ou dados pessoais junto do projeto.

**Referência acadêmica:** Lista de Exercícios de Aprendizagem de Máquina — UFPB / Centro de Informática.
