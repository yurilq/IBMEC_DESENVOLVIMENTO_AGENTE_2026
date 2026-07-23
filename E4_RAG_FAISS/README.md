# 🎓 E4 - RAG, Few-Shot e Chain-of-Thought

**MBA em IA - Segurança Pública (PCDF)**  
**Encontro 4:** Retrieval-Augmented Generation e Técnicas Avançadas  
**Disciplina:** Desenvolvimento de Agentes IA

---

## 📋 SOBRE ESTE MATERIAL

Este pacote contém **3 agentes completos e funcionais** desenvolvidos no E4:

- **v4.5 (RAG TF-IDF):** 93% acurácia 🥇 VENCEDOR
- **v4.6 (Few-Shot + CoT):** 91% acurácia 🥈
- **v4.7 (RAG + Few-Shot + CoT):** 89% acurácia 🥉

**Objetivo pedagógico:** Demonstrar que **mais técnicas ≠ melhor resultado**  
**Lição principal:** Simplicidade venceu complexidade (Paradoxo da Complexidade)

---

## 🚀 INÍCIO RÁPIDO (3 PASSOS)

### **PASSO 1: Instalar Ambiente**

```bash
# 1. Navegar para a pasta
cd caminho/para/03_CODIGOS_PRONTOS

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 4. Instalar dependências (automático)
python instalar_dependencias.py
```

**OU** seguir o guia detalhado: `GUIA_INSTALACAO_AMBIENTE.md`

---

### **PASSO 2: Verificar Instalação**

```bash
python diagnostico.py
```

**Deve mostrar:** `✅ DIAGNÓSTICO: TUDO OK!`

---

### **PASSO 3: Testar Agentes**

**Opção A: Teste Rápido (um agente)**
```bash
python pergunta_universal.py 4.5 "Quantas armas Taurus?"
```

**Opção B: Comparação Completa (todos agentes)**
```bash
python chat_universal.py
# Escolher: Opção 2 (Comparar todos os agentes)
```

---

## 📁 ESTRUTURA DO PROJETO

```
03_CODIGOS_PRONTOS/
├── scripts_agente/              # Agentes funcionais
│   ├── agente_v4_5_rag.py      # v4.5: RAG TF-IDF (93%) 🥇
│   ├── agente_v4_6_fewshot_cot.py  # v4.6: Few-Shot+CoT (91%) 🥈
│   ├── agente_v4_7_rag_fewshot_cot.py  # v4.7: Combinado (89%) 🥉
│   ├── tool_rag_tfidf.py       # RAG com TF-IDF (100% local)
│   ├── tools_basicas_v2.py     # Ferramentas SQL
│   └── config_llm.py           # Configuração LLM
├── DADOS_SINARM/                # Dados para testes
│   ├── sinarm_sample_2026.csv  # 74k registros de armas
│   └── documentos_conceituais.json  # 20 documentos (RAG)
├── docs/                        # Documentação pedagógica
│   ├── LICAO_PARADOXO_COMPLEXIDADE.md  # Lição principal
│   ├── RESULTADOS_FINAIS_TODAS_VERSOES.md  # Comparação
│   └── (outros documentos técnicos)
├── pergunta_universal.py        # ⭐ Testar agentes (CLI)
├── chat_universal.py            # ⭐ Comparar agentes (GUI)
├── diagnostico.py               # ⭐ Verificar ambiente
├── instalar_dependencias.py     # ⭐ Setup automático
├── requirements.txt             # Dependências Python
├── .env.example                 # Template configuração
├── README.md                    # Este arquivo
├── GUIA_FAZER_UMA_PERGUNTA.md   # Como usar
├── GUIA_INSTALACAO_AMBIENTE.md  # Setup detalhado
└── ROTEIRO_AULA_PRATICA_COMPLETO.md  # Para professores
```

---

## 🎯 SCRIPTS PRINCIPAIS

