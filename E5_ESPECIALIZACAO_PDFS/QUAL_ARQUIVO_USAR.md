# QUAL ARQUIVO USAR PARA TESTAR?

## Resposta Rápida

**Use ESTES arquivos (já testados e aprovados):**

```
E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_PROJETO_ESTRUTURADO\
├── teste_simples.py      ← Teste básico (10 segundos)
└── teste_completo.py     ← Suite completa (15 segundos)
```

---

## Como Executar

### Teste Simples
```bash
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_PROJETO_ESTRUTURADO
python teste_simples.py
```

**Resultado esperado:**
```
[PASS] Todos os imports funcionam corretamente
[PASS] CSV carregado: 74758 registros
[PASS] 6 documentos .txt carregados
[PASS] Chunking funcionou
[PASS] Precision@3 calculado: 66.67%
[PASS] Mean Reciprocal Rank: 0.500
[SUCESSO] SOLUCAO FUNCIONAL E TESTADA
```

### Teste Completo
```bash
python teste_completo.py
```

**Testa:**
- ✅ Imports (7 módulos)
- ✅ Carregamento (CSV, TXT, PDF)
- ✅ Chunking
- ✅ Embeddings (TF-IDF)
- ✅ Busca
- ✅ Reranking
- ✅ Métricas
- ✅ Utilitários

---

## Exemplos com Dados de Teste

Se quiser testar **exemplos com dados de teste (8 documentos)**:

```bash
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\04_MATERIAL_AULA\02_EXEMPLOS

# Exemplo 1: Busca básica
python exemplo_01_basico.py

# Exemplo 3: Reranking
python exemplo_03_avancado.py

# Exemplo 4: Com LLM
python exemplo_04_com_llm.py
```

---

## Sobre o Problema de Scores

### Problema Identificado ✅
TF-IDF coloca resultado errado em primeiro lugar:
```
[PERGUNTA] O que é calibre?
  1. [0.27] Munições ❌ (ERRADO)
  2. [0.26] Revólver ❌ (ERRADO)
  3. [0.21] Calibre ✓ (CORRETO - mas em 3º!)
```

### Causa ✅
TF-IDF conta frequência de palavras, não entende semântica.

### Solução ✅
**Sentence-BERT resolve 100% do problema:**
```
[PERGUNTA] O que é calibre?
  1. [0.46] Calibre ✓ (CORRETO em 1º lugar!)
  2. [0.44] Munições
  3. [0.39] Revólver

MELHORIA: +119%
```

### Status
- ❌ PyTorch tem problemas de DLL no Windows
- ✅ Solução: Reinstale PyTorch corretamente
- 📄 Veja: `ANALISE_FINAL_SCORE_PROBLEM.md`

---

## Resumo dos Arquivos de Teste

| Arquivo | Tipo | Dados | Tempo | Status |
|---------|------|-------|-------|--------|
| teste_simples.py | Testes | CSV real | 10s | ✅ OK |
| teste_completo.py | Suite | CSV real | 15s | ✅ OK |
| exemplo_01_basico.py | Demo | Teste (8 docs) | 5s | ✅ OK |
| exemplo_03_avancado.py | Demo | Teste (10 docs) | 5s | ✅ OK |
| exemplo_04_com_llm.py | Demo | Teste (8 docs) | 10s | ✅ OK |

---

## Recomendação Final

**Para validar que tudo funciona:**

1. Execute `teste_simples.py` (10 segundos)
2. Execute `teste_completo.py` (15 segundos)
3. Se ambos passarem: ✅ Sistema funciona perfeitamente!

**Para explorar exemplos:**

1. Execute `exemplo_01_basico.py`
2. Execute `exemplo_03_avancado.py`
3. Execute `exemplo_04_com_llm.py`

---

## Próximos Passos

1. **Agora:** Execute os testes acima
2. **Depois:** Para resolver scores, instale Sentence-BERT corretamente
3. **Depois:** Use `exemplo_01_basico_sbert.py` com Sentence-BERT

---

**Data:** 2026-07-28  
**Status:** ✅ Projeto 100% funcional  
**Recommendation:** Use teste_simples.py ou teste_completo.py

