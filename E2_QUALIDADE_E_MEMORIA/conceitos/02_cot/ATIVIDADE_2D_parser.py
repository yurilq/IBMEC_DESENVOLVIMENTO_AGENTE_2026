"""
ATIVIDADE 2D: PARSER COT (OPCIONAL - AVANÇADO)
Encontro 2 - Conceito: Chain-of-Thought (CoT)
Duração: 10 minutos

OBJETIVO:
Extrair e estruturar as seções do trace CoT (Thought, Action, Observation, Answer)
para análise, métricas, debugging e auditoria.

O QUE VOCÊ VAI FAZER:
1. Implementar parser de texto para extrair seções CoT
2. Validar que todas as 4 seções estão presentes
3. Estruturar em JSON para análise posterior
4. Usar para debugging (identificar onde agente errou)

POR QUE ISSO É IMPORTANTE:
- **Métricas**: Quantos Thoughts antes da resposta? Agente está confuso?
- **Debugging**: Em qual Action o agente errou?
- **Auditoria**: Registrar raciocínio completo para compliance
- **Otimização**: Identificar padrões de erro e melhorar prompt

CONCEITO: Do Texto Livre para Estrutura

INPUT (trace CoT como string):
═══════════════════════════════════════════════════════════════
Thought: Preciso buscar OCORRENCIAS com marca=Taurus
Action: buscar_ocorrencias("marca:Taurus")
Observation: 1.247 registros encontrados
Final Answer: 1.247 ocorrências de Taurus.
═══════════════════════════════════════════════════════════════

OUTPUT (JSON estruturado):
{
  "steps": [
    {
      "type": "thought",
      "content": "Preciso buscar OCORRENCIAS com marca=Taurus",
      "timestamp": "2026-07-15T14:32:01"
    },
    {
      "type": "action",
      "tool": "buscar_ocorrencias",
      "params": {"query": "marca:Taurus"},
      "content": "buscar_ocorrencias(\"marca:Taurus\")"
    },
    {
      "type": "observation",
      "content": "1.247 registros encontrados",
      "num_results": 1247
    },
    {
      "type": "answer",
      "content": "1.247 ocorrências de Taurus."
    }
  ],
  "num_steps": 4,
  "num_iterations": 1,
  "is_complete": true
}

CASOS DE USO:
1. **Debugging**: "Por que agente errou?" → Ver em qual Action/Observation
2. **Métricas**: "Agente está eficiente?" → Contar iterações, tempo por step
3. **Auditoria**: "Como chegou nessa resposta?" → Trace completo estruturado
4. **A/B Testing**: Comparar traces v2.0 vs v2.5 (com/sem CoT)
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional

# ========== PARSER COT ==========

class CoTParser:
    """Parser para extrair seções de Chain-of-Thought traces."""
    
    # Padrões regex para identificar seções
    PATTERNS = {
        "thought": r"(?:Thought|THOUGHT|Pensamento|PENSAMENTO):\s*(.+?)(?=(?:Action|Observation|Final Answer|$))",
        "action": r"(?:Action|ACTION|Ação|AÇÃO):\s*(.+?)(?=(?:Observation|Thought|Final Answer|$))",
        "observation": r"(?:Observation|OBSERVATION|Observação|OBSERVAÇÃO):\s*(.+?)(?=(?:Thought|Action|Final Answer|$))",
        "answer": r"(?:Final Answer|FINAL ANSWER|Resposta Final|RESPOSTA FINAL):\s*(.+?)$"
    }
    
    def __init__(self):
        self.steps = []
    
    def parse(self, trace_text: str) -> Dict:
        """
        Parseia trace CoT e extrai seções estruturadas.
        
        Args:
            trace_text: String com trace CoT completo
        
        Returns:
            Dict com steps, métricas e validação
        """
        
        self.steps = []
        
        # Limpar texto
        trace_text = trace_text.strip()
        
        # Extrair Thoughts
        thoughts = re.findall(self.PATTERNS["thought"], trace_text, re.DOTALL | re.IGNORECASE)
        for thought in thoughts:
            self.steps.append({
                "type": "thought",
                "content": thought.strip(),
                "timestamp": datetime.now().isoformat()
            })
        
        # Extrair Actions
        actions = re.findall(self.PATTERNS["action"], trace_text, re.DOTALL | re.IGNORECASE)
        for action in actions:
            action_clean = action.strip()
            
            # Tentar extrair tool e params
            tool_match = re.search(r'(buscar_\w+)\("([^"]+)"\)', action_clean)
            if tool_match:
                tool_name = tool_match.group(1)
                query = tool_match.group(2)
                
                self.steps.append({
                    "type": "action",
                    "tool": tool_name,
                    "params": {"query": query},
                    "content": action_clean
                })
            else:
                self.steps.append({
                    "type": "action",
                    "content": action_clean
                })
        
        # Extrair Observations
        observations = re.findall(self.PATTERNS["observation"], trace_text, re.DOTALL | re.IGNORECASE)
        for obs in observations:
            obs_clean = obs.strip()
            
            # Tentar extrair número de resultados
            num_match = re.search(r'(\d+)\s*(?:registros?|ocorrências?|resultados?)', obs_clean)
            num_results = int(num_match.group(1)) if num_match else None
            
            step = {
                "type": "observation",
                "content": obs_clean
            }
            if num_results is not None:
                step["num_results"] = num_results
            
            self.steps.append(step)
        
        # Extrair Final Answer
        answer_match = re.search(self.PATTERNS["answer"], trace_text, re.DOTALL | re.IGNORECASE)
        if answer_match:
            self.steps.append({
                "type": "answer",
                "content": answer_match.group(1).strip()
            })
        
        # Calcular métricas
        num_thoughts = sum(1 for s in self.steps if s["type"] == "thought")
        num_actions = sum(1 for s in self.steps if s["type"] == "action")
        num_observations = sum(1 for s in self.steps if s["type"] == "observation")
        has_answer = any(s["type"] == "answer" for s in self.steps)
        
        # Validar
        is_valid = (num_thoughts > 0 and num_actions > 0 and has_answer)
        is_complete = (num_thoughts == num_actions == num_observations and has_answer)
        
        return {
            "steps": self.steps,
            "metrics": {
                "num_steps": len(self.steps),
                "num_thoughts": num_thoughts,
                "num_actions": num_actions,
                "num_observations": num_observations,
                "num_iterations": num_thoughts,  # Aproximação: 1 iteração = 1 thought
                "has_answer": has_answer
            },
            "validation": {
                "is_valid": is_valid,
                "is_complete": is_complete,
                "missing_sections": self._get_missing_sections(num_thoughts, num_actions, num_observations, has_answer)
            }
        }
    
    def _get_missing_sections(self, thoughts, actions, observations, has_answer):
        """Identifica seções ausentes."""
        missing = []
        if thoughts == 0:
            missing.append("Thought")
        if actions == 0:
            missing.append("Action")
        if observations == 0:
            missing.append("Observation")
        if not has_answer:
            missing.append("Final Answer")
        return missing

# ========== DEBUGGING COM PARSER ==========

def debug_trace(trace_text: str):
    """
    Usa parser para debugar trace CoT.
    
    Identifica:
    - Seções ausentes
    - Iterações excessivas (agente confuso)
    - Actions sem Observations (tool falhou?)
    """
    
    parser = CoTParser()
    resultado = parser.parse(trace_text)
    
    print("\n" + "="*70)
    print("DEBUG TRACE CoT")
    print("="*70)
    
    # Resumo
    metrics = resultado["metrics"]
    validation = resultado["validation"]
    
    print(f"\n📊 MÉTRICAS:")
    print(f"   Total steps: {metrics['num_steps']}")
    print(f"   Thoughts: {metrics['num_thoughts']}")
    print(f"   Actions: {metrics['num_actions']}")
    print(f"   Observations: {metrics['num_observations']}")
    print(f"   Iterações: {metrics['num_iterations']}")
    print(f"   Tem resposta: {'✅ Sim' if metrics['has_answer'] else '❌ Não'}")
    
    # Validação
    print(f"\n🔍 VALIDAÇÃO:")
    print(f"   Válido: {'✅ Sim' if validation['is_valid'] else '❌ Não'}")
    print(f"   Completo: {'✅ Sim' if validation['is_complete'] else '⚠️ Não'}")
    
    if validation['missing_sections']:
        print(f"   ❌ Seções ausentes: {', '.join(validation['missing_sections'])}")
    
    # Alertas
    print(f"\n⚠️ ALERTAS:")
    if metrics['num_iterations'] > 5:
        print(f"   🚨 Muitas iterações ({metrics['num_iterations']}) - agente pode estar confuso")
    
    if metrics['num_actions'] > metrics['num_observations']:
        diff = metrics['num_actions'] - metrics['num_observations']
        print(f"   🚨 {diff} Action(s) sem Observation correspondente - tool falhou?")
    
    if not metrics['has_answer']:
        print(f"   🚨 Trace incompleto - faltou Final Answer")
    
    # Mostrar steps
    print(f"\n📋 STEPS DETALHADOS:")
    for i, step in enumerate(resultado["steps"], 1):
        tipo = step["type"].upper()
        content_preview = step["content"][:60] + "..." if len(step["content"]) > 60 else step["content"]
        print(f"   {i}. {tipo}: {content_preview}")
    
    print("="*70)
    
    return resultado

# ========== TESTE ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 2D: PARSER COT (OPCIONAL - AVANÇADO)             ║
║  Encontro 2 - Chain-of-Thought (CoT)                         ║
╚═══════════════════════════════════════════════════════════════╝

OBJETIVO:
Extrair e estruturar seções CoT para debugging e auditoria.

INSTRUÇÕES:
1. Copie um trace CoT (da ATIVIDADE_2B ou 2C)
2. Cole aqui para parsear
3. O parser vai extrair: Thoughts, Actions, Observations, Answer
4. Analise as métricas e validação

CASOS DE USO:
- Debugging: identificar onde agente errou
- Métricas: contar iterações, medir eficiência
- Auditoria: registrar raciocínio completo
""")
    
    # Trace de exemplo
    trace_exemplo = """
Thought: Preciso buscar OCORRENCIAS com marca=Taurus, tipo=Furto, uf=DF

Action: buscar_ocorrencias("marca:Taurus")

Observation: 1.247 registros de Taurus encontrados. Filtrando tipo=Furto e uf=DF resulta em 47 ocorrências.

Final Answer: 47 pistolas Taurus foram furtadas no DF em 2026. Fonte: SINARM/OCORRENCIAS.
"""
    
    print("\n📄 TRACE DE EXEMPLO:")
    print("─"*70)
    print(trace_exemplo)
    print("─"*70)
    
    input("\nPressione ENTER para parsear...")
    
    resultado = debug_trace(trace_exemplo)
    
    # Salvar JSON
    from pathlib import Path
    caminho_json = Path(__file__).parent / "trace_parsed_exemplo.json"
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Trace estruturado salvo em: {caminho_json}")
    
    print("\n" + "="*70)
    print("PRÓXIMOS USOS DO PARSER:")
    print("="*70)
    print("1. Integrar em pipeline de testes automatizados")
    print("2. Criar dashboard de métricas CoT")
    print("3. Alertas automáticos (>5 iterações = agente confuso)")
    print("4. Comparação A/B: v2.0 vs v2.5 (traces estruturados)")
    print("\n✅ ATIVIDADE 2 (COT) CONCLUÍDA!")
    print("   Próximo: ATIVIDADE 3A - Memory Conversacional\n")
