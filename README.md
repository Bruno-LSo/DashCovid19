# Dashboard Epidemiológico da COVID-19

## Descrição
Este repositório contém um **dashboard interativo** desenvolvido em Python e Dash para análise epidemiológica da COVID-19 no Brasil (2020–2025). Permite explorar casos acumulados, novos casos e óbitos por estado ou para o Brasil como um todo.

## 📂 Estrutura do Repositório
```
.
├── imports.py        # Script para carregar, processar e salvar dados de referência
├── dashboard.py      # Script que executa o dashboard
├── df_states.csv     # Gerado por imports.py: dados por estado
├── df_brasil.csv      # Gerado por imports.py: dados do Brasil
├── geojson/
│   └── brazil_geo.json  # GeoJSON dos estados brasileiros
└── README.md         # Este arquivo
```

## 🔗 Obtenção dos Dados
Os dados originais são fornecidos pelo Ministério da Saúde:
1. Acesse: https://covid.saude.gov.br/
2. Na seção **"Arquivo CSV"**, baixe o arquivo disponibilizado.
3. Extraia os arquivos CSV na **pasta raiz** do repositório (onde estão `imports.py` e `dashboard.py`).

## Como Clonar o Repositório
No seu computador, abra um terminal e execute:
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```
> **Substitua** `https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git` pela URL real do repositório.

## Pré-requisitos
- **Python 3.7+** instalado
- **VSCode** instalado (ou outro editor de sua preferência)
- **Git** instalado
- Pacotes Python requeridos:
  - pandas
  - numpy
  - dash
  - dash-bootstrap-components
  - plotly

### Instalação das Dependências
No terminal do VSCode, dentro da pasta do projeto:
```bash
# (Opcional) Crie e ative um ambiente virtual
python -m venv venv
# Windows
env\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instale as bibliotecas necessárias
echo "pandas" "numpy" "dash" "dash-bootstrap-components" "plotly" > requirements.txt
pip install -r requirements.txt
```

## Gerar Arquivos de Referência
Execute o `imports.py` para carregar, pré-processar e salvar os dados:
```bash
python imports.py
```
Isso irá:
- Ler e concatenar todos os CSVs `HIST_PAINEL_COVIDBR*.csv` (`load_covid_panel`).
- Pré-processar colunas (`preprocess`):
  - Converte `estado` para maiúsculas, mantendo NaNs.
  - Transforma em valor absoluto as colunas de casos e óbitos.
- Separar em dois dataframes (`split_and_save`):
  - `df_states.csv` (dados estaduais)
  - `df_brasil.csv` (dados agregados do Brasil)

## Executar o Dashboard
Com os arquivos gerados, inicie o dashboard:
```bash
python dashboard.py
```
- O app será servido em `http://127.0.0.1:8051`.
- Abra seu navegador e acesse esse endereço.

## Passo a Passo no VSCode
1. **Abra o VSCode**.
2. Selecione **File > Open Folder** e escolha a pasta do projeto.
3. Abra o terminal integrado: **Terminal > New Terminal**.
4. (Opcional) Crie e ative um ambiente virtual:
   - `python -m venv venv`
   - Windows: `venv\\Scripts\\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Instale dependências: `pip install -r requirements.txt`.
6. Baixe e extraia os CSVs da COVID-19 na pasta do projeto.
7. Rode `python imports.py` e aguarde a geração de `df_states.csv` e `df_brasil.csv`.
8. Rode `python dashboard.py`.
9. Abra seu navegador em **http://127.0.0.1:8051** para visualizar o dashboard.

---

## Agradecimentos:
Agradeço à Asimov Academy  por me proporcionar o conhecimento necessario para o desenvolvimento desse projeto.