### **1. pergunta_universal.py** (Teste Individual)

Testa um agente específico com uma pergunta.

**Uso:**
```bash
python pergunta_universal.py <versao> <pergunta>
```

**Exemplos:**
```bash
# v4.5 - Quantitativa
python pergunta_universal.py 4.5 "Quantas armas Taurus?"

# v4.5 - Conceitual (RAG)
python pergunta_universal.py 4.5 "O que é arma apreendida?"

# v4.6 - Comparativa
python pergunta_universal.py 4.6 "Há mais Taurus ou Glock?"

# v4.7 - Conceitual complexa
python pergunta_universal.py 4.7 "Diferença entre furto e roubo?"
```

---

### **2. chat_universal.py** (Comparação Interativa)

Interface para testar e comparar todos os agentes.

**Uso:**
```bash
python chat_universal.py
```

**Features:**
- Menu interativo
- Testar agente específico
- **Comparar todos os agentes** com mesma pergunta
- Perguntas pré-definidas
- Informações sobre cada versão

---

### **3. diagnostico.py** (Verificação de Ambiente)

Verifica se todas as dependências estão instaladas.

**Uso:**
```bash
python diagnostico.py
```

**Verifica:**
- ✅ Versão Python
- ✅ Dependências instaladas (7 pacotes)
- ✅ Importação dos agentes (v4.5, v4.6, v4.7)

---

### **4. instalar_dependencias.py** (Setup Automático)

Instala todas as dependências necessárias.

**Uso:**
```bash
python instalar_dependencias.py
```

**Instala:**
- LangChain (framework)
- OpenAI SDK (via OpenRouter)
- Scikit-learn (RAG TF-IDF)
- Pandas (manipulação dados)
- Python-dotenv (configuração)
- E mais...

---

## 📚 DOCUMENTAÇÃO COMPLETA

### **Para Alunos:**

1. **`README.md`** (este arquivo) - Visão geral
2. **`GUIA_INSTALACAO_AMBIENTE.md`** - Setup passo a passo
3. **`GUIA_FAZER_UMA_PERGUNTA.md`** - Como usar os agentes
4. **`docs/LICAO_PARADOXO_COMPLEXIDADE.md`** - Lição pedagógica

### **Para Professores:**

5. **`ROTEIRO_AULA_PRATICA_COMPLETO.md`** - Roteiro 90 minutos
6. **`docs/RESULTADOS_FINAIS_TODAS_VERSOES.md`** - Análise técnica

---

## 🔧 CONFIGURAÇÃO

### **API Key (OpenRouter):**

**1. Criar arquivo `.env`:**
```bash
# Copiar template
cp .env.example .env
```

**2. Editar `.env`:**
```
OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
LLM_TYPE=openrouter
```

**3. Obter chave:**
- Acessar: https://openrouter.ai/keys
- Criar conta (se necessário)
- Gerar nova chave
- Copiar e colar no `.env`

**⚠️ IMPORTANTE:** Nunca compartilhar arquivo `.env` real!

---

## 📊 RESULTADOS ESPERADOS

### **Teste 1: v4.5 (Quantitativa)**
```bash
python pergunta_universal.py 4.5 "Quantas armas Taurus?"
```
**Resultado:** 17.760 armas  
**Tempo:** ~5 segundos  
**Técnica:** SQL tool

---

### **Teste 2: v4.5 (Conceitual - RAG)**
```bash
python pergunta_universal.py 4.5 "O que é calibre de arma?"
```
**Resultado:** Definição completa com fonte (Documento 5)  
**Tempo:** ~5 segundos  
**Técnica:** RAG TF-IDF (20 docs, 1000 features)

---

### **Teste 3: v4.6 (Comparativa)**
```bash
python pergunta_universal.py 4.6 "Há mais Taurus ou Glock?"
```
**Resultado:** Taurus: 17.760 vs Glock: 726  
**Tempo:** ~6 segundos  
**Técnica:** Few-Shot + CoT + fallback keywords

