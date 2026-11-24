# Preparação do Git local e publicação no GitHub — Debian 13

Este guia prepara o **seu próprio Debian**. O ZIP fornece o repositório, mas não executa comandos diretamente no computador do usuário nem publica conteúdo sem autenticação.

## A. Instalar e verificar Git

```bash
sudo apt update
sudo apt install -y git unzip
 git --version
```

Se for usuário `root`, remova `sudo`. Recomenda-se usar uma conta comum para o projeto.

## B. Extrair e entrar na pasta

Exemplo para um ZIP baixado em `~/Downloads`:

```bash
mkdir -p ~/projetos
cd ~/projetos
unzip ~/Downloads/UFPB_Lista_ML_Repositorio_Git.zip
cd ufpb-lista-aprendizagem-maquina
ls -la
```

## C. Configurar a sua identidade Git (UMA VEZ)

Use o nome que deve constar nos commits. Para o email, prefira o endereço `noreply` oferecido no seu perfil do GitHub, se não quiser divulgar um email particular.

```bash
git config --global user.name "SEU_NOME"
git config --global user.email "SEU_EMAIL_DE_COMMIT"
```

Substitua os valores de exemplo. Não configure um email de outra pessoa.

## D. Inicializar e realizar o commit inicial

```bash
bash scripts/preparar_git.sh
git status
git log --oneline -1
```

O script cria a branch `main`, adiciona os arquivos de código/CSV/documentação e faz o commit inicial. Se o repositório já tiver um commit e não houver mudanças, não cria commit duplicado.

## E. Testar antes da publicação

```bash
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verificar_tudo.py
```

Os testes escrevem imagens e logs localmente, mas esses arquivos são ignorados pelo Git. Depois, confira:

```bash
git status --short
```

A saída deve ficar vazia quando não houver alterações versionadas.

## F. Publicar no GitHub — método 1 (site + Git)

1. Entre em https://github.com e crie um repositório **vazio**, com nome sugerido `ufpb-lista-aprendizagem-maquina`.
2. Não adicione README, .gitignore nem LICENSE pelo site, porque o projeto local já possui os dois primeiros arquivos.
3. Escolha visibilidade pública se quiser que o professor abra o link sem autenticação.
4. No terminal, de dentro da pasta do projeto, execute:

```bash
# SUBSTITUA SEU_USUARIO pelo nome REAL da sua conta no GitHub.
git remote add origin https://github.com/SEU_USUARIO/ufpb-lista-aprendizagem-maquina.git
git remote -v
git push -u origin main
```

Se a URL remota já existir, use `git remote set-url origin URL_CORRETA`, não tente adicionar `origin` duas vezes. GitHub exige autenticação para publicar; não utiliza mais senha comum de conta como senha Git HTTPS.

## G. Publicar no GitHub — método 2 (GitHub CLI)

Se optar por instalar e autenticar o `gh` no Debian, dentro do projeto, depois do primeiro commit:

```bash
gh auth login
gh repo create ufpb-lista-aprendizagem-maquina --public --source=. --remote=origin --push
```

O comando acima cria um **repositório público**. Troque `--public` por `--private` se desejar testar sem divulgar. Não execute os métodos F e G ao mesmo tempo; escolha um.

## H. Verificar o link para o professor

Após publicar, o endereço será semelhante a:

```text
https://github.com/SEU_USUARIO/ufpb-lista-aprendizagem-maquina
```

O endereço acima é UM MODELO, não um repositório criado. No documento acadêmico, substitua pelo link real depois de conferir que funciona numa janela anônima.

Sugestão de texto para a entrega:

> **Repositório de reprodução dos experimentos:** código Python, base de 300 observações e tutoriais de execução no Debian 13 disponíveis em: [URL REAL DO REPOSITÓRIO].

## I. Fluxo das próximas alterações

```bash
git status
git add .
git commit -m "Atualiza resultados de reproducao"
git push
```

**Segurança:** revise `git status` antes de `git add .`; nunca adicione arquivos `.env`, tokens, senhas, chaves SSH privadas ou conteúdo alheio aos exercícios.

Documentação oficial: https://docs.github.com/en/get-started/git-basics/set-up-git e https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
