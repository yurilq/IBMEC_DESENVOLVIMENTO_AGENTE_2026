# 🤖 Agente SINARM v1.0 - Consolidado

**Versão final do agente construído no E3**

---

## 📋 O que é?

Este é o agente SINARM completo, consolidado em um único arquivo `.py` pronto para usar.

**Funcionalidades:**
- ✅ 4 ferramentas especializadas
- ✅ Cache de dados (@lru_cache)
- ✅ Few-Shot Learning
- ✅ Chain-of-Thought
- ✅ Validação de segurança

---

## 🚀 Como Usar

### **1. Instalar Dependências**

```bash
pip install -r requirements.txt
```

### **2. Executar Modo Interativo**

```bash
python agente_sinarm_v1.py
```

### **3. Fazer Perguntas**

```
Sua pergunta: Quantas armas Taurus?
Resposta: Existem 30 armas Taurus registradas no SINARM.

Sua pergunta: Quantas armas calibre 9mm?
Resposta: Existem 40 armas calibre 9mm registradas no SINARM.

Sua pergunta: sair
Ate logo!
```

---

## 📦 Importar como Módulo

```python
from agente_sinarm_v1 import perguntar_seguro

# Fazer pergunta
resposta = perguntar_seguro("Quantas armas Glock?")
print(resposta)
```

---

## 🔧 Ferramentas Disponíveis

### **1. contar_armas_marca**
Conta armas por marca (TAURUS, GLOCK, BERETTA, etc)

### **2. contar_armas_calibre**
Conta armas por calibre (9mm, .38, .40, .45)

### **3. contar_armas_tipo**
Conta por tipo de ocorrência (FURTO, ROUBO, APREENSAO)

### **4. contar_armas_combinado**
Conta por marca E tipo combinados

---

## 🧪 Exemplos de Perguntas

```
✅ "Quantas armas Taurus?"
✅ "Quantas armas calibre 9mm?"
✅ "Quantas armas Glock foram roubadas?"
✅ "Quantas ocorrências de furto?"
✅ "Quantas armas Beretta calibre .40?"
```

---

## 🔒 Segurança

O agente possui validação de entrada que bloqueia:
- ❌ Queries muito longas (>500 caracteres)
- ❌ Queries muito curtas (<3 caracteres)
- ❌ Caracteres perigosos (`;`, `--`, `DROP`, `DELETE`)

---

## 📊 Dados

**Atualmente:** Usa dados sintéticos para demonstração (100 registros)

**Para usar dados reais:**
1. Substitua a função `carregar_csv()` 
2. Aponte para arquivo CSV real do SINARM
3. Ajuste nomes de colunas se necessário

---

## 🎓 Aprendizado

Este agente foi construído passo-a-passo no **E3 - Construção do Agente do Zero**.

Para entender como foi construído, veja:
- `../02_NOTEBOOK_PASSO_A_PASSO/E3_construcao_agente_sinarm.ipynb`

---

## 🐛 Troubleshooting

### **Erro: "Ollama not found"**
```bash
# Instalar Ollama
# Windows: https://ollama.ai/download
# Depois: ollama pull llama3.2
```

### **Erro: "Module not found"**
```bash
pip install -r requirements.txt
```

### **Agente não responde corretamente**
- Verifique se Ollama está rodando: `ollama list`
- Teste o modelo: `ollama run llama3.2 "teste"`

---

## 📝 Versão

**v1.0** - 26/07/2026
- Versão inicial consolidada
- 4 ferramentas básicas
- Dados sintéticos

---

## 🔄 Próximas Versões

**v2.0 (planejado):**
- Integração com dados reais SINARM
- Mais ferramentas (estatísticas, gráficos)
- RAG para perguntas conceituais

---

**Desenvolvido no MBA IA Generativa PCDF - IBMEC**
