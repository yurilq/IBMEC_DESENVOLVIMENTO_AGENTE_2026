# Agente SINARM v4.0 - RAG + 8 Tools E3

**Agente consolidado do E4 com RAG e todas as tools do E3**

---

## Características

### Progressão E3 → E4
- **E3**: 8 tools para dados estruturados (CSV)
- **E4**: 8 tools E3 + RAG para perguntas conceituais

### 9 Tools Implementadas

**Tools E3 (Dados Estruturados):**
1. `contar_armas_marca` - Conta por marca específica
2. `contar_armas_calibre` - Conta por calibre
3. `contar_armas_tipo` - Conta por tipo de ocorrência
4. `contar_armas_combinado` - Marca + tipo
5. `ranking_marcas` - TOP 5 marcas
6. `ranking_calibres` - TOP 5 calibres
7. `estatisticas_gerais` - Resumo completo
8. `distribuicao_marca_por_tipo` - Distribuição

**Tool E4 (RAG):**
9. `buscar_conhecimento` - Busca semântica em documentos conceituais

---

## Modos de Execução

### 1. Testes Automáticos (Padrão)
```bash
python agente_sinarm_v4_rag_completo.py
```

**Executa:**
- 7 testes de dados estruturados (Tools E3)
- 3 testes de RAG (Tool E4)
- Valida funcionamento completo

**Saída esperada:**
```
============================================================
 AGENTE SINARM v4.0 - RAG + 8 TOOLS E3
============================================================
 EXECUTANDO TESTES AUTOMTICOS
============================================================

 TESTES E3 (Dados Estruturados)
------------------------------------------------------------
 Pergunta: Quantas armas Taurus existem?
 Usando: contar_armas_marca
 Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'

...

 TESTES E4 (RAG)
------------------------------------------------------------
 Pergunta: O que  calibre?
 Usando: buscar_conhecimento
 Informaes encontradas:
[1] calibres_armas.txt (relevncia: 0.85)
Calibre  a medida do dimetro interno do cano...
```

### 2. Pergunta Única
```bash
python agente_sinarm_v4_rag_completo.py "Quantas armas Taurus?"
```

**Responde pergunta específica e encerra**

**Exemplos:**
```bash
# Dados estruturados
python agente_sinarm_v4_rag_completo.py "Quantas armas calibre 9mm?"
python agente_sinarm_v4_rag_completo.py "Ranking de marcas"

# RAG
python agente_sinarm_v4_rag_completo.py "O que é SINARM?"
python agente_sinarm_v4_rag_completo.py "Qual a diferença entre pistola e revólver?"
```

### 3. Modo Interativo
```bash
python agente_sinarm_v4_rag_completo.py --interativo
```

**Loop de perguntas até digitar 'sair'**

**Exemplo de sessão:**
```
============================================================
 MODO INTERATIVO
============================================================
Digite suas perguntas (ou 'sair' para encerrar)
------------------------------------------------------------

 Voc: Quantas armas Taurus?
 Agente: Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'

 Voc: O que  calibre?
 Agente: Informaes encontradas:
[1] calibres_armas.txt (relevncia: 0.85)
Calibre  a medida do dimetro interno do cano...

 Voc: sair
 At logo!
```

---

## Roteador Inteligente

O agente decide automaticamente qual tool usar:

### Perguntas de Dados (Tools E3)
- **Contagem**: "Quantas armas Taurus?" → `contar_armas_marca`
- **Calibre**: "Quantas armas 9mm?" → `contar_armas_calibre`
- **Tipo**: "Quantos roubos?" → `contar_armas_tipo`
- **Ranking**: "Ranking de marcas" → `ranking_marcas`
- **Estatísticas**: "Estatísticas gerais" → `estatisticas_gerais`
- **Distribuição**: "Distribuição Taurus" → `distribuicao_marca_por_tipo`

### Perguntas Conceituais (RAG)
- **Definição**: "O que é calibre?" → `buscar_conhecimento`
- **Explicação**: "Explique SINARM" → `buscar_conhecimento`
- **Diferença**: "Diferença entre pistola e revólver?" → `buscar_conhecimento`

---

## Requisitos

### Dependências
```bash
pip install pandas langchain-core scikit-learn
```

### Estrutura de Arquivos
```
E4_RAG_FAISS/
├── 01_DADOS/
│   ├── DADOS_SINARM/
│   │   └── OCORRENCIAS/
│   │       └── OCORRENCIAS_2026.csv
│   └── documentos_conceituais/
│       ├── calibres_armas.txt
│       ├── marcas_armas.txt
│       ├── tipos_armas.txt
│       ├── sistema_sinarm.txt
│       └── rag_conceitos.txt
└── 03_AGENTE_CONSOLIDADO/
    └── agente_sinarm_v4_rag_completo.py
```

