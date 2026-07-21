# 🚨 ATUALIZAÇÃO URGENTE - E3 (LangChain 1.3+)

**Data:** 21/07/2026  
**Para:** Todos os alunos do E3  
**Assunto:** Correção de código para compatibilidade LangChain 1.3+

---

## 📋 O QUE ACONTECEU?

Se você está recebendo este erro:

```python
ImportError: cannot import name 'Tool' from 'langchain.agents'
# OU
ImportError: cannot import name 'initialize_agent' from 'langchain.agents'
```

**Isso é normal!** O LangChain 1.3+ removeu algumas funções antigas. Seu código precisa de uma pequena atualização.

---

## 🔧 COMO CORRIGIR (3 opções)

### **OPÇÃO 1: Baixar arquivos atualizados** ⭐ RECOMENDADO

1. Acesse a pasta do material atualizado:
   ```
   E3_HANDS_ON_CONSTRUCAO_ZERO/02_TEMPLATES_PRONTOS/
   ```

2. Copie os arquivos atualizados para sua pasta de trabalho:
   - `TEMPLATE_HORA_2.py` → Substituir seu `agente_v0_1.py`
   - `TEMPLATE_HORA_4.py` → Substituir seu `agente_v0_2.py`
   - `TEMPLATE_HORA_5.py` → Substituir seu `agente_v3_0.py`

3. Se tiver o arquivo `experimento_react.py`, baixe a versão atualizada (veja OPÇÃO 2)

---

### **OPÇÃO 2: Corrigir manualmente seus arquivos**

#### Se você tem `experimento_react.py`:

**ANTES (código antigo - NÃO funciona):**
```python
from langchain.agents import Tool, initialize_agent, AgentType
from tools_basicas import contar_armas_marca

llm = OllamaLLM(model="llama3", temperature=0)

tool = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica"
)

agente = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

resposta = agente.invoke({"input": "Quantas armas Taurus?"})
```

**DEPOIS (código novo - funciona!):**
```python
from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

llm = OllamaLLM(model="llama3", temperature=0)

def agente_react(pergunta: str):
    """Agente manual que simula ReAct"""
    
    print("\n[THOUGHT] Analisando a pergunta...")
    
    # Detectar marca
    pergunta_lower = pergunta.lower()
    marcas = ["taurus", "glock", "rossi", "beretta"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca
            break
    
    if not marca_encontrada:
        return "Não consegui identificar a marca."
    
    print(f"\n[ACTION] contar_armas_marca('{marca_encontrada}')")
    
    # Executar tool
    resultado = contar_armas_marca(marca_encontrada.capitalize())
    
    print(f"\n[OBSERVATION] {resultado}")
    print(f"\n[FINAL ANSWER] Retornando resposta")
    
    return resultado

# Usar
resposta = agente_react("Quantas armas Taurus existem?")
print(f"RESPOSTA: {resposta}")
```

---

### **OPÇÃO 3: Usar Git para atualizar** (se souber Git)

```bash
cd E:\documentos\ibmec\CODIGOS_AULA
git pull origin main

# Depois copie os arquivos atualizados para sua pasta de trabalho
```

---

## 📝 ARQUIVOS QUE PRECISAM SER ATUALIZADOS

### Na sua pasta `meu_agente_sinarm/`:

- [ ] `experimento_react.py` (se você criou)
- [ ] `agente_v0_1.py` (se usa `initialize_agent`)
- [ ] Qualquer arquivo que importe `Tool`, `initialize_agent` ou `AgentType`

### O que NÃO precisa mudar:

- ✅ `tools_basicas.py` (com `@tool` decorator) → Já está correto!
- ✅ `tools_basicas_v2.py` (com 4 tools + cache) → Já está correto!
- ✅ Qualquer arquivo que use apenas `@tool` decorator

---

## 🎯 COMO SABER SE MEU CÓDIGO ESTÁ ATUALIZADO?

Execute este comando na sua pasta de trabalho:

```bash
python verificar_ambiente.py
```

Se aparecer:
```
✅ langchain_core 1.3+ (ou superior)
✅ @tool decorator disponível
```

Seu ambiente está atualizado! Agora basta corrigir os arquivos Python.

---

## ❓ DÚVIDAS FREQUENTES

### 1. "Por que meu código parou de funcionar?"
O LangChain atualizou para versão 1.3+ e removeu `initialize_agent` e `AgentType`. Agora usamos **agente manual** (mais pedagógico!).

### 2. "Preciso reinstalar tudo?"
**NÃO!** Só precisa atualizar os arquivos Python. As bibliotecas já estão corretas.

