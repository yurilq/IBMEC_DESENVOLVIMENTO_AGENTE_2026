# QUICK START PROFESSOR - E3

**Encontro 3 | Terça 28/07/2026 | 13h00-18h00 (5 horas)**  
**Objetivo:** Construir agente SINARM completo DO ZERO, passo a passo, JUNTO COM OS ALUNOS

---

## 1 HORA ANTES DA AULA

### Ambiente Técnico
```bash
[ ] Executar verificar_ambiente.py
[ ] Ollama serve rodando (ollama serve)
[ ] Modelo baixado: llama3.2:1b (leve, 1GB) ou llama3 (8GB)
    → ollama pull llama3.2:1b
[ ] Testar: ollama run llama3.2:1b "Olá"
```

### Materiais Preparados
```bash
[ ] Abrir arquivos principais:
    ✅ ROTEIRO_COMPLETO_E3.md (timeline minuto a minuto)
    ✅ 01_GUIAS_ALUNO/PARTE_3_DECORATOR.md (slides decorator - 45 min)
    ✅ 02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py (código final completo)
    ✅ 04_MATERIAL_APOIO/FAQ_E3.md (troubleshooting rápido)

[ ] Testar código final:
    cd meu_agente_sinarm/
    python TEMPLATE_HORA_5.py
```

### Setup Projetor
```bash
[ ] Terminal com fonte grande (20pt+)
[ ] Editor de código com syntax highlight
[ ] Navegador com documentação aberta:
    - LangChain 1.3+: https://python.langchain.com/docs/
    - Pandas: https://pandas.pydata.org/docs/
```

---

## CRONOGRAMA DA AULA

### **13:00-13:45 | PARTE 1: Setup + Hello World** (45 min)
**Arquivo:** `01_GUIAS_ALUNO/PARTE_1_SETUP.md`

```bash
[ ] Alunos executam verificar_ambiente.py
[ ] Resolver problemas de ambiente (10 min máximo)
[ ] Criar pasta meu_agente_sinarm/
[ ] Ambiente virtual: python -m venv venv
[ ] Instalar: pip install pandas langchain-core langchain-ollama
[ ] Criar teste_llm.py (Hello World)
[ ] Executar e ver LLM responder pela primeira vez
```

**CHECKPOINT 1:** LLM respondeu "Olá"?
- ✅ SIM → Prosseguir Parte 2
- ❌ NÃO → Usar llama3.2:1b (modelo leve)

**⏰ 13:45 - PAUSA 15 MIN**

---

### **14:00-15:00 | PARTE 2: Primeira Tool SEM Decorator** (60 min)
**Arquivo:** `01_GUIAS_ALUNO/PARTE_2_PRIMEIRA_TOOL.md`

```bash
[ ] Copiar CSV para DADOS_SINARM/OCORRENCIAS_2026.csv
[ ] Criar função contar_armas_marca() (versão COM BUG proposital)
[ ] INVESTIGAÇÃO (15 min): Por que retorna 0?
    → Analisar dados com analisar_dados.py
    → Descobrir espaços extras (70 chars)
    → Refatorar com .str.strip() e .str.contains()
[ ] Criar agente_v0_1.py (agente manual)
[ ] Executar e ver ReAct em ação
```

**CHECKPOINT 2A:** Agente chama tool?  
**CHECKPOINT 2B:** Entendeu ReAct (Thought → Action → Observation)?

**IMPORTANTE:** Explicar AgentType.ZERO_SHOT_REACT_DESCRIPTION
- ZERO_SHOT = sem exemplos
- REACT = Reason (pensar) + Act (agir)
- DESCRIPTION = usa descrição das tools

**⏰ 15:00 - PAUSA 15 MIN**

---

### **15:15-16:00 | PARTE 3: @DECORATOR** (45 min) ⚠️ **NÃO PULAR!**
**Arquivo:** `01_GUIAS_ALUNO/PARTE_3_DECORATOR.md`

**⚠️ CRÍTICO:** Esta é a parte MAIS IMPORTANTE da aula!  
Alunos tiveram dificuldade com decorators em E1 e E2.

