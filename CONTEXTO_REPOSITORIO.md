# 📘 DOCUMENTO DE CONTEXTO E ORIENTAÇÕES - REPOSITÓRIO 03_CODIGOS_PRONTOS

**Versão:** 1.0  
**Data:** 16/07/2026  
**Propósito:** Guia mestre para criação de conteúdo prático da disciplina

---

## 🎯 VISÃO GERAL DO REPOSITÓRIO

### Localização:
```
00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS
```

### Propósito:
Repositório Git versionado contendo **TODOS os scripts práticos** dos 7 encontros da disciplina, organizados por encontro, com setup automatizado e ambiente padronizado.

---

## 📁 ESTRUTURA OBRIGATÓRIA

```
03_CODIGOS_PRONTOS/                    ← Raiz do repositório Git
│
├── .git/                              ← Controle de versão
├── .gitignore                         ← Arquivos ignorados
├── README.md                          ← Navegação principal (já existe)
├── requirements.txt                   ← Dependências Python (já existe)
│
├── 🔧 SETUP (Criação de Ambiente):
│   ├── setup.py                       ← Setup unificado (Windows + Linux/Mac)
│   ├── setup.bat                      ← Setup Windows (já existe)
│   ├── setup.sh                       ← Setup Linux/Mac (já existe)
│   ├── verify_setup.py                ← Validação ambiente (já existe)
│   ├── GUIA_INSTALACAO.md             ← Passo a passo detalhado
│   └── TROUBLESHOOTING.md             ← Solução de problemas comuns
│
├── 📊 DADOS (Compartilhados):
│   └── DADOS_SINARM/                  ← 135k+ registros (já existe)
│       ├── OCORRENCIAS/
│       ├── PORTES/
│       ├── REGISTROS/
│       └── REQUERIMENTOS/
│
├── 🛠️ UTILITÁRIOS (Compartilhados):
│   └── utils/                         ← Tools compartilhadas (já existe)
│       ├── __init__.py
│       ├── tools_sinarm.py            ← 4 tools SINARM (E1-E7)
│       └── README_UTILS.md
│
├── 📝 LOGS (Compartilhados):
│   └── logs/                          ← Logs centralizados (já existe)
│
├── 🎓 E1_ANATOMIA_DO_AGENTE/          ← Encontro 1
│   ├── README_E1.md                   ← Guia completo E1
│   ├── conceitos/                     ← Atividades modulares
│   │   ├── 01_react_basico/
│   │   ├── 02_tools/
│   │   └── 03_error_handling/
│   ├── solucao_final/                 ← Agentes completos
│   │   ├── agente_v1.0_react.py
│   │   ├── agente_v1.5_tools.py
│   │   └── agente_v1.8_completo.py   ← Baseline E1
│   ├── demo_professor/                ← Demos ao vivo
│   │   └── DEMO_E1.py
│   └── testes/
│       └── test_e1.py
│
├── 🎓 E2_QUALIDADE_E_MEMORIA/         ← Encontro 2
│   ├── README_E2.md
│   ├── conceitos/
│   │   ├── 01_fewshot/                ← 4 atividades Few-Shot
│   │   ├── 02_cot/                    ← 4 atividades CoT
│   │   ├── 03_memory/                 ← 2 atividades Memory
│   │   └── 04_security/               ← 2 atividades Security
│   ├── solucao_final/
│   │   ├── agente_v2.0_fewshot.py    ← Few-Shot
│   │   ├── agente_v2.5_cot.py        ← CoT
│   │   └── agente_v2.8_completo.py   ← Few-Shot + CoT + Memory
│   ├── demo_professor/
│   │   └── DEMO_E2.py
│   └── testes/
│       └── test_e2.py
│
├── 🎓 E3_LANGCHAIN_CREWAI/            ← Encontro 3 (futuro)
├── 🎓 E4_RAG_FAISS/                   ← Encontro 4 (futuro)
├── 🎓 E5_ESPECIALIZACAO/              ← Encontro 5 (futuro)
├── 🎓 E6_DEPLOY_GUARDRAILS/           ← Encontro 6 (futuro)
└── 🎓 E7_METRICAS_FINAL/              ← Encontro 7 (futuro)
```

---

