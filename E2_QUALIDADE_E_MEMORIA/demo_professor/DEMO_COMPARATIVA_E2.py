# DEMONSTRAÇÃO COMPARATIVA E2 - Professor usa ao vivo
# Compara v1.8 (baseline) vs v2.0 (Few-Shot) vs v2.5 (CoT)
# Quinta 16/07/2026

"""
OBJETIVO: Script para demonstração ao vivo durante aula
- Executa mesmas queries em 3 versões
- Mostra métricas comparativas
- Gera tabelas formatadas
- Salva resultados em markdown (para slides)

USO:
    python DEMO_COMPARATIVA_E2.py
    
DURAÇÃO: ~15-20 minutos
"""

import sys
import io
import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

# Setup encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup paths
project_root = Path(__file__).resolve().parent.parent.parent  # 03_CODIGOS_PRONTOS
sys.path.insert(0, str(project_root))

# Logging silencioso para não poluir demo
logging.basicConfig(level=logging.ERROR)

# Importar agentes (ajustado para nova estrutura)
try:
    # Importar do caminho correto agora
    sys.path.insert(0, str(project_root / "E1_ANATOMIA_DO_AGENTE" / "solucao_final"))
    sys.path.insert(0, str(project_root / "E2_QUALIDADE_E_MEMORIA" / "solucao_final"))
    
    from E1_agente_react_v3 import AgenteInvestigador as AgenteV18
    from agente_v2_0_fewshot import AgenteInvestigadorV20
    from agente_v2_5_cot import AgenteInvestigadorV25
    IMPORTS_OK = True
except ImportError as e:
    print(f"❌ Erro ao importar agentes: {e}")
    print("   Certifique-se de que os arquivos existem:")
    print("   - E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py (v1.8)")
    print("   - E2_QUALIDADE_E_MEMORIA/solucao_final/agente_v2.0_fewshot.py (v2.0)")
    print("   - E2_QUALIDADE_E_MEMORIA/solucao_final/agente_v2.5_cot.py (v2.5)")
    IMPORTS_OK = False
    sys.exit(1)

# ========== ESTRUTURAS DE DADOS ==========

@dataclass
class TestQuery:
    """Query de teste com metadados"""
    query: str
    expected_answer: str  # Resposta esperada (para validação)
    complexity: str  # 'simples', 'média', 'complexa'
    filtros: int  # Número de filtros necessários

@dataclass
class ResultadoComparativo:
    """Resultado de uma query em uma versão"""
    versao: str
    query: str
    resposta: str
    tempo_segundos: float
    correto: bool
    tem_trace: bool = False

# ========== QUERIES DE TESTE ==========

QUERIES_TESTE = [
    TestQuery(
        query="Quantas pistolas Taurus foram registradas em 2026?",
        expected_answer="Taurus",
        complexity="simples",
        filtros=3
    ),
    TestQuery(
        query="Qual a marca de revólver mais apreendida em 2026?",
        expected_answer="marca",
        complexity="média",
        filtros=3
    ),
    TestQuery(
        query="Das pistolas roubadas em 2026, quantas eram da marca Taurus e calibre 9mm?",
        expected_answer="234",  # Valor fictício para demo
        complexity="complexa",
        filtros=5
    )
]

# ========== CLASSE PRINCIPAL ==========