```bash
[ ] SLIDE 1: Função normal (exemplo_funcao.py)
[ ] SLIDE 2: Problema - código repetido (log em toda função)
[ ] SLIDE 3: Solução - Decorator "embrulha" função
[ ] SLIDE 4: Analogia visual - Papel de presente
    
    função normal    →    @decorator    →    função decorada
    presente         →    embrulhar     →    presente embrulhado
    
[ ] SLIDE 5: Anatomia do decorator (3 partes)
    1. def decorator(func)
    2. def wrapper(*args, **kwargs)
    3. return wrapper
    
[ ] SLIDE 6: Ver @tool em ação (exemplo_tool_decorator.py)
[ ] SLIDE 7: Comparação lado a lado (manual vs decorator)
[ ] SLIDE 8: Benefícios (DRY, reutilizável, limpo)
```

**CHECKPOINT 3A:** Entendeu o conceito de decorator?  
**CHECKPOINT 3B:** Viu @tool em ação?

**DICA:** Usar 20 min explicando, 15 min codando junto, 10 min perguntas

**⏰ 16:00 - PAUSA 15 MIN**

---

### **16:15-17:15 | PARTE 4: 4 Tools + Cache** (60 min)
**Arquivo:** `01_GUIAS_ALUNO/PARTE_4_QUATRO_TOOLS.md`

**ESTRATÉGIA:** Criar arquivo NOVO `tools_basicas_v2.py` (não modificar anterior)

```bash
[ ] Adicionar @lru_cache em carregar_csv()
[ ] Criar 4 tools com @tool:
    1. contar_armas_marca
    2. contar_armas_calibre
    3. contar_armas_tipo
    4. contar_armas_combinado (2 parâmetros)
[ ] Criar agente_v0_2.py (agente manual com 4 tools)
[ ] Executar e observar cache em ação
[ ] Ver carregar_csv.cache_info()
```

**CHECKPOINT 4A:** 4 tools criadas?  
**CHECKPOINT 4B:** Cache funciona? (70% mais rápido!)

**PERFORMANCE:**
- Sem cache: 14s (4 × 3.5s)
- Com cache: 4.1s (3.5s + 3 × 0.2s)

**⏰ 17:15 - PAUSA 15 MIN**

---

### **17:30-18:00 | PARTE 5: Few-Shot + CoT** (30 min)
**Arquivo:** `01_GUIAS_ALUNO/PARTE_5_FEWSHOT_COT.md`

**IMPORTANTE:** Se estiver sem tempo, esta parte pode ser EXERCÍCIO DE CASA

```bash
[ ] Criar agente_v3_0.py com:
    - Few-Shot Learning (3-5 exemplos PCDF)
    - Chain-of-Thought (5 passos estruturados)
    - Detecção conceitual vs dados
[ ] Testar 3 perguntas:
    1. "Quantas armas Taurus?" (dados)
    2. "O que é BO de furto?" (conceito)
    3. "Há mais Taurus ou Glock?" (complexo)
[ ] Comparar v0_2 vs v3_0
```

**CHECKPOINT 5:** Agente v3.0 completo?

**EVOLUÇÃO:**
- v0_1: Básico (1 tool manual)
- v0_2: Otimizado (4 tools + cache)
- v3_0: Profissional (Few-Shot + CoT + Security)

---

## SE FICAR SEM TEMPO

### Prioridade 1 (NÃO PULAR):
✅ Parte 3 - @DECORATOR (45 min)  
É o conceito mais difícil e mais importante.

### Prioridade 2 (CORE):
✅ Parte 1 - Setup + Hello World (45 min)  
✅ Parte 2 - Primeira Tool (60 min)  
✅ Parte 4 - 4 Tools + Cache (60 min)

### Flexível (Pode ser casa):
⏭️ Parte 5 - Few-Shot + CoT (30 min)  
Alunos podem completar em casa seguindo o guia.

---

## TROUBLESHOOTING RÁPIDO

### Erro: "Out of memory" / "Connection error"
**Causa:** Modelo muito pesado (llama3 = 8GB RAM)  
**Solução:**
```bash
ollama pull llama3.2:1b  # Modelo leve (1GB)
```

No código Python:
```python
llm = OllamaLLM(model="llama3.2:1b", temperature=0)  # ← Trocar aqui
```

**Ver:** `04_MATERIAL_APOIO/GUIA_ESCOLHA_MODELO_LLM.md`

---

### Erro: "ImportError: initialize_agent"
**Causa:** LangChain 1.3+ removeu `initialize_agent` e `AgentType`  
**Solução:** Usar agente manual (já implementado nos templates)

**Ver:** `04_MATERIAL_APOIO/MUDANCAS_LANGCHAIN_1_3.md`

