# 🎓 Desenvolvimento de Agentes - Códigos Prontos

## 📋 Visão Geral

Este repositório contém **todo o código prático** da disciplina **Desenvolvimento de Agentes** do MBA em IA.

**Estrutura**: Organizado por **encontros** (E1, E2, E3...), cada um com **conceitos modulares** + **solução final integrada**.

---

## 📂 Estrutura Organizada

```
03_CODIGOS_PRONTOS/
│
├── README.md                       # Este arquivo (navegação principal)
├── requirements.txt                # Dependências Python (todas)
├── .gitignore
├── setup.bat                       # Setup Windows
├── setup.sh                        # Setup Linux/Mac
├── verify_setup.py                 # Verificar instalação
│
├── utils/                          # 🛠️ Utilitários compartilhados (E1-E7)
│   ├── __init__.py
│   └── tools_sinarm.py             # Tools SINARM (4 datasets)
│
├── DADOS_SINARM/                   # 📊 Dados reais (135k+ registros)
│   ├── OCORRENCIAS/                # 74.758 registros
│   ├── PORTES/                     # 2.328 registros
│   ├── REGISTROS/                  # 12.798 registros
│   └── REQUERIMENTOS/              # 46.116 registros
│
├── logs/                           # 📝 Logs centralizados
│
├── E1_ANATOMIA_DO_AGENTE/          # 🎯 Encontro 1 (BASELINE)
│   ├── README_E1.md                # Guia completo E1
│   ├── conceitos/                  # Conceitos modulares
│   │   ├── 01_react_basico/
│   │   ├── 02_tools/
│   │   │   └── E1_tools_sinarm.py  # 4 tools SINARM
│   │   └── 03_error_handling/
│   ├── solucao_final/              # Versões integradas
│   │   ├── E1_agente_react_v3.py
│   │   └── agente_v1.8.py          # ⭐ Baseline E1 (60-70% accuracy)
│   └── testes/
│       └── TESTES_COMPLETOS.py
│
├── E2_QUALIDADE_E_MEMORIA/         # 🎯 Encontro 2 (QUALIDADE)
│   ├── README_E2.md                # Guia completo E2
│   ├── INDEX.md                    # Navegação rápida
│   ├── conceitos/                  # 10 atividades práticas
│   │   ├── 01_fewshot/             # Few-Shot Learning (4 atividades)
│   │   │   ├── ATIVIDADE_1A_baseline.py
│   │   │   ├── ATIVIDADE_1B_criar_exemplos.py
│   │   │   ├── ATIVIDADE_1C_implementar.py
│   │   │   ├── ATIVIDADE_1D_comparar.py
│   │   │   └── EXPLICACAO.md       # Teoria completa
│   │   ├── 02_cot/                 # Chain-of-Thought (4 atividades)
│   │   │   ├── ATIVIDADE_2A_classificar.py
│   │   │   ├── ATIVIDADE_2B_trace_manual.py
│   │   │   ├── ATIVIDADE_2C_implementar.py
│   │   │   ├── ATIVIDADE_2D_parser.py
│   │   │   └── template_cot.txt
│   │   ├── 03_memory_conversacional/  # Memory (1 atividade)
│   │   │   └── ATIVIDADE_3A_buffer.py
│   │   └── 04_security_basica/     # Security (2 atividades)
│   │       ├── ATIVIDADE_4A_validation.py
│   │       └── ATIVIDADE_4B_testar_ataque.py
│   ├── solucao_final/
│   │   ├── agente_v2.0_fewshot.py  # ⭐ Few-Shot (75-85% accuracy)
│   │   ├── agente_v2.5_cot.py      # ⭐ CoT (80-90% accuracy)
│   │   ├── COMPARACAO_V1_V2.py
│   │   └── README_SOLUCAO.md
│   └── demo_professor/
│       ├── DEMO_AULA.py
│       └── ROTEIRO_PROFESSOR.md
│
├── E3_LANGCHAIN_CREWAI/            # 🎯 Encontro 3 (futuro)
├── E4_RAG_FAISS/                   # 🎯 Encontro 4 (futuro)
├── E5_ESPECIALIZACAO/              # 🎯 Encontro 5 (futuro)
├── E6_DEPLOY_GUARDRAILS/           # 🎯 Encontro 6 (futuro)
├── E7_METRICAS_FINAL/              # 🎯 Encontro 7 (futuro)
│
└── agente_producao.py              # ⭐ VERSÃO FINAL (ao final disciplina)
```

---

## 🎯 Progressão da Disciplina

### Evolução do Agente:

