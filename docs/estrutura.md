# Estrutura do Projeto

```
bairro-score/
├── README.md
├── docs/
│   ├── pesquisa-mercado.md
│   ├── plano-90-dias.md
│   └── fontes-dados.md
├── scrapers/
│   ├── ssp_sp.py          # Criminalidade SSP-SP
│   ├── fipezap.py         # Preços FipeZap
│   ├── inep.py            # Escolas INEP
│   └── transporte.py      # Metrô/ônibus
├── data/
│   ├── raw/               # Dados brutos coletados
│   └── processed/         # Dados limpos e normalizados
├── scoring/
│   └── calculate.py       # Algoritmo de score por bairro
├── site/                   # Frontend (Astro/Next.js)
│   ├── src/
│   │   ├── pages/         # Páginas geradas
│   │   ├── components/    # Componentes reutilizáveis
│   │   └── layouts/       # Layouts base
│   └── public/
└── scripts/
    └── generate-pages.py  # Gera páginas a partir dos dados
```
