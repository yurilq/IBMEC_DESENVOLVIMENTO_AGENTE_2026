# ⚙️ GUIA: ESCOLHENDO O MODELO LLM ADEQUADO

**Problema Real Encontrado:** Falta de memória RAM ao usar llama3 (8B)  
**Solução:** Usar modelo menor (llama3.2:1b)  
**Lição:** Nem sempre o modelo maior é a melhor escolha!

---

## 🎯 Contexto

Durante o desenvolvimento, você pode encontrar este erro:

```
llama-server reported out-of-memory during startup: 
ggml_backend_cpu_buffer_type_alloc_buffer: failed to allocate buffer
```

**O que significa?** Seu computador não tem RAM suficiente para carregar o modelo LLM.

---

## 📊 Comparação de Modelos

### llama3 (8B parâmetros)

```
Tamanho: 4.7 GB
RAM necessária: ~6-8 GB (modelo + contexto)
Velocidade: ~2-5 tokens/segundo (CPU)
Qualidade: Muito boa
Caso de uso: Produção, tarefas complexas
```

**Prós:**
- ✅ Respostas mais precisas
- ✅ Entende contexto melhor
- ✅ Segue instruções complexas

**Contras:**
- ❌ Requer muita RAM (6-8 GB)
- ❌ Mais lento em CPUs
- ❌ Pode não rodar em laptops básicos

---

### llama3.2:1b (1B parâmetros)

```
Tamanho: 1.3 GB
RAM necessária: ~2-3 GB
Velocidade: ~10-20 tokens/segundo (CPU)
Qualidade: Boa (suficiente para muitas tarefas)
Caso de uso: Desenvolvimento, prototipagem, laptops
```

**Prós:**
- ✅ Leve (roda em quase qualquer PC)
- ✅ Rápido (2-4x mais rápido)
- ✅ Menos consumo de energia
- ✅ Ideal para aprendizado

**Contras:**
- ⚠️ Menos preciso em tarefas complexas
- ⚠️ Pode não seguir instruções muito específicas
- ⚠️ Contexto menor

---

## 🔧 Como Trocar de Modelo

### Opção 1: Baixar Modelo Menor

```bash
# Baixar llama3.2:1b
ollama pull llama3.2:1b

# Verificar modelos instalados
ollama list
```

### Opção 2: Usar Modelo Menor no Código

```python
# ANTES (modelo grande)
llm = OllamaLLM(model="llama3", temperature=0)

# DEPOIS (modelo pequeno)
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
```

**É só isso!** O resto do código permanece igual.

---

## 📋 Decisão: Qual Modelo Usar?

### Use llama3 (8B) SE:
- ✅ Tem 8GB+ de RAM disponível
- ✅ Desktop/workstation potente
- ✅ Precisa de alta qualidade
- ✅ Deploy em produção

### Use llama3.2:1b (1B) SE:
- ✅ Laptop/PC com pouca RAM
- ✅ Desenvolvimento/aprendizado
- ✅ Prototipagem rápida
- ✅ Bateria limitada (notebook)

---

## 🎓 Para Esta Aula

**Recomendação:** Use o modelo que **funciona no seu computador!**

```python
# Opção A: Se tem RAM suficiente (8GB+)
llm = OllamaLLM(model="llama3", temperature=0)

# Opção B: Se tem pouca RAM (4-6GB)
llm = OllamaLLM(model="llama3.2:1b", temperature=0)

# Opção C: Extremamente limitado (2-4GB)
llm = OllamaLLM(model="tinyllama", temperature=0)
```

### Verificar RAM Disponível

**Windows:**
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

**Mac/Linux:**
```bash
free -h
```

**Regra prática:**
- **<4GB livre:** tinyllama
- **4-6GB livre:** llama3.2:1b
- **>8GB livre:** llama3

---

## 🔬 Testando o Modelo Escolhido

Crie arquivo: `testar_modelo.py`

```python
from langchain_ollama import OllamaLLM
import time

# Escolha seu modelo aqui
MODELO = "llama3.2:1b"  # ou "llama3" ou "tinyllama"

print("="*60)
print(f"TESTANDO MODELO: {MODELO}")
print("="*60)

# Criar LLM
print("\n1. Carregando modelo...")
try:
    llm = OllamaLLM(model=MODELO, temperature=0)
    print("   ✓ Modelo carregado com sucesso")
except Exception as e:
    print(f"   ✗ ERRO ao carregar: {e}")
    exit(1)

# Teste de resposta
print("\n2. Testando resposta simples...")
inicio = time.time()
resposta = llm.invoke("Responda apenas: OK")
tempo = time.time() - inicio
print(f"   ✓ Resposta: {resposta[:50]}")
print(f"   ✓ Tempo: {tempo:.2f}s")

# Teste de qualidade
print("\n3. Testando qualidade...")
inicio = time.time()
pergunta = "Explique em uma frase o que é Python"
resposta = llm.invoke(pergunta)
tempo = time.time() - inicio
print(f"   Pergunta: {pergunta}")
print(f"   Resposta: {resposta}")
print(f"   Tempo: {tempo:.2f}s")

print("\n" + "="*60)
print("MODELO APROVADO PARA USO!")
print("="*60)
```

