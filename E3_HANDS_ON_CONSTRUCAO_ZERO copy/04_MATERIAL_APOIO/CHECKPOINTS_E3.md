# ✅ CHECKPOINTS E3

**Objetivo:** Auto-avaliação durante a aula  
**Use:** Marcar checkpoints conforme avança

---

## 🎯 COMO USAR

Após cada parte da aula, verifique se conseguiu completar os checkpoints.

✅ = Consegui  
❌ = Não consegui (pedir ajuda!)  
⏭️ = Pulei (voltar depois)

---

## CHECKPOINT 1: SETUP (13:45)

### Ambiente

- [ ] Python 3.9+ instalado e funcionando
- [ ] `python --version` mostra versão correta
- [ ] Ollama instalado
- [ ] `ollama list` mostra llama3
- [ ] `ollama serve` roda sem erro
- [ ] VSCode ou editor aberto

### Primeiro Script

- [ ] Arquivo `teste_llm.py` criado
- [ ] Import funciona (sem ModuleNotFoundError)
- [ ] Script executa sem erro
- [ ] LLM retorna resposta em português
- [ ] Resposta aparece no terminal

**SE TODOS ✅: Pronto para Parte 2!**

---

## CHECKPOINT 2A: FUNÇÃO PYTHON (14:30)

### Arquivo tools_basicas.py

- [ ] Arquivo criado
- [ ] Import pandas funciona
- [ ] Função `contar_armas_marca` definida
- [ ] Function tem docstring
- [ ] Function tem type hint (marca: str)

### Teste Isolado

- [ ] CSV encontrado (não FileNotFoundError)
- [ ] Teste retorna número (não zero)
- [ ] Teste para "Taurus" funciona
- [ ] Teste para "Glock" funciona
- [ ] Números fazem sentido (>0, <1 milhão)

**SE TODOS ✅: Função básica OK!**

---

## CHECKPOINT 2B: AGENTE BÁSICO (15:00)

### Arquivo agente_v0_1.py

- [ ] Arquivo criado
- [ ] LLM criado sem erro
- [ ] Tool criada manualmente (Tool())
- [ ] Agente inicializado
- [ ] verbose=True ativado

### Execução

- [ ] Agente executa sem erro
- [ ] Viu "Entering new AgentExecutor chain"
- [ ] Viu THOUGHT (raciocínio)
- [ ] Viu ACTION (chamada tool)
- [ ] Viu OBSERVATION (resultado)
- [ ] Viu FINAL ANSWER (resposta)
- [ ] Tool foi chamada (ContarArmas)
- [ ] Resposta correta (número esperado)

**SE TODOS ✅: Agente básico funcionando!**

---

## CHECKPOINT 3A: ENTENDER DECORATOR (15:45)

### Conceitos

- [ ] Entendeu o que é função normal
- [ ] Viu problema de código repetido
- [ ] Entendeu analogia "papel de presente"
- [ ] Sabe que @ é atalho
- [ ] Entendeu que decorator "embrulha" função
- [ ] Decorator NÃO muda função original

### Arquivo decorator_exemplo.py

- [ ] Arquivo criado
- [ ] Decorator `mostrar_log` definido
- [ ] Funções com @mostrar_log executam
- [ ] Log aparece automaticamente
- [ ] Resultado correto

**TESTE:** Consegue explicar decorator para colega?

**SE TODOS ✅: Dominou decorators!**

---

## CHECKPOINT 3B: USAR @tool (16:00)

### Refatoração

- [ ] `tools_basicas.py` modificado
- [ ] Import `from langchain_core.tools import tool`
- [ ] @tool adicionado na função
- [ ] Docstring melhorada
- [ ] Type hints completos (-> str)

### Agente Simplificado

- [ ] `agente_v0_1.py` modificado
- [ ] Removeu Tool() manual
- [ ] Passa função direto: `tools=[contar_armas_marca]`
- [ ] Agente funciona igual antes
- [ ] Código mais limpo/curto

**SE TODOS ✅: @tool dominado!**

---

## CHECKPOINT 4A: 4 TOOLS (16:55)

### Novas Tools

- [ ] `contar_armas_calibre` criada com @tool
- [ ] `contar_armas_tipo` criada com @tool
- [ ] `contar_armas_combinado` criada com @tool
- [ ] Todas com docstring
- [ ] Todas com type hints

### Agente com 4 Tools

- [ ] Agente atualizado com 4 tools
- [ ] Pergunta 1 (marca) → usa tool 1
- [ ] Pergunta 2 (calibre) → usa tool 2
- [ ] Pergunta 3 (tipo) → usa tool 3
- [ ] Pergunta 4 (marca+tipo) → usa tool 4
- [ ] Agente escolhe tool correta

