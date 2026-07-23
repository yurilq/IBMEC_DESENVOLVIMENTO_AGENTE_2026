# 📢 COMUNICADO PARA ALUNOS - E4_RAG_FAISS

**Data:** 23/07/2026  
**Assunto:** Material E4 atualizado + Troubleshooting para problemas comuns

---

## ✅ O QUE FOI CORRIGIDO

Atualizei o material da aula prática E4 (RAG + TF-IDF) com correções para **3 erros comuns** que apareceram nos testes:

### 1️⃣ Erro: `scikit-learn==1.9.0` não encontrado
**✅ CORRIGIDO** - `requirements.txt` atualizado com versões corretas

### 2️⃣ Erro: `UnicodeDecodeError: 'charmap' codec`
**✅ CORRIGIDO** - Script agora tenta múltiplos encodings automaticamente (latin1, utf-8, cp1252, iso-8859-1)

### 3️⃣ Erro: `ModuleNotFoundError: No module named 'pandas'`
**✅ DOCUMENTADO** - Guia completo de como resolver problemas com venv

---

## 📥 COMO ATUALIZAR SEU REPOSITÓRIO

```bash
# 1. Baixar atualizações
git pull origin main

# 2. Reinstalar dependências (versões corrigidas)
pip install -r E4_RAG_FAISS/requirements.txt --upgrade

# 3. Testar se está tudo funcionando
cd E4_RAG_FAISS
python teste_funcoes_direto.py
```

**Resultado esperado:** Todos os testes devem passar ✅

---

## 🆘 SE TIVER PROBLEMAS

Criamos 2 guias de troubleshooting detalhados:

### 📄 Para erro de encoding UTF-8:
```
E4_RAG_FAISS/TROUBLESHOOTING_ENCODING.md
```
**Contém:**
- 4 soluções diferentes
- Script de diagnóstico
- Como converter CSV manualmente

### 📄 Para erro de módulos/venv:
```
E4_RAG_FAISS/TROUBLESHOOTING_VENV.md
```
**Contém:**
- Como instalar dependências corretamente
- Diferença entre venv e Python global
- Como recriar venv do zero
- Checklist completo de diagnóstico

---

## 🎯 PREPARAÇÃO PARA AULA

### Opção A: Usar Python Global (RECOMENDADO - mais simples)
```bash
# 1. NÃO criar venv
cd E4_RAG_FAISS

# 2. Instalar dependências globalmente
pip install -r requirements.txt

# 3. Testar
python teste_funcoes_direto.py
```
**Vantagens:** Mais simples, menos erros

---

### Opção B: Usar venv (avançado)
```bash
# 1. Criar venv
cd E4_RAG_FAISS
python -m venv venv

# 2. Ativar
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Testar
python teste_funcoes_direto.py
```
**Vantagens:** Isolamento, boa prática

---

## ✅ VALIDAÇÃO

Após seguir os passos acima, você deve ver:

```
======================================================================
TODOS OS TESTES CONCLUIDOS COM SUCESSO!
======================================================================
```

Com os seguintes resultados:
- ✅ Taurus: 17.760 armas
- ✅ Calibre .380: 17.564 armas
- ✅ RAG: 20 documentos indexados
- ✅ TF-IDF: 1.000 features

---

## 📚 ARQUIVOS IMPORTANTES

```
E4_RAG_FAISS/
├── requirements.txt               ← ✅ VERSÕES CORRIGIDAS
├── GUIA_RAPIDO_DIA_DA_AULA.md    ← Resumo para o professor
├── ROTEIRO_AULA_ATUALIZADO_TF_IDF.md  ← Roteiro completo 120 min
├── TROUBLESHOOTING_ENCODING.md    ← ✨ NOVO - Erros UTF-8
├── TROUBLESHOOTING_VENV.md        ← ✨ NOVO - Erros de módulos
├── teste_funcoes_direto.py        ← Script para validar setup
└── scripts_agente/
    ├── tools_basicas_v2.py        ← ✅ ENCODING CORRIGIDO
    └── agente_v4_5_rag.py         ← Agente RAG com TF-IDF
```

---

## 🤔 DÚVIDAS FREQUENTES

### "Preciso deletar meu venv antigo?"
Não necessariamente. Tente primeiro:
```bash
pip install -r requirements.txt --upgrade
```

### "Posso usar Python global ao invés de venv?"
**Sim!** É até mais simples para esta aula. Veja "Opção A" acima.

### "Como saber se está funcionando?"
```bash
python teste_funcoes_direto.py
```
Deve mostrar todos os testes com ✅

### "Ainda estou com erro, e agora?"
1. Verifique os arquivos de troubleshooting
2. Tente a "Solução Universal" no `GUIA_RAPIDO_DIA_DA_AULA.md`
3. Peça ajuda no Discord/Slack da turma
4. Fale com o professor no início da aula

---

## 📊 REQUISITOS MÍNIMOS

- **Python:** 3.10 ou superior (`python --version`)
- **Espaço:** ~500 MB para dependências
- **Sistema:** Windows 10/11, Linux, ou macOS
- **Opcional:** Ollama instalado (pode usar OpenRouter como alternativa)

---

## 🎓 NO DIA DA AULA

**Chegue 10 minutos antes** para validar seu ambiente:

```bash
# 1. Ir para pasta
cd E4_RAG_FAISS

# 2. Rodar teste
python teste_funcoes_direto.py

# 3. Se tudo ✅ → você está pronto!
# 4. Se algo ❌ → consultar troubleshooting ou pedir ajuda
```

---

## 📞 SUPORTE

**Durante a aula:**
- Levantar a mão
- Compartilhar tela no Zoom (se online)
- Pedir ajuda ao colega ao lado

**Antes da aula:**
- Discord/Slack da turma
- Email do professor
- GitHub Issues (abrir issue com print do erro)

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Atualizar repositório (`git pull`)
2. ✅ Reinstalar dependências (`pip install -r requirements.txt`)
3. ✅ Testar ambiente (`python teste_funcoes_direto.py`)
4. ✅ Ler `ROTEIRO_AULA_ATUALIZADO_TF_IDF.md` (opcional)
5. ✅ Chegar 10 min antes na aula

---

**Nos vemos na aula! 🎯**

Professor Yuri  
E4 - RAG, Few-Shot, e Chain-of-Thought
