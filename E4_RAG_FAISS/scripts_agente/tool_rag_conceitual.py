"""
TOOL RAG CONCEITUAL
Substitui dicionário estático do v4.0 por busca em documentos via RAG
"""

from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path

class RetrieverRAG:
    """Retriever para busca semântica em documentos SINARM"""
    
    def __init__(self, index_path: str, docs_path: str, metadata_path: str, 
                 model_name: str = 'all-MiniLM-L6-v2'):
        print("[INFO] Inicializando RetrieverRAG...")
        
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        
        with open(docs_path, 'r', encoding='utf-8') as f:
            self.documentos = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadados = json.load(f)
        
        print(f"[INFO] RetrieverRAG pronto! {len(self.documentos):,} documentos\n")
    
    def get_context(self, query: str, k: int = 3, threshold: float = 0.5) -> str:
        """Retorna contexto formatado para LLM"""
        
        # Gerar embedding da query
        query_vec = self.model.encode([query]).astype('float32')
        
        # Buscar no FAISS
        distances, indices = self.index.search(query_vec, k)
        
        # Filtrar por threshold
        resultados = []
        for idx, dist in zip(indices[0], distances[0]):
            similaridade = 1 / (1 + dist)
            
            if similaridade >= threshold:
                resultados.append({
                    'documento': self.documentos[idx],
                    'metadados': self.metadados[idx],
                    'similaridade': float(similaridade)
                })
        
        # Formatar contexto
        if not resultados:
            return "[INFO] Nenhum documento relevante encontrado."
        
        contexto = "DOCUMENTOS RECUPERADOS:\n\n"
        for i, r in enumerate(resultados, 1):
            contexto += f"[Doc {i}] (similaridade: {r['similaridade']:.3f})\n"
            contexto += f"ID: {r['metadados'].get('id', 'N/A')}\n"
            contexto += r['documento']
            contexto += "\n" + "="*60 + "\n\n"
        
        return contexto


# ===== INICIALIZAR RETRIEVER GLOBAL =====

# Ajustar caminho baseado na estrutura do projeto
# Script está em: 03_CODIGOS_PRONTOS/scripts_agente/
# Outputs estão em: 03_CODIGOS_PRONTOS/03_outputs/
CAMINHO_BASE = Path(__file__).parent.parent  # Subir 1 nível (para 03_CODIGOS_PRONTOS)

# Os alunos vão executar os scripts do diretório raiz, então outputs estão em:
OUTPUT_DIR = CAMINHO_BASE / "03_outputs"

print("="*70)
print("INICIALIZANDO TOOL RAG CONCEITUAL")
print("="*70)
print(f"\n[INFO] Buscando arquivos em: {OUTPUT_DIR}\n")

try:
    RETRIEVER = RetrieverRAG(
        index_path=str(OUTPUT_DIR / "faiss_index.bin"),
        docs_path=str(OUTPUT_DIR / "documentos.json"),
        metadata_path=str(OUTPUT_DIR / "metadados.json")
    )
    RETRIEVER_DISPONIVEL = True
    
except FileNotFoundError as e:
    print(f"[INFO] ERRO: Arquivos RAG não encontrados!")
    print(f"   {e}")
    print(f"\n[INFO] Execute primeiro:")
    print(f"   1. 01_preparar_documentos.py")
    print(f"   2. 02_gerar_embeddings.py")
    print(f"   3. 03_criar_indice_faiss.py")
    print(f"\n   Ou ajuste CAMINHO_BASE no código.\n")
    RETRIEVER_DISPONIVEL = False


def buscar_conhecimento_sinarm(pergunta: str) -> str:
    """
    Busca conhecimento conceitual em documentos SINARM via RAG
    
    USAR PARA perguntas tipo:
    - "O que é X?"
    - "Qual o procedimento para Y?"
    - "Como funciona Z?"
    - "Qual a diferença entre A e B?"
    
    Args:
        pergunta: pergunta conceitual do usuário
    
    Returns:
        Contexto com documentos recuperados ou mensagem de erro
    """
    if not RETRIEVER_DISPONIVEL:
        return "[INFO] RAG não disponível. Execute pipeline RAG primeiro."
    
    print(f"\n[TOOL RAG] Buscando: '{pergunta}'")
    contexto = RETRIEVER.get_context(pergunta, k=3, threshold=0.6)
    print(f"[TOOL RAG] Retornou {len(contexto)} caracteres")
    
    return contexto


# ===== TESTE =====
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTE DA TOOL RAG CONCEITUAL")
    print("="*70)
    
    if not RETRIEVER_DISPONIVEL:
        print("\n[INFO] RAG não disponível para teste.")
        print("Execute o pipeline RAG primeiro!")
        exit(1)
    
    # Testes
    testes = [
        "O que é BO de furto?",
        "Qual o procedimento para arma sem número de série?",
        "Como funciona o registro de armas?",
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n{'#'*70}")
        print(f"TESTE {i}/{len(testes)}")
        print(f"{'#'*70}")
        
        resultado = buscar_conhecimento_sinarm(teste)
        
        print(f"\nRESULTADO:")
        print("-"*70)
        print(resultado[:500] + "..." if len(resultado) > 500 else resultado)
        
        if i < len(testes):
            input(f"\n[ENTER para próximo teste]")
    
    print("\n" + "="*70)
    print("TESTES CONCLUÍDOS!")
    print("="*70)
