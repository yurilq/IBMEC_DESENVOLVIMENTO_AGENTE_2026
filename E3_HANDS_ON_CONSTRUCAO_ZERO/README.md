# E3 - Construção do Agente SINARM do Zero

**MBA IA Generativa PCDF - IBMEC**  
**Encontro 3:** Hands-On - Construção Incremental

---

## 🎯 Objetivos

- Construir ferramentas especializadas com `@tool` decorator
- Implementar cache de dados com `@lru_cache`
- Criar roteador inteligente para análise de perguntas
- Adicionar validação de segurança
- Desenvolver modo interativo funcional

---

## 📁 Estrutura

```
E3_HANDS_ON_CONSTRUCAO_ZERO/
├── 01_GUIAS_ALUNO/              # Material de apoio
├── 02_NOTEBOOK_PASSO_A_PASSO/   # Implementação incremental ⭐
│   ├── E3_construcao_agente_sinarm_v2.ipynb
│   └── scripts_auxiliares/
├── 03_AGENTE_CONSOLIDADO/       # Arquivo .py final ⭐
│   ├── agente_sinarm_v2_completo.py
│   └── testes/
└── DADOS_SINARM/                # Dados para testes
```

---

## 🚀 Como Usar

### Opção 1: Notebook (Didático)

**Melhor para:** Aprender passo a passo

```bash
cd 02_NOTEBOOK_PASSO_A_PASSO
jupyter notebook E3_construcao_agente_sinarm_v2.ipynb
```

**Passos:**
1. Kernel → Restart & Clear Output
2. Cell → Run All
3. Testar modo interativo (última célula)

---

### Opção 2: Arquivo .py (Produção)

**Melhor para:** Usar o agente pronto

```bash
cd 03_AGENTE_CONSOLIDADO
```

#### Modo 1: Testes Automáticos (Padrão)
```bash
python agente_sinarm_v2_completo.py
```
Executa 9 testes automaticamente e mostra relatório.

#### Modo 2: Pergunta Única
```bash
python agente_sinarm_v2_completo.py "Quantas armas Taurus?"
```
Responde a pergunta e encerra.

#### Modo 3: Modo Interativo
```bash
python agente_sinarm_v2_completo.py --interativo
```
Inicia loop de perguntas. Digite `sair` para encerrar.

#### Modo 4: Ajuda
```bash
python agente_sinarm_v2_completo.py --help
```
Mostra todas as opções disponíveis.

---

## 🛠️ Funcionalidades

### Tools Básicas (4)

1. **contar_armas_marca** - Conta armas por marca específica
   ```
   Exemplo: "Quantas armas Taurus?"
   Resposta: Encontrei 30 armas da marca 'TAURUS'
   ```

2. **contar_armas_calibre** - Conta armas por calibre
   ```
   Exemplo: "Quantas armas calibre 9mm?"
   Resposta: Encontrei 50 armas calibre '9mm'
   ```

3. **contar_armas_tipo** - Conta por tipo de ocorrência
   ```
   Exemplo: "Quantas armas foram roubadas?"
   Resposta: Encontrei 43 ocorrências tipo 'ROUBO'
   ```

4. **contar_armas_combinado** - Conta marca + tipo
   ```
   Exemplo: "Quantas armas Glock foram roubadas?"
   Resposta: Encontrei 15 armas 'GLOCK' tipo 'ROUBO'
   ```

### Tools Avançadas (4)

5. **ranking_marcas** - TOP 5 marcas mais registradas
   ```
   Exemplo: "Qual marca tem mais registros?"
   Resposta:
   TOP 5 MARCAS MAIS REGISTRADAS:
     1º - TAURUS: 30 armas
     2º - GLOCK: 25 armas
     3º - BERETTA: 20 armas
     4º - IMBEL: 15 armas
     5º - ROSSI: 12 armas
   ```

6. **ranking_calibres** - TOP 5 calibres mais comuns
   ```
   Exemplo: "Top 5 calibres"
   Resposta:
   TOP 5 CALIBRES MAIS COMUNS:
     1º - 9mm: 50 armas
     2º - .38: 33 armas
     3º - .40: 22 armas
     4º - .357: 7 armas
     5º - .380: 6 armas
   ```

