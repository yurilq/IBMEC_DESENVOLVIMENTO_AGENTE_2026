# Agente Investigador SINARM - E1: Anatomia do Agente

## Descrição do Projeto

Este repositório contém o código-fonte desenvolvido durante o **Encontro 1 (E1)** da disciplina **Desenvolvimento de Agentes** do curso de MBA. O objetivo é criar um agente investigador inteligente usando LangChain e Ollama para consultar datasets reais do SINARM (Sistema Nacional de Armas).

O agente implementa o padrão **ReAct (Reasoning + Acting)** de forma didática e simplificada, permitindo que os alunos compreendam:
- Ciclo ReAct manual (Thought → Action → Observation)
- Como estruturar chamadas a ferramentas (tools)
- Debug e logging em produção
- Tratamento de dados reais de segurança pública

---

## Estrutura do Projeto

```
03_CODIGOS_PRONTOS/
├── E1_agente_react_v3.py          # Agente principal com padrão ReAct
├── E1_tools_sinarm.py             # Ferramentas para consulta aos datasets
├── TESTES_COMPLETOS.py            # Suite de testes automatizados
├── agente_v1.8.py                 # Versão anterior (referência)
├── DADOS_SINARM/                  # Datasets SINARM organizados
│   ├── OCORRENCIAS/               # Furtos, apreensões, recuperações (4 arquivos CSV)
│   ├── PORTES/                    # Portes de armas (4 arquivos CSV)
│   ├── REGISTROS/                 # Registros de armas (9 arquivos CSV)
│   └── REQUERIMENTOS/             # Requerimentos de porte/registro (8 arquivos CSV)
├── logs/                          # Logs de execução do agente
└── __pycache__/                   # Cache Python (não versionado)
```

---

## Datasets SINARM

O projeto trabalha com **4 tipos de datasets** reais do SINARM:

### 1. OCORRÊNCIAS (74.758 registros)
- **Arquivos**: `OCORRENCIAS_2024.csv`, `OCORRENCIAS_2025.csv`, `OCORRENCIAS_2026.csv`, `OCORRENCIAS_ate_2023.csv`
- **Conteúdo**: Furtos, roubos, apreensões e recuperações de armas
- **Colunas principais**: data, tipo_ocorrencia, uf, cidade, arma, calibre

### 2. PORTES (2.328 registros)
- **Arquivos**: `PORTES_2024.csv`, `PORTES_2025.csv`, `PORTES_2026.csv`, `PORTE_ate_2023.csv`
- **Conteúdo**: Autorizações de porte de arma
- **Colunas principais**: status, data_validade, uf, categoria

### 3. REGISTROS (12.798 registros)
- **Arquivos**: 9 arquivos CSV cobrindo período 1965-2026
- **Conteúdo**: Registros de armas para defesa pessoal
- **Colunas principais**: ano_registro, uf, categoria, arma, calibre

### 4. REQUERIMENTOS (46.116 registros)
- **Arquivos**: 8 arquivos CSV cobrindo período 2019-2026
- **Conteúdo**: Solicitações de porte e registro
- **Colunas principais**: data_requerimento, tipo, status, uf

---

## Pré-requisitos

### 1. Python 3.8+
Verifique sua versão:
```bash
python --version
```

### 2. Ollama Instalado
O agente utiliza modelos locais via Ollama. Instale seguindo as instruções em:
- **Site oficial**: https://ollama.ai
- **Instalação Windows**: Baixe o instalador e execute
- **Instalação Linux/Mac**: Use o comando oficial

Após instalar, baixe o modelo recomendado:
```bash
ollama pull llama3
```

### 3. Git (opcional, mas recomendado)
Para clonar e versionar o código:
```bash
git --version
```

---

## Instalação

### Passo 1: Clone o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd 03_CODIGOS_PRONTOS
```

### Passo 2: Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as dependências
```bash
pip install -r requirements.txt
```

---

## Como Usar

### 1. Execute o Agente Principal
```bash
python E1_agente_react_v3.py
```

### 2. Exemplos de Consultas

O agente aceita perguntas em linguagem natural:

**Exemplo 1 - Ocorrências por UF:**
```
Pergunta: Quantos furtos de arma ocorreram no Rio de Janeiro em 2024?
```

**Exemplo 2 - Análise de Portes:**
```
Pergunta: Quais estados têm mais portes de arma vigentes?
```

**Exemplo 3 - Investigação de Registros:**
```
Pergunta: Qual o calibre de arma mais registrado em São Paulo?
```

**Exemplo 4 - Análise Temporal:**
```
Pergunta: Houve aumento nos requerimentos de porte entre 2023 e 2024?
```

### 3. Execute os Testes
```bash
python TESTES_COMPLETOS.py
```

---

## Arquitetura do Agente

### Padrão ReAct Implementado

O agente segue o ciclo **ReAct (Reason + Act)**:

```
1. THOUGHT (Pensamento)
   └─> Agente analisa a pergunta e decide qual ferramenta usar

