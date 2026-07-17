# 🎓 CÓDIGOS AULA - MBA IA GENERATIVA

**Repositório de Códigos Práticos**  
**Disciplina**: Desenvolvimento de Agentes Conversacionais  
**Instituição**: IBMEC + PCDF

---

## 🚀 COMECE AQUI (3 PASSOS)

### 1️⃣ Clone ou Baixe
```bash
git clone [URL_REPOSITORIO]
cd CODIGOS_AULA
```

### 2️⃣ Configure o Ambiente
```bash
# Windows
_SETUP\setup.bat

# Linux/Mac
bash _SETUP/setup.sh
```

### 3️⃣ Verifique a Instalação
```bash
python _SETUP/verify_setup.py
```

✅ **Pronto! Agora pode começar.**

---

## 📂 ESTRUTURA (Organizada e Clara)

```
CODIGOS_AULA/
│
├── 📘 README.md                   ← Você está aqui
├── 🚀 QUICK_START.md              ← Setup rápido (1 página)
├── 📦 requirements.txt            ← Dependências Python
│
├── 🎯 E1_ANATOMIA_DO_AGENTE/      ← Encontro 1 (Tools + ReAct)
├── 🎯 E2_QUALIDADE_E_MEMORIA/     ← Encontro 2 (Few-shot + CoT)
├── 🎯 E3_HANDS_ON_CONSTRUCAO_ZERO/← Encontro 3 (LangChain vs CrewAI)
│
├── 📊 DADOS_SINARM/               ← Datasets reais PCDF
│   ├── OCORRENCIAS_2026.csv       (74.758 registros)
│   ├── PORTES_2026.csv
│   ├── REGISTROS_2026.csv
│   └── REQUERIMENTOS_2026.csv
│
├── 🛠️ utils/                      ← Ferramentas compartilhadas
│   └── tools_sinarm.py            (4 tools prontas)
│
├── 📚 _DOCUMENTACAO/              ← Guias e instruções
│   ├── GUIA_GITHUB.md
│   ├── GUIA_INSTALACAO.md
│   ├── INSTRUCOES_ALUNOS.md
│   ├── TROUBLESHOOTING.md
│   └── ...
│
├── ⚙️ _SETUP/                     ← Scripts de instalação
│   ├── setup.bat                  (Windows)
│   ├── setup.sh                   (Linux/Mac)
│   ├── verify_setup.py            (Testar ambiente)
│   └── teste_imports.py
│
└── 📁 _INTERNO/                   ← Arquivos internos (professor)
    └── ... (versões antigas, relatórios)
```

---

## 🎯 ENCONTROS (E1 → E7)

| # | Encontro | Tópico | Status | Código |
|---|----------|--------|--------|--------|
| **E1** | 14-16/07 | Anatomia do Agente | ✅ Pronto | `E1_ANATOMIA_DO_AGENTE/` |
| **E2** | 21-23/07 | Qualidade & Memória | ✅ Pronto | `E2_QUALIDADE_E_MEMORIA/` |
| **E3** | 28-30/07 | LangChain vs CrewAI | 🔄 Em prep. | `E3_HANDS_ON_CONSTRUCAO_ZERO/` |
| **E4** | 04-06/08 | RAG + FAISS | ⏳ | - |
| **E5** | 11-13/08 | Especialização PDFs | ⏳ | - |
| **E6** | 18-20/08 | Deploy + Guardrails | ⏳ | - |
| **E7** | 25-27/08 | Métricas + Final | ⏳ | - |

---

## 📖 GUIAS RÁPIDOS

### Para Alunos

| Preciso de... | Arquivo |
|---------------|---------|
| Setup rápido (5 min) | `QUICK_START.md` |
| Instruções completas | `_DOCUMENTACAO/INSTRUCOES_ALUNOS.md` |
| Problemas? | `_DOCUMENTACAO/TROUBLESHOOTING.md` |
| Como usar Git? | `_DOCUMENTACAO/GUIA_GITHUB.md` |

### Para Professores

| Preciso de... | Localização |
|---------------|-------------|
| Relatórios internos | `_INTERNO/` |
| Versões antigas | `_INTERNO/_versoes_antigas/` |

---

## 💻 REQUISITOS

### Python
- Python 3.10+
- pip atualizado

### Bibliotecas Principais
```
langchain
openai
python-dotenv
pandas
faiss-cpu
```

Tudo em: `requirements.txt`