## 🐍 ESPECIFICAÇÕES TÉCNICAS

### Python:
- **Versão obrigatória:** Python 3.10.x
- **Alternativa:** Python 3.11.x (testado)
- **Não suportado:** Python 3.9 ou inferior, Python 3.12+ (incompatibilidades)

### Ambiente Virtual:
- **Ferramenta:** venv (built-in Python)
- **Nome padrão:** `venv/`
- **Localização:** `03_CODIGOS_PRONTOS/venv/`

### Dependências Principais:
```
# Core
langchain>=0.1.0
langchain-core>=0.1.0
langchain-community>=0.0.13
langchain-ollama>=0.1.0

# LLM Local
# Ollama (instalação separada): https://ollama.ai

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Utilities
python-dotenv>=1.0.0
```

---

## 📋 REGRAS DE CRIAÇÃO DE CONTEÚDO

### Para CADA Encontro (E1, E2, E3...):

#### 1. Estrutura Obrigatória:
```
EX_NOME_ENCONTRO/
├── README_EX.md                # Guia completo do encontro
├── conceitos/                  # Atividades modulares (hands-on)
│   ├── 01_conceito_1/
│   │   ├── ATIVIDADE_1A_*.py
│   │   ├── ATIVIDADE_1B_*.py
│   │   ├── EXPLICACAO.md       # Teoria do conceito
│   │   └── SOLUCAO.md          # Solução comentada
│   └── 02_conceito_2/
│       └── ...
├── solucao_final/              # Agentes completos (integrados)
│   ├── agente_vX.Y_*.py        # Versões evolutivas
│   └── README_SOLUCAO.md       # Como usar
├── demo_professor/             # Scripts para projeção em aula
│   ├── DEMO_EX.py              # Demo interativa
│   └── ROTEIRO_PROFESSOR.md    # Texto para falar
└── testes/                     # Testes automatizados
    └── test_ex.py
```

#### 2. Nomenclatura de Arquivos:

**Conceitos Modulares:**
```
ATIVIDADE_[NÚMERO][LETRA]_[DESCRICAO].py

Exemplos:
- ATIVIDADE_1A_baseline.py
- ATIVIDADE_1B_criar_exemplos.py
- ATIVIDADE_2A_cot_manual.py
```

**Agentes Finais:**
```
agente_v[MAJOR].[MINOR]_[FEATURE].py

Exemplos:
- agente_v1.0_react.py
- agente_v1.8_completo.py
- agente_v2.0_fewshot.py
- agente_v2.5_cot.py
```

**Demos:**
```
DEMO_E[NUMERO].py

Exemplos:
- DEMO_E1.py
- DEMO_E2.py
```

#### 3. Cabeçalho Obrigatório em Todos os Scripts:

```python
"""
ENCONTRO [N] - [TÍTULO DO ENCONTRO]
[Data do encontro]

VERSÃO: [v1.0, v2.0, etc]
OBJETIVO: [Breve descrição 1-2 linhas]

PROGRESSÃO:
v1.0 (E1): [Feature]
v1.8 (E1): [Feature]
v2.0 (E2): [Feature] ← VOCÊ ESTÁ AQUI

PRÉ-REQUISITOS:
- Python 3.10+
- Ambiente virtual ativado
- Dependências instaladas (requirements.txt)
- [Outros pré-requisitos específicos]

COMO USAR:
python [nome_do_arquivo].py

TEMPO ESTIMADO: [10 min, 45 min, etc]
"""

import sys
import os
import io
from pathlib import Path

# ========== CONFIGURAÇÃO INICIAL ==========

# Fix encoding Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup paths (relativo ao repositório)
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # 03_CODIGOS_PRONTOS
sys.path.insert(0, str(PROJECT_ROOT))

# ... resto do código
```

#### 4. Importações Compartilhadas:

**SEMPRE usar utilitários compartilhados:**
```python
from utils.tools_sinarm import (
    buscar_ocorrencias,
    buscar_registros,
    buscar_portes,
    buscar_requerimentos
)
```

**NUNCA duplicar código entre encontros.**

#### 5. Dados SINARM:

**SEMPRE usar dados reais:**
```python
DADOS_SINARM = PROJECT_ROOT / "DADOS_SINARM"
```