### 3. "Vou perder meu código?"
**NÃO!** Faça backup da sua pasta antes:
```bash
# Criar backup
cp -r meu_agente_sinarm meu_agente_sinarm_backup
```

### 4. "O código novo é mais difícil?"
**NÃO!** Na verdade é mais fácil de entender! Você vê exatamente como o ReAct funciona.

### 5. "Meus arquivos com @tool estão funcionando?"
**SIM!** Se você usou `@tool` decorator (Parte 4 em diante), está tudo certo. Só precisa corrigir se usou `initialize_agent`.

---

## 🆘 SUPORTE

### Se continuar com problemas:

1. **Verifique sua versão do LangChain:**
   ```bash
   pip list | findstr langchain
   ```
   
   Deve mostrar:
   ```
   langchain            1.3.14 (ou superior)
   langchain-core       1.5.0 (ou superior)
   langchain-ollama     1.1.0 (ou superior)
   ```

2. **Se as versões estiverem antigas, atualize:**
   ```bash
   pip install --upgrade langchain-core langchain-ollama
   ```

3. **Consulte o material de apoio:**
   - `04_MATERIAL_APOIO/MUDANCAS_LANGCHAIN_1_3.md`
   - `04_MATERIAL_APOIO/FAQ_E3.md`
   - `QUICK_START_PROFESSOR.md`

4. **Pergunte no grupo ou ao professor**

---

## 📦 DOWNLOAD RÁPIDO (Arquivo Corrigido)

### experimento_react.py (versão atualizada)

Crie um arquivo `experimento_react.py` na sua pasta `meu_agente_sinarm/` com este conteúdo:

```python
"""
Experimento para VISUALIZAR o ciclo ReAct
ATUALIZADO PARA LANGCHAIN 1.3+
"""

from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

print("="*70)
print("EXPERIMENTO: VISUALIZANDO REACT (LangChain 1.3+)")
print("="*70)

def agente_react(pergunta: str):
    """Agente manual que MOSTRA o ciclo ReAct passo a passo"""
    
    print("\n[THOUGHT] Analisando a pergunta...")
    print('   "Preciso descobrir quantas armas de uma marca existem"')
    
    # Detectar marca
    pergunta_lower = pergunta.lower()
    marcas = ["taurus", "glock", "rossi", "beretta"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca
            break
    
    if not marca_encontrada:
        print("\n[THOUGHT] Nao identifiquei uma marca")
        return "Nao consegui identificar a marca da arma."
    
    print(f"\n[ACTION] Vou usar: contar_armas_marca")
    print(f"[ACTION INPUT] marca='{marca_encontrada.capitalize()}'")
    
    # Executar tool
    resultado = contar_armas_marca(marca_encontrada.capitalize())
    
    print(f"\n[OBSERVATION] A tool retornou: '{resultado}'")
    print(f"\n[THOUGHT] Agora tenho a informacao!")
    print(f"\n[FINAL ANSWER] Pronto para responder!")
    
    return resultado

# Testar
print("\nPERGUNTA: Quantas armas Taurus existem?")
print("-"*70)

resposta = agente_react("Quantas armas Taurus existem?")

print("-"*70)
print(f"\nRESPOSTA FINAL: {resposta}")

print("\n" + "="*70)
print("CICLO ReAct COMPLETO:")
print("="*70)
print("""
[THOUGHT] -> [ACTION] -> [OBSERVATION] -> [THOUGHT] -> [ANSWER]

Reason (pensar) -> Act (agir) -> Reason (pensar) -> Answer (responder)
""")
```

**Salve e execute:**
```bash
python experimento_react.py
```

---

## ✅ CHECKLIST DE ATUALIZAÇÃO

Marque conforme for completando:

- [ ] Li este documento completo
- [ ] Verifiquei minha versão do LangChain (`pip list | findstr langchain`)
- [ ] Fiz backup da minha pasta (`cp -r meu_agente_sinarm meu_agente_sinarm_backup`)
- [ ] Atualizei ou substituí os arquivos com problemas
- [ ] Testei o código atualizado (`python experimento_react.py`)
- [ ] Tudo está funcionando! ✅

---

## 📚 PARA SABER MAIS

- **Por que mudou?** Leia: `04_MATERIAL_APOIO/MUDANCAS_LANGCHAIN_1_3.md`
- **Entender o código novo:** Leia: `01_GUIAS_ALUNO/PARTE_2_PRIMEIRA_TOOL.md`
- **Ver todos os templates atualizados:** `02_TEMPLATES_PRONTOS/`

---

**Qualquer dúvida, pergunte! Estamos aqui para ajudar. 🚀**

**Atualizado em:** 21/07/2026  
**Versão do material:** E3 v2.0 (LangChain 1.3+)
