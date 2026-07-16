# 📘 E1: ANATOMIA DO AGENTE - GUIA COMPLETO

## 🎯 Visão Geral

**Encontro 1** é a base da disciplina: construir um agente ReAct do zero, entendendo cada componente.

### Tópicos Principais:
1. **ReAct Pattern** (Reason + Act)
2. **Tools SINARM** (4 datasets reais)
3. **Error Handling** (Retry, fallback, validation)
4. **LLM Integration** (AWS Bedrock + Claude)

### Objetivos de Aprendizagem:
- ✅ Entender arquitetura ReAct (Thought → Action → Observation → loop)
- ✅ Criar tools robustas para datasets reais (74k+ registros)
- ✅ Implementar error handling e validação
- ✅ Integrar LLM (Bedrock) com ferramentas externas
- ✅ Testar agente com queries complexas

---

## 📂 Estrutura do E1

```
E1_ANATOMIA_DO_AGENTE/
│
├── README_E1.md                    # Este arquivo
│
├── conceitos/                      # 📚 Conceitos modulares
│   │
│   ├── 01_react_basico/            # ReAct Pattern
│   │   └── (materiais teóricos - a criar)
│   │
│   ├── 02_tools/                   # Tools SINARM
│   │   └── E1_tools_sinarm.py      # 4 tools + validação + cache
│   │
│   └── 03_error_handling/          # Error Handling
│       └── (exemplos - a criar)
│
├── solucao_final/                  # 🎯 Versões do agente
│   ├── E1_agente_react_v3.py       # Versão completa ReAct
│   └── agente_v1.8.py              # Versão final E1 (baseline para E2)
│
└── testes/                         # 🧪 Testes
    └── TESTES_COMPLETOS.py         # Suite de testes completa
```

---

## 🎓 Conceitos Cobertos

### 1️⃣ ReAct Pattern (Reason + Act)

**O que é?**
Padrão arquitetural onde o agente alterna entre **raciocínio** (Thought) e **ação** (Action), observando resultados (Observation) até chegar na resposta.

**Ciclo ReAct:**
```
┌─────────────────────────────────────────────────────────────┐
│ 1. THOUGHT (Raciocínio)                                     │
│    "Preciso buscar ocorrências de Taurus no dataset..."     │
├─────────────────────────────────────────────────────────────┤
│ 2. ACTION (Ação)                                            │
│    buscar_ocorrencias("marca:Taurus")                       │
├─────────────────────────────────────────────────────────────┤
│ 3. OBSERVATION (Observação)                                 │
│    "Retornou 1.247 registros de Taurus"                     │
├─────────────────────────────────────────────────────────────┤
│ 4. DECISÃO                                                  │
│    ├─ Tenho resposta? → FINAL ANSWER                       │
│    └─ Preciso mais dados? → Volta para THOUGHT (loop)      │
└─────────────────────────────────────────────────────────────┘
```

**Vantagens:**
- ✅ Transparência (raciocínio explícito)
- ✅ Debugging fácil (ver onde falhou)
- ✅ Flexibilidade (pode usar N tools)

**Implementação:**
Ver `solucao_final/E1_agente_react_v3.py`

---

### 2️⃣ Tools SINARM (4 Datasets)

**Datasets Reais:**

| Dataset | Registros | Descrição | Arquivo |
|---------|-----------|-----------|---------|
| **OCORRENCIAS** | 74.758 | Furtos, apreensões, recuperações | OCORRENCIAS_2026.csv |
| **PORTES** | 2.328 | Portes válidos/vencidos | PORTES_2026.csv |
| **REGISTROS** | 12.798 | Registros de armas (defesa pessoal) | REGISTROS_com_categoria_2026.csv |
| **REQUERIMENTOS** | 46.116 | Requerimentos de porte/registro | REQUERIMENTOS_com_categoria_2026.csv |

**Tools Implementadas:**
```python
@tool
def buscar_ocorrencias(query: str) -> str:
    """Busca furtos, apreensões, recuperações."""
    # Formato: "campo:valor" (ex: "marca:Taurus")
    
@tool
def buscar_portes(query: str) -> str:
    """Busca portes válidos/vencidos."""
    
@tool
def buscar_registros(query: str) -> str:
    """Busca registros de armas."""
    
@tool
def buscar_requerimentos(query: str) -> str:
    """Busca requerimentos aprovados/negados."""
```

