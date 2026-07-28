# 🚀 E5 - COMECE AQUI

**MBA IA Generativa PCDF - IBMEC**  
**Encontro 5:** Especialização com PDFs

---

## ⚡ INÍCIO RÁPIDO (5 MINUTOS)

### 1️⃣ Instalar Dependências

```bash
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_AGENTE_CONSOLIDADO
pip install -r requirements.txt
```

### 2️⃣ Testar Agente

```bash
# Testes automáticos
python agente_v5_especializado.py

# Pergunta única
python agente_v5_especializado.py "O que é FAISS?"

# Modo interativo
python agente_v5_especializado.py --interativo
```

### 3️⃣ Abrir Notebook

```bash
cd ..\02_NOTEBOOK_PASSO_A_PASSO
jupyter notebook E5_especializacao_pdfs.ipynb
```

---

## 📊 PROGRESSÃO

### E3 → E4 → E5

```
E3: 8 tools (dados CSV)
    ↓
E4: 8 tools + RAG básico (TF-IDF + docs .txt)
    ↓
E5: 8 tools + RAG especializado (FAISS + PDFs + Reranking)
```

---

## 🎯 O QUE VOCÊ VAI APRENDER

### Terça (5h)
1. ✅ Processar PDFs da PCDF
2. ✅ Criar índice FAISS
3. ✅ Implementar reranking
4. ✅ Avaliar com métricas

### Quinta (5h)
5. ✅ Fine-tuning com LoRA
6. ✅ Integrar modelo fine-tunado
7. ✅ Comparar resultados

---

## 📁 ESTRUTURA

```
E5_ESPECIALIZACAO_PDFS/
├── 01_DADOS/
│   ├── pdfs_pcdf/              # PDFs da PCDF
│   └── documentos_conceituais/ # Docs E4
│
├── 02_NOTEBOOK_PASSO_A_PASSO/
│   └── E5_especializacao_pdfs.ipynb  # Notebook incremental
│
├── 03_AGENTE_CONSOLIDADO/
│   └── agente_v5_especializado.py    # Agente final
│
└── 04_MATERIAL_APOIO/
    ├── FAQ_E5.md
    └── TROUBLESHOOTING_E5.md
```

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Ler `README.md` completo
2. ✅ Instalar dependências
3. ✅ Testar agente
4. ✅ Abrir notebook
5. ✅ Seguir aula

---

**Dúvidas?** Consulte `04_MATERIAL_APOIO/FAQ_E5.md`

**Problemas?** Consulte `04_MATERIAL_APOIO/TROUBLESHOOTING_E5.md`