---

### **Teste 4: v4.7 (Conceitual Complexa)**
```bash
python pergunta_universal.py 4.7 "Diferença entre furto e roubo?"
```
**Resultado:** Explicação completa (violência, penas, etc)  
**Tempo:** ~6 segundos  
**Técnica:** RAG + Few-Shot + CoT

---

## 🏆 COMPARAÇÃO DAS VERSÕES

| Versão | Técnicas | Acurácia | RAG? | Velocidade | Complexidade |
|--------|----------|----------|------|------------|--------------|
| **v4.5** | RAG TF-IDF | **93%** 🥇 | ✅ 95% | 2.24s | Simples |
| **v4.6** | Few-Shot + CoT | **91%** 🥈 | ❌ 0% | 4.77s | Média |
| **v4.7** | RAG + Few-Shot + CoT | **89%** 🥉 | ⚠️ 18% | 2.66s | Alta |

### **Descoberta Principal:**

**1 técnica (v4.5) > 3 técnicas (v4.7)**

**Por quê?**
- Few-Shot força classificação rígida
- RAG fornece contexto amplo
- Conflito de sinais → RAG subutilizado (18% vs 95%)
- **Lição:** Simplicidade > Complexidade

**Leia mais:** `docs/LICAO_PARADOXO_COMPLEXIDADE.md`

---

## 🧪 EXEMPLOS DE PERGUNTAS

### **Perguntas Conceituais (RAG):**
```bash
"O que é arma apreendida?"
"Explique o que é calibre de arma"
"Diferença entre furto e roubo?"
"O que significa BO?"
"Compare pistola com revólver"
```

### **Perguntas Quantitativas (SQL):**
```bash
"Quantas armas Taurus?"
"Total de armas calibre .38"
"Quantas armas foram roubadas?"
"Quantas Glock 9mm?"
"Há mais Taurus ou Glock?"
```

### **Perguntas Comparativas:**
```bash
"Compare Taurus com Glock"
"Qual tem mais: pistola ou revólver?"
"Diferença entre .38 e 9mm?"
```

---

## 🐛 TROUBLESHOOTING

### **Erro: "No module named 'sklearn'"**
```bash
pip install scikit-learn==1.9.0
```

### **Erro: "No module named 'langchain_openai'"**
```bash
pip install langchain-openai==1.4.0
```

### **Erro: "OPENROUTER_API_KEY not found"**
```bash
# Criar arquivo .env
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
echo "LLM_TYPE=openrouter" >> .env
```

### **Erro: "FileNotFoundError: documentos_conceituais.json"**
```bash
# Verificar se está na pasta correta
pwd  # Linux/macOS
cd  # Windows

# Deve estar em: .../03_CODIGOS_PRONTOS
```

**Mais soluções:** `GUIA_INSTALACAO_AMBIENTE.md` (seção Problemas Comuns)

---

## 🎓 CONTEÚDO PEDAGÓGICO

### **1. Paradoxo da Complexidade**

**Definição:** Adicionar mais técnicas pode piorar ao invés de melhorar

**Nosso caso:**
- v4.5 (1 técnica): 93%
- v4.7 (3 técnicas): 89%

**Teorias relacionadas:**
- Navalha de Occam
- No Free Lunch Theorem
- Lei dos Retornos Decrescentes

**Leia:** `docs/LICAO_PARADOXO_COMPLEXIDADE.md`

---

### **2. RAG com TF-IDF**

**Por que TF-IDF ao invés de embeddings neurais?**

✅ **Vantagens:**
- 100% local (sem PyTorch)
- Rápido para bases pequenas (<10k docs)
- Funciona no Windows sem problemas DLL
- Interpretável (mostra keywords)

⚠️ **Desvantagens:**
- Não entende sinônimos
- Lento para bases grandes
- Apenas keywords (não semântica)