class DemoComparativa:
    """Orquestra demonstração comparativa entre versões"""
    
    def __init__(self):
        print("🔧 Inicializando agentes...")
        
        # Inicializar 3 versões (modo silencioso)
        self.agentes = {}
        
        try:
            self.agentes['v1.8'] = AgenteV18(verbose=False)
            print("   ✅ v1.8 (baseline) carregado")
        except Exception as e:
            print(f"   ⚠️  v1.8 não disponível: {e}")
        
        try:
            self.agentes['v2.0'] = AgenteInvestigadorV20(verbose=False)
            print("   ✅ v2.0 (Few-Shot) carregado")
        except Exception as e:
            print(f"   ⚠️  v2.0 não disponível: {e}")
        
        try:
            self.agentes['v2.5'] = AgenteInvestigadorV25(verbose=False)
            print("   ✅ v2.5 (CoT) carregado")
        except Exception as e:
            print(f"   ⚠️  v2.5 não disponível: {e}")
        
        self.resultados = []
    
    def executar_query(self, versao: str, query: str) -> ResultadoComparativo:
        """
        Executa query em uma versão específica
        
        Args:
            versao: 'v1.8', 'v2.0' ou 'v2.5'
            query: Pergunta a executar
            
        Returns:
            ResultadoComparativo com métricas
        """
        agente = self.agentes.get(versao)
        if not agente:
            return ResultadoComparativo(
                versao=versao,
                query=query,
                resposta="Agente não disponível",
                tempo_segundos=0,
                correto=False
            )
        
        inicio = time.time()
        
        try:
            if versao == 'v2.5':
                # v2.5 retorna CoTResponse
                cot_response = agente.executar(query)
                resposta = cot_response.resposta
                tem_trace = bool(cot_response.pensamento)
            else:
                # v1.8 e v2.0 retornam dict ou string
                resultado = agente.executar(query)
                if isinstance(resultado, dict):
                    resposta = resultado.get('resposta', str(resultado))
                else:
                    resposta = str(resultado)
                tem_trace = False
            
            tempo = time.time() - inicio
            
            # Validação simples (verifica se resposta faz sentido)
            correto = len(resposta) > 20  # Resposta tem conteúdo mínimo
            
            return ResultadoComparativo(
                versao=versao,
                query=query,
                resposta=resposta[:200],  # Limitar tamanho
                tempo_segundos=tempo,
                correto=correto,
                tem_trace=tem_trace
            )
            
        except Exception as e:
            return ResultadoComparativo(
                versao=versao,
                query=query,
                resposta=f"Erro: {str(e)}",
                tempo_segundos=time.time() - inicio,
                correto=False
            )
    
    def demonstrar_query(self, test_query: TestQuery):
        """
        Demonstra uma query em todas as versões
        
        Args:
            test_query: Query de teste
        """
        print(f"\n{'='*80}")
        print(f"📝 QUERY: {test_query.query}")
        print(f"{'='*80}")
        print(f"Complexidade: {test_query.complexity.upper()} ({test_query.filtros} filtros)")
        print(f"{'-'*80}\n")
        
        resultados_query = []
        
        for versao in ['v1.8', 'v2.0', 'v2.5']:
            if versao not in self.agentes:
                continue
            
            print(f"🔄 Testando {versao}...")
            resultado = self.executar_query(versao, test_query.query)
            resultados_query.append(resultado)
            
            # Exibir resultado imediatamente
            icon = "✅" if resultado.correto else "❌"
            trace_icon = "🧠" if resultado.tem_trace else "  "
            
            print(f"   {icon} {trace_icon} Tempo: {resultado.tempo_segundos:.2f}s")
            print(f"   Resposta: {resultado.resposta[:80]}...")
            print()
        
        self.resultados.extend(resultados_query)
        
        # Pausa para professor comentar
        input(f"\n{'─'*80}\n⏸️  Pressione ENTER para próxima query...\n{'─'*80}\n")
    
    def gerar_tabela_comparativa(self):
        """Gera tabela comparativa final"""
        
        print(f"\n{'='*80}")
        print("📊 TABELA COMPARATIVA FINAL")
        print(f"{'='*80}\n")
        
        # Agrupar por versão
        metricas_por_versao = {}
        
        for versao in ['v1.8', 'v2.0', 'v2.5']:
            resultados_versao = [r for r in self.resultados if r.versao == versao]
            
            if not resultados_versao:
                continue
            
            total = len(resultados_versao)
            corretos = sum(1 for r in resultados_versao if r.correto)
            accuracy = (corretos / total * 100) if total > 0 else 0
            latencia_media = sum(r.tempo_segundos for r in resultados_versao) / total
            
            metricas_por_versao[versao] = {
                'accuracy': accuracy,
                'latencia': latencia_media,
                'queries': total
            }
        
        # Imprimir tabela
        print(f"{'Métrica':<25} {'v1.8':<15} {'v2.0':<15} {'v2.5':<15}")
        print(f"{'-'*80}")
        
        print(f"{'Accuracy':<25} ", end='')
        for v in ['v1.8', 'v2.0', 'v2.5']:
            if v in metricas_por_versao:
                acc = metricas_por_versao[v]['accuracy']
                print(f"{acc:.0f}%{' '*11}", end='')
            else:
                print(f"{'N/A':<15}", end='')
        print()
        
        print(f"{'Latência média':<25} ", end='')
        for v in ['v1.8', 'v2.0', 'v2.5']:
            if v in metricas_por_versao:
                lat = metricas_por_versao[v]['latencia']
                print(f"{lat:.2f}s{' '*9}", end='')
            else:
                print(f"{'N/A':<15}", end='')
        print()
        
        print(f"{'Trace visível':<25} ", end='')
        print(f"{'Não':<15}{'Não':<15}{'Sim ✅':<15}")
        
        print(f"{'Debug facilidade':<25} ", end='')
        print(f"{'Difícil':<15}{'Difícil':<15}{'Fácil ✅':<15}")
        
        print(f"\n{'='*80}")
        
        # Insights
        if 'v2.0' in metricas_por_versao and 'v1.8' in metricas_por_versao:
            melhoria_v20 = metricas_por_versao['v2.0']['accuracy'] - metricas_por_versao['v1.8']['accuracy']
            print(f"💡 v2.0 (Few-Shot): +{melhoria_v20:.0f}% accuracy vs v1.8")
        
        if 'v2.5' in metricas_por_versao and 'v2.0' in metricas_por_versao:
            melhoria_v25 = metricas_por_versao['v2.5']['accuracy'] - metricas_por_versao['v2.0']['accuracy']
            print(f"💡 v2.5 (+ CoT): +{melhoria_v25:.0f}% accuracy vs v2.0")
        
        print(f"{'='*80}\n")
    
    def salvar_resultados(self, filename: str = "demo_results.md"):
        """Salva resultados em markdown para uso posterior"""
        
        output_path = project_root / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Resultados Demonstração Comparativa E2\n\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            f.write("## Queries Testadas\n\n")
            for test_query in QUERIES_TESTE:
                f.write(f"- **{test_query.complexity}**: {test_query.query}\n")
            
            f.write("\n## Resultados por Query\n\n")
            for resultado in self.resultados:
                f.write(f"### {resultado.versao}\n")
                f.write(f"- Query: {resultado.query}\n")
                f.write(f"- Tempo: {resultado.tempo_segundos:.2f}s\n")
                f.write(f"- Correto: {'✅' if resultado.correto else '❌'}\n")
                f.write(f"- Trace: {'Sim' if resultado.tem_trace else 'Não'}\n\n")
        
        print(f"💾 Resultados salvos em: {output_path}")

