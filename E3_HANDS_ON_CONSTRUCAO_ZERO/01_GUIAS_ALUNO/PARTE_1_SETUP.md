# 🚀 PARTE 1: SETUP + HELLO WORLD

**Horário:** 13:00-13:45 (45 minutos)  
**Objetivo:** Verificar ambiente e fazer LLM responder pela primeira vez  
**Nível:** Iniciante

---

## 🎯 O QUE VOCÊ VAI FAZER

1. Verificar que Python, Ollama e VSCode estão funcionando
2. Criar primeiro script que se comunica com LLM
3. Ver LLM responder "Olá, tudo bem?"

---

## ✅ PRÉ-REQUISITOS

Antes de começar, você precisa ter instalado:

- [ ] Python 3.9 ou superior
- [ ] Ollama instalado e rodando
- [ ] Modelo llama3 baixado no Ollama
- [ ] VSCode ou editor de código
- [ ] Biblioteca LangChain instalada

---

## 📋 PASSO A PASSO

### PASSO 1: Verificar Python (5 min)

Abra o terminal e digite:

```bash
python --version
```

**Resultado esperado:**
```
Python 3.9.x (ou superior)
```

Se der erro, Python não está instalado ou não está no PATH.

---

### PASSO 2: Verificar Ollama (5 min)

No terminal, digite:

```bash
ollama list
```

**Resultado esperado:**
```
NAME            ID              SIZE
llama3:latest   abc123def456    4.7 GB
```

Se der erro "command not found":
- Ollama não está instalado
- Consulte: [https://ollama.ai/download](https://ollama.ai/download)

Se lista estiver vazia (sem llama3):
```bash
ollama pull llama3
```

**Verificar se Ollama está rodando:**
```bash
ollama serve
```

Deixe rodando em uma aba do terminal.

---

### PASSO 3: Criar Pasta do Projeto (2 min)

Crie uma pasta para seus códigos:

```bash
mkdir meu_agente_sinarm
cd meu_agente_sinarm
```

---

### PASSO 4: Criar Ambiente Virtual (5 min)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Mac/Linux)
source venv/bin/activate
```

Você verá `(venv)` no início da linha do terminal.

---

### PASSO 5: Instalar Bibliotecas (5 min)

```bash
pip install langchain-ollama langchain pandas
```

Aguarde instalação terminar.

---

### PASSO 6: Criar Primeiro Script (10 min)

Abra VSCode e crie arquivo: `teste_llm.py`

Digite o código a seguir **LINHA POR LINHA** (acompanhe o professor):

```python
# teste_llm.py
# Primeiro contato com LLM

# LINHA 1: Importar LangChain
from langchain_ollama import OllamaLLM

# LINHA 2: Criar conexão com Ollama
llm = OllamaLLM(model="llama3")

# LINHA 3: Enviar pergunta
resposta = llm.invoke("Olá, tudo bem?")

# LINHA 4: Mostrar resposta
print(resposta)
```

**Salve o arquivo!**

---

### PASSO 7: Executar Script (5 min)

No terminal (dentro da pasta do projeto):

```bash
python teste_llm.py
```

**Aguarde...**

LLM está processando (pode demorar 5-10 segundos).

**Resultado esperado:**
```
Olá! Sim, tudo bem comigo, obrigado por perguntar! Como posso ajudá-lo hoje?
```

---

## ✅ CHECKPOINT 1

Marque se conseguiu:

- [ ] Python respondeu versão corretamente
- [ ] Ollama listou modelo llama3
- [ ] Script `teste_llm.py` executou sem erros
- [ ] LLM retornou uma resposta em português

**Se marcou TODOS:** Parabéns! Ambiente configurado! 🎉

**Se algum NÃO funcionou:** Peça ajuda ao professor ou colega.

---

## 🔍 ENTENDENDO O CÓDIGO

### Linha 1: Import

```python
from langchain_ollama import OllamaLLM
```

**O que faz:** Importa ferramenta para conectar com Ollama  
**Analogia:** Trazer chave de fenda da caixa de ferramentas

---

### Linha 2: Criar LLM

```python
llm = OllamaLLM(model="llama3")
```

**O que faz:** Cria objeto que se comunica com modelo llama3  
**Analogia:** Discar número de telefone (preparar conexão)

**Parâmetros:**
- `model="llama3"` → qual modelo usar

---

### Linha 3: Invocar

```python
resposta = llm.invoke("Olá, tudo bem?")
```

**O que faz:** Envia pergunta e recebe resposta  
**Analogia:** Falar ao telefone e ouvir resposta

**Parâmetros:**
- String → pergunta enviada ao LLM
- Retorna → string com resposta

---

### Linha 4: Print

```python
print(resposta)
```

**O que faz:** Mostra resposta na tela  
**Analogia:** Escrever resposta no papel

---

## 🎓 EXERCÍCIO RÁPIDO

Modifique `teste_llm.py` para fazer 3 perguntas diferentes:

```python
perguntas = [
    "Quantas armas existem no Brasil?",
    "O que é o sistema SINARM?",
    "Qual a diferença entre calibre .38 e 9mm?"
]

for pergunta in perguntas:
    print(f"\n❓ PERGUNTA: {pergunta}")
    resposta = llm.invoke(pergunta)
    print(f"💬 RESPOSTA: {resposta}\n")
    print("-" * 60)
```

**Execute e veja as respostas!**

---

## ⚠️ PROBLEMAS COMUNS

### Erro: "ModuleNotFoundError: No module named 'langchain_ollama'"

**Solução:**
```bash
pip install langchain-ollama
```

---

### Erro: "Connection refused" ou "Cannot connect to Ollama"

**Solução:**
```bash
# Em outro terminal, execute:
ollama serve
```

Deixe rodando e execute script novamente.

---

### LLM demora muito (>30 segundos)

**Causa:** CPU lento ou memória insuficiente

**Solução temporária:**
- Feche outros programas
- Use modelo menor: `model="llama3:8b"`

---

### Resposta em inglês

**Solução:** Pergunte em português ou adicione instrução:

```python
resposta = llm.invoke("Responda em português: Olá, tudo bem?")
```

---

## 📚 CONCEITOS APRENDIDOS

✅ **LLM**: Large Language Model (modelo de linguagem)  
✅ **Ollama**: Framework para rodar LLMs localmente  
✅ **OllamaLLM**: Classe LangChain para conectar com Ollama  
✅ **invoke()**: Método para enviar pergunta e receber resposta  
✅ **model**: Parâmetro que define qual LLM usar

---

## 🚀 PRÓXIMOS PASSOS

Agora que LLM está funcionando, vamos para **PARTE 2**:
- Criar função Python que lê dados
- Conectar função ao LLM (primeira tool!)
- Ver agente usar tool para responder perguntas

**Arquivo:** [PARTE_2_PRIMEIRA_TOOL.md](PARTE_2_PRIMEIRA_TOOL.md)

---

## 📞 AJUDA

**Durante aula:**
- Levante a mão
- Pergunte ao colega ao lado
- Chame o professor

**Material de apoio:**
- [FAQ_E3.md](../04_MATERIAL_APOIO/FAQ_E3.md)
- [TROUBLESHOOTING_E3.md](../04_MATERIAL_APOIO/TROUBLESHOOTING_E3.md)

**Se ficar muito travado:**
- Use [TEMPLATE_HORA_1.py](../02_TEMPLATES_PRONTOS/TEMPLATE_HORA_1.py)

---

**Parte:** 1/5  
**Tempo:** 45 minutos  
**Status:** ✅ PRONTO PARA USO

**Boa aula! Vamos construir juntos! 🚀**
