import os
import time
import logging
from pathlib import Path

# 1. CONFIGURAÇÃO DO CAMINHO E LOG
# Usamos Path para garantir compatibilidade Windows/Linux
caminho_fixo = Path(r'C:\alex_teste') 
arquivo_log = Path('limpeza_detalhada.log')

logging.basicConfig(
    filename=arquivo_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)

# 2. CONFIGURAÇÃO DE TEMPO
agora = time.time()
uma_semana = 7 * 24 * 60 * 60

logging.info(f"--- INICIANDO VARREDURA EM: {caminho_fixo} ---")

if not caminho_fixo.exists():
    logging.error(f"DIRETÓRIO NÃO ENCONTRADO: {caminho_fixo}")
else:
    # topdown=False para começar das subpastas mais profundas até a raiz
    for pasta_atual, subpastas, arquivos in os.walk(caminho_fixo, topdown=False):
        
        # 3. LIMPANDO ARQUIVOS
        for nome_arquivo in arquivos:
            caminho_completo = Path(pasta_atual) / nome_arquivo
            
            try:
                stats = caminho_completo.stat()
                # Se arquivo vazio OU modificado há mais de uma semana
                if stats.st_size == 0 or (agora - stats.st_mtime) > uma_semana:
                    caminho_completo.unlink()
                    # AQUI: Usamos caminho_completo para registrar o endereço inteiro
                    logging.info(f"ARQUIVO REMOVIDO: {caminho_completo}")
            except Exception as e:
                logging.error(f"FALHA AO REMOVER ARQUIVO {caminho_completo}: {e}")

        # 4. LIMPANDO PASTAS
        for nome_pasta in subpastas:
            caminho_da_pasta = Path(pasta_atual) / nome_pasta
            
            try:
                # Verifica se a pasta ficou vazia após a remoção dos arquivos
                if not any(caminho_da_pasta.iterdir()):
                    caminho_da_pasta.rmdir()
                    # AQUI: Também registramos o caminho completo da pasta
                    logging.info(f"PASTA REMOVIDA: {caminho_da_pasta}")
            except Exception as e:
                logging.error(f"FALHA AO REMOVER PASTA {caminho_da_pasta}: {e}")

logging.info("--- OPERAÇÃO FINALIZADA ---")