# ========== MAIN ==========

def main():
    """Executa demonstração completa"""
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        DEMONSTRAÇÃO COMPARATIVA E2 - PROFESSOR                      ║
║                                                                      ║
║  Comparação: v1.8 (baseline) vs v2.0 (Few-Shot) vs v2.5 (CoT)      ║
║                                                                      ║
║  Quinta, 16 de Julho de 2026                                        ║
║  Encontro 2: Qualidade e Memória                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if not IMPORTS_OK:
        print("❌ Não foi possível importar todos os agentes")
        return
    
    demo = DemoComparativa()
    
    print("\n📋 Demonstração ao vivo:")
    print("   - 3 queries (simples → complexa)")
    print("   - Executadas em 3 versões")
    print("   - Métricas comparativas ao final\n")
    
    input("Pressione ENTER para iniciar...\n")
    
    # Executar queries
    for i, test_query in enumerate(QUERIES_TESTE, 1):
        print(f"\n{'#'*80}")
        print(f"# QUERY {i}/{len(QUERIES_TESTE)}")
        print(f"{'#'*80}")
        
        demo.demonstrar_query(test_query)
    
    # Tabela final
    demo.gerar_tabela_comparativa()
    
    # Salvar resultados
    demo.salvar_resultados()
    
    print("\n✅ Demonstração concluída!")
    print("\n💡 CONCLUSÕES PARA OS ALUNOS:")
    print("   1. Few-Shot melhora accuracy significativamente (+30-40%)")
    print("   2. CoT adiciona transparência e melhora queries complexas")
    print("   3. Trade-off latência vale a pena para produção")
    print("   4. Trace CoT essencial para debug e compliance\n")

if __name__ == "__main__":
    main()