---

### Erro: "CSV não encontrado"
**Causa:** Executando código na pasta errada  
**Solução:**
```bash
cd meu_agente_sinarm/  # ← Pasta de TRABALHO
python agente_v0_1.py
```

**Ver:** `ESTRUTURA_PASTAS_E3.md`

---

### Erro: "Retorna 0 armas" (Parte 2)
**Causa:** BUG PEDAGÓGICO proposital!  
**Solução:** Guiar investigação com `analisar_dados.py`
- Descobrir espaços extras (70 chars)
- Aprender `.str.strip()` e `.str.contains()`

**Ver:** `01_GUIAS_ALUNO/PARTE_2_PRIMEIRA_TOOL.md` (seção Investigação)

---

### Aluno perdido?
**Ação:**
1. Identificar checkpoint atual
2. Usar templates prontos em `02_TEMPLATES_PRONTOS/`
3. Copiar código e continuar junto com turma

**Templates disponíveis:**
- TEMPLATE_HORA_1.py (Hello World)
- TEMPLATE_HORA_2.py (Tool manual)
- TEMPLATE_HORA_3.py (Decorators)
- TEMPLATE_HORA_4.py (4 tools + cache)
- TEMPLATE_HORA_5.py (⭐ CÓDIGO FINAL COMPLETO)

---

## RECURSOS IMPORTANTES

