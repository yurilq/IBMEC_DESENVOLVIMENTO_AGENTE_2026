"""
ATIVIDADE 3A: MEMORY CONVERSACIONAL (SHORT-TERM BUFFER)
Encontro 2 - Conceito: Memory Management
Duração: 10 minutos

OBJETIVO:
Implementar memória conversacional simples (short-term buffer) para o agente
manter contexto entre múltiplas interações do usuário.

O QUE VOCÊ VAI FAZER:
1. Criar classe ShortTermMemory (buffer de últimas N mensagens)
2. Integrar ao agente v2.5 (Few-Shot + CoT + Memory)
3. Testar conversação multi-turno
4. Observar como contexto melhora respostas

POR QUE ISSO É IMPORTANTE:
- Usuários conversam naturalmente ("E quantas são Glock?" após perguntar sobre Taurus)
- Sem memória: agente não entende pronomes/referências
- Com memória: agente mantém contexto e responde corretamente
- Essencial para chatbots, assistentes, interfaces conversacionais

CONCEITO: Tipos de Memória em Agentes

┌──────────────────────────────────────────────────────────────┐
│ SEM MEMÓRIA (Stateless)                                      │
├──────────────────────────────────────────────────────────────┤
│ User: Quantas pistolas Taurus existem?                       │
│ Agent: 892 pistolas Taurus. Fonte: SINARM/REGISTROS.        │
│                                                              │
│ User: E quantas são Glock?                                   │
│ Agent: ❌ "E quantas são Glock?" não é uma query válida.    │
│        [AGENTE ESQUECEU O CONTEXTO]                         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ COM MEMÓRIA SHORT-TERM (Buffer de 5 mensagens)              │
├──────────────────────────────────────────────────────────────┤
│ User: Quantas pistolas Taurus existem?                       │
│ Agent: 892 pistolas Taurus. Fonte: SINARM/REGISTROS.        │
│                                                              │
│ [MEMÓRIA: armazena contexto "falando sobre pistolas"]       │
│                                                              │
│ User: E quantas são Glock?                                   │
│ Agent: ✅ 487 pistolas Glock. Fonte: SINARM/REGISTROS.      │
│        [AGENTE LEMBROU DO CONTEXTO]                         │
└──────────────────────────────────────────────────────────────┘

TIPOS DE MEMÓRIA:
1. **Short-Term (Buffer)**: Últimas N mensagens (rápido, limitado)
2. **Long-Term (RAG)**: Histórico completo em vector DB (escalável, complexo)
3. **Summary**: Resumo periódico da conversa (compacto, perde detalhes)
4. **Entity Memory**: Extrai entidades mencionadas (marca, UF, tipo...)

TRADE-OFFS:

Buffer Size     Contexto    Latência    Custo Tokens
─────────────────────────────────────────────────────
3 mensagens     Básico      +5%         +10%
5 mensagens     Bom         +10%        +20%
10 mensagens    Excelente   +20%        +40%
∞ (RAG)         Completo    +30%        +15% (embeddings)
"""

from typing import List, Dict
from datetime import datetime
import json

# ========== SHORT-TERM MEMORY ==========

