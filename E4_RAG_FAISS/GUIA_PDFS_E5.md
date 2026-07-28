# 📚 GUIA: PDFs para E5 - Especialização PCDF

**Data:** 26/07/2026  
**Objetivo:** Orientar busca e uso de PDFs para o Encontro 5

---

## 🎯 CONTEXTO DO E5

### Tema
**Especialização de Agentes com PDFs Reais**

### Objetivos
- RAG especializado para domínio PCDF
- Fine-tuning LoRA
- Multimodal (análise de imagens)
- Reranking para melhorar precisão

### Tipos de PDFs Necessários

**1. Documentos Legais**
- Portarias da PCDF
- Leis e decretos
- Resoluções
- Instruções normativas

**2. Manuais Operacionais**
- Procedimentos policiais
- Protocolos de atendimento
- Guias técnicos
- Manuais de equipamentos

**3. Documentos Técnicos**
- Laudos periciais (anonimizados)
- Relatórios técnicos
- Estudos de caso
- Análises estatísticas

---

## 🔍 FONTES DE PDFs PÚBLICOS

### 1. Site da PCDF

**URL:** https://www.pcdf.df.gov.br/

**Seções Relevantes:**

**a) Manuais e Protocolos**
- URL: https://www.pcdf.df.gov.br/informacoes/manuais-e-protocolos
- Encontrado: Manual de Depoimento Especial de Crianças e Adolescentes
- Status: ✅ Disponível para download

**b) Base Jurídica**
- URL: https://www.pcdf.df.gov.br/institucional/base-juridica
- Conteúdo: Leis, decretos, portarias
- Status: ⏳ Verificar disponibilidade

**c) Cartilhas e Folders**
- URL: https://www.pcdf.df.gov.br/imprensa/cartilhas-e-folders
- Conteúdo: Material educativo
- Status: ⏳ Verificar disponibilidade

### 2. Diário Oficial do DF

**URL:** https://www.dodf.df.gov.br/

**Conteúdo:**
- Portarias da PCDF
- Nomeações e exonerações
- Atos administrativos
- Licitações e contratos

**Como buscar:**
```
Site: https://www.dodf.df.gov.br/
Buscar: "PCDF" ou "Polícia Civil"
Filtrar: Por data, tipo de ato
```

### 3. Legislação Federal

**a) Planalto**
- URL: https://www.planalto.gov.br/ccivil_03/leis/leis_2001.htm
- Leis relevantes:
  - Lei 10.826/2003 (Estatuto do Desarmamento)
  - Lei 12.830/2013 (Investigação Criminal)
  - Lei 13.869/2019 (Abuso de Autoridade)

**b) Senado Federal**
- URL: https://www12.senado.leg.br/
- Legislação consolidada
- Projetos de lei

### 4. Repositórios Acadêmicos

**a) Scielo**
- URL: https://www.scielo.br/
- Buscar: "polícia civil", "investigação criminal", "perícia"
- Artigos científicos em PDF

**b) Google Scholar**
- URL: https://scholar.google.com.br/
- Buscar: "PCDF", "polícia científica", "criminalística"
- Teses e dissertações

### 5. Órgãos Relacionados

**a) Polícia Federal**
- URL: https://www.gov.br/pf/
- Manuais técnicos
- Cartilhas educativas

**b) SENASP**
- URL: https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica
- Manuais de procedimentos
- Protocolos nacionais

**c) Ministério da Justiça**
- URL: https://www.gov.br/mj/
- Legislação
- Políticas públicas

---

## 📋 LISTA DE PDFs RECOMENDADOS

### Prioridade ALTA (Essenciais)

**1. Estatuto do Desarmamento**
- Nome: Lei 10.826/2003
- URL: https://www.planalto.gov.br/ccivil_03/leis/2003/l10.826.htm
- Tamanho: ~50 páginas
- Uso: RAG especializado em armamento

**2. Código de Processo Penal**
- Nome: Decreto-Lei 3.689/1941
- URL: https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm
- Tamanho: ~200 páginas
- Uso: Procedimentos policiais

