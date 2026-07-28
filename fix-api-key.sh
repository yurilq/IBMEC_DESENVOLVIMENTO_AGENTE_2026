#!/bin/bash
# Script para remover API key do historico Git

# Substituir API key nos arquivos se existirem
if [ -f "E4_RAG_FAISS/docs/COMPARACAO_LLMS_2026.md" ]; then
    sed -i 's/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/sk-or-v1-SUA_CHAVE_AQUI/g' E4_RAG_FAISS/docs/COMPARACAO_LLMS_2026.md
fi

if [ -f "E4_RAG_FAISS/docs/IMPLEMENTACAO_MULTI_LLM.md" ]; then
    sed -i 's/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/sk-or-v1-SUA_CHAVE_AQUI/g' E4_RAG_FAISS/docs/IMPLEMENTACAO_MULTI_LLM.md
fi