```
E1: v1.8 (Baseline)
  ├─ ReAct básico
  ├─ 4 tools SINARM
  ├─ Error handling
  ├─ Accuracy: 60-70%
  └─ Latência: ~2.3s

E2: v2.0 (Few-Shot)
  ├─ v1.8 + Few-Shot Learning (3 exemplos)
  ├─ Accuracy: 75-85% (+15pp)
  └─ Latência: +10%

E2: v2.5 (Few-Shot + CoT)
  ├─ v2.0 + Chain-of-Thought
  ├─ Accuracy: 80-90% (+5-10pp queries complexas)
  ├─ Raciocínio explícito (debugging fácil)
  └─ Latência: +30%

E2: v2.5+ (Completo)
  ├─ v2.5 + Memory conversacional
  ├─ v2.5 + Security (input validation)
  └─ Conversação multi-turno + Proteção ataques

E3: v3.0 (LangChain)
  └─ Refactoring com framework
      (reduz 50% código, +10% performance)

E4: v3.5 (RAG + FAISS)
  └─ Vector DB + Retrieval
      (busca semântica, histórico longo)

E5-E7: v4.0+ (Produção)
  └─ Especialização + Deploy + Métricas
      (production-ready, escalável)
```

---

## 🚀 Quick Start

### 1. Instalação Inicial

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Verificar Instalação
```bash
python verify_setup.py
```

### 3. Configurar AWS (para Bedrock)
```bash
aws configure
# Ou exportar:
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"
```

### 4. Executar Agente

**E1 (Baseline):**
```bash
cd E1_ANATOMIA_DO_AGENTE/solucao_final
python agente_v1.8.py
```

**E2 (Few-Shot):**
```bash
cd E2_QUALIDADE_E_MEMORIA/solucao_final
python agente_v2.0_fewshot.py
```

**E2 (CoT):**
```bash
cd E2_QUALIDADE_E_MEMORIA/solucao_final
python agente_v2.5_cot.py
```

---

## 📚 Guias por Encontro

### 📘 E1: Anatomia do Agente
**Objetivo**: Construir agente ReAct do zero  
**Duração**: 5 horas  
**Guia completo**: [E1_ANATOMIA_DO_AGENTE/README_E1.md](E1_ANATOMIA_DO_AGENTE/README_E1.md)

**Conceitos:**
- ReAct Pattern (Thought → Action → Observation)
- Tools SINARM (4 datasets, 135k+ registros)
- Error handling (retry, fallback, validation)
- LLM Integration (Bedrock + Claude)

**Output**: Agente v1.8 (baseline 60-70% accuracy)

---

### 📗 E2: Qualidade e Memória
**Objetivo**: Melhorar accuracy e adicionar contexto  
**Duração**: 5 horas  
**Guia completo**: [E2_QUALIDADE_E_MEMORIA/README_E2.md](E2_QUALIDADE_E_MEMORIA/README_E2.md)  
**Navegação rápida**: [E2_QUALIDADE_E_MEMORIA/INDEX.md](E2_QUALIDADE_E_MEMORIA/INDEX.md)

**Conceitos:**
- Few-Shot Learning (4 atividades, +15-30% accuracy)
- Chain-of-Thought (4 atividades, raciocínio explícito)
- Memory Conversacional (1 atividade, buffer 5 mensagens)
- Security Basics (2 atividades, input validation)

**Output**: Agente v2.5 (80-90% accuracy, conversacional, protegido)

---

### 📙 E3-E7: Em Desenvolvimento
Materiais serão adicionados progressivamente ao longo da disciplina.

---

## 🛠️ Utilitários Compartilhados

### utils/tools_sinarm.py
**Tools disponíveis em TODOS os encontros:**

```python
from utils.tools_sinarm import (
    buscar_ocorrencias,   # Furtos, apreensões (74k registros)
    buscar_portes,        # Portes válidos (2k registros)
    buscar_registros,     # Registros armas (12k registros)
    buscar_requerimentos  # Requerimentos (46k registros)
)
```

**Características:**
- ✅ Cache LRU (performance)
- ✅ Validação SQL injection
- ✅ Conformidade LGPD (remove "idade")
- ✅ Logging auditável
- ✅ Mapeamento inteligente de colunas

**Formato de query:**
```python
# Padrão: "campo:valor"
buscar_ocorrencias("marca:Taurus")
buscar_portes("status:Válido")
buscar_registros("calibre:9mm")
buscar_requerimentos("decisao:Aprovado")
```

---

## 📊 Datasets SINARM

### Visão Geral:

| Dataset | Registros | Descrição | Pasta |
|---------|-----------|-----------|-------|
| **OCORRENCIAS** | 74.758 | Furtos, apreensões, recuperações | `DADOS_SINARM/OCORRENCIAS/` |
| **PORTES** | 2.328 | Portes válidos/vencidos | `DADOS_SINARM/PORTES/` |
| **REGISTROS** | 12.798 | Registros de armas (defesa pessoal) | `DADOS_SINARM/REGISTROS/` |
| **REQUERIMENTOS** | 46.116 | Requerimentos aprovados/negados | `DADOS_SINARM/REQUERIMENTOS/` |
| **TOTAL** | **135.900** | - | - |

