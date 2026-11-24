#!/usr/bin/env bash
set -euo pipefail

# Trabalha com a raiz do projeto, mesmo quando chamado de outra pasta.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v git >/dev/null 2>&1 || { echo 'ERRO: instale Git: sudo apt install git'; exit 1; }

if [[ ! -d .git ]]; then
  git init -b main
else
  echo 'Repositorio Git local ja existe; sera reutilizado.'
fi

if [[ -z "$(git config user.name || :)" || -z "$(git config user.email || :)" ]]; then
  echo 'Configure sua identidade de commit ANTES de continuar:'
  echo '  git config --global user.name "SEU_NOME"'
  echo '  git config --global user.email "SEU_EMAIL_DE_COMMIT"'
  exit 2
fi

git add -A
if git diff --cached --quiet; then
  echo 'Nenhuma alteracao a registrar.'
else
  git commit -m 'Adiciona experimentos reproduziveis da lista de ML (etapas 1-8)'
fi

echo
echo 'Estado do repositorio:'
git status --short
echo
printf 'Branch: '; git branch --show-current
printf 'Ultimo commit: '; git log --oneline -1 || true
printf '
Para publicar: veja GUIA_GIT_GITHUB.md
'
