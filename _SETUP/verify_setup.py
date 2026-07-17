#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE VERIFICACAO DA INSTALACAO
Agente Investigador SINARM E1

Verifica se todas as dependencias estao instaladas corretamente
e se o ambiente esta pronto para executar o agente.
"""

import sys
import os
from pathlib import Path

# Cores para output (funciona em Windows 10+ e Unix)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Imprime cabecalho formatado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    """Imprime mensagem de aviso"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    """Imprime mensagem informativa"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

def check_python_version():
    """Verifica a versao do Python"""
    print_header("VERIFICANDO PYTHON")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Versao do Python: {version_str}")
    
    if version.major < 3:
        print_error("Python 3 e necessario!")
        return False
    
    if version.major == 3 and version.minor < 8:
        print_error("Python 3.8+ e necessario!")
        print_info(f"Versao atual: {version_str}")
        return False
    
    if version.major == 3 and version.minor < 10:
        print_warning("Python 3.10+ e recomendado")
        print_info(f"Versao atual: {version_str}")
    else:
        print_success(f"Versao adequada: {version_str}")
    
    return True

def check_dependencies():
    """Verifica se as dependencias estao instaladas"""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    dependencies = {
        'langchain': 'LangChain',
        'langchain_core': 'LangChain Core',
        'langchain_community': 'LangChain Community',
        'langchain_ollama': 'LangChain Ollama',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
    }
    
    all_installed = True
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            
            # Tentar pegar a versao
            try:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'desconhecida')
                print_success(f"{name:25s} v{version}")
            except:
                print_success(f"{name:25s} (instalado)")
                
        except ImportError:
            print_error(f"{name:25s} (NAO INSTALADO)")
            all_installed = False
    
    return all_installed

def check_project_files():
    """Verifica se os arquivos do projeto existem"""
    print_header("VERIFICANDO ARQUIVOS DO PROJETO")
    
    required_files = [
        'E1_agente_react_v3.py',
        'E1_tools_sinarm.py',
        'TESTES_COMPLETOS.py',
        'requirements.txt',
        'README.md',
    ]
    
    required_dirs = [
        'DADOS_SINARM',
        'DADOS_SINARM/OCORRENCIAS',
        'DADOS_SINARM/PORTES',
        'DADOS_SINARM/REGISTROS',
        'DADOS_SINARM/REQUERIMENTOS',
    ]
    
    all_exist = True
    
    # Verificar arquivos
    for file in required_files:
        if Path(file).exists():
            print_success(f"Arquivo: {file}")
        else:
            print_error(f"Arquivo: {file} (NAO ENCONTRADO)")
            all_exist = False
    
    # Verificar diretorios
    for dir in required_dirs:
        dir_path = Path(dir)
        if dir_path.exists() and dir_path.is_dir():
            # Contar arquivos CSV
            csv_files = list(dir_path.glob('*.csv'))
            if csv_files:
                print_success(f"Diretorio: {dir} ({len(csv_files)} CSVs)")
            else:
                print_warning(f"Diretorio: {dir} (vazio)")
        else:
            print_error(f"Diretorio: {dir} (NAO ENCONTRADO)")
            all_exist = False
    
    return all_exist

def check_environment():
    """Verifica se esta em um ambiente virtual"""
    print_header("VERIFICANDO AMBIENTE VIRTUAL")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success("Executando dentro de ambiente virtual")
        print_info(f"Python prefix: {sys.prefix}")
        return True
    else:
        print_warning("NAO esta em um ambiente virtual")
        print_info("Recomenda-se usar um ambiente virtual (venv)")
        print_info("Execute: python -m venv venv")
        return False

