# 📓 Notebook Passo-a-Passo - E3

**Construção do Agente SINARM do Zero**

---

## ⚠️ IMPORTANTE: Use a Versão v2

**Arquivo recomendado:** `E3_construcao_agente_sinarm_v2.ipynb` ⭐

**Motivo:** A versão original (v1) tem erro de import do LangChain. A v2 está corrigida e funciona 100%.

Veja detalhes em: [CORRECAO_NOTEBOOK_v2.md](CORRECAO_NOTEBOOK_v2.md)

---

## 📋 O que é?

Este Jupyter Notebook guia você na construção de ferramentas (tools) SINARM completas, **passo-a-passo**.

**Diferença do arquivo .py:**
- 📓 **Notebook:** Didático, célula por célula, com explicações
- 📄 **.py:** Código consolidado, pronto para usar

---

## 🚀 Como Usar

### **1. Abrir o Notebook v2**

```bash
# Instalar Jupyter (se não tiver)
pip install jupyter

# Abrir notebook v2
jupyter notebook E3_construcao_agente_sinarm_v2.ipynb
```

### **2. Executar Células**

- **Shift + Enter:** Executa célula e vai para próxima
- **Ctrl + Enter:** Executa célula e fica na mesma
- **Alt + Enter:** Executa célula e cria nova abaixo

### **3. Seguir a Ordem**

⚠️ **IMPORTANTE:** Execute as células **NA ORDEM** (de cima para baixo)

---

## 📚 Estrutura do Notebook

### **PASSO 1: Instalação e Imports**
- Instalar dependências
- Importar bibliotecas
- Verificar se tudo está OK

### **PASSO 2: Carregar Dados**
- Criar função `carregar_csv()`
- Usar `@lru_cache` (cache)
- Visualizar dados

### **PASSO 3: Primeira Tool**
- Criar `contar_armas_marca()`
- Usar decorator `@tool`
- Testar tool

### **PASSO 4: Mais Tools**
- `contar_armas_calibre()`
- `contar_armas_tipo()`
- `contar_armas_combinado()`

### **PASSO 5: Criar Agente**
- Configurar LLM (Ollama)
- Criar prompt (Few-Shot + CoT)
- Montar agente

### **PASSO 6: Testar Agente**
- Fazer perguntas
- Ver raciocínio do agente
- Analisar resultados

### **PASSO 7: Validação**
- Criar `validar_input()`
- Bloquear queries perigosas
- Criar `perguntar_seguro()`

---

## 🎯 Objetivos de Aprendizado

Ao final deste notebook, você saberá:

✅ Como criar ferramentas com `@tool`  
✅ Como usar cache com `@lru_cache`  
✅ Como criar agentes com LangChain  
✅ Como usar Few-Shot Learning  
✅ Como implementar Chain-of-Thought  
✅ Como validar entrada do usuário  

---

## ⏱️ Tempo Estimado

- **Execução rápida:** 30 min (apenas executar células)
- **Com leitura:** 1-2h (ler explicações)
- **Com experimentação:** 3-4h (testar variações)

---

## 🧪 Exercícios Sugeridos

Após completar o notebook, tente:

1. **Adicionar nova tool:** Criar `contar_armas_uf()` (por estado)
2. **Melhorar prompt:** Adicionar mais exemplos Few-Shot
3. **Dados reais:** Substituir dados sintéticos por CSV real
4. **Gráficos:** Adicionar visualizações com matplotlib

---

## 🐛 Troubleshooting

### **Erro: "Kernel not found"**
```bash
pip install ipykernel
python -m ipykernel install --user
```

### **Erro: "Ollama not found"**
```bash
# Instalar Ollama
# Windows: https://ollama.ai/download
ollama pull llama3.2
```

### **Célula não executa**
- Verifique se executou células anteriores
- Reinicie kernel: `Kernel > Restart & Clear Output`

---

## 💾 Exportar para .py

Para converter notebook em arquivo Python:

```bash
jupyter nbconvert --to script E3_construcao_agente_sinarm.ipynb
```

Ou use o arquivo já pronto: `../03_AGENTE_CONSOLIDADO/agente_sinarm_v1.py`

---

## 📝 Notas

- **Dados:** Usa dados sintéticos para demonstração
- **LLM:** Requer Ollama + Llama 3.2 instalados
- **Tempo:** Agente pode demorar alguns segundos para responder

---

**Desenvolvido no MBA IA Generativa PCDF - IBMEC**
