# 📊 ORGANIZAÇÃO DOS MATERIAIS - E2

## ✅ ESTRUTURA FINAL

```
E2_QUALIDADE_E_MEMORIA/
│
├── 📄 ROTEIRO_ALUNO_PRATICA_E2.md       ← PÚBLICO (para alunos)
│   • Sem gabaritos
│   • Sem respostas
│   • Instruções passo-a-passo
│   • FAQ estudantil
│
├── 📁 _INTERNO_PROFESSOR/               ← PRIVADO (gitignore)
│   ├── README.md                        (explicação da pasta)
│   ├── ROTEIRO_PROFESSOR_PRATICA_E2.md  (completo, 24KB)
│   ├── GUIA_RAPIDO_EXECUCAO.md          (resumido, 7KB)
│   └── CHECKLIST_PROFESSOR.md           (checklist, 7KB)
│
├── conceitos/                           ← Atividades práticas
│   ├── 01_fewshot/
│   ├── 02_cot/
│   ├── 03_memory_conversacional/
│   └── 04_security_basica/
│
├── solucao_final/                       ← Código referência
│   ├── agente_v2.0_fewshot.py
│   └── agente_v2.5_cot.py
│
├── demo_professor/                      ← Demo ao vivo
│   └── DEMO_COMPARATIVA_E2.py
│
├── README_E2.md                         ← Guia completo E2
└── INDEX.md                             ← Navegação rápida
```

---

## 🔐 CONTROLE DE ACESSO

### ✅ PÚBLICO (Pode compartilhar)

```
✅ ROTEIRO_ALUNO_PRATICA_E2.md
✅ README_E2.md
✅ INDEX.md
✅ conceitos/**/*.py (atividades)
✅ solucao_final/**/*.py (código referência)
✅ demo_professor/DEMO_COMPARATIVA_E2.py
```

### ❌ PRIVADO (Gitignore - Não committar)

```
❌ _INTERNO_PROFESSOR/
   ❌ ROTEIRO_PROFESSOR_PRATICA_E2.md (gabaritos)
   ❌ GUIA_RAPIDO_EXECUCAO.md (soluções)
   ❌ CHECKLIST_PROFESSOR.md (métricas internas)
```

---

## 🛡️ GITIGNORE

A pasta `_INTERNO_PROFESSOR/` está protegida por:

```gitignore
# Em: .gitignore (raiz do projeto)

# Pasta interna do professor
**/_INTERNO_PROFESSOR/

# Roteiros do professor
**/ROTEIRO_PROFESSOR*.md
**/GABARITO*.md
**/NOTAS_INTERNAS*.md
```

**Resultado:** Mesmo se tentar `git add .`, esses arquivos NÃO serão incluídos.

---

## 📝 DIFERENÇAS: PROFESSOR vs ALUNO

| Aspecto | Roteiro Professor | Roteiro Aluno |
|---------|-------------------|---------------|
| **Gabaritos** | ✅ Sim (resultados esperados) | ❌ Não |
| **Soluções** | ✅ Sim (troubleshooting completo) | ⚠️ Parcial (só FAQs) |
| **Scripts de fala** | ✅ Sim (word-for-word) | ❌ Não |
| **Timing detalhado** | ✅ Sim (minuto a minuto) | ⚠️ Parcial (blocos gerais) |
| **Métricas** | ✅ Sim (valores exatos esperados) | ❌ Não |
| **Estratégias pedagógicas** | ✅ Sim | ❌ Não |
| **Discussões guiadas** | ✅ Sim (perguntas+respostas) | ❌ Não |

---

## 🎯 USO RECOMENDADO

### 👨‍🏫 Para o Professor:

**Antes da aula:**
```bash
# 1. Ler roteiro completo
open _INTERNO_PROFESSOR/ROTEIRO_PROFESSOR_PRATICA_E2.md

# 2. Imprimir checklist
print _INTERNO_PROFESSOR/CHECKLIST_PROFESSOR.md

# 3. Abrir guia rápido (segunda tela)
open _INTERNO_PROFESSOR/GUIA_RAPIDO_EXECUCAO.md
```

**Durante a aula:**
- Seguir timeline do `GUIA_RAPIDO_EXECUCAO.md`
- Consultar `ROTEIRO_PROFESSOR` se necessário
- Marcar `CHECKLIST_PROFESSOR` a cada bloco

**Compartilhar com alunos:**
- ✅ `ROTEIRO_ALUNO_PRATICA_E2.md`
- ❌ NUNCA a pasta `_INTERNO_PROFESSOR/`

### 🎓 Para o Aluno:

**Antes da aula:**
```bash
# 1. Ler roteiro
open ROTEIRO_ALUNO_PRATICA_E2.md

# 2. Verificar pré-requisitos
python --version
ollama run llama3.2

# 3. Testar agente v1.8
python ../E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py
```

**Durante a aula:**
- Seguir roteiro aluno passo-a-passo
- Fazer TODAS as atividades na ordem
- Anotar dúvidas para perguntar

---

## 🔄 ATUALIZAÇÕES

**Após ministrar aula:**

1. Abrir `_INTERNO_PROFESSOR/ROTEIRO_PROFESSOR_PRATICA_E2.md`
2. Adicionar seção "Observações da Turma X":
   ```markdown
   ## 📝 Observações - Turma 1A (16/07/2026)
   
   - Timing real: Atrasou 15 min (ATIVIDADE 1B demorou mais)
   - Dúvida comum: "Exemplos não carregam" (path absoluto vs relativo)
   - Métrica real: Accuracy média v2.0 = 79% (vs 82% esperado)
   - Ajuste: Próxima turma → Dar 25 min na ATIVIDADE 1B
   ```

3. Salvar versão atualizada

---

## 📞 SUPORTE

**Dúvidas sobre organização:**
- Consulte este arquivo (`ORGANIZACAO.md`)

**Dúvidas sobre conteúdo:**
- Professor: Ver `_INTERNO_PROFESSOR/`
- Aluno: Ver `ROTEIRO_ALUNO_PRATICA_E2.md`

---

## ✅ CHECKLIST FINAL

### Professor:

```
□ Roteiros do professor estão em _INTERNO_PROFESSOR/
□ Pasta _INTERNO_PROFESSOR/ está no .gitignore
□ ROTEIRO_ALUNO_PRATICA_E2.md está na raiz (público)
□ Nenhum gabarito está em arquivo público
```

### Aluno:

```
□ Tenho acesso a ROTEIRO_ALUNO_PRATICA_E2.md
□ Não tenho acesso a _INTERNO_PROFESSOR/
□ Pré-requisitos testados
□ Pronto para aula!
```

---

**🎓 Organização completa! Privacidade garantida pelo gitignore.**

_Última atualização: 16/07/2026_
