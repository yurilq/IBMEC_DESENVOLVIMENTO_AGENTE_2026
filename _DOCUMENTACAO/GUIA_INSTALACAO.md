# 🚀 GUIA DE INSTALAÇÃO - Ambiente de Desenvolvimento

**Disciplina:** Desenvolvimento de Agentes - MBA IA  
**Versão:** 1.0  
**Tempo estimado:** 30-45 minutos

---

## 📋 PRÉ-REQUISITOS

### 1. Python 3.10 ou 3.11

**Verificar versão instalada:**
```bash
python --version
# OU
python3 --version
```

**Resultado esperado:**
```
Python 3.10.x ou Python 3.11.x
```

**Se não tiver ou versão errada:**

#### Windows:
1. Baixar: https://www.python.org/downloads/
2. Selecionar Python 3.10.11 (recomendado) ou 3.11.x
3. ✅ **IMPORTANTE:** Marcar "Add Python to PATH"
4. Instalar

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

#### macOS:
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.10
```

---

### 2. Git

**Verificar se tem Git:**
```bash
git --version
```

**Se não tiver:**
- **Windows:** https://git-scm.com/download/win
- **Linux:** `sudo apt install git`
- **macOS:** `brew install git`

---

### 3. Ollama (Opcional - Apenas para Agentes com LLM)

**O que é?**
Ollama permite rodar LLMs localmente (como ChatGPT, mas no seu computador).

**Quando é necessário?**
- ✅ Necessário: Para agentes E2+ (agente_v2.0+)
- ❌ Não necessário: Para atividades com dados mock (ATIVIDADE_*.py)

**Instalação:**
1. Baixar: https://ollama.ai
2. Instalar (executável simples)
3. Baixar modelo:
   ```bash
   ollama pull llama3
   ```
   ⏱️ **Atenção:** Download de ~4GB, pode demorar 10-30 min

**Verificar instalação:**
```bash
ollama --version
ollama list  # Deve mostrar llama3
```

---

## 📥 PASSO 1: CLONAR REPOSITÓRIO

### Se você tem acesso ao Git:

```bash
cd /caminho/onde/voce/quer/o/projeto

# Clonar repositório
git clone [URL_DO_REPOSITORIO]

# Entrar na pasta
cd 03_CODIGOS_PRONTOS
```

### Se você recebeu ZIP:

1. Extrair arquivo `03_CODIGOS_PRONTOS.zip`
2. Abrir terminal na pasta extraída

---

## 🐍 PASSO 2: CRIAR AMBIENTE VIRTUAL

**Por que?**
Ambiente virtual isola as dependências do projeto, evitando conflitos.

### Windows:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar
venv\Scripts\activate

# Verificar (prompt deve mostrar (venv))
```

### Linux/macOS:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar
source venv/bin/activate

# Verificar (prompt deve mostrar (venv))
```

**✅ Resultado esperado:**
Seu prompt deve mostrar `(venv)` no início:
```
(venv) C:\Users\...\03_CODIGOS_PRONTOS>
```

---

## 📦 PASSO 3: INSTALAR DEPENDÊNCIAS

**Com ambiente virtual ativado:**

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

⏱️ **Tempo estimado:** 2-5 minutos

**Verificar instalação:**
```bash
pip list
```

Deve mostrar:
- langchain
- langchain-core
- langchain-community
- langchain-ollama
- pandas
- numpy
- python-dotenv

---

## ✅ PASSO 4: VALIDAR INSTALAÇÃO

**Executar script de verificação:**

```bash
python verify_setup.py
```

**Resultado esperado:**
```
🔍 VERIFICANDO AMBIENTE...

