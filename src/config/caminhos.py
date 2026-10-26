from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

#DATA_DIR = BASE_DIR / 'data'
DATA_PROCESSED = BASE_DIR / 'data' / 'processed'
DATA_RAW       = BASE_DIR / 'data' /'raw'

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
DATA_RAW.mkdir(parents=True, exist_ok=True)


#Path(__file__) representa o arquivo atual
# Path(__file__).resolve() Transforma em um caminho absoluto: C:/Users/Fabiano/meu_projeto/src/config/caminhos.py

#Código	Resultado
#Path(__file__)	Caminho do arquivo caminhos.py
#.resolve()	Caminho absoluto do arquivo
#.parent	Pasta config
#.parent.parent	Pasta src
#.parent.parent.parent	Raiz meu_projeto
















"""from pathlib import Path

BASE_DIR =  Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / 'data'
DATA_RAW = DATA_DIR / 'raw'
DATA_PROCESSED = DATA_DIR / 'processed'

DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
"""