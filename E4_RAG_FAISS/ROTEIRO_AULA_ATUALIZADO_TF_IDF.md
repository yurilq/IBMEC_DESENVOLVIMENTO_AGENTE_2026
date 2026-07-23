# 🎓 ROTEIRO DE AULA ATUALIZADO - RAG COM TF-IDF

**Disciplina:** Desenvolvimento de Agentes IA  
**Encontro:** E4 - RAG, Few-Shot e Chain-of-Thought  
**Duracao:** 120 minutos  
**Tecnologia:** RAG com TF-IDF (ao inves de FAISS)

---

## 📋 PRE-REQUISITOS

### Antes da Aula (Professor)

- [ ] Ollama instalado (https://ollama.ai)
- [ ] Modelo llama3 baixado (`ollama pull llama3`)
- [ ] Testar `teste_funcoes_direto.py` funcionando
- [ ] Preparar slide "TF-IDF vs FAISS" (justificativa)

### Materiais para Alunos

- [ ] Projeto E4_RAG_FAISS clonado/baixado
- [ ] Python 3.11+ instalado
- [ ] (Opcional) Conta OpenRouter com API key

---

## ⏱️ CRONOGRAMA (120 min)

```
00:00 - 00:10  Introducao + Justificativa TF-IDF
00:10 - 00:25  Setup (venv + dependencias)
00:25 - 00:40  Exploracao dos Dados SINARM
00:40 - 00:70  Teste das Funcoes (SQL + RAG)
00:70 - 01:40  Agente v4.5 Completo
01:40 - 02:00  Pratica Livre + Discussao
```

---

## 🎬 PARTE 1: INTRODUCAO (10 min)

### Slide 1: Objetivo da Aula

**Fala do professor:**

> "Bom dia/tarde! Hoje vamos construir um agente inteligente que responde perguntas sobre um banco de dados REAL de 74 mil registros de armas!
>
> **Nosso desafio:**
> - Dados: 74.758 ocorrencias de armas (SINARM)
> - Problema: Como responder perguntas quantitativas E conceituais?
> - Solucao: Agente com SQL tools + RAG
>
> **O que vamos fazer:**
> 1. Entender os dados SINARM
> 2. Testar ferramentas SQL (contar por marca, calibre, tipo)
> 3. Testar ferramenta RAG (buscar conhecimento conceitual)
> 4. Integrar tudo em um agente inteligente
> 5. Comparar 3 versoes de agentes (v4.5, v4.6, v4.7)
>
> Ao final, voces vao ver uma licao importante: **mais complexidade nem sempre e melhor!**"

### Slide 2: Nota Tecnica - Por que TF-IDF?

**Fala do professor:**

> "Nota tecnica rapida: o plano original era usar FAISS (ferramenta da Meta), mas encontramos problemas de compatibilidade no Windows (erros de DLL).
>
> **Entao substituimos por TF-IDF (Scikit-learn).**
>
> Por que? Tres razoes:
> 1. **Funciona em QUALQUER maquina** (100% compativel)
> 2. **Suficiente para nossa base** (20 documentos)
> 3. **Mais facil de entender** (algebra linear basica)
>
> Isso e uma licao de engenharia: escolher a ferramenta CERTA para o contexto, nao a mais sofisticada!
>
> No final da aula, vou mostrar quando usar TF-IDF vs quando usar FAISS. Vamos la!"

**Tempo:** 2-3 minutos (nao estender)

---

## 🛠️ PARTE 2: SETUP (15 min)

### Passo 1: Clonar/Baixar Projeto

```bash
# Se ainda nao tem o projeto
cd E:\documentos\ibmec\CODIGOS_AULA
cd E4_RAG_FAISS
```

### Passo 2: Criar Ambiente Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

**Explicar durante:**
> "Ambiente virtual isola as dependencias deste projeto. Boa pratica profissional!"

### Passo 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Enquanto instala (~5 min), explicar:**
> "Estamos instalando:
> - langchain: framework para agentes
> - langchain-ollama: integracao com Ollama
> - scikit-learn: TF-IDF e machine learning classico
> - pandas: manipulacao de dados
> - python-dotenv: gerenciamento de configuracoes
>
> Total: ~200 MB (muito menor que FAISS com PyTorch, que seria ~500 MB)"

### Passo 4: Configurar .env

```bash
# Opcao A: Ollama Local (100% gratuito)
copy .env.example .env
# Ja esta configurado! LLM_TYPE=ollama

# Opcao B: OpenRouter (se nao tem Ollama)
# Editar .env:
# LLM_TYPE=openrouter
# OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
```

**Perguntar:** "Quem ja tem Ollama instalado? Quem prefere usar OpenRouter?"

### Passo 5: Validar Configuracao

```bash
python scripts_agente\config_llm.py
```

**Resultado esperado:**
```
======================================================================
VALIDANDO CONFIGURACAO DE LLM
======================================================================
Tipo de LLM: ollama
  - Modelo: llama3
  - URL: http://localhost:11434
  - Status: [OK] Ollama respondendo
[OK] Configuracao valida!
[TESTE] Fazendo pergunta simples...
[RESPOSTA] Hi!
[OK] LLM funcionando corretamente!
```

---

## 📊 PARTE 3: EXPLORACAO DOS DADOS (15 min)

### 3.1: Entender Estrutura do Projeto

```bash
dir
```

**Mostrar:**
```
E4_RAG_FAISS/
├── .env                    [Configuracao]
├── scripts_agente/         [Agentes e ferramentas]
├── DADOS_SINARM/           [Dados reais]
└── teste_funcoes_direto.py [Script de teste]
```

### 3.2: Ver Dados SINARM

```bash
# Ver CSVs disponiveis
dir DADOS_SINARM\OCORRENCIAS
```

**Resultado:**
```
OCORRENCIAS_2024.csv      2.6 MB
OCORRENCIAS_2025.csv      2.7 MB
OCORRENCIAS_2026.csv     21.4 MB  <- Principal
OCORRENCIAS_ate_2023.csv 18.4 MB
```

**Abrir CSV no Excel/VSCode (primeiras linhas):**

```bash
type DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv | more
```

**Explicar colunas:**
```
ANO,SEMESTRE,UF,MUNICIPIO,TIPO,MARCA_ARMA,CALIBRE_ARMA,TIPO_OCORRENCIA
2026,1,SP,SAO PAULO,Pistola,GLOCK,9mm,Roubo
2026,1,RJ,RIO DE JANEIRO,Revolver,TAURUS,.38,Apreensao
...
```

> "74.758 registros de armas! Cada linha e uma ocorrencia: tipo de arma, marca, calibre, se foi roubada/furtada/apreendida..."

### 3.3: Ver Documentos Conceituais

```bash
type DADOS_SINARM\documentos_conceituais.json | more
```

**Explicar:**
> "20 documentos com definicoes tecnicas:
> - O que e calibre de arma?
> - Diferenca entre furto e roubo?
> - O que e BO?
> - Tipos de armas...
>
> Esses documentos vao ser usados pelo RAG para responder perguntas conceituais!"

---

## 🧪 PARTE 4: TESTAR FUNCOES (30 min)

### 4.1: Executar Testes Automaticos

```bash
python teste_funcoes_direto.py
```

**Resultado esperado:**
```
======================================================================
TESTE DIRETO - FUNCOES SQL E RAG
======================================================================

======================================================================
TESTE 1: FUNCAO SQL - Contar armas Taurus
======================================================================
[EXECUTANDO] contar_armas_marca('Taurus')
[OK] CSV carregado! 74758 linhas
[RESULTADO RAW]
Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'
[TOTAL] 17.760 armas Taurus
[STATUS] TESTE 1 - SUCESSO!

======================================================================
TESTE 2: FUNCAO SQL - Contar armas calibre .38
======================================================================
[EXECUTANDO] contar_armas_calibre('.38')
[RESULTADO RAW]
Encontrei 17564 armas calibre '.380'
[TOTAL] 17.564 armas calibre .380
[STATUS] TESTE 2 - SUCESSO!

======================================================================
TESTE 3: FUNCAO RAG - Buscar conhecimento sobre 'calibre'
======================================================================
[EXECUTANDO] buscar_conhecimento_sinarm('o que e calibre de arma')
[RAG-LOCAL] Inicializando RAG com TF-IDF...
[RAG-LOCAL] 20 documentos carregados
[RAG-LOCAL] Criando indice TF-IDF...
[RAG-LOCAL] Indice criado: 20 docs, 1000 features
[RAG-LOCAL] RAG pronto para uso!

[RESULTADO RAW]
DOCUMENTOS SINARM RELEVANTES:

[Documento 5] (Relevancia: 0.21)
Categoria: Definicoes_Tecnicas
Calibre de arma de fogo e a medida do diametro interno do cano...

[STATUS] TESTE 3 - SUCESSO!

======================================================================
TESTE 4: COMPARACAO - Taurus vs Glock
======================================================================
[EXECUTANDO] contar_armas_marca('Taurus')
  -> Taurus: 17.760 armas
[EXECUTANDO] contar_armas_marca('Glock')
  -> Glock: 726 armas
[COMPARACAO]
  Taurus: 17.760 armas
  Glock: 726 armas
[STATUS] TESTE 4 - SUCESSO!

======================================================================
TODOS OS TESTES CONCLUIDOS COM SUCESSO!
======================================================================
```

### 4.2: Explicar Cada Teste

**TESTE 1 (SQL - Marca):**
> "Busca quantitativa: 'Quantas armas Taurus?'
> - Usa Pandas para filtrar CSV
> - Busca: `df[df['MARCA_ARMA'].str.contains('TAURUS')]`
> - Resultado: 17.760 armas (23.7% do total)"

**TESTE 2 (SQL - Calibre):**
> "Busca por calibre: 'Quantas armas .38?'
> - Mesmo processo, coluna CALIBRE_ARMA
> - Resultado: 17.564 armas calibre .380"

**TESTE 3 (RAG - Conceitual):**
> "Busca conceitual: 'O que e calibre de arma?'
> - NAO busca no CSV (nao tem essa informacao la)
> - Usa RAG TF-IDF:
>   1. Vetoriza query ('calibre arma')
>   2. Calcula similaridade com 20 documentos
>   3. Retorna top-3 mais relevantes
> - Resultado: Encontrou definicao tecnica de calibre!"

**TESTE 4 (Comparacao):**
> "Multiplas queries: 'Taurus vs Glock?'
> - Executa contar_armas_marca('Taurus')
> - Executa contar_armas_marca('Glock')
> - Compara resultados
> - Conclusao: Taurus tem 24x mais armas que Glock!"

### 4.3: Analisar Como Funciona o RAG TF-IDF

**Abrir codigo:**
```bash
code scripts_agente\tool_rag_tfidf.py
```

**Explicar (10 min):**

```python
# 1. VECTORIZACAO (TF-IDF)
self.vectorizer = TfidfVectorizer(
    max_features=1000,  # 1000 features (palavras mais importantes)
    stop_words='english',
    ngram_range=(1, 2)  # Unigramas e bigramas
)
self.tfidf_matrix = self.vectorizer.fit_transform(self.textos)

# 2. BUSCA (Similaridade Coseno)
query_vec = self.vectorizer.transform([query])
similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

# 3. RANKING (Top-K)
top_indices = similarities.argsort()[::-1][:top_k]
```

**Analogia:**
> "TF-IDF e como um dicionario inteligente:
> - TF (Term Frequency): Palavra aparece muito no doc? Importante!
> - IDF (Inverse Document Frequency): Palavra aparece em TODOS docs? Menos importante!
> - Exemplo: 'calibre' aparece no Doc 5, mas nao em outros → alta relevancia!
>
> Similaridade Coseno: angulo entre vetores. Quanto menor o angulo, mais similar!"

---

## 🤖 PARTE 5: AGENTE COMPLETO (30 min)

### 5.1: Estrutura do Agente v4.5

**Mostrar diagrama no quadro:**

```
USUARIO
  |
  v
"Quantas armas Taurus?"
  |
  v
AGENTE v4.5
  |
  +---> [PASSO 1] LLM analisa pergunta
  |       └─> Tipo: "marca"
  |       └─> Parametro: {"marca": "Taurus"}
  |
  +---> [PASSO 2] Executa ferramenta
  |       └─> contar_armas_marca("Taurus")
  |       └─> SQL: df[df['MARCA_ARMA'].contains('TAURUS')]
  |       └─> Resultado: 17.760 armas
  |
  +---> [PASSO 3] LLM formata resposta
          └─> "Segundo o SINARM 2026, ha 17.760 armas Taurus."
```

### 5.2: Testar Agente Manualmente

**Abrir Python interativo:**

```python
import sys
sys.path.append('scripts_agente')

from agente_v4_5_rag import agente_v4_5_rag

# TESTE 1: Pergunta quantitativa (SQL)
resposta = agente_v4_5_rag("Quantas armas Glock?")
print(resposta)

# TESTE 2: Pergunta conceitual (RAG)
resposta = agente_v4_5_rag("O que e calibre de arma?")
print(resposta)

# TESTE 3: Comparacao
resposta = agente_v4_5_rag("Ha mais Taurus ou Glock?")
print(resposta)
```

**Ir executando ao vivo e explicando o output!**

### 5.3: Analisar Decisoes do LLM

**Mostrar logs:**

```
[PASSO 1] LLM analisando pergunta...
[LLM] {
    "tipo": "marca",
    "parametros": {"marca": "Glock"},
    "justificativa": "Pergunta menciona marca especifica Glock"
}
```

**Explicar:**
> "O LLM decidiu que tipo de ferramenta usar baseado na pergunta!
> - Viu 'Quantas' → pergunta quantitativa
> - Viu 'Glock' → marca especifica
> - Escolheu: contar_armas_marca
>
> Se tivesse visto 'O que e' → escolheria RAG (conceitual)"

### 5.4: Fallback: Palavras-chave

**Mostrar codigo:**

```python
# Se LLM errar JSON, usa fallback
except Exception as e:
    print(f"[FALLBACK] Usando deteccao por palavras-chave...")
    analise = detectar_por_palavras_chave(pergunta_usuario)
```

**Explicar:**
> "Se o LLM nao conseguir gerar JSON correto, o agente tem um plano B:
> detecta palavras-chave ('quantas', 'o que e', 'compare').
>
> Isso garante que o agente SEMPRE funciona, mesmo se LLM falhar!"

---

## 📊 PARTE 6: COMPARACAO DE VERSOES (20 min)

### 6.1: Agente v4.5 (RAG)

**Caracteristicas:**
- 1 tecnica: RAG TF-IDF
- SQL tools para dados quantitativos
- RAG para conceitos
- Acuracia: 93% (melhor!)

### 6.2: Agente v4.6 (Few-Shot + CoT)

**Caracteristicas:**
- 2 tecnicas: Few-Shot Learning + Chain-of-Thought
- Exemplos de classificacao
- Raciocinio passo a passo
- Acuracia: 91%

### 6.3: Agente v4.7 (RAG + Few-Shot + CoT)

**Caracteristicas:**
- 3 tecnicas: RAG + Few-Shot + CoT
- Combina tudo
- Acuracia: 89% (PIOR!)

### 6.4: Paradoxo da Complexidade

**Slide:**

```
╔════════════════════════════════════════════════════════════╗
║           PARADOXO DA COMPLEXIDADE                         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Versao     Tecnicas    Acuracia    Ranking               ║
║  ─────────────────────────────────────────────────────     ║
║  v4.5       1 (RAG)      93%         🥇 1º                ║
║  v4.6       2 (FS+CoT)   91%         🥈 2º                ║
║  v4.7       3 (ALL)      89%         🥉 3º                ║
║                                                            ║
║  Licao: MAIS TECNICAS ≠ MELHOR RESULTADO                  ║
║                                                            ║
║  Por que v4.7 perdeu?                                     ║
║  - Few-Shot forca classificacao rigida                    ║
║  - RAG fornece contexto amplo                             ║
║  - CONFLITO DE SINAIS → RAG subutilizado                  ║
║                                                            ║
║  Conclusao: SIMPLICIDADE > COMPLEXIDADE                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Discussao (10 min):**
- Por que isso aconteceu?
- Quando mais tecnicas ajudam vs atrapalham?
- Exemplos na industria (Netflix Prize)
- Navalha de Occam

---

## 🎯 PARTE 7: PRATICA LIVRE (20 min)

### Desafios para os Alunos

**NIVEL 1: Basico**
1. Testar perguntas diferentes no agente
2. Adicionar uma nova marca ao CSV
3. Criar um novo documento conceitual

**NIVEL 2: Intermediario**
4. Modificar threshold do RAG (testar 0.05, 0.1, 0.2)
5. Modificar top_k do RAG (testar 1, 3, 5 documentos)
6. Adicionar nova funcao SQL (ex: contar_por_estado)

**NIVEL 3: Avancado**
7. Implementar cache de resultados SQL
8. Adicionar logs detalhados
9. Criar interface web simples (Streamlit)

**NIVEL 4: Desafio**
10. Integrar FAISS (para quem quiser aprender)
11. Comparar TF-IDF vs FAISS (mesma query)
12. Criar dashboard com estatisticas

---

## 📝 ENCERRAMENTO (10 min)

### Revisao da Aula

**Perguntar aos alunos:**
1. "O que vocês aprenderam hoje?"
2. "Qual foi a parte mais interessante?"
3. "Alguma duvida?"

### Mensagens-chave

**Resumir:**

> "Hoje aprendemos 3 coisas principais:
>
> 1. **RAG nao e complicado:** TF-IDF + Similaridade Coseno ja funciona muito bem!
>
> 2. **Engenharia e tradeoffs:** Escolhemos TF-IDF ao inves de FAISS por compatibilidade. Essa e uma decisao real de projetos!
>
> 3. **Simplicidade vence:** v4.5 (1 tecnica) teve melhor resultado que v4.7 (3 tecnicas). Paradoxo da Complexidade!
>
> **Proximos passos:**
> - Pratiquem com perguntas diferentes
> - Leiam `LICAO_PARADOXO_COMPLEXIDADE.md`
> - Se quiserem, experimentem FAISS (material complementar)
>
> Obrigado e ate a proxima aula!"

---

## 📚 MATERIAL COMPLEMENTAR

### Para os Alunos

**Obrigatorio:**
- `README.md` - Visao geral do projeto
- `EXECUCAO_REAL_SUCESSO.md` - Resultados dos testes
- `LICAO_PARADOXO_COMPLEXIDADE.md` - Conceito principal

**Opcional:**
- `JUSTIFICATIVA_PEDAGOGICA_TF_IDF.md` - Por que TF-IDF?
- `ANALISE_ROTEIRO_VS_IMPLEMENTACAO.md` - Analise tecnica
- Tutorial FAISS (criar se houver demanda)

### Para o Professor

- `GUIA_DIA_DA_AULA.md` - Roteiro original (FAISS)
- `INSTRUCOES_PROFESSOR.md` - Detalhes tecnicos
- Este arquivo - Roteiro atualizado (TF-IDF)

---

## ✅ CHECKLIST FINAL DO PROFESSOR

**Antes da aula:**
- [ ] Testar `teste_funcoes_direto.py` funcionando
- [ ] Preparar slide "TF-IDF vs FAISS"
- [ ] Preparar slide "Paradoxo da Complexidade"
- [ ] Ollama rodando (ou API keys OpenRouter disponiveis)

**Durante a aula:**
- [ ] Justificar TF-IDF (max 3 min)
- [ ] Executar testes ao vivo
- [ ] Mostrar agente funcionando
- [ ] Discutir paradoxo da complexidade

**Depois da aula:**
- [ ] Compartilhar material complementar
- [ ] Coletar feedback dos alunos
- [ ] Responder duvidas no forum/grupo

---

**Roteiro atualizado por:** OpenCode AI  
**Data:** 23/07/2026  
**Versao:** 2.0 (TF-IDF)  
**Status:** Pronto para uso! ✅
