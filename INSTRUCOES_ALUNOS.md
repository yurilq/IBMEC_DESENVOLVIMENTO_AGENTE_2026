# REPOSITÓRIO GITHUB - AGENTE INVESTIGADOR SINARM

## REPOSITÓRIO PUBLICADO COM SUCESSO!

---

## URL do Repositório

**GitHub:** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026

**Clone SSH:** `git@github.com:yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git`

**Clone HTTPS:** `https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git`

---

## INSTRUÇÕES PARA OS ALUNOS

Copie e envie estas instruções para seus alunos via email, LMS ou WhatsApp:

---

### Como Baixar o Projeto do Curso

Olá, alunos!

O código do **E1 - Anatomia do Agente** está disponível no GitHub. Sigam as instruções abaixo para baixar e configurar:

#### Opção 1: Git Clone (Recomendado)

```bash
# 1. Abra o terminal/PowerShell
# 2. Navegue até a pasta onde quer salvar o projeto
cd C:\Users\SeuUsuario\Documents

# 3. Clone o repositório
git clone https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git

# 4. Entre na pasta
cd IBMEC_DESENVOLVIMENTO_AGENTE_2026
```

#### Opção 2: Download ZIP

1. Acesse: https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026
2. Clique no botão verde **"Code"**
3. Selecione **"Download ZIP"**
4. Extraia o arquivo ZIP na pasta desejada
5. Abra a pasta no terminal

---

### Configuração do Ambiente

Após baixar o projeto:

#### 1. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 3. Instalar e Configurar Ollama

1. Baixe o Ollama em: https://ollama.ai
2. Instale seguindo as instruções
3. Baixe o modelo:

```bash
ollama pull llama3
```

#### 4. Executar o Agente

```bash
python E1_agente_react_v3.py
```

---

### Estrutura do Projeto

```
IBMEC_DESENVOLVIMENTO_AGENTE_2026/
├── README.md                      # Leia primeiro!
├── GUIA_GITHUB.md                 # Guia completo do GitHub
├── requirements.txt               # Dependências
├── E1_agente_react_v3.py          # Agente principal
├── E1_tools_sinarm.py             # Ferramentas
├── TESTES_COMPLETOS.py            # Testes automatizados
└── DADOS_SINARM/                  # Datasets (26 CSVs)
    ├── OCORRENCIAS/
    ├── PORTES/
    ├── REGISTROS/
    └── REQUERIMENTOS/
```

---

### Exemplos de Uso

Após executar o agente, você pode fazer perguntas como:

```
Pergunta: Quantos furtos de arma ocorreram no Rio de Janeiro em 2024?
Pergunta: Quais estados têm mais portes de arma vigentes?
Pergunta: Qual o calibre de arma mais registrado em São Paulo?
Pergunta: Houve aumento nos requerimentos entre 2023 e 2024?
```

---

### Suporte e Dúvidas

- **Repositório GitHub:** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026
- **Issues (Bugs/Dúvidas):** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026/issues
- **README Completo:** Leia o README.md no repositório

---

### Atualizações Futuras

Durante o curso, o repositório será atualizado com novos encontros (E2, E3, etc.).

Para baixar atualizações:

```bash
# Navegue até a pasta do projeto
cd caminho/para/IBMEC_DESENVOLVIMENTO_AGENTE_2026

# Baixe as atualizações
git pull origin main
```

---

**Bons estudos!**

**Professor(a): [Seu Nome]**
**Curso: MBA - Desenvolvimento de Agentes**
**Disciplina: E1 - Anatomia do Agente**

---

## MENSAGEM CURTA PARA WHATSAPP/TELEGRAM

Copie e cole:

```
🚀 Código do E1 - Anatomia do Agente disponível!

GitHub: https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026

📥 Como baixar:
git clone https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026.git

Ou baixe o ZIP direto do GitHub.

📖 Leia o README.md com todas as instruções!

Qualquer dúvida, abra uma Issue no GitHub.
```

---

## SLIDE PARA APRESENTAÇÃO

Use este texto em um slide:

```
REPOSITÓRIO DO CURSO

GitHub: github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026

COMO USAR:
1. Clone ou baixe o ZIP
2. Crie ambiente virtual
3. pip install -r requirements.txt
4. Instale Ollama
5. python E1_agente_react_v3.py

LEIA O README.md!
```

---

## VERIFICAÇÃO

Status do repositório:

✅ Publicado no GitHub
✅ Branch main configurada
✅ 3 commits enviados
✅ 33 arquivos versionados
✅ README.md completo
✅ GUIA_GITHUB.md disponível
✅ requirements.txt incluído
✅ Datasets SINARM completos

---

## PRÓXIMOS PASSOS

### Para Você (Professor)

1. **Configure o repositório no GitHub:**
   - Adicione descrição
   - Adicione topics: `langchain`, `ollama`, `agents`, `python`, `education`, `mba`
   - Configure branch protection (opcional)
   - Ative Discussions (opcional)

2. **Compartilhe com os alunos:**
   - Envie as instruções acima
   - Disponibilize no LMS
   - Apresente na aula

3. **Para futuros encontros (E2, E3, etc.):**
   ```bash
   # Fazer alterações...
   git add .
   git commit -m "E2: Adiciona memória ao agente"
   git push origin main
   ```

### Para Atualizações

Quando adicionar conteúdo dos próximos encontros:

```bash
cd "E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS"

# Ver mudanças
git status

# Adicionar mudanças
git add .

# Commit descritivo
git commit -m "E2: Implementa memória e contexto

- Adiciona ConversationBufferMemory
- Implementa histórico de conversas
- Atualiza README com novos conceitos"

# Push para GitHub
git push origin main
```

---

## COMANDOS ÚTEIS

### Ver histórico:
```bash
git log --oneline
```

### Ver status:
```bash
git status
```

### Baixar atualizações:
```bash
git pull origin main
```

### Criar branch para encontro específico:
```bash
git checkout -b encontro-2
# fazer mudanças...
git push origin encontro-2
```

---

**REPOSITÓRIO PRONTO E FUNCIONANDO!**

**URL:** https://github.com/yurilq/IBMEC_DESENVOLVIMENTO_AGENTE_2026

**Use durante todo o curso 2026!**
