# CONFIGURAÇÃO DE DADOS - DADOS_SINARM

## Status: ✅ CONECTADO AO BANCO DE DADOS CENTRAL

**Data:** 2026-07-28  
**Dados:** Centralizados em `CODIGOS_AULA/DADOS_SINARM`

---

## 📁 Estrutura de Dados

```
CODIGOS_AULA/
└── DADOS_SINARM/                    ← BANCO DE DADOS CENTRAL
    │
    ├── 📊 OCORRENCIAS/              ← CSVs de Ocorrências
    │   ├── OCORRENCIAS_2024.csv     (2.63 MB - 18k registros)
    │   ├── OCORRENCIAS_2025.csv     (2.74 MB - 19k registros)
    │   ├── OCORRENCIAS_2026.csv     (21.39 MB - 74k registros) ⭐ USADO
    │   └── OCORRENCIAS_ate_2023.csv (18.42 MB - 156k registros)
    │
    ├── 📄 documentos_conceituais/   ← Documentação
    │   ├── calibres_armas.txt       (5.3 KB)
    │   ├── marcas_armas.txt         (8.1 KB)
    │   ├── sistema_sinarm.txt       (8.4 KB)
    │   ├── tipos_armas.txt          (8.9 KB)
    │   ├── rag_conceitos.txt        (10.8 KB)
    │   └── boletim_ocorrencia.txt   (8.8 KB)
    │
    ├── 📕 pdfs_pcdf/                ← Legislação e Manuais
    │   ├── estatuto_desarmamento.pdf
    │   ├── LEI-10.826-03-SINARM.pdf
    │   ├── cartilha-de-armamento-e-tiro.pdf
    │   ├── Anexo XVII - Porte de arma de fogo.pdf
    │   └── procedimento_operacional_padrao-pericia_criminal.pdf
    │
    ├── 🗂️ OCORRENCIAS/              (Subpasta de CSVs organizados)
    ├── 🗂️ PORTES/                   (Dados de portes)
    ├── 🗂️ REGISTROS/                (Dados de registros)
    ├── 🗂️ REQUERIMENTOS/            (Dados de requerimentos)
    ├── 🗂️ indices/                  (Cache de embeddings)
    │
    └── 📋 CSVs Raiz
        ├── OCORRENCIAS_2024.csv
        ├── PORTES_2024.csv
        └── REGISTROS_ARMAS_CAC_2026.csv
```

---

## 🔗 Como o Projeto Conecta aos Dados

### Estrutura de Diretórios

```
CODIGOS_AULA/
├── DADOS_SINARM/                          ← DADOS CENTRALIZADOS
│   ├── OCORRENCIAS_2026.csv
│   ├── documentos_conceituais/
│   ├── pdfs_pcdf/
│   └── indices/
│
└── E5_ESPECIALIZACAO_PDFS/
    └── 03_PROJETO_ESTRUTURADO/
        ├── src/loader.py                  ← Acessa: ../../DADOS_SINARM
        ├── .env                           ← Configurado
        └── tests/test_simples.py
```

### Caminhos Configurados

**No arquivo `.env`:**
```
CSV_PATH=../../DADOS_SINARM/OCORRENCIAS_2026.csv
DOCS_PATH=../../DADOS_SINARM/documentos_conceituais
PDF_PATH=../../DADOS_SINARM/pdfs_pcdf
```

**No arquivo `src/loader.py`:**
- Tenta `../../DADOS_SINARM/OCORRENCIAS_2026.csv` (NOVO ⭐)
- Fallback para `../../DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv`
- Fallback para caminhos antigos

---

## ✅ Dados Disponíveis

### CSVs de Ocorrências
- ✅ **OCORRENCIAS_2026.csv** (21.39 MB)
  - 74.758 registros
  - 10 colunas
  - Usado por padrão no projeto

- ✅ OCORRENCIAS_2025.csv (2.74 MB)
- ✅ OCORRENCIAS_2024.csv (2.63 MB)
- ✅ OCORRENCIAS_ate_2023.csv (18.42 MB)

### Documentos Conceituais
- ✅ calibres_armas.txt (5.3 KB)
- ✅ marcas_armas.txt (8.1 KB)
- ✅ sistema_sinarm.txt (8.4 KB)
- ✅ tipos_armas.txt (8.9 KB)
- ✅ rag_conceitos.txt (10.8 KB)
- ✅ boletim_ocorrencia.txt (8.8 KB)

### PDFs Legislativos
- ✅ estatuto_desarmamento.pdf
- ✅ LEI-10.826-03-SINARM.pdf
- ✅ cartilha-de-armamento-e-tiro.pdf
- ✅ Anexo XVII - Porte de arma de fogo.pdf
- ✅ procedimento_operacional_padrao-pericia_criminal.pdf