**3. Lei de Investigação Criminal**
- Nome: Lei 12.830/2013
- URL: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12830.htm
- Tamanho: ~5 páginas
- Uso: Atribuições do delegado

**4. Lei de Abuso de Autoridade**
- Nome: Lei 13.869/2019
- URL: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13869.htm
- Tamanho: ~15 páginas
- Uso: Limites da atuação policial

**5. Manual PCDF (se disponível)**
- Nome: Manual de Depoimento Especial
- URL: Site PCDF
- Tamanho: ~50 páginas
- Uso: Procedimentos específicos PCDF

### Prioridade MÉDIA (Importantes)

**6. Portarias PCDF**
- Fonte: Diário Oficial DF
- Buscar: Últimos 2 anos
- Uso: Normas internas

**7. Cartilhas Educativas**
- Fonte: Site PCDF
- Temas: Prevenção, segurança
- Uso: Linguagem acessível

**8. Artigos Científicos**
- Fonte: Scielo, Google Scholar
- Temas: Criminalística, perícia
- Uso: Conhecimento técnico

### Prioridade BAIXA (Complementares)

**9. Relatórios Estatísticos**
- Fonte: PCDF, SENASP
- Dados: Criminalidade, apreensões
- Uso: Análise de dados

**10. Manuais de Equipamentos**
- Fonte: Fabricantes
- Temas: Armas, equipamentos
- Uso: Especificações técnicas

---

## 🛠️ COMO PREPARAR OS PDFs

### 1. Download

```bash
# Criar pasta
mkdir -p E5_ESPECIALIZACAO_PDFs/01_DADOS/pdfs_pcdf

# Baixar PDFs
# (manual ou script)
```

### 2. Organização

```
pdfs_pcdf/
├── leis/
│   ├── estatuto_desarmamento.pdf
│   ├── codigo_processo_penal.pdf
│   └── lei_investigacao_criminal.pdf
├── manuais/
│   ├── manual_depoimento_especial.pdf
│   └── protocolo_atendimento.pdf
├── portarias/
│   ├── portaria_2023_001.pdf
│   └── portaria_2024_015.pdf
└── cartilhas/
    ├── prevencao_crimes.pdf
    └── seguranca_publica.pdf
```

### 3. Validação

**Checklist:**
- [ ] PDF é legível (não é imagem escaneada)
- [ ] Texto é extraível (não precisa OCR)
- [ ] Tamanho razoável (< 50 MB)
- [ ] Conteúdo relevante para PCDF
- [ ] Sem dados pessoais (LGPD)

### 4. Processamento

```python
# Extrair texto
from PyPDF2 import PdfReader

reader = PdfReader("documento.pdf")
texto = ""
for page in reader.pages:
    texto += page.extract_text()

# Salvar texto
with open("documento.txt", "w", encoding="utf-8") as f:
    f.write(texto)
```

---

## ⚠️ CUIDADOS IMPORTANTES

### LGPD (Lei Geral de Proteção de Dados)

**NÃO incluir:**
- ❌ Nomes de vítimas
- ❌ Nomes de suspeitos
- ❌ CPF, RG, endereços
- ❌ Fotos de pessoas
- ❌ Dados sensíveis

**Anonimizar:**
- ✅ Substituir nomes por "PESSOA A", "PESSOA B"
- ✅ Remover números de documentos
- ✅ Ocultar endereços específicos
- ✅ Generalizar datas (mês/ano apenas)

### Direitos Autorais

**Usar apenas:**
- ✅ Documentos públicos (leis, portarias)
- ✅ Material educativo oficial
- ✅ Artigos com licença aberta
- ✅ Conteúdo próprio da PCDF

**Evitar:**
- ❌ Livros comerciais
- ❌ Artigos pagos
- ❌ Material protegido

### Segurança

**Verificar:**
- ✅ PDF não contém malware
- ✅ Fonte confiável
- ✅ Não é documento sigiloso
- ✅ Pode ser usado em treinamento

---

## 🎓 USO NO E5

### Terça (RAG + Reranking)