**SE TODOS ✅: 4 tools funcionando!**

---

## CHECKPOINT 4B: CACHE (17:15)

### Implementação Cache

- [ ] Import `from functools import lru_cache`
- [ ] Função `carregar_csv()` criada
- [ ] @lru_cache(maxsize=1) adicionado
- [ ] Todas tools usam `carregar_csv()`
- [ ] Print "Carregando CSV..." adicionado

### Performance

- [ ] Executou 4 perguntas
- [ ] Viu "Carregando CSV..." SÓ 1 VEZ
- [ ] 2ª-4ª perguntas muito mais rápidas
- [ ] `cache_info()` mostra hits>0

**SE TODOS ✅: Cache funcionando!**

---

## CHECKPOINT 5A: FEW-SHOT (17:40)

### System Message

- [ ] Arquivo `agente_v2_0.py` criado
- [ ] `system_message` definido
- [ ] 3+ exemplos Few-Shot adicionados
- [ ] Formato: Pergunta → Resposta
- [ ] Exemplos relevantes (PCDF/SINARM)

### Teste

- [ ] Agente com `agent_kwargs`
- [ ] Resposta mais técnica (vs antes)
- [ ] Usa terminologia PCDF
- [ ] Cita fonte

**SE TODOS ✅: Few-Shot melhora respostas!**

---

## CHECKPOINT 5B: CHAIN-OF-THOUGHT (17:50)

### Instrução CoT

- [ ] PASSO 1 - ANÁLISE definido
- [ ] PASSO 2 - BUSCA definido
- [ ] PASSO 3 - RESULTADO definido
- [ ] PASSO 4 - RESPOSTA definido
- [ ] Instrução "sempre seguir passos"

### Teste

- [ ] Pergunta complexa testada
- [ ] Resposta mostra PASSO 1, 2, 3, 4
- [ ] Raciocínio explícito visível
- [ ] Conclusão clara no final

**SE TODOS ✅: CoT estrutura raciocínio!**

---

## CHECKPOINT 5C: SECURITY (18:00)

### Validação

- [ ] Função `validar_input()` criada
- [ ] Valida tamanho (máx 500)
- [ ] Valida caracteres perigosos (;, --, DROP)
- [ ] Valida prompt injection
- [ ] Função `perguntar_agente_seguro()` criada

### Testes de Segurança

- [ ] Pergunta normal: PASSA
- [ ] SQL injection: BLOQUEADA
- [ ] Query longa: BLOQUEADA
- [ ] Prompt injection: BLOQUEADA
- [ ] Mensagens de erro claras

**SE TODOS ✅: Segurança implementada!**

---

## ✅ CHECKPOINT FINAL: AGENTE V2.0 COMPLETO (18:00)

### Componentes

- [ ] 4 Tools SINARM funcionando
- [ ] @tool em todas
- [ ] @lru_cache otimizando
- [ ] Few-Shot (3+ exemplos)
- [ ] Chain-of-Thought (4 passos)
- [ ] Validação de segurança
- [ ] System message completo
- [ ] Interface interativa (opcional)

### Testes Finais

- [ ] Pergunta simples: funciona
- [ ] Pergunta complexa: funciona
- [ ] Pergunta combinada: funciona
- [ ] Ataque bloqueado: funciona
- [ ] Raciocínio visível: funciona

### Qualidade do Código

- [ ] ~150 linhas total
- [ ] Código organizado
- [ ] Comentários claros
- [ ] Sem erros/warnings
- [ ] Executável

**SE TODOS ✅: PARABÉNS! AGENTE COMPLETO! 🎉**

---

## 📊 RESUMO GERAL

Conte quantos ✅ você tem:

- **0-10**: Precisa de ajuda urgente
- **11-20**: Acompanhando, mas com dificuldades
- **21-30**: Bom progresso
- **31-40**: Muito bem!
- **41-50**: Excelente!
- **51+**: PERFEITO! 🌟

---

## 🚀 PRÓXIMOS PASSOS

### Se completou TODOS checkpoints:
✅ Salve todos os arquivos  
✅ Teste bastante  
✅ Experimente modificar  
✅ Pronto para E4!

### Se faltou algum:
⚠️ Revise parte específica  
⚠️ Consulte FAQ/Troubleshooting  
⚠️ Use templates se necessário  
⚠️ Peça ajuda antes de E4

---

**Arquivo:** CHECKPOINTS_E3.md  
**Localização:** 04_MATERIAL_APOIO/  
**Total:** 50+ checkpoints  
**Status:** ✅ PRONTO PARA AUTO-AVALIAÇÃO