---

## 🔧 INSTALAÇÃO DETALHADA

### Windows
1. Abrir terminal na pasta `CODIGOS_AULA`
2. Executar:
   ```cmd
   _SETUP\setup.bat
   ```
3. Verificar:
   ```cmd
   python _SETUP\verify_setup.py
   ```

### Linux/Mac
1. Abrir terminal na pasta `CODIGOS_AULA`
2. Executar:
   ```bash
   bash _SETUP/setup.sh
   ```
3. Verificar:
   ```bash
   python3 _SETUP/verify_setup.py
   ```

---

## 📊 DADOS SINARM

### Datasets Disponíveis

| Dataset | Registros | Arquivo |
|---------|-----------|---------|
| Ocorrências | 74.758 | `DADOS_SINARM/OCORRENCIAS_2026.csv` |
| Portes de Arma | 2.328 | `DADOS_SINARM/PORTES_2026.csv` |
| Registros de Arma | 12.798 | `DADOS_SINARM/REGISTROS_2026.csv` |
| Requerimentos | 46.116 | `DADOS_SINARM/REQUERIMENTOS_2026.csv` |

**Total**: 135.000+ registros reais

---

## 🛠️ FERRAMENTAS PRONTAS

### `utils/tools_sinarm.py`

4 tools profissionais prontas para usar:

1. **buscar_ocorrencias_por_tipo** - Busca por tipo de crime
2. **buscar_ocorrencias_por_regiao** - Busca por região
3. **buscar_portes_por_status** - Status de portes
4. **buscar_registros_por_calibre** - Registros por calibre

**Uso**:
```python
from utils.tools_sinarm import buscar_ocorrencias_por_tipo

resultado = buscar_ocorrencias_por_tipo("FURTO")
print(resultado)
```

---

## 🎯 COMO USAR POR ENCONTRO

### E1 - Anatomia do Agente
```bash
cd E1_ANATOMIA_DO_AGENTE
python solucao_final/agente_v1.8.py
```

### E2 - Qualidade & Memória
```bash
cd E2_QUALIDADE_E_MEMORIA
python solucao_final/agente_v2.0.py
```

### E3 - LangChain vs CrewAI
```bash
cd E3_HANDS_ON_CONSTRUCAO_ZERO
# (em desenvolvimento)
```

---

## 📝 LOGS

Todos os logs são salvos em:
```
logs/agente_YYYYMMDD_HHMMSS.log
```

Para ver logs em tempo real:
```bash
# Windows
type logs\agente_*.log

# Linux/Mac
cat logs/agente_*.log
```

---

## 🔒 VARIÁVEIS DE AMBIENTE

Crie um arquivo `.env` na raiz:

```bash
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.0
MAX_TOKENS=2000
```

---

## 🆘 PROBLEMAS COMUNS

### ImportError: No module named 'X'
```bash
pip install -r requirements.txt
```

### Erro de API Key
Verifique se `.env` existe e tem `OPENAI_API_KEY`

### Dados não encontrados
Verifique se está na pasta `CODIGOS_AULA/` ao executar

**Mais ajuda**: `_DOCUMENTACAO/TROUBLESHOOTING.md`

---

## 🤝 CONTRIBUINDO

Este é um repositório educacional. Para sugestões:
1. Crie uma issue
2. Ou fale com o professor

---

## 📞 SUPORTE

### Documentação
- `QUICK_START.md` - Setup rápido
- `_DOCUMENTACAO/` - Guias completos
- `_SETUP/verify_setup.py` - Teste de ambiente

### Professor
- Durante as aulas
- Ou via email institucional

---

## 📜 LICENÇA

Material educacional - MBA IBMEC/PCDF  
Uso restrito a alunos da disciplina

---

## ✅ CHECKLIST DE INÍCIO

- [ ] Clonar/baixar repositório
- [ ] Executar `_SETUP/setup.bat` (ou `.sh`)
- [ ] Verificar com `python _SETUP/verify_setup.py`
- [ ] Criar arquivo `.env` com API key
- [ ] Testar com `python E1_tools_sinarm.py`
- [ ] Ler `QUICK_START.md`
- [ ] Começar com E1!

---

**Organizado por**: OpenCode AI  
**Data**: 17/07/2026  
**Versão**: 2.0 (Estrutura limpa e organizada)  
**Status**: ✅ Pronto para uso

**BOA AULA! 🎓**
