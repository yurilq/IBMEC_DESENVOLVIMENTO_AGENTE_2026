"""
PASSO 1: PREPARAR DOCUMENTOS
Transforma CSV SINARM em textos descritivos para RAG
"""

import pandas as pd
from pathlib import Path
import json

print("="*70)
print("PASSO 1: PREPARANDO DOCUMENTOS PARA RAG")
print("="*70)

# Carregar dados SINARM (pasta local)
# Script está em: 03_CODIGOS_PRONTOS/scripts_pipeline/
# Dados estão em: 03_CODIGOS_PRONTOS/DADOS_SINARM/
CAMINHO_DADOS = Path(__file__).parent.parent / "DADOS_SINARM"

print(f"\n[PASTA] Carregando dados de: {CAMINHO_DADOS}")

# Verificar se pasta existe
if not CAMINHO_DADOS.exists():
    print(f"[ERRO] ERRO: Pasta DADOS_SINARM não encontrada!")
    print(f"   Esperado em: {CAMINHO_DADOS}")
    print(f"\n   Certifique-se de copiar a pasta DADOS_SINARM para:")
    print(f"   {Path(__file__).parent}")
    exit(1)

df_ocorrencias = pd.read_csv(
    CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
    sep=';',
    encoding='latin1'
)

print(f"[OK] {len(df_ocorrencias):,} ocorrências carregadas\n")

# Verificar colunas
print("Colunas disponíveis:")
print(df_ocorrencias.columns.tolist())
print()

# Mostrar exemplo de linha
print("Exemplo de linha (formato atual):")
print(df_ocorrencias.iloc[0].to_dict())
print()

# ===== FUNÇÃO PARA CRIAR DOCUMENTO DESCRITIVO =====

def criar_documento_descritivo(row):
    """
    Transforma linha CSV em texto rico para embedding
    
    ANTES (CSV):
    ID | MARCA | TIPO | ...
    1  | TAURUS| PISTOLA | ...
    
    DEPOIS (Texto Descritivo):
    "Ocorrência ID 1: Pistola marca Taurus calibre 9mm,
     situação Roubado em Brasília-DF em 15/03/2026.
     Tipo de ocorrência: Roubo de veículo.
     Número de série: ABC123456."
    """
    
    doc = f"""
Ocorrência ID: {row.get('ID', 'N/A')}
Arma: {row.get('MARCA', 'N/A')} {row.get('TIPO', 'N/A')} calibre {row.get('CALIBRE', 'N/A')}
Situação: {row.get('SITUACAO', 'N/A')}
Localização: {row.get('CIDADE', 'N/A')}, {row.get('UF', 'N/A')}
Data: {row.get('DATA', 'N/A')}
Tipo de ocorrência: {row.get('TIPO_OCORRENCIA', 'N/A')}
Número de série: {row.get('NUMERO_SERIE', 'N/A')}
Observações: {row.get('OBSERVACOES', 'N/A')}
""".strip()
    
    return doc

# ===== CRIAR DOCUMENTOS =====

print("[PROC] Transformando linhas CSV em documentos descritivos...")
print("(Isso pode levar alguns minutos para 300k registros)\n")

# Limitar para teste inicial (remover .head() para processar tudo)
df_sample = df_ocorrencias.head(1000)  # 1000 registros para teste rápido
# df_sample = df_ocorrencias  # Descomentar para processar todos

documentos = []
metadados = []

for idx, row in df_sample.iterrows():
    doc = criar_documento_descritivo(row)
    documentos.append(doc)
    
    # Guardar metadados (ID original para rastreabilidade)
    metadados.append({
        'id': row.get('ID', idx),
        'marca': row.get('MARCA', 'N/A'),
        'tipo': row.get('TIPO', 'N/A'),
        'situacao': row.get('SITUACAO', 'N/A')
    })
    
    # Progresso
    if (idx + 1) % 100 == 0:
        print(f"  Processados: {idx + 1:,} registros...")

print(f"\n[OK] {len(documentos):,} documentos criados!")
print()

# Mostrar exemplo de documento transformado
print("="*70)
print("EXEMPLO DE DOCUMENTO TRANSFORMADO:")
print("="*70)
print(documentos[0])
print("="*70)
print()

# ===== SALVAR DOCUMENTOS =====

OUTPUT_DIR = Path(__file__).parent.parent / "03_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

print("[SAVE] Salvando documentos...")

# Salvar lista de documentos
with open(OUTPUT_DIR / "documentos.json", 'w', encoding='utf-8') as f:
    json.dump(documentos, f, ensure_ascii=False, indent=2)

# Salvar metadados
with open(OUTPUT_DIR / "metadados.json", 'w', encoding='utf-8') as f:
    json.dump(metadados, f, ensure_ascii=False, indent=2)

print(f"[OK] Documentos salvos em: {OUTPUT_DIR / 'documentos.json'}")
print(f"[OK] Metadados salvos em: {OUTPUT_DIR / 'metadados.json'}")
print()

# ===== ESTATÍSTICAS =====

print("="*70)
print("ESTATÍSTICAS:")
print("="*70)
print(f"Total de documentos: {len(documentos):,}")
print(f"Tamanho médio (caracteres): {sum(len(d) for d in documentos) / len(documentos):.0f}")
print(f"Maior documento: {max(len(d) for d in documentos):,} caracteres")
print(f"Menor documento: {min(len(d) for d in documentos):,} caracteres")
print()

print("[OK] PASSO 1 CONCLUÍDO!")
print("[INFO]  Próximo: Execute 02_gerar_embeddings.py")