**Características:**
- ✅ Cache LRU (performance)
- ✅ Validação SQL injection
- ✅ Conformidade LGPD (remove campo "idade")
- ✅ Logging para auditoria
- ✅ Mapeamento inteligente de colunas

**Implementação:**
Ver `conceitos/02_tools/E1_tools_sinarm.py` (444 linhas)

---

### 3️⃣ Error Handling

**Camadas de Proteção:**

1. **Input Validation**
   - Formato "campo:valor" obrigatório
   - Tamanho máximo (1000 caracteres)
   - SQL injection detection

2. **Tool Errors**
   - Dataset não encontrado
   - Coluna não existe
   - Arquivo corrompido

3. **LLM Errors**
   - Parsing errors (resposta malformada)
   - Rate limiting (429)
   - Timeout

4. **Graceful Degradation**
   - Se tool falha → mensagem clara ao usuário
   - Se LLM falha → retry automático (max 3x)
   - Se tudo falha → log + resposta genérica

**Implementação:**
Ver `solucao_final/agente_v1.8.py` (error handling integrado)

---

## 🚀 Como Usar

### Pré-requisitos:
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar AWS credentials
aws configure
# Ou exportar:
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"

# 3. Verificar setup
python verify_setup.py
```

### Executar Agente v1.8:
```bash
cd solucao_final
python agente_v1.8.py
```

**Query de exemplo:**
```
Query: Quantas pistolas Taurus calibre 9mm foram furtadas no DF em 2026?

Resposta esperada:
"Foram encontradas 127 pistolas Taurus calibre 9mm furtadas no DF em 2026.
Fonte: SINARM/OCORRENCIAS."
```

### Executar Testes:
```bash
cd testes
python TESTES_COMPLETOS.py
```

**Output esperado:**
```
=== TESTE TOOLS SINARM ===
TEST 1: Busca Ocorrências ✅ 1.247 registros
TEST 2: Busca Portes ✅ 1.856 registros
TEST 3: Busca Registros ✅ 9.847 registros
TEST 4: Busca Requerimentos ✅ 28.456 registros
TEST 5: Proteção SQL Injection ✅ Rejeitado
=== FIM DOS TESTES ===
```

---

## 📊 Evolução das Versões

### v1.0 (ReAct Básico)
- ReAct pattern simples
- 1 tool (buscar_ocorrencias)
- Sem error handling

### v1.5 (Multi-Tool)
- 4 tools SINARM
- Validação básica
- Cache implementado

### v1.8 (Produção E1) ← **BASELINE PARA E2**
- 4 tools robustas
- Error handling completo
- Validação SQL injection
- Conformidade LGPD
- Logging auditável
- **Accuracy: 60-70%**
- **Latência: ~2.3s**

---

## 🔗 Relação com E2

O E1 estabelece a **baseline** (v1.8) que será melhorada no E2:

```
E1: v1.8 (Baseline)
  ├─ ReAct básico
  ├─ 4 tools
  ├─ Error handling
  └─ Accuracy: 60-70%

E2: v2.0 (Few-Shot)
  ├─ v1.8 + Few-Shot Learning
  └─ Accuracy: 75-85% (+15pp)

E2: v2.5 (CoT)
  ├─ v2.0 + Chain-of-Thought
  └─ Accuracy: 80-90% (+5-10pp)