**Execute:**
```bash
python testar_modelo.py
```

Se funcionar, use esse modelo no resto da aula!

---

## 💡 Dicas de Otimização

### 1. Reduzir Contexto

```python
# Usar menos contexto = menos memória
llm = OllamaLLM(
    model="llama3",
    temperature=0,
    num_ctx=2048  # Padrão: 4096
)
```

### 2. Limitar Modelos Carregados

```bash
# Só carregar 1 modelo por vez
export OLLAMA_MAX_LOADED_MODELS=1  # Mac/Linux
$env:OLLAMA_MAX_LOADED_MODELS = "1"  # Windows
```

### 3. Fechar Outros Programas

Antes de rodar:
- Feche navegador (Chrome/Edge usa muita RAM)
- Feche IDEs pesadas
- Feche aplicativos desnecessários

### 4. Verificar Uso de RAM

**Durante execução:**
```powershell
# Windows
Get-Process ollama | Select-Object PM, CPU
```

---

## 📚 Modelos Disponíveis no Ollama

```bash
# Listar todos modelos disponíveis
ollama list

# Outros modelos úteis:
ollama pull tinyllama        # 637 MB (muito leve)
ollama pull phi3:mini        # 2.2 GB (boa qualidade)
ollama pull llama3.2:1b      # 1.3 GB (recomendado)
ollama pull llama3.2:3b      # 2.0 GB (meio-termo)
ollama pull llama3           # 4.7 GB (melhor qualidade)
ollama pull llama3:70b       # 40 GB (servidor/GPU)
```

---

## 🎯 Impacto na Qualidade das Respostas

### Exemplo Real: "Quantas armas Taurus?"

**llama3 (8B):**
```
Existem 17.760 armas da marca Taurus registradas no banco de 
dados SINARM, conforme a consulta realizada. Fonte: SINARM 
OCORRENCIAS_2026.csv
```
*Resposta perfeita, profissional*

**llama3.2:1b (1B):**
```
Existem 17.760 armas Taurus registradas no SINARM.
```
*Resposta correta, mais direta*

**tinyllama (1B antigo):**
```
Há 17760 armas.
```
*Resposta curta, menos contexto*

**Conclusão:** Todos funcionam, mas com diferentes níveis de eloquência.

---

## ⚠️ Problemas Comuns

### Problema 1: "Model not found"

```bash
# Solução: Baixar o modelo
ollama pull llama3.2:1b
```

### Problema 2: "Out of memory"

```python
# Solução: Trocar para modelo menor
llm = OllamaLLM(model="llama3.2:1b")  # em vez de "llama3"
```

### Problema 3: "Muito lento"

- **Causa:** Modelo muito grande para CPU
- **Solução:** Usar modelo menor ou GPU

---

## 🎓 Lição Aprendida

### Para Desenvolvimento/Aprendizado:
✅ **Use modelo MENOR** (llama3.2:1b)
- Rápido
- Funciona em qualquer PC
- Qualidade suficiente para aprender

### Para Produção:
✅ **Use modelo MAIOR** (llama3)
- Melhor qualidade
- Servidor com mais recursos
- Respostas mais profissionais

---

## 📌 Resumo

| Aspecto | llama3 (8B) | llama3.2:1b (1B) |
|---------|-------------|------------------|
| **RAM necessária** | 6-8 GB | 2-3 GB |
| **Tamanho** | 4.7 GB | 1.3 GB |
| **Velocidade (CPU)** | 2-5 tok/s | 10-20 tok/s |
| **Qualidade** | Excelente | Boa |
| **Uso recomendado** | Produção | Desenvolvimento |
| **Funciona em laptop?** | Depende | Sempre |

---

## 🔄 Como Aplicar na Aula

### No Início da Aula (Parte 1):

**Professor anuncia:**

> "Antes de começar, vamos escolher o modelo adequado ao seu computador.  
> Se tiver erro de memória, usaremos modelo menor - **funciona igual!**"

### Durante a Aula:

Se aluno tiver erro de memória:

1. ✅ Identificar: "Out of memory"
2. ✅ Solução imediata: `ollama pull llama3.2:1b`
3. ✅ Modificar código: `model="llama3.2:1b"`
4. ✅ Continuar aula normalmente

### Lição Pedagógica:

**"Esta é uma lição importante sobre desenvolvimento real:**
- Hardware limita escolhas
- Otimização é essencial
- Trade-offs: tamanho vs qualidade vs velocidade"

---

**Arquivo:** GUIA_ESCOLHA_MODELO_LLM.md  
**Localização:** 04_MATERIAL_APOIO/  
**Criado:** 20/07/2026  
**Status:** ✅ Experiência real documentada

**Transforme limitações técnicas em oportunidades de aprendizado! 🎓**