**NUNCA usar dados mock/simulados** (exceto em demonstrações pedagógicas explícitas).

#### 6. Logs:

**SEMPRE logar ações importantes:**
```python
import logging

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'agente_v2.0.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
```

---

## 🔧 SETUP DO AMBIENTE (Para Alunos)

### Documento Obrigatório: `GUIA_INSTALACAO.md`

**Estrutura:**

1. **Pré-requisitos**
   - Verificar versão Python
   - Instalar Ollama (se necessário)
   - Baixar modelo llama3

2. **Clonagem do Repositório**
   ```bash
   git clone [URL]
   cd 03_CODIGOS_PRONTOS
   ```

3. **Criação do Ambiente Virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instalação de Dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Validação do Setup**
   ```bash
   python verify_setup.py
   ```

6. **Teste Rápido**
   ```bash
   # Testar E1
   cd E1_ANATOMIA_DO_AGENTE/solucao_final
   python agente_v1.8_completo.py
   ```

---

## 📝 DOCUMENTAÇÃO OBRIGATÓRIA POR ENCONTRO

### 1. README_E[N].md

**Seções:**
- 🎯 Objetivos do Encontro
- 📊 Métricas de Sucesso
- 📂 Estrutura de Arquivos
- 🚀 Como Começar
- 📋 Atividades (ordem de execução)
- 🎓 Conceitos Aprendidos
- 📚 Recursos Adicionais
- ❓ FAQ

### 2. EXPLICACAO.md (por conceito)

**Seções:**
- 💡 O Que É?
- 🎯 Por Quê?
- 🔍 Como Funciona?
- 📊 Exemplo Prático
- ✅ Checklist de Implementação
- 🔗 Recursos

### 3. SOLUCAO.md (por atividade)

**Seções:**
- 📝 Código Completo Comentado
- 🔍 Explicação Linha por Linha
- ⚠️ Armadilhas Comuns
- 💡 Dicas de Otimização

---

## 🎯 PROGRESSÃO ENTRE ENCONTROS

### Versionamento dos Agentes:

```
E1: v1.0 → v1.5 → v1.8 (Baseline)
  Foco: ReAct + Tools + Error Handling
  Accuracy: 60-70%

E2: v2.0 → v2.5 → v2.8
  Foco: Few-Shot + CoT + Memory
  Accuracy: 75-90%

E3: v3.0 → v3.5
  Foco: LangChain + CrewAI
  Accuracy: 85-92%

E4: v4.0 → v4.5
  Foco: RAG + FAISS
  Accuracy: 90-95%

E5: v5.0 → v5.5
  Foco: Especialização + Fine-tuning
  Accuracy: 92-96%

E6: v6.0 → v6.5
  Foco: Deploy + Guardrails
  Production-ready

E7: v7.0 (FINAL)
  Foco: Métricas + Projeto Final
  Production + Monitoring
```

### Compatibilidade:

- **TODOS os agentes de E2+ DEVEM funcionar com tools de E1**
- **NUNCA quebrar retrocompatibilidade**
- **Sempre testar versão anterior antes de criar nova**

---

## 🧪 TESTES OBRIGATÓRIOS

### Para Cada Script:

**Antes de criar/commitar:**
1. ✅ Executa sem erro?
2. ✅ Imports funcionam?
3. ✅ Paths corretos?
4. ✅ Dados carregam?
5. ✅ Output legível?
6. ✅ Tempo execução < 60s?
7. ✅ Logs criados?
8. ✅ Documentação completa?

### Script de Validação:

**Criar `test_ex.py` por encontro:**
```python
import pytest
from pathlib import Path

def test_imports():
    """Testa se imports funcionam"""
    # ...

def test_data_loading():
    """Testa carregamento de dados"""
    # ...

def test_agent_execution():
    """Testa execução do agente"""
    # ...
```

---

## 🔒 CONTROLE DE QUALIDADE

### Checklist Antes de Criar Novo Encontro:

- [ ] README_EX.md criado e completo
- [ ] Estrutura de pastas seguindo padrão
- [ ] Todos os scripts têm cabeçalho correto
- [ ] Todos os scripts testados individualmente
- [ ] EXPLICACAO.md criado para cada conceito
- [ ] SOLUCAO.md criado para cada atividade
- [ ] Demo professor criada e testada
- [ ] Testes automatizados criados
- [ ] Dependências adicionadas ao requirements.txt (se aplicável)
- [ ] Git commit com mensagem descritiva
- [ ] README.md principal atualizado