---

## Funcionamento Interno

### 1. Carregamento de Dados
```python
# CSV (cache)
@lru_cache(maxsize=1)
def carregar_csv():
    # Tenta múltiplos encodings e separadores
    # Retorna DataFrame com 74.758 registros

# Documentos (cache)
@lru_cache(maxsize=1)
def carregar_documentos_conceituais():
    # Carrega 5 documentos .txt
    # Retorna lista de dicionários
```

### 2. Sistema RAG
```python
class SistemaRAG:
    def inicializar(self):
        # Cria índice TF-IDF dos documentos
    
    def buscar(self, pergunta, k=3):
        # Busca top-K documentos mais relevantes
        # Retorna trechos com similaridade
```

### 3. Roteamento
```python
def rotear_pergunta(pergunta):
    # Analisa pergunta
    # Decide qual tool usar
    # Retorna (tool_function, args)
```

### 4. Processamento
```python
def processar_pergunta(pergunta):
    # Roteia pergunta
    # Executa tool
    # Retorna resposta
```

---

## Exemplos de Uso

### Dados Estruturados

```python
# Contagem por marca
>>> processar_pergunta("Quantas armas Taurus?")
"Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'"

# Contagem por calibre
>>> processar_pergunta("Quantas armas 9mm?")
"Encontrei 275 armas calibre '9mm'"

# Ranking
>>> processar_pergunta("Ranking de marcas")
" TOP 5 Marcas:
1. TAURUS ARMAS S.A.: 17748 armas
2. ROSSI: 16646 armas
..."

# Estatísticas
>>> processar_pergunta("Estatísticas gerais")
" ESTATÍSTICAS GERAIS SINARM
Total de Armas: 74758
..."
```

### RAG (Perguntas Conceituais)

```python
# Definição
>>> processar_pergunta("O que é calibre?")
" Informaes encontradas:
[1] calibres_armas.txt (relevncia: 0.85)
Calibre  a medida do dimetro interno do cano..."

# Explicação
>>> processar_pergunta("O que é SINARM?")
" Informaes encontradas:
[1] sistema_sinarm.txt (relevncia: 0.92)
SINARM  o Sistema Nacional de Armas..."

# Diferença
>>> processar_pergunta("Diferença entre pistola e revólver?")
" Informaes encontradas:
[1] tipos_armas.txt (relevncia: 0.78)
Pistola tem carregador removvel, revlver tem tambor..."
```

---

## Comparação E3 vs E4

| Aspecto | E3 | E4 |
|---------|----|----|
| **Tools** | 8 | 9 (8 + RAG) |
| **Dados** | CSV | CSV + Documentos |
| **Perguntas** | Estruturadas | Estruturadas + Conceituais |
| **Exemplo E3** | "Quantas armas Taurus?" | ✅ Funciona |
| **Exemplo E4** | "O que é calibre?" | ❌ Não funciona | ✅ Funciona |

---

## Troubleshooting

### Erro: CSV não encontrado
```
FileNotFoundError: CSV não encontrado
```
**Solução:** Verificar caminho do CSV em `CSV_PATH`

### Erro: Documentos não encontrados
```
[AVISO] Pasta de documentos não encontrada
```
**Solução:** Verificar pasta `01_DADOS/documentos_conceituais/`

### Erro: Encoding
```
UnicodeDecodeError
```
**Solução:** Agente tenta múltiplos encodings automaticamente

### RAG não funciona
```
Sistema RAG não disponível
```
**Solução:** Verificar se documentos .txt existem na pasta

---

## Melhorias Futuras

### Curto Prazo
- [ ] Adicionar mais marcas ao roteador
- [ ] Melhorar extração de parâmetros
- [ ] Adicionar validação de entrada

### Médio Prazo
- [ ] Substituir TF-IDF por Sentence-BERT
- [ ] Adicionar FAISS para busca mais rápida
- [ ] Implementar cache de embeddings

### Longo Prazo
- [ ] Integrar com LLM (GPT, Claude)
- [ ] Adicionar interface web
- [ ] Implementar feedback do usuário

---

## Autor

**MBA IA Generativa PCDF - IBMEC**  
**Data:** 26/07/2026  
**Versão:** 4.0

---

## Licença

Uso educacional - MBA IA Generativa PCDF
