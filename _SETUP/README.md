# ⚙️ SETUP - INSTALAÇÃO E CONFIGURAÇÃO

Scripts automatizados para configurar o ambiente de desenvolvimento.

---

## 📁 Arquivos Disponíveis

| Arquivo | Sistema | Descrição |
|---------|---------|-----------|
| `setup.bat` | Windows | Instalação automática |
| `setup.sh` | Linux/Mac | Instalação automática |
| `verify_setup.py` | Todos | Verificar instalação |
| `teste_imports.py` | Todos | Testar imports Python |

---

## 🚀 INSTALAÇÃO RÁPIDA

### Windows
```cmd
setup.bat
```

### Linux/Mac
```bash
bash setup.sh
```

---

## ✅ VERIFICAR INSTALAÇÃO

Após executar o setup:

```bash
python verify_setup.py
```

**Saída esperada**:
```
✅ Python 3.10+ detectado
✅ Todas as bibliotecas instaladas
✅ Dados SINARM encontrados
✅ Ambiente pronto!
```

---

## 🔧 O QUE OS SCRIPTS FAZEM

### 1. `setup.bat` / `setup.sh`
- Cria ambiente virtual Python
- Instala dependências do `requirements.txt`
- Verifica estrutura de pastas
- Testa imports básicos

### 2. `verify_setup.py`
- Verifica versão do Python
- Testa todas as bibliotecas
- Checa se dados existem
- Testa imports principais

### 3. `teste_imports.py`
- Testa imports específicos
- Valida tools SINARM
- Verifica OpenAI API (se configurada)

---

## ⚠️ PROBLEMAS COMUNS

### Erro: Python não encontrado
```bash
# Instalar Python 3.10+
# Windows: https://python.org/downloads
# Linux: sudo apt install python3.10
# Mac: brew install python@3.10
```

### Erro: pip não funciona
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Erro: Permissão negada (Linux/Mac)
```bash
chmod +x setup.sh
bash setup.sh
```

---

## 📚 MAIS AJUDA

- **Problemas de instalação**: `../_DOCUMENTACAO/TROUBLESHOOTING.md`
- **Guia completo**: `../_DOCUMENTACAO/GUIA_INSTALACAO.md`
- **Voltar ao início**: `../README.md`

---

## ✅ CHECKLIST

- [ ] Executei `setup.bat` ou `setup.sh`
- [ ] Executei `python verify_setup.py`
- [ ] Todos os testes passaram ✅
- [ ] Pronto para começar!

---

**Dica**: Execute `verify_setup.py` sempre que tiver dúvida se o ambiente está OK!
