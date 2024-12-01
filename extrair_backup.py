import os
import rarfile

def extrair_backup_rar(arquivo_backup, destino):
    """
    Extrai os arquivos de um backup compactado em formato .rar e salva na pasta de destino.

    Args:
        arquivo_backup (str): Caminho do arquivo compactado (.rar).
        destino (str): Caminho da pasta de destino onde os arquivos serão salvos.
    """
    # Garantir que a pasta de destino existe
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    try:
        # Verificar se o arquivo é um RAR válido
        if rarfile.is_rarfile(arquivo_backup):
            with rarfile.RarFile(arquivo_backup) as rar_ref:
                rar_ref.extractall(destino)
                print(f"Arquivos extraídos com sucesso para {destino}")
        else:
            print("O arquivo fornecido não é um arquivo RAR válido.")
    except Exception as e:
        print(f"Erro ao extrair o backup: {e}")

# Configurações
arquivo_backup = 'Backup_de_dados_92577.rar'  # Substituir pelo caminho do arquivo
destino = 'data/input'  # Pasta para salvar os arquivos extraídos

# Executar a extração
extrair_backup_rar(arquivo_backup, destino)