```

**Materiais E2:** `../E2_QUALIDADE_E_MEMORIA/`

---

## 📚 Arquivos Principais

### 1. Tools SINARM
**Arquivo:** `conceitos/02_tools/E1_tools_sinarm.py`  
**Linhas:** 444  
**Funções:**
- `_load_dataset()` - Carrega CSV com cache
- `_validar_query()` - Valida formato e SQL injection
- `_mapear_coluna()` - Mapeia campos para colunas reais
- `_buscar_impl()` - Implementação genérica de busca
- `buscar_ocorrencias()`, `buscar_portes()`, `buscar_registros()`, `buscar_requerimentos()` - Tools decoradas

### 2. Agente v1.8 (Baseline)
**Arquivo:** `solucao_final/agente_v1.8.py`  
**Características:**
- ReAct completo
- 4 tools integradas
- Error handling robusto
- Prompt engineering otimizado
- Accuracy: 60-70%

### 3. Agente ReAct v3
**Arquivo:** `solucao_final/E1_agente_react_v3.py`  
**Características:**
- Versão anterior (referência histórica)
- Base para desenvolvimento v1.8

### 4. Testes Completos
**Arquivo:** `testes/TESTES_COMPLETOS.py`  
**Testa:**
- Todas as 4 tools
- SQL injection detection
- Error handling
- Performance (latência, cache)

---

## 🧪 Testes e Validação

### Suite de Testes:
```bash
python testes/TESTES_COMPLETOS.py
```

**Cobertura:**
- ✅ Tools funcionais (4/4)
- ✅ Validação de input
- ✅ SQL injection blocked
- ✅ Cache funcionando
- ✅ Error handling
- ✅ Conformidade LGPD

**Métricas Esperadas:**
- Accuracy: 60-70%
- Latência média: 2-3s
- Cache hit rate: >80% (após warmup)
- Taxa de erro: <5%

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'langchain_aws'"
```bash
pip install langchain-aws boto3
```

### "NoCredentialsError: Unable to locate credentials"
```bash
aws configure
# Ou exportar manualmente:
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### "FileNotFoundError: OCORRENCIAS_2026.csv not found"
```bash
# Verificar estrutura de pastas
# Dados devem estar em: ../DADOS_SINARM/
# Ajustar ARQUIVOS_DIR em E1_tools_sinarm.py se necessário
```

### "Tool retorna erro 'Campo não encontrado'"
```bash
# Listar colunas disponíveis:
from E1_tools_sinarm import listar_colunas
print(listar_colunas("ocorrencias"))
```

### "Agente muito lento"
```bash
# 1. Verificar se cache está ativo (deve estar)
# 2. Reduzir max_tokens no LLM (padrão: 4096)
# 3. Usar dataset menor para testes
```

---

## 📖 Materiais Complementares

### Documentação Raiz:
- [README.md](../README.md) - Guia geral do projeto
- [QUICK_START.md](../QUICK_START.md) - Início rápido
- [INSTRUCOES_ALUNOS.md](../INSTRUCOES_ALUNOS.md) - Instruções detalhadas

### Setup:
- [requirements.txt](../requirements.txt) - Dependências Python
- [setup.bat](../setup.bat) - Setup Windows
- [setup.sh](../setup.sh) - Setup Linux/Mac
- [verify_setup.py](../verify_setup.py) - Verificar instalação

### Git:
- [GUIA_GITHUB.md](../GUIA_GITHUB.md) - Como usar Git/GitHub
- [.gitignore](../.gitignore) - Arquivos ignorados

---

## ✅ Checklist de Conclusão E1

Ao final do E1, você deve:

- [ ] Entender ciclo ReAct (Thought → Action → Observation)
- [ ] Conhecer os 4 datasets SINARM (registros, portes, ocorrências, requerimentos)
- [ ] Executar agente v1.8 com sucesso
- [ ] Testar queries simples e complexas
- [ ] Verificar conformidade LGPD (campo "idade" removido)
- [ ] Executar suite de testes (TESTES_COMPLETOS.py)
- [ ] Entender error handling (validação, retry, fallback)
- [ ] Medir baseline: accuracy ~60-70%, latência ~2.3s
- [ ] Estar pronto para E2 (Few-Shot, CoT, Memory)

---

## 🎯 Próximos Passos

**Concluiu E1?** Parabéns! 🎉

**Próximo**: E2 - Qualidade e Memória
- Few-Shot Learning (+15-30% accuracy)
- Chain-of-Thought (raciocínio explícito)
- Memory conversacional (contexto multi-turno)
- Security basics (input validation)

**Preparação para E2:**
1. Anote queries onde v1.8 errou ou ficou confuso
2. Liste padrões de erro (dataset errado? filtros esquecidos?)
3. Pense: "Como exemplos (Few-Shot) poderiam ajudar?"

**Materiais E2:** `../E2_QUALIDADE_E_MEMORIA/README_E2.md`

---

## 📞 Suporte

### Dúvidas Comuns:
- **"Agente não responde"** → Verificar AWS credentials, Bedrock ativo
- **"Tool retorna vazio"** → Query mal formatada (use "campo:valor")
- **"Muitos erros"** → Verificar datasets em DADOS_SINARM/
- **"Accuracy baixa"** → Normal para v1.8 (baseline). Melhora no E2!

### Onde Pedir Ajuda:
- Fórum da disciplina
- Issues no repositório
- Email do professor
- Monitoria

---

**Boa jornada no E1! 🚀**

_Dúvidas? Abra issue no repositório ou pergunte no fórum da disciplina._
