# ⚡ SETUP RÁPIDO - E4 RAG + FAISS

## 📋 PASSO A PASSO (5 minutos)

### 1️⃣ Copiar Dados SINARM

**Opção A - Script Automático (Recomendado):**

```bash
# 1. Abrir terminal na pasta 03_CODIGOS_PRONTOS
cd "E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E4_RAG_FAISS\03_CODIGOS_PRONTOS"

# 2. Executar script de cópia
copiar_dados_sinarm.bat
```

**Opção B - Manual:**

```bash
# Copiar pasta DADOS_SINARM
xcopy /E /I /Y "..\..\DADOS_SINARM" "DADOS_SINARM"
```

---

### 2️⃣ Validar Configuração

```bash
python validar_configuracao.py
```

**Resultado esperado:**
```
🎉 CONFIGURAÇÃO OK!
✅ Tudo configurado corretamente!
```

Se houver erros, siga as instruções na tela.

---

### 3️⃣ Instalar Dependências (se necessário)

```bash
pip install pandas numpy sentence-transformers faiss-cpu langchain langchain-community
```

---

### 4️⃣ Executar Pipeline RAG

```bash
# Passo 1: Transformar CSV em documentos
python 01_preparar_documentos.py

# Passo 2: Gerar embeddings
python 02_gerar_embeddings.py

# Passo 3: Criar índice FAISS
python 03_criar_indice_faiss.py

# Passo 4: Testar retrieval
python 04_testar_retrieval.py
```

---

### 5️⃣ Testar Agente v4.5

```bash
python agente_v4_5_rag.py
```

---

## 📁 Estrutura Final

Após configuração, você deve ter:

```
03_CODIGOS_PRONTOS/
├── DADOS_SINARM/              ✅ Copiado
│   └── OCORRENCIAS/
│       └── OCORRENCIAS_2026.csv
├── 03_outputs/                ✅ Criado automaticamente
│   ├── documentos.json
│   ├── embeddings.npy
│   └── faiss_index.bin
├── 01_preparar_documentos.py
├── 02_gerar_embeddings.py
├── 03_criar_indice_faiss.py
├── 04_testar_retrieval.py
├── agente_v4_5_rag.py
└── ...
```

---

## 🆘 Problemas?

### Erro: "Pasta DADOS_SINARM não encontrada"

**Solução:** Execute `copiar_dados_sinarm.bat` ou copie manualmente

---

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install pandas numpy sentence-transformers faiss-cpu langchain langchain-community
```

---

### Script muito lento

**Solução:** Editar `01_preparar_documentos.py` linha ~60:
```python
df_sample = df_ocorrencias.head(100)  # Processar só 100 registros (teste rápido)
```

---

## ✅ Checklist Rápido

- [ ] Pasta DADOS_SINARM copiada
- [ ] `validar_configuracao.py` executou OK
- [ ] Dependências instaladas
- [ ] Pipeline RAG executado (4 scripts)
- [ ] Agente v4.5 testado

---

## 📞 Mais Informações

- **Detalhes completos:** `README_CONFIGURACAO.md`
- **Troubleshooting:** `../04_AVALIACOES_FAQ/TROUBLESHOOTING_E4.md`
- **FAQ:** `../04_AVALIACOES_FAQ/FAQ_E4.md`

---

**Tempo total:** ~5-10 minutos (primeira vez)  
**Resultado:** Pipeline RAG funcionando! 🚀
