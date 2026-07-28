# 🚀 COMECE AQUI - E4 RAG FAISS

**Guia de Início Rápido**

---

## ⚡ Setup Rápido (5 minutos)

### 1. Criar Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Verificar Ambiente
```bash
python 04_UTILITARIOS/verificar_ambiente.py
```

✅ Se tudo OK, prossiga!

---

## 📚 Opção 1: Pipeline RAG (Passo a Passo)

**Melhor para:** Entender como funciona

```bash
cd 02_NOTEBOOK_PASSO_A_PASSO/scripts_auxiliares

# Executar na ordem:
python 01_preparar_documentos.py
python 02_gerar_embeddings.py
python 03_criar_indice_faiss.py
python 04_testar_retrieval.py
```

**O que faz:**
1. Prepara documentos conceituais
2. Gera embeddings (TF-IDF)
3. Cria índice FAISS
4. Testa busca semântica

---

## 🤖 Opção 2: Agente Completo (Direto)

**Melhor para:** Usar o agente pronto

```bash
cd 03_AGENTE_CONSOLIDADO

# Modo interativo
python agente_v4_7_rag_fewshot_cot.py --interativo
```

**Teste:**
```
Sua pergunta: Quantas armas Taurus?
Sua pergunta: O que é calibre?
Sua pergunta: sair
```

---

## 🎯 O que Você Vai Testar

### Perguntas Estruturadas (Tools E3)
```
✅ "Quantas armas Taurus?"
✅ "Top 5 marcas"
✅ "Glock roubadas"
```

### Perguntas Conceituais (RAG - NOVO)
```
✅ "O que é calibre?"
✅ "Como funciona SINARM?"
✅ "Diferença entre furto e roubo?"
```

---

## 📁 Estrutura

```
01_DADOS/                    # Dados estruturados + documentos
02_NOTEBOOK_PASSO_A_PASSO/   # Pipeline RAG
03_AGENTE_CONSOLIDADO/       # Agente final
04_UTILITARIOS/              # Scripts auxiliares
```

---

## 🆘 Problemas?

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "FAISS not found"
```bash
pip install faiss-cpu
```

### Erro: "Ollama connection"
```bash
# Verificar se Ollama está rodando
ollama serve
```

---

## 📚 Próximos Passos

1. ✅ Executar pipeline RAG
2. ✅ Testar agente completo
3. ✅ Comparar E3 vs E4
4. ✅ Consultar material teórico

**Material Teórico:** `MODULO 01\...\E4_RAG_FAISS`

---

**Dúvidas?** Consulte README.md ou material teórico
