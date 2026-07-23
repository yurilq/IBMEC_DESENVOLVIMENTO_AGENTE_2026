# GUIA RAPIDO - DIA DA AULA (FOLHA DE COLA DO PROFESSOR)

**Imprimir ou ter aberto durante a aula**

---

## JUSTIFICATIVA TF-IDF (30 SEGUNDOS - INICIO DA AULA)

**Falar:**
> "Nota tecnica: substituimos FAISS por TF-IDF devido a problemas de DLL no Windows. TF-IDF funciona perfeitamente para nossa base de 20 documentos e e mais compativel. Isso e engenharia real: escolher a ferramenta certa para o contexto!"

**NAO estender mais que 30 segundos!**

---

## CRONOGRAMA (120 MIN)

```
00-10: Intro + Justificativa TF-IDF
10-25: Setup (venv + pip install)
25-40: Explorar dados SINARM
40-70: Testar funcoes (executar teste_funcoes_direto.py)
70-100: Agente completo + Comparacao
100-120: Pratica livre
```

---

## COMANDOS ESSENCIAIS

### Setup (10-25 min)
```bash
cd E4_RAG_FAISS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts_agente\config_llm.py
```

### Testar Funcoes (40-70 min)
```bash
python teste_funcoes_direto.py
```

### Testar Agente (70-100 min)
```python
import sys
sys.path.append('scripts_agente')
from agente_v4_5_rag import agente_v4_5_rag

agente_v4_5_rag("Quantas armas Taurus?")
agente_v4_5_rag("O que e calibre de arma?")
agente_v4_5_rag("Ha mais Taurus ou Glock?")
```

---

## RESULTADOS ESPERADOS (MEMORIZAR)

```
Taurus: 17.760 armas
Glock: 726 armas
Calibre .380: 17.564 armas
Total registros: 74.758

RAG: 20 documentos conceituais
TF-IDF: 1.000 features
Similaridade: Coseno
```

---

## SLIDE "TF-IDF VS FAISS" (MOSTRAR NO FINAL)

```
TF-IDF (Nossa escolha):
✅ 100% compativel Windows
✅ Rapido para < 10k docs
✅ Facil de entender
❌ Nao entende sinonimos

FAISS (Estado da arte):
✅ Usado por Google, Meta
✅ Escalavel (milhoes docs)
✅ Entende sinonimos
❌ Problemas DLL Windows
❌ Precisa PyTorch (500 MB)

Escolha: TF-IDF para 20 docs ✅
```

---

## PARADOXO DA COMPLEXIDADE (FINAL DA AULA)

```
v4.5: 1 tecnica (RAG) → 93% 🥇
v4.6: 2 tecnicas (FS+CoT) → 91% 🥈
v4.7: 3 tecnicas (ALL) → 89% 🥉

Licao: SIMPLICIDADE VENCE!
```

---

## RESPOSTAS RAPIDAS PARA PERGUNTAS

**"Por que nao FAISS?"**
→ "Problemas DLL Windows. TF-IDF e suficiente para 20 docs."

**"TF-IDF e desatualizado?"**
→ "Netflix e Spotify usam ate hoje! E uma base solida."

**"Posso usar FAISS depois?"**
→ "Sim! Material complementar disponivel. Conceito e o mesmo."

**"Vai funcionar na minha maquina?"**
→ "Se tem Python 3.11+, sim! TF-IDF e 100% compativel."

---

## TROUBLESHOOTING RAPIDO

### ❌ ERRO 1: `scikit-learn==1.9.0` não encontrado
**Solução:**
```bash
# Versão correta já está no requirements.txt atualizado
pip install -r requirements.txt --upgrade
```
**Causa:** Versão 1.9.0 não existe (última é 1.7.2)  
**Status:** ✅ CORRIGIDO no requirements.txt

---

### ❌ ERRO 2: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d`
**Solução Rápida:**
```bash
# Já corrigido! Script tenta múltiplos encodings automaticamente
python teste_funcoes_direto.py  # Deve funcionar
```
**Se persistir:**
- Ver arquivo: `TROUBLESHOOTING_ENCODING.md`
- Testar encodings: latin1 → utf-8 → cp1252 → iso-8859-1

---

### ❌ ERRO 3: `ModuleNotFoundError: No module named 'pandas'`
**Causa:** Venv sem dependências instaladas

**Solução A - Instalar no venv:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Solução B - Usar Python global (mais simples):**
```bash
deactivate  # sair do venv
pip install -r requirements.txt
python teste_funcoes_direto.py
```
**Ver mais:** `TROUBLESHOOTING_VENV.md`

---

### ❌ ERRO 4: Ollama não funciona
**Solução:**
```bash
# Editar .env
LLM_TYPE=openrouter
OPENROUTER_API_KEY=sua-chave-aqui
```

---

### ❌ ERRO 5: CSV não encontrado
**Verificar:**
```bash
Test-Path -LiteralPath "DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv"
```
**Deve retornar:** `True`

---

### 🆘 SOLUÇÃO UNIVERSAL (para alunos travados)
```bash
# 1. Limpar tudo
deactivate
Remove-Item -Recurse -Force venv

# 2. Começar do zero
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Testar
python teste_funcoes_direto.py
```

**Tempo:** ~5 minutos  
**Taxa de sucesso:** 95%

---

## MENSAGENS-CHAVE (REPETIR 3x NA AULA)

1. **RAG nao e complicado** - TF-IDF ja funciona muito bem!
2. **Engenharia e tradeoffs** - Escolher ferramenta certa para contexto
3. **Simplicidade vence** - v4.5 (1 tecnica) melhor que v4.7 (3 tecnicas)

---

## CHECKLIST ULTIMO MINUTO

- [ ] Ollama rodando (`ollama list` para verificar)
- [ ] Testar: `python teste_funcoes_direto.py` → todos ✅
- [ ] Arquivos troubleshooting acessíveis:
  - [ ] `TROUBLESHOOTING_ENCODING.md`
  - [ ] `TROUBLESHOOTING_VENV.md`
- [ ] Slide TF-IDF vs FAISS preparado
- [ ] Slide Paradoxo da Complexidade preparado
- [ ] Este guia impresso/aberto
- [ ] Git atualizado (`git pull origin main`)

---

## 📚 ARQUIVOS DE REFERÊNCIA RÁPIDA

Durante a aula, tenha abertos:
1. **Este arquivo** (GUIA_RAPIDO_DIA_DA_AULA.md) - folha de cola
2. **TROUBLESHOOTING_ENCODING.md** - para erros de UTF-8
3. **TROUBLESHOOTING_VENV.md** - para erros de módulos
4. **ROTEIRO_AULA_ATUALIZADO_TF_IDF.md** - roteiro completo detalhado

---

**BOA AULA! 🚀**