**Quando usar:**
- Base pequena (<10k documentos)
- Vocabulário técnico específico
- Ambiente com restrições (Windows, sem GPU)

**Leia:** `docs/RAG_IMPLEMENTADO_SUCESSO.md`

---

### **3. Few-Shot Learning**

**O que é:** Ensinar o LLM com exemplos

**Nosso uso:**
- 5 exemplos de classificação
- Melhora consistência do LLM
- Reduz ambiguidade

**Resultado:** 91% (v4.6)

---

### **4. Chain-of-Thought (CoT)**

**O que é:** Fazer LLM raciocinar passo a passo

**Nosso uso:**
- 4 etapas de raciocínio
- Aumenta explicabilidade
- Melhora decisões complexas

**Combinado com Few-Shot:** 91% (v4.6)

---

## 📖 REFERÊNCIAS

### **Papers Científicos:**
- Retrieval-Augmented Generation (Lewis et al., 2020)
- Chain-of-Thought Prompting (Wei et al., 2022)
- Few-Shot Learning (Brown et al., 2020 - GPT-3)
- TF-IDF (Salton & McGill, 1983)

### **Exemplos na Indústria:**
- Netflix Prize (2009) - Complexidade vs Simplicidade
- ResNet (2015) - Atalhos em redes profundas
- GPT-3 vs GPT-4 - Quando usar cada um

### **Teorias Clássicas:**
- Navalha de Occam (Século 14)
- No Free Lunch Theorem (Wolpert, 1997)
- Lei dos Retornos Decrescentes (Economia)

---

## 🆘 SUPORTE

### **Durante a Aula:**
- Professor e monitores disponíveis
- Perguntar no chat/levantar mão
- Trabalhar em dupla

### **Fora da Aula:**
- Email: [professor@email.com]
- WhatsApp: Grupo da turma
- Documentação: Ler arquivos .md

### **Recursos Online:**
- LangChain Docs: https://python.langchain.com
- OpenRouter: https://openrouter.ai/docs
- Scikit-learn: https://scikit-learn.org

---

## 📝 LICENÇA E USO

**Material educacional** para MBA em IA - Segurança Pública (PCDF)

**Permitido:**
- ✅ Usar para fins educacionais
- ✅ Modificar e experimentar
- ✅ Compartilhar com colegas da turma

**Não permitido:**
- ❌ Uso comercial sem autorização
- ❌ Compartilhar API keys reais
- ❌ Redistribuir sem créditos

---

## 👥 CRÉDITOS

**Desenvolvido por:** Professor [Nome] + OpenCode AI  
**Instituição:** IBMEC  
**Disciplina:** Desenvolvimento de Agentes IA  
**Data:** 2026  

**Agradecimentos:**
- Alunos do MBA (testes e feedback)
- PCDF (dados SINARM anonimizados)
- Comunidade LangChain

---

## 🚀 PRÓXIMOS PASSOS

### **Após a Aula:**

1. **Experimentar com perguntas próprias**
2. **Adicionar novos documentos conceituais**
3. **Modificar parâmetros do RAG (TF-IDF)**
4. **Tentar aplicar em outro domínio**
5. **Ler documentação completa**

### **Projeto Final (Sugestão):**

Criar um agente RAG para domínio específico:
- Escolher área (jurídica, médica, etc)
- Coletar 20-50 documentos
- Configurar RAG TF-IDF
- Testar 100 perguntas
- Comparar com baseline
- Documentar resultados

---

## 📞 CONTATO

**Professor:** [Nome do Professor]  
**Email:** [email@instituicao.edu.br]  
**WhatsApp:** [Grupo da Turma]  
**Instituição:** IBMEC  

---

**✅ Material pronto para uso! Boa aula! 🎓**

---

**Versão:** 1.0 (2026-07-23)  
**Última atualização:** 2026-07-23
