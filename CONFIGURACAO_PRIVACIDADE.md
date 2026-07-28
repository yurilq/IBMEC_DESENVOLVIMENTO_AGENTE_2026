# 🔒 ARQUIVOS PRIVADOS - CONFIGURAÇÃO

Este repositório contém **dois tipos de conteúdo**:

---

## 👥 PARA ALUNOS (Público no Git)

✅ **O que OS ALUNOS VEEM no GitHub:**

```
CODIGOS_AULA/
├── README.md
├── QUICK_START.md
├── INDICE.md
├── requirements.txt
│
├── E1_ANATOMIA_DO_AGENTE/
│   ├── conceitos/
│   ├── solucao_final/
│   └── testes/
│
├── E2_QUALIDADE_E_MEMORIA/
│   ├── conceitos/
│   └── solucao_final/
│
├── E3_HANDS_ON_CONSTRUCAO_ZERO/
│
├── DADOS_SINARM/
├── utils/
│
├── _DOCUMENTACAO/
│   ├── GUIA_GITHUB.md
│   ├── GUIA_INSTALACAO.md
│   ├── INSTRUCOES_ALUNOS.md
│   └── TROUBLESHOOTING.md
│
└── _SETUP/
    ├── setup.bat
    ├── setup.sh
    └── README.md
```

---

## 🔒 PARA PROFESSOR (Privado - Git Ignore)

❌ **O que OS ALUNOS NÃO VEEM (ignorado pelo Git):**

```
_INTERNO/                           ← Pasta completa ignorada
├── CONCLUSAO_ESTRUTURACAO.md
├── CONFIRMACAO_FINAL_100_FUNCIONAL.md
├── RELATORIO_TESTES_AMBIENTE.md
├── RESUMO_ESTRUTURACAO_REPOSITORIO.md
├── SCRIPTS_AUTOMATIZADOS_RESUMO.md
├── codigos corrigidos.zip
└── _versoes_antigas/

E1_ANATOMIA_DO_AGENTE/
└── _INTERNO_PROFESSOR/             ← Ignorado

E2_QUALIDADE_E_MEMORIA/
└── _INTERNO_PROFESSOR/             ← Ignorado

E3_HANDS_ON_CONSTRUCAO_ZERO/
└── _INTERNO_PROFESSOR/             ← Ignorado

Scripts de teste (raiz):
├── TESTAR_TUDO.py                  ← Ignorado
├── TESTAR_E1.py                    ← Ignorado
├── VALIDACAO_FINAL.py              ← Ignorado
└── RELATORIO_VALIDACAO.md          ← Ignorado
```

---

## 📋 REGRAS DO .gitignore

### Pastas Completas Ignoradas
```gitignore
_INTERNO/
E1_ANATOMIA_DO_AGENTE/_INTERNO_PROFESSOR/
E2_QUALIDADE_E_MEMORIA/_INTERNO_PROFESSOR/
E3_HANDS_ON_CONSTRUCAO_ZERO/_INTERNO_PROFESSOR/
_versoes_antigas/
```

### Padrões de Arquivos Ignorados
```gitignore
*ROTEIRO_PROFESSOR*
*ROTEIRO_TERCA*
*ROTEIRO_QUINTA*
*GABARITO*
*SOLUCAO_PROFESSOR*
*RELATORIO_TESTES*
TESTAR_*.py
VALIDACAO_*.py
```

---

## ✅ COMO USAR

### Para o Professor (Você)

**Tudo funciona localmente:**
1. Você tem TODAS as pastas (_INTERNO, scripts de teste, etc.)
2. Você pode usar todos os arquivos normalmente
3. Quando fizer `git add .` → Arquivos privados NÃO serão incluídos

**Para adicionar conteúdo privado:**
```bash
# Criar nova pasta interna
mkdir E4_RAG_FAISS/_INTERNO_PROFESSOR

# Adicionar arquivo de roteiro
echo "..." > E1_ANATOMIA_DO_AGENTE/ROTEIRO_PROFESSOR.md

# Git vai ignorar automaticamente!
```

### Para os Alunos

**GitHub mostra apenas:**
- ✅ Códigos dos encontros
- ✅ Dados SINARM
- ✅ Documentação pública
- ✅ Scripts de setup

**GitHub NÃO mostra:**
- ❌ Pastas _INTERNO/
- ❌ Roteiros de aula
- ❌ Gabaritos
- ❌ Scripts de teste do professor
- ❌ Versões antigas

---

## 🔍 VERIFICAR O QUE SERÁ COMMITADO

### Antes de fazer push:

```bash
# Ver o que está tracked (público)
git status

# Ver o que está ignored (privado)
git status --ignored

# Verificar se algo privado vazou
git status | grep -i "INTERNO\|GABARITO\|ROTEIRO"
```

**Se aparecer algo privado** → Adicione ao `.gitignore`!

---

## 🚨 ATENÇÃO

### ⚠️ Antes de Push para GitHub

**SEMPRE verificar:**

1. `_INTERNO/` está ignorada?
2. Scripts `TESTAR_*.py` estão ignorados?
3. `RELATORIO_VALIDACAO.md` está ignorado?
4. Pastas `_INTERNO_PROFESSOR/` estão ignoradas?

**Comando rápido:**
```bash
git status --ignored | grep "_INTERNO\|TESTAR\|VALIDACAO\|GABARITO"
```

Se aparecer na lista de "ignored" → ✅ OK!  
Se aparecer no `git status` normal → ❌ PROBLEMA!

---

## 📝 ADICIONAR NOVOS PADRÕES

**Se criar novos tipos de arquivos privados:**

1. Editar `.gitignore`
2. Adicionar padrão
3. Testar com `git status --ignored`

**Exemplo:**
```gitignore
# Adicionar no .gitignore
*RESPOSTA_EXERCICIO*
*CORRECAO_PROVA*
```

---

## 🎯 RESUMO

| Tipo | Status | Alunos Veem? |
|------|--------|--------------|
| Códigos (E1, E2, E3) | ✅ Público | Sim |
| DADOS_SINARM | ✅ Público | Sim |
| utils/ | ✅ Público | Sim |
| _DOCUMENTACAO/ | ✅ Público | Sim |
| _SETUP/ | ✅ Público | Sim |
| **_INTERNO/** | ❌ Privado | **NÃO** |
| **_INTERNO_PROFESSOR/** | ❌ Privado | **NÃO** |
| **TESTAR_*.py** | ❌ Privado | **NÃO** |
| **VALIDACAO_*.py** | ❌ Privado | **NÃO** |
| **ROTEIRO_PROFESSOR*** | ❌ Privado | **NÃO** |
| **GABARITO*** | ❌ Privado | **NÃO** |

---

## ✅ CHECKLIST PRÉ-PUSH

Antes de `git push`:

- [ ] Executei `git status`
- [ ] Verifiquei `git status --ignored`
- [ ] Nenhum arquivo privado aparece no status normal
- [ ] Todos os privados aparecem em "ignored"
- [ ] Revisei o que será commitado
- [ ] Tudo OK para push

---

**Configurado em**: 17/07/2026  
**Última verificação**: Use `git status --ignored`
