# 📋 DATASET DE TESTE E5 - PDFs PCDF

**Objetivo:** Perguntas e respostas esperadas para avaliar o sistema RAG E5

---

## 📄 PDFs Disponíveis

1. **estatuto_desarmamento.pdf** (22 páginas)
   - Estatuto do Desarmamento
   - Lei sobre controle de armas

2. **LEI-10.826-03-SINARM.pdf** (14 páginas)
   - Lei 10.826/2003
   - Sistema Nacional de Armas (SINARM)
   - Registro, posse e comercialização

3. **cartilha-de-armamento-e-tiro.pdf** (27 páginas)
   - Cartilha da Academia Nacional de Polícia
   - Capacitação técnica
   - Normas de segurança

4. **Anexo XVII - Porte de arma de fogo.pdf** (1 página)
   - Certificado de porte federal
   - Deveres do portador

---

## 🧪 DATASET DE TESTE

### Categoria 1: Perguntas sobre SINARM

```python
{
    "pergunta": "O que é o SINARM?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf", "sistema_sinarm.txt"],
    "resposta_esperada": "Sistema Nacional de Armas, instituído no Ministério da Justiça"
}

{
    "pergunta": "Quais são as competências do SINARM?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"],
    "resposta_esperada": "Identificar características de armas, cadastrar proprietários, etc."
}

{
    "pergunta": "Onde funciona o SINARM?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"],
    "resposta_esperada": "No âmbito da Polícia Federal, com circunscrição em todo território nacional"
}
```

### Categoria 2: Perguntas sobre Estatuto do Desarmamento

```python
{
    "pergunta": "O que é o Estatuto do Desarmamento?",
    "docs_relevantes": ["estatuto_desarmamento.pdf"],
    "resposta_esperada": "Lei que regula o controle de armas de fogo no Brasil"
}

{
    "pergunta": "Quando foi publicado o Estatuto do Desarmamento?",
    "docs_relevantes": ["estatuto_desarmamento.pdf"],
    "resposta_esperada": "2003/2004"
}
```

### Categoria 3: Perguntas sobre Porte de Arma

```python
{
    "pergunta": "O que diz a lei sobre porte de arma em estado de embriaguez?",
    "docs_relevantes": ["Anexo XVII - Porte de arma de fogo.pdf", "LEI-10.826-03-SINARM.pdf"],
    "resposta_esperada": "A autorização de porte perde automaticamente sua eficácia"
}

{
    "pergunta": "O porte de arma é transferível?",
    "docs_relevantes": ["Anexo XVII - Porte de arma de fogo.pdf"],
    "resposta_esperada": "Não, o porte é pessoal, intransferível e revogável"
}

{
    "pergunta": "Qual a validade do porte federal de arma?",
    "docs_relevantes": ["Anexo XVII - Porte de arma de fogo.pdf"],
    "resposta_esperada": "Válido em todo território nacional, com prazo definido no certificado"
}
```

### Categoria 4: Perguntas sobre Capacitação Técnica

```python
{
    "pergunta": "O que é necessário para comprovar capacidade técnica para manuseio de arma?",
    "docs_relevantes": ["cartilha-de-armamento-e-tiro.pdf"],
    "resposta_esperada": "Conhecimento de conceituação, normas de segurança, componentes da arma e habilidade de uso"
}

{
    "pergunta": "Quem elaborou a cartilha de armamento e tiro?",
    "docs_relevantes": ["cartilha-de-armamento-e-tiro.pdf"],
    "resposta_esperada": "Serviço de Armamento e Tiro (SAT) da Academia Nacional de Polícia (ANP) e CONAT/DARM"
}

{
    "pergunta": "Quais são as normas de segurança para manuseio de arma de fogo?",
    "docs_relevantes": ["cartilha-de-armamento-e-tiro.pdf"],
    "resposta_esperada": "Conhecimento de segurança, componentes e partes da arma"
}
```

### Categoria 5: Perguntas sobre Lei 10.826/2003

```python
{
    "pergunta": "O que a Lei 10.826 regulamenta?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"],
    "resposta_esperada": "Registro, posse e comercialização de armas de fogo e munição"
}

{
    "pergunta": "Quando foi sancionada a Lei 10.826?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"],
    "resposta_esperada": "22 de dezembro de 2003"
}

{
    "pergunta": "O que acontece se o portador for detido embriagado?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf", "Anexo XVII - Porte de arma de fogo.pdf"],
    "resposta_esperada": "A autorização de porte perde automaticamente sua eficácia (Art. 10, §2º)"
}
```

### Categoria 6: Perguntas Conceituais (Docs .txt)

```python
{
    "pergunta": "O que é calibre de arma?",
    "docs_relevantes": ["calibres_armas.txt"],
    "resposta_esperada": "Medida do diâmetro interno do cano"
}

{
    "pergunta": "Quais são as principais marcas brasileiras de armas?",
    "docs_relevantes": ["marcas_armas.txt"],
    "resposta_esperada": "Taurus, Rossi, CBC, Boito"
}

{
    "pergunta": "Diferença entre pistola e revólver?",
    "docs_relevantes": ["tipos_armas.txt"],
    "resposta_esperada": "Pistola usa carregador, revólver usa tambor"
}
```

### Categoria 7: Perguntas Cruzadas (PDFs + .txt)