### Colunas Principais:

**OCORRENCIAS:**
- marca_arma, especie_arma, calibre_arma
- tipo_ocorrencia (Furto, Apreensão, Recuperação)
- uf, municipio, ano_ocorrencia, mes_ocorrencia

**PORTES:**
- status_porte (Válido, Vencido)
- marca_arma, especie_arma, calibre_arma
- uf, municipio, ano_emissao

**REGISTROS:**
- status_registro (Ativo, Cancelado)
- marca_arma, especie_arma, calibre_arma
- categoria (CAC, Defesa)
- uf, municipio

**REQUERIMENTOS:**
- tipo_requerimento (Porte, Registro)
- decisao (Aprovado, Negado, Aguardando)
- categoria (CAC, Defesa)
- uf, municipio

---

## 🧪 Testes

### Executar Testes E1:
```bash
cd E1_ANATOMIA_DO_AGENTE/testes
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
```

### Executar Atividades E2:
```bash
cd E2_QUALIDADE_E_MEMORIA/conceitos/01_fewshot
python ATIVIDADE_1A_baseline.py
python ATIVIDADE_1B_criar_exemplos.py
# ... continuar sequência
```

---

## 📖 Documentação

### Guias Principais:
- [README.md](README.md) - Este arquivo (navegação geral)
- [QUICK_START.md](QUICK_START.md) - Início rápido
- [INSTRUCOES_ALUNOS.md](INSTRUCOES_ALUNOS.md) - Instruções detalhadas
- [GUIA_GITHUB.md](GUIA_GITHUB.md) - Como usar Git/GitHub

### Por Encontro:
- [E1: README_E1.md](E1_ANATOMIA_DO_AGENTE/README_E1.md) - Guia completo E1
- [E2: README_E2.md](E2_QUALIDADE_E_MEMORIA/README_E2.md) - Guia completo E2
- [E2: INDEX.md](E2_QUALIDADE_E_MEMORIA/INDEX.md) - Navegação rápida E2

### Conceitos Específicos:
- [Few-Shot: EXPLICACAO.md](E2_QUALIDADE_E_MEMORIA/conceitos/01_fewshot/EXPLICACAO.md)
- [CoT: template_cot.txt](E2_QUALIDADE_E_MEMORIA/conceitos/02_cot/template_cot.txt)

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'langchain_aws'"
```bash
pip install langchain-aws boto3
```

### "NoCredentialsError: Unable to locate credentials"
```bash
aws configure
```

### "FileNotFoundError: OCORRENCIAS_2026.csv not found"
```bash
# Verificar que DADOS_SINARM/ está no local correto
# Ajustar caminho em utils/tools_sinarm.py se necessário
```

### "ImportError: cannot import name 'buscar_ocorrencias'"
```bash
# Adicionar ao path:
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
from utils.tools_sinarm import buscar_ocorrencias
```

### "Agente muito lento"
```bash
# 1. Verificar cache ativo
# 2. Reduzir max_tokens (padrão: 4096 → 2048)
# 3. Usar temperature=0.0 (determinístico)
```

---

## 🤝 Contribuindo

### Reportar Bugs:
- Abra issue no repositório
- Descreva: ambiente, erro, passos para reproduzir

### Sugerir Melhorias:
- Fork → Branch → Commit → Pull Request
- Seguir padrões de código existentes

---

## 📞 Suporte

### Canais:
- **Fórum da disciplina** (principal)
- **Issues GitHub** (bugs/melhorias)
- **Email professor** (dúvidas urgentes)
- **Monitoria** (horários fixos)

### FAQ:
Consulte os README específicos:
- [E1 FAQ](E1_ANATOMIA_DO_AGENTE/README_E1.md#-troubleshooting)
- [E2 FAQ](E2_QUALIDADE_E_MEMORIA/README_E2.md#-faq)

---

## 📜 Licença

Uso educacional - MBA em Inteligência Artificial.  
Material desenvolvido para disciplina "Desenvolvimento de Agentes".

---

## ✅ Checklist Geral

### Setup Inicial:
- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] AWS credentials configuradas
- [ ] Setup verificado (`python verify_setup.py`)

### E1 Completo:
- [ ] Executei agente v1.8
- [ ] Testei 4 tools SINARM
- [ ] Entendi ciclo ReAct
- [ ] Medi baseline (60-70% accuracy)

### E2 Completo:
- [ ] Completei 10 atividades (1A-4B)
- [ ] Implementei Few-Shot (+15-30% accuracy)
- [ ] Implementei CoT (raciocínio explícito)
- [ ] Adicionei Memory (conversação)
- [ ] Protegi com Security (validation)

---

**Última atualização**: 2026-07-15  
**Versão**: 2.0 (estrutura modular organizada)  

🚀 **Boa jornada no desenvolvimento de agentes!**
