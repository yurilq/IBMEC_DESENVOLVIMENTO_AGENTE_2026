# 🔧 SOLUÇÃO: Erro de DLL do PyTorch no Windows

## ❌ ERRO IDENTIFICADO

```
OSError: [WinError 1114] Uma rotina de inicialização da biblioteca de vínculo dinâmico (DLL) falhou. 
Error loading "torch\lib\c10.dll" or one of its dependencies.
```

## ✅ CAUSA

PyTorch precisa de bibliotecas C++ do Visual Studio que podem não estar instaladas no Windows.

## 🛠️ SOLUÇÕES (em ordem de prioridade)

### Solução 1: Instalar Visual C++ Redistributable (RECOMENDADO)

1. **Baixar e instalar:**
   - Link: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Executar o instalador
   - Reiniciar o computador

2. **Testar novamente:**
   ```bash
   python -c "import torch; print(torch.__version__)"
   ```

### Solução 2: Reinstalar PyTorch

```bash
# Desinstalar PyTorch atual
pip uninstall torch torchvision torchaudio

# Reinstalar versão CPU (mais leve)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Solução 3: Usar Conda (alternativa)

Se as soluções acima não funcionarem:

```bash
# Instalar Miniconda
# Link: https://docs.conda.io/en/latest/miniconda.html

# Criar ambiente
conda create -n e5 python=3.11

# Ativar ambiente
conda activate e5

# Instalar PyTorch via conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Instalar outras dependências
pip install sentence-transformers faiss-cpu PyPDF2 pandas scikit-learn langchain-core
```

### Solução 4: Usar Google Colab (temporária)

Se nenhuma solução funcionar localmente, use Google Colab:

1. Acessar: https://colab.research.google.com/
2. Upload do notebook E5
3. Executar no Colab (tem todas as dependências)

## 🧪 VALIDAR INSTALAÇÃO

Após aplicar qualquer solução, execute:

```bash
python E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\04_MATERIAL_APOIO\validar_ambiente.py
```

**Resultado esperado:**
```
[2/6] Verificando dependencias...
  OK: pandas
  OK: numpy
  OK: scikit-learn
  OK: langchain-core
  OK: sentence-transformers  ← DEVE APARECER
  OK: faiss-cpu
  OK: PyPDF2
  OK: transformers
  OK: torch  ← DEVE APARECER
```

## 📋 CHECKLIST DE SOLUÇÃO

- [ ] Solução 1: Instalar Visual C++ Redistributable
- [ ] Reiniciar computador
- [ ] Testar: `python -c "import torch"`
- [ ] Se falhar: Solução 2 (reinstalar PyTorch)
- [ ] Se falhar: Solução 3 (usar Conda)
- [ ] Se falhar: Solução 4 (usar Google Colab)

## 🎯 PRÓXIMOS PASSOS

Após resolver o problema de DLL:

1. ✅ Validar ambiente: `python validar_ambiente.py`
2. ✅ Abrir Jupyter: `jupyter notebook`
3. ✅ Executar notebook E5 sequencialmente

## 📚 RECURSOS

- **Visual C++ Redistributable:** https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
- **PyTorch Installation:** https://pytorch.org/get-started/locally/
- **Conda Installation:** https://docs.conda.io/en/latest/miniconda.html
- **Google Colab:** https://colab.research.google.com/

## ⚠️ OBSERVAÇÃO IMPORTANTE

Este erro é **específico do Windows** e **não afeta o conteúdo do notebook**.

O notebook E5 está **100% correto** e funcionará perfeitamente após resolver o problema de DLL.

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Solução documentada