### Durante a Aula:
- **FAQ_E3.md** → Respostas rápidas (588 linhas!)
- **ROTEIRO_COMPLETO_E3.md** → Timeline detalhada
- **02_TEMPLATES_PRONTOS/** → Código de referência

### Para Aprofundar (Pós-aula):
- **CONCEITOS_DETALHADOS_E3.md** → Explicações técnicas (1903 linhas!)
- **CHECKPOINTS_E3.md** → Auto-avaliação completa
- **ERROS_COMUNS_PARTE4.md** → Guia visual de erros

---

## CHECKPOINTS DO DIA

Ao final da aula, alunos devem ter:

### Checkpoint 1: ✅ LLM respondeu
```python
# teste_llm.py funcionando
llm.invoke("Olá") → "Olá! Como posso ajudar?"
```

### Checkpoint 2A: ✅ Agente chama tool
```python
# agente_v0_1.py funcionando
agente("Quantas armas Taurus?") → "Encontrei 150 armas"
```

### Checkpoint 2B: ✅ Entendeu ReAct
```
[THOUGHT] Preciso usar a tool ContarArmas
[ACTION] ContarArmas("Taurus")
[OBSERVATION] Encontrei 150 armas
[ANSWER] Existem 150 armas Taurus
```

### Checkpoint 3: ✅ Entendeu @decorator
```python
@tool
def minha_funcao():
    pass  # Decorator "embrulha" função
```

### Checkpoint 4: ✅ Cache funciona
```python
carregar_csv.cache_info()
# hits=3, misses=1 (3× cache, 1× leitura)
```

### Checkpoint 5: ✅ Agente v3.0 completo
```python
# agente_v3_0.py com:
# - 4 tools (@tool)
# - Cache (@lru_cache)
# - Few-Shot (3-5 exemplos)
# - Chain-of-Thought (5 passos)
# - Segurança (validação)
```

---

## ESTRUTURA DE ARQUIVOS (Referência Rápida)

```
E3_HANDS_ON_CONSTRUCAO_ZERO/        ← Material de referência (NÃO MEXER)
│
├── 00_COMECE_AQUI_E3.md            ← Visão geral
├── ROTEIRO_COMPLETO_E3.md          ← Timeline detalhada
├── verificar_ambiente.py           ← Verificar antes da aula
│
├── 01_GUIAS_ALUNO/                 ← Seguir passo a passo
│   ├── PARTE_1_SETUP.md            (13:00-13:45)
│   ├── PARTE_2_PRIMEIRA_TOOL.md    (14:00-15:00)
│   ├── PARTE_3_DECORATOR.md        (15:15-16:00) ⚠️ CRÍTICO
│   ├── PARTE_4_QUATRO_TOOLS.md     (16:15-17:15)
│   └── PARTE_5_FEWSHOT_COT.md      (17:30-18:00)
│
├── 02_TEMPLATES_PRONTOS/           ← Código de referência
│   ├── TEMPLATE_HORA_1.py
│   ├── TEMPLATE_HORA_2.py
│   ├── TEMPLATE_HORA_3.py
│   ├── TEMPLATE_HORA_4.py
│   └── TEMPLATE_HORA_5.py          ⭐ CÓDIGO FINAL
│
└── 04_MATERIAL_APOIO/              ← Troubleshooting
    ├── FAQ_E3.md                   (588 linhas!)
    ├── CONCEITOS_DETALHADOS_E3.md  (1903 linhas!)
    ├── CHECKPOINTS_E3.md
    ├── GUIA_ESCOLHA_MODELO_LLM.md
    └── MUDANCAS_LANGCHAIN_1_3.md   ⚠️ Importante

meu_agente_sinarm/                  ← Pasta de TRABALHO (alunos)
├── venv/                           (ambiente virtual)
├── DADOS_SINARM/
│   └── OCORRENCIAS_2026.csv
├── teste_llm.py                    (Parte 1)
├── agente_v0_1.py                  (Parte 2)
├── tools_basicas_v2.py             (Parte 3+4)
├── agente_v0_2.py                  (Parte 4)
└── agente_v3_0.py                  (Parte 5)
```

---

## SLIDES DECORATOR (PARTE 3 - 45 MIN)

### Slide 1: Função Normal
```python
# exemplo_funcao.py
def calcular(x, y):
    return x + y
```

### Slide 2: Problema - Código Repetido
```python
# Toda função precisa de log...
def calcular(x, y):
    print("[LOG] Executando calcular")  # ← Repetição!
    return x + y

def multiplicar(x, y):
    print("[LOG] Executando multiplicar")  # ← Repetição!
    return x * y
```

### Slide 3: Solução - Decorator
```python
# Decorator "embrulha" função
@adicionar_log
def calcular(x, y):
    return x + y  # ← Sem log explícito!
```

### Slide 4: Analogia Visual
```
presente simples  →  embrulhar  →  presente embrulhado
                     (decorator)

função simples    →  @decorator  →  função decorada
```

### Slide 5: Anatomia do Decorator
```python
def adicionar_log(func):           # 1. Recebe função
    def wrapper(*args, **kwargs):  # 2. Cria wrapper
        print(f"[LOG] Executando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper                 # 3. Retorna wrapper
```

### Slide 6: @tool em Ação
```python
from langchain_core.tools import tool

@tool
def contar_armas(marca: str) -> str:
    """Conta armas de uma marca"""
    # ... código ...
    return resultado
```

### Slide 7: Comparação Manual vs Decorator
```python
# ANTES (manual - 10 linhas)
tool_contar = Tool(
    name="ContarArmas",
    func=contar_armas,
    description="..."
)

# DEPOIS (decorator - 3 linhas)
@tool
def contar_armas(marca: str):
    """Conta armas de uma marca"""
```

### Slide 8: Benefícios
✅ DRY (Don't Repeat Yourself)  
✅ Reutilizável  
✅ Código limpo  
✅ Padrão profissional  

---

## PÓS-AULA

### Alunos Completaram:
✅ Agente SINARM v3.0 funcionando  
✅ 4 tools + cache + Few-Shot + CoT  
✅ Entenderam @decorator (gap resolvido!)  
✅ Consolidaram E1 + E2  

### Próxima Aula (E4):
- LangChain vs CrewAI (frameworks)
- Memory (memória de conversação)
- Agentes multi-turnos

### Material Extra (Opcional):
- `DESAFIOS_E3.md` (se existir)
- Melhorar agente v3.0 com:
  - Mais tools (data, região, delegacia)
  - Logging estruturado
  - Testes automatizados
  - Interface CLI interativa

---

## CHECKLIST FINAL

Antes de sair:
```bash
[ ] Todos os alunos têm agente funcionando?
[ ] Checkpoints 1-5 cumpridos?
[ ] Dúvidas respondidas?
[ ] Material E4 preparado?
[ ] Feedback coletado?
```

---

## CONTATOS ÚTEIS

**Problemas técnicos:**
- LangChain Docs: https://python.langchain.com/docs/
- Ollama Docs: https://ollama.ai/docs
- Pandas Docs: https://pandas.pydata.org/docs/

**Suporte:**
- FAQ_E3.md (local)
- CONCEITOS_DETALHADOS_E3.md (local)

---

**Boa aula! 🚀**

**Lembre-se:** PARTE 3 (Decorators) é CRÍTICA - 45 min bem gastos!