✅ Python versão: 3.10.11 (OK)
✅ Ambiente virtual: Ativado
✅ langchain: 0.1.0 (OK)
✅ langchain-ollama: 0.1.0 (OK)
✅ pandas: 2.0.3 (OK)
✅ DADOS_SINARM/: Encontrado (135.254 registros)
✅ utils/tools_sinarm.py: OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AMBIENTE PRONTO PARA USO!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Se algum item falhar:**
- Consultar seção [Troubleshooting](#troubleshooting) abaixo
- Ou arquivo `TROUBLESHOOTING.md`

---

## 🎯 PASSO 5: TESTE RÁPIDO

### Testar E1 (Não precisa Ollama):

```bash
cd E1_ANATOMIA_DO_AGENTE/solucao_final
python agente_v1.8_completo.py
```

**Resultado esperado:**
```
================================================================================
AGENTE v1.8 - COMPLETO (E1)
================================================================================

✅ Tools carregadas: 4
✅ Dados SINARM: 135.254 registros

Query: Quantas pistolas foram registradas em 2026?
...
📤 Resposta: 12.750 pistolas registradas em 2026
```

### Testar E2 (Requer Ollama):

```bash
cd E2_QUALIDADE_E_MEMORIA/solucao_final
python agente_v2.0_fewshot.py
```

**Se Ollama não estiver rodando:**
```bash
# Em outro terminal
ollama serve
```

---

## 📚 ESTRUTURA DO PROJETO

```
03_CODIGOS_PRONTOS/
├── venv/                      ← Seu ambiente virtual (criado)
├── DADOS_SINARM/              ← Dados reais
├── utils/                     ← Tools compartilhadas
├── E1_ANATOMIA_DO_AGENTE/     ← Encontro 1
├── E2_QUALIDADE_E_MEMORIA/    ← Encontro 2
└── requirements.txt           ← Dependências
```

---

## 🔧 WORKFLOW DIÁRIO

### Sempre que for trabalhar:

**1. Ativar ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**2. (Se usar Ollama) Iniciar servidor:**
```bash
ollama serve
```

**3. Trabalhar normalmente**

**4. Ao terminar, desativar:**
```bash
deactivate
```

---

## 🆘 TROUBLESHOOTING

### Problema 1: "python não é reconhecido"

**Windows:**
```bash
# Tentar com py
py --version
py -m venv venv
```

**Linux/macOS:**
```bash
# Usar python3
python3 --version
python3 -m venv venv
```

### Problema 2: "No module named 'langchain'"

**Causa:** Ambiente virtual não ativado ou dependências não instaladas

**Solução:**
```bash
# Verificar se (venv) aparece no prompt
# Se não, ativar:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema 3: "Ollama connection refused"

**Causa:** Ollama não está rodando

**Solução:**
```bash
# Terminal 1
ollama serve

# Terminal 2 (seu trabalho)
cd 03_CODIGOS_PRONTOS
venv\Scripts\activate
python ...
```

### Problema 4: "Permission denied" ao criar venv

**Linux/macOS:**
```bash
sudo apt install python3.10-venv
python3 -m venv venv
```

### Problema 5: Erro SSL ao instalar dependências

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Problema 6: "DADOS_SINARM/ não encontrado"

**Causa:** CSVs não foram baixados/extraídos

**Solução:**
1. Verificar se existe `DADOS_SINARM/` na raiz
2. Se não, baixar ZIP dos dados (instrutor fornece)
3. Extrair na raiz do projeto

---

## 📞 SUPORTE

### Problemas comuns:
- Consultar `TROUBLESHOOTING.md`
- Ler FAQ no `README.md`

### Problemas específicos:
- Contatar instrutor
- Abrir issue no repositório (se aplicável)

---

## ✅ CHECKLIST FINAL

Antes de começar a trabalhar, verificar:

- [ ] Python 3.10 ou 3.11 instalado
- [ ] Git instalado
- [ ] Repositório clonado/extraído
- [ ] Ambiente virtual criado
- [ ] Ambiente virtual ativado (mostra `(venv)`)
- [ ] Dependências instaladas (`pip list` mostra langchain)
- [ ] `verify_setup.py` executado com sucesso
- [ ] (Opcional) Ollama instalado e modelo llama3 baixado
- [ ] Teste rápido executado com sucesso

**✅ Se todos os itens OK: VOCÊ ESTÁ PRONTO!**

---

## 🎓 PRÓXIMOS PASSOS

1. Ler `README.md` principal
2. Ler `README_E1.md` (Encontro 1)
3. Começar com `E1_ANATOMIA_DO_AGENTE/conceitos/01_react_basico/`
4. Seguir sequência de atividades

---

**Dúvidas?** Consultar instrutor ou documentação completa.

**Boa jornada!** 🚀
