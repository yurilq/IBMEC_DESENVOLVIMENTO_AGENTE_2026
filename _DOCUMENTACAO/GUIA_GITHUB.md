# GUIA: Como Criar o Repositório no GitHub

Este guia mostra o passo a passo para publicar o projeto no GitHub e compartilhar com os alunos.

---

## Opção 1: Usando a Interface Web do GitHub (Recomendado para Iniciantes)

### Passo 1: Criar o Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha os campos:
   - **Repository name**: `agente-investigador-sinarm-e1`
   - **Description**: `Agente Investigador com LangChain + Ollama - E1: Anatomia do Agente`
   - **Visibilidade**: 
     - ✅ **Public** (para compartilhar com alunos)
     - ⚠️ **Private** (se quiser controlar acesso)
   - **NÃO** marque as opções:
     - ❌ Add a README file (já temos)
     - ❌ Add .gitignore (já temos)
     - ❌ Choose a license
5. Clique em **"Create repository"**

### Passo 2: Conectar Repositório Local ao GitHub

Após criar o repositório, o GitHub mostra instruções. Use estas:

**No terminal/PowerShell, dentro da pasta do projeto:**

```bash
# Navegar até a pasta do projeto
cd "E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS"

# Adicionar o remote (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1.git

# Verificar se o remote foi adicionado
git remote -v

# Fazer push do código
git branch -M main
git push -u origin main
```

**Exemplo real:**
```bash
# Se seu usuário for "professorjohn"
git remote add origin https://github.com/professorjohn/agente-investigador-sinarm-e1.git
git branch -M main
git push -u origin main
```

### Passo 3: Verificar Upload

1. Recarregue a página do repositório no GitHub
2. Você deve ver todos os arquivos:
   - README.md
   - requirements.txt
   - .gitignore
   - E1_agente_react_v3.py
   - E1_tools_sinarm.py
   - TESTES_COMPLETOS.py
   - DADOS_SINARM/ (pasta com CSVs)

---

## Opção 2: Usando GitHub CLI (gh) - Mais Rápido

Se você tem o GitHub CLI instalado:

```bash
# Navegar até a pasta do projeto
cd "E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS"

# Criar repositório e fazer push em um comando
gh repo create agente-investigador-sinarm-e1 --public --source=. --push

# Ou se preferir privado
gh repo create agente-investigador-sinarm-e1 --private --source=. --push
```

---

## Opção 3: Usando GitHub Desktop (Interface Gráfica)