2. ACTION (Ação)
   └─> Agente executa a ferramenta escolhida com os parâmetros corretos

3. OBSERVATION (Observação)
   └─> Agente recebe o resultado e decide se precisa de mais ações

4. FINAL ANSWER (Resposta Final)
   └─> Agente formula a resposta baseada nas observações
```

### Ferramentas Disponíveis

O arquivo `E1_tools_sinarm.py` implementa 4 ferramentas principais:

| Ferramenta | Descrição | Dataset |
|------------|-----------|---------|
| `buscar_ocorrencias()` | Busca furtos, roubos e apreensões | OCORRENCIAS |
| `buscar_portes()` | Consulta portes de arma vigentes | PORTES |
| `buscar_registros()` | Busca registros de armas | REGISTROS |
| `buscar_requerimentos()` | Consulta requerimentos | REQUERIMENTOS |

**Recursos das ferramentas:**
- Cache LRU para performance
- Validação rigorosa de input
- Logging para auditoria
- Tratamento de erros robusto
- Output estruturado em JSON
- Conformidade LGPD (sem dados pessoais sensíveis)

---

## Logs e Debugging

O agente gera logs detalhados em `logs/`:

```
logs/
├── agente_YYYYMMDD_HHMMSS.log    # Log principal do agente
└── tools_YYYYMMDD_HHMMSS.log     # Log das ferramentas
```

**Níveis de log:**
- `INFO`: Operações normais
- `DEBUG`: Detalhes técnicos
- `WARNING`: Situações inesperadas (não críticas)
- `ERROR`: Erros que afetam a execução

---

## Troubleshooting

### Problema 1: Ollama não encontrado
```
Erro: Ollama model not found
```
**Solução:**
1. Verifique se o Ollama está instalado: `ollama --version`
2. Baixe o modelo: `ollama pull llama3`
3. Verifique se o serviço está rodando

### Problema 2: Erro de encoding (Windows)
```
Erro: UnicodeEncodeError
```
**Solução:**
O código já trata encoding UTF-8, mas se persistir:
```bash
set PYTHONIOENCODING=utf-8
python E1_agente_react_v3.py
```

### Problema 3: Arquivos CSV não encontrados
```
Erro: FileNotFoundError: [Errno 2] No such file or directory
```
**Solução:**
Verifique se a pasta `DADOS_SINARM/` está no mesmo diretório dos scripts Python.

### Problema 4: Dependências não instaladas
```
Erro: ModuleNotFoundError: No module named 'langchain'
```
**Solução:**
```bash
pip install -r requirements.txt
```

---

## Recursos de Aprendizado

### Para os Alunos

Este projeto foi desenvolvido com propósito educacional. Recomendamos:

1. **Leia o código comentado**: Todos os scripts têm comentários detalhados
2. **Execute passo a passo**: Use breakpoints para entender o fluxo
3. **Modifique e experimente**: Crie novas ferramentas e consultas
4. **Analise os logs**: Entenda como o agente toma decisões

### Conceitos Abordados

- **LangChain**: Framework para desenvolvimento de agentes LLM
- **Ollama**: Execução local de modelos de linguagem
- **ReAct Pattern**: Padrão de raciocínio e ação
- **Tool Calling**: Chamada de funções externas pelo agente
- **Data Analysis**: Análise de dados reais com Pandas
- **Logging e Debugging**: Boas práticas de desenvolvimento
- **LGPD**: Conformidade com lei de proteção de dados

---

## Próximos Passos

Este é o código do **Encontro 1 (E1)**. Nos próximos encontros, você irá:

- **E2**: Adicionar memória e contexto ao agente
- **E3**: Implementar RAG (Retrieval-Augmented Generation)
- **E4**: Criar interface web para o agente
- **E5**: Deploy e produção do agente
- **E6**: Multi-agentes e orquestração
- **E7**: Projeto final integrado

---

## Contribuindo

Este é um projeto educacional. Se você é aluno e encontrou melhorias:

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/minha-melhoria`
3. Commit suas mudanças: `git commit -m 'Adiciona melhoria X'`
4. Push para a branch: `git push origin feature/minha-melhoria`
5. Abra um Pull Request

---

## Licença

Este projeto é de uso educacional para o curso de MBA em Desenvolvimento de Agentes.

---

## Contato e Suporte

- **Dúvidas técnicas**: Abra uma issue no GitHub
- **Discussões**: Use a aba Discussions do repositório
- **Professor responsável**: [Adicionar informações de contato]

---

## Changelog

### v3.0 (Atual)
- Implementação do padrão ReAct manual
- 4 ferramentas SINARM funcionais
- Suporte completo a Ollama
- Logging e debugging melhorados
- Suite de testes automatizados

### v1.8 (Anterior)
- Versão inicial com create_agent()
- Limitações com Ollama

---

**Desenvolvido para o curso de MBA - Disciplina: Desenvolvimento de Agentes**

**Encontro 1: Anatomia do Agente**
