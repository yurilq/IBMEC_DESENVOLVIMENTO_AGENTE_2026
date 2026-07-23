# 🔧 TROUBLESHOOTING - ERRO DE MÓDULOS NO VENV

**Erro:** `ModuleNotFoundError: No module named 'pandas'` (ou sklearn, langchain, etc.)

---

## 🎯 CAUSA

Você criou um **ambiente virtual (venv)** mas não instalou as dependências nele, ou está usando o Python global ao invés do venv.

---

## ✅ SOLUÇÃO RÁPIDA

### OPÇÃO 1: Instalar no venv atual (Recomendado)

```bash
# 1. Ativar o venv (Windows)
venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Testar
python teste_funcoes_direto.py
```

**Linux/Mac:**
```bash
# 1. Ativar o venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Testar
python teste_funcoes_direto.py
```

---

### OPÇÃO 2: Usar Python global (mais simples)

Se você **NÃO** quer usar venv:

```bash
# 1. Desativar venv (se estiver ativo)
deactivate

# 2. Instalar globalmente
pip install -r requirements.txt

# 3. Testar
python teste_funcoes_direto.py
```

---

### OPÇÃO 3: Recriar venv do zero

Se o venv estiver corrompido:

```bash
# 1. Deletar venv antigo
Remove-Item -Recurse -Force venv

# 2. Criar novo venv
python -m venv venv

# 3. Ativar
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Testar
python teste_funcoes_direto.py
```

---

## 🔍 DIAGNÓSTICO

Para saber **qual Python você está usando**:

```bash
# Windows PowerShell
Get-Command python | Select-Object -ExpandProperty Source

# Windows CMD
where python

# Linux/Mac
which python
```

Para saber **quais pacotes estão instalados**:

```bash
pip list
```

Para verificar **se está no venv**:

```bash
# Windows - deve mostrar (venv) no prompt
(venv) PS E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS>

# Linux/Mac - deve mostrar (venv) no prompt
(venv) user@host:~/E4_RAG_FAISS$
```

---

## 🎓 PARA ALUNOS (SOLUÇÃO MAIS SIMPLES)

**Use Python global ao invés de venv:**

```bash
# 1. Fechar terminal
# 2. Abrir novo terminal
# 3. Ir para pasta do projeto
cd E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS

# 4. Instalar (SEM ativar venv)
pip install -r requirements.txt

# 5. Rodar teste
python teste_funcoes_direto.py
```

**Vantagens:**
- ✅ Mais simples
- ✅ Menos erros
- ✅ Funciona imediatamente

**Desvantagens:**
- ⚠️ Pacotes ficam misturados com outros projetos
- ⚠️ Pode ter conflito de versões (raro)

---

## 🆘 SE NADA FUNCIONAR

### Problema 1: `pip` não encontrado

```bash
# Windows - usar python -m pip
python -m pip install -r requirements.txt

# Verificar se pip está instalado
python -m ensurepip --upgrade
```

### Problema 2: Versão antiga do Python

```bash
# Verificar versão (mínimo: 3.10)
python --version

# Se for < 3.10, baixar do site:
# https://www.python.org/downloads/
```

### Problema 3: Permissão negada

```bash
# Windows - rodar PowerShell como Administrador
# Ou instalar com --user
pip install --user -r requirements.txt
```

### Problema 4: requirements.txt não encontrado

```bash
# Verificar se está na pasta correta
Test-Path -LiteralPath "requirements.txt"  # Windows
ls requirements.txt  # Linux/Mac

# Se não estiver, ir para pasta correta
cd E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS
```

---

## 📋 CHECKLIST COMPLETO

### Antes de chamar o professor:

- [ ] Verificar se está na pasta `E4_RAG_FAISS`
- [ ] Verificar se `requirements.txt` existe
- [ ] Verificar versão Python (`python --version` → mínimo 3.10)
- [ ] Tentar instalar: `pip install -r requirements.txt`
- [ ] Ver se há erros na instalação
- [ ] Tentar rodar teste: `python teste_funcoes_direto.py`
- [ ] Capturar print do erro completo

### Informações úteis para debug:

```bash
# 1. Versão Python
python --version

# 2. Localização Python
Get-Command python | Select-Object -ExpandProperty Source

# 3. Pacotes instalados
pip list

# 4. Pasta atual
pwd

# 5. Conteúdo da pasta
ls
```

---

## 💡 DICA PROFISSIONAL

**Para evitar esse problema no futuro:**

### Método 1: Sempre usar venv

```bash
# Criar venv uma vez
python -m venv venv

# SEMPRE ativar antes de trabalhar
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### Método 2: Usar Python global

```bash
# Instalar uma vez globalmente
pip install -r requirements.txt

# Nunca usar venv
# Sempre rodar direto: python script.py
```

**Escolha UM método e use sempre!**

---

## 🔗 LINKS ÚTEIS

- **Python Download:** https://www.python.org/downloads/
- **Pip Documentation:** https://pip.pypa.io/
- **Virtual Environments:** https://docs.python.org/3/library/venv.html

---

## 📞 AINDA COM PROBLEMA?

1. **Abrir issue no GitHub** com:
   - Sistema operacional (Windows/Linux/Mac)
   - Versão Python (`python --version`)
   - Print do erro completo
   - Comando que você rodou

2. **Perguntar no Discord/Slack** da turma

3. **Falar com professor** na aula

---

**Arquivo criado:** 23/07/2026  
**Para:** Alunos com erro de módulos no venv  
**Status:** Soluções testadas e validadas