class ShortTermMemory:
    """
    Buffer simples de memória conversacional.
    
    Armazena últimas N mensagens (user + agent) para manter contexto.
    """
    
    def __init__(self, buffer_size: int = 5):
        """
        Args:
            buffer_size: Número de mensagens a manter no buffer (default: 5)
        """
        self.buffer_size = buffer_size
        self.messages: List[Dict] = []
    
    def add_message(self, role: str, content: str):
        """
        Adiciona mensagem ao buffer.
        
        Args:
            role: "user" ou "agent"
            content: Texto da mensagem
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.messages.append(message)
        
        # Manter apenas últimas N mensagens
        if len(self.messages) > self.buffer_size:
            self.messages = self.messages[-self.buffer_size:]
    
    def get_context(self) -> str:
        """
        Retorna contexto formatado para incluir no prompt.
        
        Returns:
            String com últimas N mensagens formatadas
        """
        if not self.messages:
            return ""
        
        context = "\n\n## 📝 CONTEXTO DA CONVERSA:\n\n"
        for msg in self.messages:
            role_label = "Usuário" if msg["role"] == "user" else "Agente"
            context += f"{role_label}: {msg['content']}\n"
        
        context += "\nContinue a conversa considerando o contexto acima.\n"
        return context
    
    def clear(self):
        """Limpa o buffer (reinicia conversa)."""
        self.messages = []
    
    def get_last_n(self, n: int) -> List[Dict]:
        """Retorna últimas N mensagens."""
        return self.messages[-n:] if len(self.messages) >= n else self.messages
    
    def to_json(self) -> str:
        """Serializa buffer para JSON (para salvar)."""
        return json.dumps({
            "buffer_size": self.buffer_size,
            "messages": self.messages
        }, ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str):
        """Carrega buffer de JSON."""
        data = json.loads(json_str)
        memory = cls(buffer_size=data["buffer_size"])
        memory.messages = data["messages"]
        return memory

# ========== INTEGRAR MEMORY AO AGENTE ==========

def criar_agente_com_memory(memory: ShortTermMemory):
    """
    Cria agente v2.5 com memória conversacional.
    
    NOTA: Implementação simplificada - na versão completa (solucao_final/),
          integraremos com LangChain memory nativa.
    """
    
    print("🧠 Agente com memória conversacional criado!")
    print(f"   Buffer size: {memory.buffer_size} mensagens")
    
    # TODO: Integrar com create_react_agent + PromptTemplate customizado
    # Por enquanto, demonstração manual
    
    return memory

# ========== TESTE CONVERSACIONAL ==========

def testar_conversacao():
    """Simula conversação multi-turno com memory."""
    
    print("\n" + "="*70)
    print("TESTE: CONVERSAÇÃO MULTI-TURNO COM MEMORY")
    print("="*70)
    
    # Criar memória
    memory = ShortTermMemory(buffer_size=5)
    agente = criar_agente_com_memory(memory)
    
    # Conversação de exemplo
    conversacao = [
        {
            "turno": 1,
            "user": "Quantas pistolas Taurus estão registradas?",
            "agent": "892 pistolas Taurus estão registradas. Fonte: SINARM/REGISTROS."
        },
        {
            "turno": 2,
            "user": "E quantas são Glock?",  # REFERÊNCIA ao contexto anterior
            "agent": "487 pistolas Glock estão registradas. Fonte: SINARM/REGISTROS."
        },
        {
            "turno": 3,
            "user": "Qual dessas duas marcas tem mais furtos no DF?",  # REFERÊNCIA a "Taurus" e "Glock"
            "agent": "Taurus tem mais furtos no DF: 487 ocorrências vs 312 de Glock. Fonte: SINARM/OCORRENCIAS."
        },
        {
            "turno": 4,
            "user": "Por quê?",  # REFERÊNCIA vaga - precisa de contexto completo
            "agent": "Taurus é mais popular no DF (1.289 registros vs 487 Glock), logo há mais armas Taurus circulando, resultando em mais furtos em números absolutos."
        }
    ]
    
    print("\n📖 SIMULAÇÃO DE CONVERSAÇÃO:\n")
    
    for conv in conversacao:
        print(f"{'─'*70}")
        print(f"TURNO {conv['turno']}")
        print(f"{'─'*70}")
        
        # Adicionar mensagem do usuário
        memory.add_message("user", conv["user"])
        print(f"👤 Usuário: {conv['user']}")
        
        # Mostrar contexto disponível
        print(f"\n🧠 Contexto no buffer ({len(memory.messages)} mensagens):")
        for msg in memory.get_last_n(3):
            role = "👤" if msg["role"] == "user" else "🤖"
            print(f"   {role} {msg['content'][:50]}...")
        
        # Adicionar resposta do agente
        memory.add_message("agent", conv["agent"])
        print(f"\n🤖 Agente: {conv['agent']}")
        print()
    
    print("="*70)
    print("ANÁLISE:")
    print("="*70)
    print("✅ Turno 2: 'E quantas são Glock?' - Agente entendeu que se referia a PISTOLAS")
    print("✅ Turno 3: 'dessas duas marcas' - Agente lembrou de Taurus e Glock")
    print("✅ Turno 4: 'Por quê?' - Agente usou contexto completo para explicar")
    print("\n❌ SEM MEMORY: Todos os turnos 2-4 falhariam (contexto ausente)")
    print("="*70)

# ========== COMPARAÇÃO: COM vs SEM MEMORY ==========

def comparar_com_sem_memory():
    """Mostra diferença entre agente com/sem memory."""
    
    print("\n" + "="*70)
    print("COMPARAÇÃO: COM MEMORY vs SEM MEMORY")
    print("="*70)
    
    query_ambigua = "E quantas são Glock?"
    
    print(f"\n📝 Query: '{query_ambigua}'\n")
    
    print("❌ SEM MEMORY (Stateless):")
    print("   Agente: 'Erro: Query ambígua. Especifique: pistolas Glock? portes Glock?")
    print("           registros Glock? ocorrências Glock?'\n")
    
    print("✅ COM MEMORY (contexto: 'pistolas Taurus' na mensagem anterior):")
    print("   Agente: '487 pistolas Glock estão registradas. Fonte: SINARM/REGISTROS.'\n")
    
    print("="*70)
    print("CONCLUSÃO:")
    print("Memory permite queries naturais (como humanos conversam).")
    print("Custo: +10-20% latência, +20-40% tokens (depende do buffer size).")
    print("="*70)

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 3A: MEMORY CONVERSACIONAL (SHORT-TERM BUFFER)    ║
║  Encontro 2 - Memory Management                              ║
╚═══════════════════════════════════════════════════════════════╝

OBJETIVO:
Implementar memória conversacional simples (buffer) para manter contexto.

CONCEITO:
- Short-Term Memory = buffer das últimas N mensagens
- Permite referências ("E quantas são Glock?" após "Quantas Taurus?")
- Essencial para interfaces conversacionais naturais

TRADE-OFF:
- Buffer 5 mensagens: +10% latência, +20% tokens
- Melhora UX significativamente (usuário conversa naturalmente)
""")
    
    print("\n1️⃣  Teste: Conversação Multi-Turno")
    testar_conversacao()
    
    input("\n\nPressione ENTER para comparação COM vs SEM memory...")
    
    print("\n2️⃣  Comparação: COM vs SEM Memory")
    comparar_com_sem_memory()
    
    print("\n" + "="*70)
    print("✅ ATIVIDADE 3A CONCLUÍDA!")
    print("="*70)
    print("\nVocê aprendeu:")
    print("  ✓ Implementar ShortTermMemory (buffer)")
    print("  ✓ Integrar memory ao agente")
    print("  ✓ Testar conversação multi-turno")
    print("  ✓ Avaliar trade-offs (latência vs UX)")
    print("\n🎯 PRÓXIMO: ATIVIDADE 4A - Security (Input Validation)")
    print("   Proteger agente contra injection attacks e inputs maliciosos.\n")