**Atividade 1: Criar índice FAISS**
```python
# Carregar PDFs
pdfs = load_pdfs("pdfs_pcdf/")

# Extrair texto
textos = [extract_text(pdf) for pdf in pdfs]

# Criar chunks
chunks = chunk_texts(textos, chunk_size=500)

# Gerar embeddings
embeddings = model.encode(chunks)

# Criar índice FAISS
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
```

**Atividade 2: Implementar reranking**
```python
# Busca inicial (top-20)
docs_iniciais = index.search(query, k=20)

# Reranking (top-5)
docs_finais = rerank(query, docs_iniciais, k=5)
```

### Quinta (Fine-tuning LoRA)

**Atividade 1: Preparar dataset**
```python
# Criar pares pergunta-resposta
dataset = []
for pdf in pdfs:
    texto = extract_text(pdf)
    perguntas = generate_questions(texto)
    respostas = extract_answers(texto, perguntas)
    dataset.extend(zip(perguntas, respostas))
```

**Atividade 2: Fine-tunar modelo**
```python
# Configurar LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
)

# Treinar
trainer.train()
```

---

## 📊 MÉTRICAS DE QUALIDADE

### RAG

**Precision@K**
- Top-3: 80%+
- Top-5: 90%+

**MRR (Mean Reciprocal Rank)**
- Objetivo: 0.7+

**Relevância**
- Documentos relevantes: 90%+

### Fine-tuning

**Perplexity**
- Objetivo: < 10

**BLEU Score**
- Objetivo: > 0.5

**Human Evaluation**
- Coerência: 4/5+
- Relevância: 4/5+

---

## 🚀 PRÓXIMOS PASSOS

### Imediato
1. ⏳ Baixar PDFs prioritários (leis, manuais)
2. ⏳ Organizar em pastas
3. ⏳ Validar qualidade
4. ⏳ Testar extração de texto

### Médio Prazo
5. ⏳ Criar dataset de perguntas-respostas
6. ⏳ Implementar pipeline de processamento
7. ⏳ Testar RAG com PDFs
8. ⏳ Avaliar métricas

### Longo Prazo
9. ⏳ Expandir base de PDFs
10. ⏳ Melhorar qualidade do dataset
11. ⏳ Fine-tunar modelo especializado
12. ⏳ Deploy em produção

---

## 📝 TEMPLATE DE BUSCA

### Script Python para Buscar PDFs

```python
"""
Script para buscar e baixar PDFs relevantes para E5
"""

import requests
from bs4 import BeautifulSoup
import os

# URLs para buscar
urls = [
    "https://www.pcdf.df.gov.br/informacoes/manuais-e-protocolos",
    "https://www.pcdf.df.gov.br/imprensa/cartilhas-e-folders",
    # Adicionar mais URLs
]

# Pasta de destino
output_dir = "pdfs_pcdf"
os.makedirs(output_dir, exist_ok=True)

# Buscar PDFs
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar links de PDFs
    pdf_links = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))
    
    for link in pdf_links:
        pdf_url = link['href']
        pdf_name = pdf_url.split('/')[-1]
        
        # Baixar PDF
        pdf_response = requests.get(pdf_url)
        with open(f"{output_dir}/{pdf_name}", 'wb') as f:
            f.write(pdf_response.content)
        
        print(f"✅ Baixado: {pdf_name}")

print(f"\n✅ Total: {len(os.listdir(output_dir))} PDFs baixados")
```

---

## ✅ CHECKLIST FINAL

### Antes da Aula
- [ ] PDFs baixados e organizados
- [ ] Texto extraído e validado
- [ ] Dataset criado (se fine-tuning)
- [ ] Índice FAISS criado
- [ ] Métricas calculadas

### Durante a Aula
- [ ] Demonstrar busca em PDFs
- [ ] Mostrar reranking funcionando
- [ ] Testar fine-tuning (se tempo)
- [ ] Avaliar resultados

### Depois da Aula
- [ ] Coletar feedback
- [ ] Melhorar dataset
- [ ] Expandir base de PDFs
- [ ] Documentar lições aprendidas

---

**Status:** ⏳ AGUARDANDO DOWNLOAD DE PDFs

**Próximo passo:** Baixar PDFs prioritários e validar qualidade
