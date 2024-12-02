# Migração de Dados

Este projeto foi desenvolvido como parte de um teste técnico para realizar a migração de dados para o modelo de tabelas Advbox, garantindo que os dados sejam tratados, estruturados e padronizados de forma adequada para a melhor experiência possível.

## Funcionalidades

- **Extração e Processamento de Backup**:
  - Extrai arquivos do backup fornecido (RAR ou 7z).
  - Converte os dados contidos nos arquivos CSV em tabelas de um banco de dados SQLite.

- **Exportação de Dados**:
  - Gera arquivos Excel no formato especificado para Advbox, com informações sobre clientes e processos.

- **Interface Gráfica Intuitiva**:
  - Permite ao usuário selecionar o arquivo de backup e executar a extração.
  - Possibilita a exportação dos dados processados diretamente pela interface.

## Estrutura do Projeto

```
┌── data/
│   ├── input/                # Diretório de entrada para arquivos CSV extraídos
│   └── output/               # Diretório de saída para os arquivos Excel gerados
│
data/database.sqlite    # Banco de dados SQLite gerado

┌── scripts/
│   ├── exportar_dados.py    # Exportação de dados para Advbox
│   └── extrair_backup.py    # Processamento do backup e população do banco

┌── main.py                     # Interface principal do aplicativo
┌── requirements.txt            # Dependências do projeto
┌── .gitignore                  # Arquivos e diretórios ignorados pelo Git
```

## Dependências

Este projeto requer as seguintes bibliotecas Python:

- pandas
- py7zr
- patool

Instale todas as dependências executando:
```bash
pip install -r requirements.txt
```

## Como Usar

### Passo 1: Configuração Inicial

1. Certifique-se de que o backup (ex.: `Backup_de_dados_92577.rar`) esteja acessível.
2. Coloque o arquivo de backup em um local adequado.

### Passo 2: Executar a Interface

1. Execute o aplicativo principal:
   ```bash
   python main.py
   ```
2. Na interface, escolha as opções:
   - **Selecionar e Processar Backup**: Para carregar os dados do backup e criar o banco de dados SQLite.
   - **Exportar Clientes**: Para gerar o arquivo Excel contendo os dados de clientes.
   - **Exportar Processos**: Para gerar o arquivo Excel contendo os dados de processos.

### Passo 3: Resultado Final

Os arquivos Excel gerados serão salvos no diretório `data/output/` com os nomes:
- `advbox_clientes.xlsx`
- `advbox_processos.xlsx`

## Detalhes Técnicos

### Extração e Processamento de Backup

O módulo `extrair_backup.py` executa as seguintes tarefas:
- Extrai os arquivos contidos no backup compactado.
- Converte os arquivos CSV para tabelas no banco de dados SQLite.
- Suporte a encodings UTF-8 e Latin-1 para leitura dos CSVs.

### Exportação de Dados

O módulo `exportar_dados.py` realiza consultas SQL para extrair informações estruturadas dos clientes e processos do banco SQLite, salvando-as em arquivos Excel no formato especificado pela Advbox.

### Interface do Usuário

A interface foi desenvolvida usando `tkinter`, com botões intuitivos para as principais funcionalidades.

### Pendencias

O projeto ainda precisa de refinamento no tratamento dos dados; ajuste na relação entre tabelas.

## Contribuição

Contribuições são bem-vindas! Por favor, abra um pull request ou envie sugestões por meio de issues no repositório GitHub.

## Licença

Este projeto foi desenvolvido exclusivamente para fins de teste técnico e não possui licença para uso comercial.