def check_data_integrity():
    """Verifica a integridade basica dos dados"""
    print_header("VERIFICANDO INTEGRIDADE DOS DADOS")
    
    datasets = {
        'DADOS_SINARM/OCORRENCIAS': 4,
        'DADOS_SINARM/PORTES': 4,
        'DADOS_SINARM/REGISTROS': 9,
        'DADOS_SINARM/REQUERIMENTOS': 8,
    }
    
    all_ok = True
    
    for dir_path, expected_count in datasets.items():
        path = Path(dir_path)
        if not path.exists():
            print_error(f"{dir_path}: Diretorio nao encontrado")
            all_ok = False
            continue
        
        csv_files = list(path.glob('*.csv'))
        actual_count = len(csv_files)
        
        if actual_count == expected_count:
            print_success(f"{dir_path}: {actual_count}/{expected_count} arquivos CSV")
        elif actual_count > 0:
            print_warning(f"{dir_path}: {actual_count}/{expected_count} arquivos CSV")
        else:
            print_error(f"{dir_path}: Nenhum arquivo CSV encontrado")
            all_ok = False
    
    return all_ok

def test_imports():
    """Testa se os modulos podem ser importados"""
    print_header("TESTANDO IMPORTS")
    
    all_ok = True
    
    # Testar import do LangChain
    try:
        from langchain_ollama import OllamaLLM
        print_success("LangChain Ollama importado com sucesso")
    except ImportError as e:
        print_error(f"Falha ao importar LangChain Ollama: {e}")
        all_ok = False
    
    # Testar import do Pandas
    try:
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        print_success("Pandas importado e funcional")
    except Exception as e:
        print_error(f"Falha ao usar Pandas: {e}")
        all_ok = False
    
    # Testar import das tools (se existir)
    try:
        if Path('E1_tools_sinarm.py').exists():
            sys.path.insert(0, str(Path.cwd()))
            from E1_tools_sinarm import (
                buscar_ocorrencias,
                buscar_registros,
                buscar_portes,
                buscar_requerimentos
            )
            print_success("Tools SINARM importadas com sucesso")
        else:
            print_warning("Arquivo E1_tools_sinarm.py nao encontrado")
    except Exception as e:
        print_error(f"Falha ao importar tools SINARM: {e}")
        all_ok = False
    
    return all_ok

def print_summary(results):
    """Imprime resumo dos resultados"""
    print_header("RESUMO DA VERIFICACAO")
    
    total = len(results)
    passed = sum(results.values())
    
    for check, result in results.items():
        if result:
            print_success(f"{check}")
        else:
            print_error(f"{check}")
    
    print(f"\n{Colors.BOLD}Resultado: {passed}/{total} verificacoes passaram{Colors.END}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ TUDO PRONTO!{Colors.END}")
        print(f"{Colors.GREEN}O ambiente esta configurado corretamente.{Colors.END}\n")
        print("Proximo passo:")
        print(f"  {Colors.BLUE}python E1_agente_react_v3.py{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ ATENCAO!{Colors.END}")
        print(f"{Colors.YELLOW}Alguns componentes precisam de atencao.{Colors.END}\n")
        print("Solucoes:")
        print(f"  1. Execute: {Colors.BLUE}pip install -r requirements.txt{Colors.END}")
        print(f"  2. Verifique se todos os arquivos foram baixados corretamente")
        print(f"  3. Consulte o README.md para mais informacoes\n")
        return 1

def main():
    """Funcao principal"""
    print(f"\n{Colors.BOLD}VERIFICACAO DE INSTALACAO - AGENTE INVESTIGADOR SINARM E1{Colors.END}")
    
    results = {}
    
    # Executar verificacoes
    results['Versao do Python'] = check_python_version()
    results['Ambiente Virtual'] = check_environment()
    results['Dependencias'] = check_dependencies()
    results['Arquivos do Projeto'] = check_project_files()
    results['Integridade dos Dados'] = check_data_integrity()
    results['Imports de Modulos'] = test_imports()
    
    # Mostrar resumo
    return print_summary(results)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Verificacao interrompida pelo usuario.{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Erro inesperado: {e}{Colors.END}\n")
        sys.exit(1)