1. Baixe e instale [GitHub Desktop](https://desktop.github.com/)
2. Faça login com sua conta GitHub
3. Clique em **"File" → "Add local repository"**
4. Selecione a pasta: `E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS`
5. Clique em **"Publish repository"**
6. Escolha:
   - Nome: `agente-investigador-sinarm-e1`
   - Descrição: `Agente Investigador com LangChain + Ollama - E1: Anatomia do Agente`
   - ✅ ou ❌ Keep this code private
7. Clique em **"Publish Repository"**

---

## Compartilhando com os Alunos

### 1. URL do Repositório

Após criar, você terá uma URL como:
```
https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1
```

**Compartilhe essa URL com os alunos via:**
- Email
- Sistema LMS da faculdade
- Grupo de WhatsApp/Telegram
- Apresentação de slides

### 2. Instruções para os Alunos Clonarem

Crie um arquivo ou mensagem com estas instruções:

```markdown
## Como Baixar o Projeto

### Opção 1: Via Git Clone (Recomendado)

1. Abra o terminal/PowerShell
2. Navegue até a pasta onde quer salvar o projeto
3. Execute:

```bash
git clone https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1.git
cd agente-investigador-sinarm-e1
```

### Opção 2: Download ZIP

1. Acesse: https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1
2. Clique no botão verde **"Code"**
3. Selecione **"Download ZIP"**
4. Extraia o arquivo ZIP
5. Abra a pasta no terminal

### Após Baixar

Siga as instruções do README.md para:
1. Criar ambiente virtual
2. Instalar dependências
3. Configurar Ollama
4. Executar o agente
```

### 3. Criar Releases (Opcional)

Para versões específicas do curso:

1. No GitHub, vá em **"Releases"**
2. Clique em **"Create a new release"**
3. Preencha:
   - **Tag**: `v1.0-E1` (ou `encontro-1`)
   - **Release title**: `E1 - Anatomia do Agente`
   - **Description**:
     ```
     Versão inicial do agente investigador SINARM
     
     ## Conteúdo
     - Agente ReAct com LangChain + Ollama
     - 4 ferramentas de consulta SINARM
     - Datasets completos
     - Testes automatizados
     
     ## Para usar
     Siga as instruções do README.md
     ```
4. Clique em **"Publish release"**

Os alunos podem então baixar a versão específica de cada encontro.

---

## Atualizações Futuras

### Quando Adicionar Novos Encontros (E2, E3, etc.)

```bash
# Navegar até a pasta do projeto
cd "E:\documentos\ibmec\MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E1_ANATOMIA_DO_AGENTE\03_CODIGOS_PRONTOS"

# Ver o que mudou
git status

# Adicionar as mudanças
git add .

# Commit descritivo
git commit -m "E2: Adiciona memória e contexto ao agente

- Implementa ConversationBufferMemory
- Adiciona histórico de conversas
- Atualiza README com novos conceitos"

# Enviar para o GitHub
git push origin main
```

### Criar Branch para Cada Encontro (Alternativa)

Se quiser manter versões separadas:

```bash
# Criar branch para E2
git checkout -b encontro-2

# Fazer mudanças...

# Commit
git add .
git commit -m "E2: Implementação completa"

# Push da nova branch
git push origin encontro-2
```

Então os alunos podem escolher qual encontro baixar:
```bash
# Baixar encontro específico
git clone -b encontro-2 https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1.git
```

---

## Configurações Recomendadas do Repositório

### 1. Adicionar Topics (Tags)

No GitHub, adicione topics para facilitar descoberta:
- `langchain`
- `ollama`
- `agents`
- `react-pattern`
- `education`
- `python`
- `sinarm`
- `mba`

### 2. Configurar Branch Protection (Opcional)

Se for trabalhar com assistentes/monitores:

1. Vá em **Settings → Branches**
2. Clique em **"Add branch protection rule"**
3. Branch name pattern: `main`
4. Marque:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass

### 3. Adicionar Licença (Opcional)

Para uso educacional, considere:
- MIT License (mais permissiva)
- Apache 2.0 License
- Educational use only (custom)

1. Vá em **Add file → Create new file**
2. Nome: `LICENSE`
3. Clique em **"Choose a license template"**
4. Selecione uma licença
5. Commit

---

## Troubleshooting

### Erro: Permission Denied

```bash
# Configure suas credenciais
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

# Use token em vez de senha
# Gere em: Settings → Developer settings → Personal access tokens
```

### Erro: Remote Already Exists

```bash
# Remover remote antigo
git remote remove origin

# Adicionar novamente
git remote add origin https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1.git
```

### Repositório Muito Grande

Se der erro de tamanho:

1. Verifique tamanho dos CSVs
2. Considere usar Git LFS para arquivos grandes:

```bash
# Instalar Git LFS
git lfs install

# Rastrear CSVs grandes
git lfs track "*.csv"

# Commit e push
git add .gitattributes
git commit -m "Adiciona Git LFS"
git push origin main
```

---

## Checklist Final

Antes de compartilhar com os alunos:

- [ ] README.md está completo e claro
- [ ] requirements.txt lista todas as dependências
- [ ] .gitignore está configurado corretamente
- [ ] Código está comentado e documentado
- [ ] Testes estão funcionando
- [ ] Instruções de instalação estão testadas
- [ ] Dados sensíveis foram removidos (senhas, tokens, etc.)
- [ ] Repositório está público (ou alunos têm acesso)
- [ ] URL do repositório foi compartilhada

---

## Suporte Contínuo

### Issues

Instrua os alunos a usarem Issues para:
- Reportar bugs
- Fazer perguntas técnicas
- Sugerir melhorias

### Discussions

Ative Discussions para:
- Dúvidas gerais
- Compartilhamento de projetos
- Discussões sobre conceitos

1. Vá em **Settings**
2. Marque ✅ **Discussions**
3. Crie categorias:
   - Anúncios
   - Dúvidas
   - Projetos dos Alunos
   - Encontro 1, 2, 3...

---

**Pronto! Seu repositório está configurado e pronto para os alunos.**

**URL para compartilhar:** `https://github.com/SEU_USUARIO/agente-investigador-sinarm-e1`