```python
{
    "pergunta": "Como funciona o registro de armas no Brasil?",
    "docs_relevantes": ["LEI-10.826-03-SINARM.pdf", "sistema_sinarm.txt"],
    "resposta_esperada": "Através do SINARM, sistema da Polícia Federal"
}

{
    "pergunta": "Quais documentos regulam o porte de arma no Brasil?",
    "docs_relevantes": ["estatuto_desarmamento.pdf", "LEI-10.826-03-SINARM.pdf", "Anexo XVII - Porte de arma de fogo.pdf"],
    "resposta_esperada": "Estatuto do Desarmamento, Lei 10.826/2003, Decreto 9.847/19"
}
```

---

## 📊 DATASET COMPLETO (Python)

```python
dataset_teste_completo = [
    # SINARM
    {
        "pergunta": "O que é o SINARM?",
        "docs_relevantes": ["LEI-10.826-03-SINARM.pdf", "sistema_sinarm.txt"]
    },
    {
        "pergunta": "Onde funciona o SINARM?",
        "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"]
    },
    
    # Porte de Arma
    {
        "pergunta": "O que acontece se o portador de arma for detido embriagado?",
        "docs_relevantes": ["Anexo XVII - Porte de arma de fogo.pdf", "LEI-10.826-03-SINARM.pdf"]
    },
    {
        "pergunta": "O porte de arma é transferível?",
        "docs_relevantes": ["Anexo XVII - Porte de arma de fogo.pdf"]
    },
    
    # Capacitação
    {
        "pergunta": "O que é necessário para comprovar capacidade técnica para manuseio de arma?",
        "docs_relevantes": ["cartilha-de-armamento-e-tiro.pdf"]
    },
    {
        "pergunta": "Quem elaborou a cartilha de armamento e tiro?",
        "docs_relevantes": ["cartilha-de-armamento-e-tiro.pdf"]
    },
    
    # Lei 10.826
    {
        "pergunta": "O que a Lei 10.826 regulamenta?",
        "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"]
    },
    {
        "pergunta": "Quando foi sancionada a Lei 10.826?",
        "docs_relevantes": ["LEI-10.826-03-SINARM.pdf"]
    },
    
    # Conceituais (.txt)
    {
        "pergunta": "O que é calibre de arma?",
        "docs_relevantes": ["calibres_armas.txt"]
    },
    {
        "pergunta": "Diferença entre pistola e revólver?",
        "docs_relevantes": ["tipos_armas.txt"]
    },
    
    # Cruzadas
    {
        "pergunta": "Como funciona o registro de armas no Brasil?",
        "docs_relevantes": ["LEI-10.826-03-SINARM.pdf", "sistema_sinarm.txt"]
    },
    {
        "pergunta": "Quais documentos regulam o porte de arma no Brasil?",
        "docs_relevantes": ["estatuto_desarmamento.pdf", "LEI-10.826-03-SINARM.pdf", "Anexo XVII - Porte de arma de fogo.pdf"]
    },
]
```

---

## 🎯 MÉTRICAS ESPERADAS

### Com os PDFs reais:

| Métrica | Objetivo | Descrição |
|---------|----------|-----------|
| **Precision@5** | > 0.80 | 80%+ dos top-5 são relevantes |
| **MRR** | > 0.70 | Primeiro relevante nas primeiras posições |
| **Recall@5** | > 0.75 | 75%+ dos relevantes são recuperados |

### Casos de Sucesso:

✅ **Pergunta:** "O que é o SINARM?"
- **Esperado:** `LEI-10.826-03-SINARM.pdf` em 1º lugar
- **Precision@5:** 1.0 (se todos top-5 falam de SINARM)

✅ **Pergunta:** "O porte de arma é transferível?"
- **Esperado:** `Anexo XVII - Porte de arma de fogo.pdf` em 1º lugar
- **MRR:** 1.0 (primeiro resultado é o correto)

### Casos de Falha:

❌ **Pergunta muito genérica:** "Fale sobre armas"
- **Problema:** Todos os documentos são relevantes
- **Solução:** Refinar pergunta

❌ **Pergunta sobre conteúdo não presente:** "Qual o preço de uma Glock?"
- **Problema:** Informação não está nos documentos
- **Solução:** Sistema deve responder "Não encontrei informações"

---

## 🧪 TESTES RECOMENDADOS

### Teste 1: Busca Específica
```python
pergunta = "O que é o SINARM?"
# Deve retornar: LEI-10.826-03-SINARM.pdf em 1º lugar
```

### Teste 2: Busca com Múltiplos Documentos
```python
pergunta = "Quais documentos regulam o porte de arma?"
# Deve retornar: estatuto_desarmamento.pdf, LEI-10.826-03-SINARM.pdf, Anexo XVII
```

### Teste 3: Busca Conceitual
```python
pergunta = "O que é calibre?"
# Deve retornar: calibres_armas.txt em 1º lugar
```

### Teste 4: Busca com Reranking
```python
pergunta = "O que acontece se o portador for detido embriagado?"
# SEM reranking: pode retornar documentos irrelevantes
# COM reranking: deve retornar Anexo XVII em 1º lugar
```

---

## 📝 OBSERVAÇÕES

### Encoding dos PDFs
- ⚠️ Alguns PDFs têm encoding problemático (caracteres estranhos)
- ✅ PyPDF2 consegue extrair texto, mas pode ter erros
- 💡 Considerar OCR para PDFs escaneados

### Qualidade dos Chunks
- ✅ Chunking semântico funciona melhor que fixo
- ✅ Overlap de 50 caracteres evita perder contexto
- 💡 Testar diferentes tamanhos (300, 500, 700 chars)

### Reranking
- ✅ CrossEncoder melhora drasticamente a precisão
- ✅ Especialmente importante para perguntas específicas
- 💡 Trade-off: +10x tempo, mas +100% precisão

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