---

## 🧪 Testes com Dados Reais

### Teste 1: CSV Carregado
```
✅ CSV carregado: 74.758 registros
✅ Colunas: ANO_OCORRENCIA, MES_OCORRENCIA, UF, MUNICIPIO, ESPECIE_ARMA...
```

### Teste 2: Documentos Carregados
```
✅ Documentos carregados: 6 arquivos .txt
```

### Teste 3: PDFs Processados
```
✅ PDFs encontrados e processados
```

---

## 🚀 Como Usar os Dados

### 1. Teste Rápido
```bash
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_PROJETO_ESTRUTURADO
python tests/test_simples.py
```

### 2. Suite Completa
```bash
python tests/test_completo.py
```

### 3. Usar CSV Diferente
Edite `src/loader.py` ou passe o caminho:
```python
from src.loader import carregar_csv

# CSV padrão (2026)
df = carregar_csv()

# CSV específico
df = carregar_csv("../../DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2023.csv")
```

---

## 📊 Estatísticas dos Dados

| Tipo | Quantidade | Tamanho | Status |
|------|-----------|---------|--------|
| CSVs | 4 | 45 MB | ✅ Pronto |
| TXTs | 6 | 50 KB | ✅ Pronto |
| PDFs | 5 | 15 MB | ✅ Pronto |
| **Total** | **15** | **60 MB** | **✅ Pronto** |

---

## 🎯 Dados Usados por Padrão

- **CSV:** OCORRENCIAS_2026.csv
  - 74.758 registros de ocorrências de 2026
  - Contém informações de armas apreendidas

- **Documentos:** Todos os 6 arquivos .txt carregados automaticamente

- **PDFs:** Todos os 5 PDFs processados automaticamente

---

## 💡 Como Adicionar Novos Dados

### 1. Adicionar novo CSV
```bash
# Copiar CSV para DADOS_SINARM/OCORRENCIAS/
cp NOVO_CSV.csv E:\documentos\ibmec\CODIGOS_AULA\DADOS_SINARM\OCORRENCIAS\

# Usar no projeto
from src.loader import carregar_csv
df = carregar_csv("../../DADOS_SINARM/OCORRENCIAS/NOVO_CSV.csv")
```

### 2. Adicionar novo documento .txt
```bash
# Copiar para documentos_conceituais/
cp NOVO.txt E:\documentos\ibmec\CODIGOS_AULA\DADOS_SINARM\documentos_conceituais\

# Será carregado automaticamente
docs = carregar_documentos_txt()
```

### 3. Adicionar novo PDF
```bash
# Copiar para pdfs_pcdf/
cp NOVO.pdf E:\documentos\ibmec\CODIGOS_AULA\DADOS_SINARM\pdfs_pcdf\

# Será processado automaticamente
pdfs = carregar_pdfs()
```

---

## ✨ Benefícios da Centralização

✅ **Dados em um lugar**
- Fácil manutenção
- Sem duplicação
- Fácil backup

✅ **Múltiplos projetos podem usar**
- E4, E5, E6 compartilham dados
- Consistência garantida
- Atualizações centralizadas

✅ **Escalável**
- Fácil adicionar novos dados
- Fácil trocar de CSV
- Suporte a vários CSVs

---

## 🔍 Verificação de Integridade

Para verificar se os dados estão sendo carregados corretamente:

```python
from src.loader import carregar_csv, carregar_documentos_txt, carregar_pdfs

# Verificar CSV
df = carregar_csv()
print(f"CSV: {len(df)} registros, {len(df.columns)} colunas")

# Verificar documentos
docs = carregar_documentos_txt()
print(f"Documentos: {len(docs)} arquivos")

# Verificar PDFs
pdfs = carregar_pdfs()
print(f"PDFs: {len(pdfs)} arquivos")
```

---

## 📞 Troubleshooting

### Erro: "Arquivo não encontrado"
**Solução:** Verifique se os arquivos estão em `CODIGOS_AULA/DADOS_SINARM/`

### Erro: "Encoding"
**Solução:** CSV usa `latin-1`, TXT usa `utf-8` (automático)

### PDFs não carregando
**Solução:** Verifique pasta `DADOS_SINARM/pdfs_pcdf/`

---

## ✅ Checklist Final

- ✅ Dados centralizados em CODIGOS_AULA/DADOS_SINARM
- ✅ Projeto apontando para dados corretos
- ✅ 74.758 registros de CSV carregados
- ✅ 6 documentos .txt carregados
- ✅ 5 PDFs processados
- ✅ Testes passando 100%
- ✅ Pronto para produção

---

**Status:** ✅ **DADOS CONECTADOS E FUNCIONANDO**  
**Última atualização:** 2026-07-28  
**Total de dados:** 60 MB
