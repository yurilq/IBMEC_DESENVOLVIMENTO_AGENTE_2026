# 🚀 QUICK START - Comece em 5 Minutos!

Guia super rápido para começar a trabalhar com os códigos.

---

## ⚡ 3 PASSOS RÁPIDOS

### 1️⃣ Baixar o Código
```bash
# Opção A: Git (recomendado)
git clone [URL_DO_REPOSITORIO]
cd CODIGOS_AULA

# Opção B: Download ZIP
# Baixe e extraia em qualquer pasta
```

### 2️⃣ Instalar Dependências
```bash
# Windows
_SETUP\setup.bat

# Linux/Mac
bash _SETUP/setup.sh
```

### 3️⃣ Verificar
```bash
python _SETUP/verify_setup.py
```

✅ **Se todos os testes passaram, você está pronto!**

---

## 🎯 TESTAR AGORA

### Teste Rápido (30 segundos)
```bash
python E1_tools_sinarm.py
```

**Saída esperada**: Lista de ferramentas SINARM disponíveis

---

## 📂 ESTRUTURA RÁPIDA

```
CODIGOS_AULA/
├── E1_ANATOMIA_DO_AGENTE/      ← Encontro 1 (começar aqui)
├── E2_QUALIDADE_E_MEMORIA/     ← Encontro 2
├── DADOS_SINARM/               ← Dados reais
├── _SETUP/                     ← Scripts de instalação
└── _DOCUMENTACAO/              ← Guias detalhados
```

---

## 🎓 COMEÇAR COM E1

```bash
cd E1_ANATOMIA_DO_AGENTE
python solucao_final/agente_v1.8.py
```

---

## 🔑 CONFIGURAR API KEY (OPENAI)

Crie arquivo `.env` na raiz:

```bash
# .env
OPENAI_API_KEY=sk-sua-chave-aqui
OPENAI_MODEL=gpt-4o-mini
```

---

## ⚠️ PROBLEMAS?

### Erro de instalação
```bash
pip install -r requirements.txt
```

### Python não encontrado
Instale Python 3.10+ de [python.org](https://python.org)

### Mais ajuda
Veja: `_DOCUMENTACAO/TROUBLESHOOTING.md`

---

## 📚 PRÓXIMOS PASSOS

1. ✅ Instalou tudo? → Leia `E1_ANATOMIA_DO_AGENTE/README_E1.md`
2. ✅ Quer detalhes? → Leia `_DOCUMENTACAO/INSTRUCOES_ALUNOS.md`
3. ✅ Problemas? → Leia `_DOCUMENTACAO/TROUBLESHOOTING.md`

---

## ✅ CHECKLIST

- [ ] Baixei o código
- [ ] Executei `_SETUP/setup.bat` (ou `.sh`)
- [ ] `verify_setup.py` passou todos os testes
- [ ] Criei arquivo `.env` com API key
- [ ] Testei com `python E1_tools_sinarm.py`
- [ ] Pronto para E1! 🎉

---

**Tempo total**: 5 minutos  
**Próximo**: Entre em `E1_ANATOMIA_DO_AGENTE/`

**BOA AULA! 🎓**