7. **estatisticas_gerais** - Resumo completo do banco
   ```
   Exemplo: "Resumo dos dados"
   Resposta:
   ESTATISTICAS GERAIS DO SINARM:
   TOTAIS:
     - Registros: 120
     - Marcas diferentes: 7
     - Calibres diferentes: 6
   MAIS COMUNS:
     - Marca: TAURUS
     - Calibre: 9mm
     - Tipo: FURTO
   ```

8. **distribuicao_marca_por_tipo** - Distribuição com percentuais
   ```
   Exemplo: "Beretta em ocorrencias"
   Resposta:
   DISTRIBUICAO DE BERETTA POR TIPO:
     Total: 20 armas
     - APREENSAO: 10 armas (50.0%)
     - FURTO: 7 armas (35.0%)
     - ROUBO: 3 armas (15.0%)
   ```

---

## ✨ Recursos Especiais

### Busca Inteligente
- Aceita variações de digitação: `taurus`, `tauros`, `tauru`
- Busca parcial com `.str.contains()`
- Resolve erros automaticamente

### Roteador Expandido
- 5 prioridades de detecção
- Suporte a 8 tools diferentes
- Mensagens de erro educativas

### Validação de Segurança
- Bloqueia queries muito longas (>500 chars)
- Bloqueia queries muito curtas (<3 chars)
- Bloqueia caracteres perigosos (`;`, `--`, `DROP`, `DELETE`)

### Cache de Dados
- `@lru_cache` na função `carregar_csv()`
- Carrega dados UMA VEZ
- Melhora performance

---

## 📋 Requisitos

- Python 3.8+
- pandas >= 2.0.0
- langchain-core >= 0.3.0

### Instalação

```bash
pip install pandas langchain-core
```

---

## 🧪 Testes

### Executar Testes Automáticos
```bash
python agente_sinarm_v2_completo.py --testes
```

**Resultado esperado:**
```
RESULTADO: 9/9 testes aprovados
Taxa de sucesso: 100.0%
```

### Testes Incluídos
1. ✅ Teste básico (Taurus)
2. ✅ Teste básico (9mm)
3. ✅ Teste combinado (Glock roubadas)
4. ✅ Teste distribuição (Beretta)
5. ✅ Teste ranking (marcas)
6. ✅ Teste ranking (calibres)
7. ✅ Teste estatísticas
8. ✅ Teste erro digitação (tauros)
9. ✅ Teste distribuição (Glock)

---

## 📊 Status

| Componente | Status | Validação |
|------------|--------|-----------|
| Notebook | ✅ 100% | 23/23 aprovado |
| Arquivo .py | ✅ 100% | 9/9 aprovado |
| Tools | ✅ 8/8 | Todas funcionais |
| Documentação | ✅ Completa | README + Comentários |

---

## 🔄 Próximos Passos

### E4 - RAG (Retrieval-Augmented Generation)
- Adicionar busca semântica com FAISS
- Integrar embeddings
- Responder perguntas conceituais

### E5 - Integração LLM
- Integrar com Ollama
- Roteamento inteligente com LLM
- Respostas mais naturais

### Melhorias Futuras
- Integrar com dados reais SINARM
- Adicionar gráficos (matplotlib/plotly)
- Exportação de relatórios (PDF/Excel)
- Deploy em produção

---

## 📚 Documentação Adicional

- `PADRAO_DESENVOLVIMENTO_IBMEC.txt` - Padrão completo de desenvolvimento
- `RELATORIO_FINAL_COMPLETO.txt` - Relatório detalhado do projeto
- `NOVA_FUNCIONALIDADE_v2_1.txt` - Documentação da tool de distribuição

---

## 👥 Autores

**MBA IA Generativa PCDF - IBMEC**  
Desenvolvido no Encontro 3 - Construção do Agente do Zero

---

## 📝 Licença

Material didático para uso exclusivo do MBA IA Generativa PCDF - IBMEC.

---

## 🆘 Suporte

Problemas? Consulte:
1. `04_MATERIAL_APOIO/FAQ.md`
2. `04_MATERIAL_APOIO/troubleshooting.md`
3. Professor do encontro

---

**Última atualização:** 26/07/2026  
**Versão:** 2.1
