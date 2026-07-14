# QUICK START - Agente Investigador SINARM E1

## Para Alunos com Pressa

**3 passos simples para começar:**

---

## Windows

```bash
# 1. Clone o repositório
git clone https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git
cd IBMEC_DESENVOLVIMENTO_AGENTE_2026

# 2. Execute o setup automático
setup.bat

# 3. Execute o agente
venv\Scripts\activate
python E1_agente_react_v3.py
```

**Pronto! O agente está rodando.**

---

## Linux/Mac

```bash
# 1. Clone o repositório
git clone https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git
cd IBMEC_DESENVOLVIMENTO_AGENTE_2026

# 2. Execute o setup automático
chmod +x setup.sh
./setup.sh

# 3. Execute o agente
source venv/bin/activate
python E1_agente_react_v3.py
```

**Pronto! O agente está rodando.**

---

## Não Funcionou?

### 1. Verifique o Ollama

O agente precisa do Ollama para funcionar.

**Instalar Ollama:**

Windows:
- Baixe em: https://ollama.ai
- Instale o executável

Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Mac:
```bash
brew install ollama
```

**Baixar modelo:**
```bash
ollama pull llama3
```

### 2. Execute o Verificador

```bash
# Ative o ambiente virtual primeiro
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Depois execute
python verify_setup.py
```

Ele vai te dizer exatamente o que está faltando!

### 3. Ainda com problemas?

1. Abra uma issue no GitHub: https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026/issues
2. Consulte o README.md completo
3. Procure seu erro no Troubleshooting do README.md

---

## Comandos Úteis

### Ativar ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Desativar ambiente virtual

```bash
deactivate
```

### Executar agente

```bash
python E1_agente_react_v3.py
```

### Executar testes

```bash
python TESTES_COMPLETOS.py
```

### Verificar instalação

```bash
python verify_setup.py
```

---

## Exemplos de Perguntas para o Agente

Após executar `python E1_agente_react_v3.py`, teste com:

```
Quantos furtos de arma ocorreram no Rio de Janeiro em 2024?
```

```
Quais estados têm mais portes de arma vigentes?
```

```
Qual o calibre de arma mais registrado em São Paulo?
```

```
Houve aumento nos requerimentos entre 2023 e 2024?
```

---

## Estrutura do Projeto

```
📦 IBMEC_DESENVOLVIMENTO_AGENTE_2026/
├── 🚀 setup.bat              # Windows: Execute primeiro!
├── 🚀 setup.sh               # Linux/Mac: Execute primeiro!
├── ✅ verify_setup.py        # Verifica se tudo está OK
│
├── 🤖 E1_agente_react_v3.py  # AGENTE PRINCIPAL
├── 🛠️ E1_tools_sinarm.py     # Ferramentas do agente
├── 🧪 TESTES_COMPLETOS.py    # Testes
│
└── 📊 DADOS_SINARM/          # Dados (26 CSVs)
    ├── OCORRENCIAS/
    ├── PORTES/
    ├── REGISTROS/
    └── REQUERIMENTOS/
```

---

## Requisitos Mínimos

- **Python:** 3.8+ (recomendado: 3.10+)
- **Ollama:** Última versão
- **Espaço em disco:** ~500 MB
- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Sistema operacional:** Windows 10+, Linux (qualquer distro recente), macOS 10.15+

---

## O Que Você Vai Aprender

Neste E1 (Encontro 1), você vai entender:

✅ Como funciona um agente LLM  
✅ Padrão ReAct (Reasoning + Acting)  
✅ LangChain framework  
✅ Integração com Ollama (modelos locais)  
✅ Criação de tools customizadas  
✅ Manipulação de datasets reais  
✅ Logging e debugging de agentes  

---

## Próximos Encontros

- **E2:** Memória e contexto
- **E3:** RAG (Retrieval-Augmented Generation)
- **E4:** Interface web
- **E5:** Deploy em produção
- **E6:** Multi-agentes
- **E7:** Projeto final

---

## Links Importantes

- **Repositório:** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026
- **Ollama:** https://ollama.ai
- **LangChain Docs:** https://python.langchain.com
- **Issues (dúvidas/bugs):** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026/issues

---

**Bons estudos! 🚀**