---

## 📚 RECURSOS E REFERÊNCIAS

### Para Criadores de Conteúdo:

**Sempre consultar antes de criar:**
1. Este documento (CONTEXTO_REPOSITORIO.md)
2. README.md principal
3. Estrutura de encontros anteriores (E1, E2)
4. requirements.txt (dependências atuais)

**Sempre testar:**
1. Ambiente limpo (novo venv)
2. Python 3.10 e 3.11
3. Windows e Linux (se possível)

---

## 🚨 ERROS COMUNS A EVITAR

### ❌ NÃO FAZER:

1. **Paths absolutos hardcoded**
   ```python
   # ERRADO
   path = "E:\documentos\ibmec\..."
   
   # CERTO
   path = Path(__file__).resolve().parent
   ```

2. **Imports relativos sem PROJECT_ROOT**
   ```python
   # ERRADO
   from tools_sinarm import buscar_ocorrencias
   
   # CERTO
   from utils.tools_sinarm import buscar_ocorrencias
   ```

3. **Dados mock quando há dados reais**
   ```python
   # EVITAR (usar apenas se pedagógico)
   data = {"mock": 123}
   
   # PREFERIR
   df = pd.read_csv(DADOS_SINARM / "REGISTROS/...")
   ```

4. **Código duplicado entre encontros**
   - Sempre usar utils/ para compartilhar

5. **Scripts sem documentação**
   - Todo script precisa de docstring + README

6. **Dependências não documentadas**
   - Sempre atualizar requirements.txt

---

## 📞 SUPORTE E MANUTENÇÃO

### Quando Criar Novo Encontro:

1. **Criar branch:**
   ```bash
   git checkout -b feature/eX-nome-encontro
   ```

2. **Criar estrutura:**
   ```bash
   mkdir -p EX_NOME/conceitos/01_conceito
   mkdir -p EX_NOME/solucao_final
   mkdir -p EX_NOME/demo_professor
   mkdir -p EX_NOME/testes
   ```

3. **Criar README_EX.md**

4. **Desenvolver scripts** (seguindo este guia)

5. **Testar tudo**

6. **Commitar:**
   ```bash
   git add .
   git commit -m "feat: Add EX - [Nome do Encontro]"
   git push origin feature/eX-nome-encontro
   ```

7. **Merge para main** (após revisão)

---

## ✅ CHECKLIST FINAL

### Para Cada Novo Encontro:

**Arquitetura:**
- [ ] Estrutura de pastas seguindo padrão
- [ ] README_EX.md completo
- [ ] Scripts nomeados corretamente

**Conteúdo:**
- [ ] Conceitos modulares criados
- [ ] Atividades práticas testadas
- [ ] Agentes finais funcionando
- [ ] Demo professor criada

**Documentação:**
- [ ] EXPLICACAO.md por conceito
- [ ] SOLUCAO.md por atividade
- [ ] Comentários nos scripts
- [ ] ROTEIRO_PROFESSOR.md

**Testes:**
- [ ] test_ex.py criado
- [ ] Todos os scripts executam sem erro
- [ ] Imports funcionam
- [ ] Dados carregam corretamente

**Integração:**
- [ ] requirements.txt atualizado
- [ ] README.md principal atualizado
- [ ] Git commit feito
- [ ] Testado em ambiente limpo

---

## 🎯 OBJETIVO FINAL

Ao seguir este guia, **TODOS os encontros terão:**

✅ Estrutura consistente e navegável  
✅ Scripts testados e funcionais  
✅ Documentação completa e clara  
✅ Setup automatizado e simples  
✅ Ambiente reproduzível (Python 3.10 + venv + requirements.txt)  
✅ Dados reais e relevantes  
✅ Progressão pedagógica clara  

---

**Documento vivo:** Atualizar conforme surgem novos padrões ou necessidades.

**Última atualização:** 16/07/2026  
**Versão:** 1.0  
**Mantenedor:** Equipe de conteúdo MBA IA
