# BairroScore

Plataforma de ranking e comparação de bairros no Brasil, com dados de segurança, preço, escolas, transporte e qualidade de vida.

## Modelo de Negócio

- **Receita**: Ads (Google AdSense/Mediavine) + Afiliados (QuintoAndar, Zap, Loft)
- **Custo**: Hosting (~R$50/mês) + Domínio (~R$40/ano)
- **Meta**: 50-100k visitas/mês em 6 meses → R$2-10k/mês

## Stack Técnico

- **Scraper/Data Pipeline**: Python (requests, BeautifulSoup, pandas)
- **Backend/Gerador de páginas**: Next.js ou Astro (SSG - Static Site Generation)
- **Frontend**: React/Tailwind (esposa)
- **Hosting**: Vercel ou Cloudflare Pages (grátis)
- **Dados**: Arquivos JSON/CSV gerados pelo pipeline

## Fontes de Dados (públicas e gratuitas)

| Fonte | Dados | URL |
|-------|-------|-----|
| SSP-SP | Criminalidade por distrito | http://www.ssp.sp.gov.br/estatistica/dados-mensais |
| FipeZap | Preço m² por bairro | https://fipezap.zapimoveis.com.br |
| INEP/MEC | Notas de escolas (IDEB) | https://www.gov.br/inep |
| IBGE | Censo, renda, demografia | https://www.ibge.gov.br |
| SPTrans | Linhas de ônibus | https://www.sptrans.com.br |
| Metrô SP | Estações e linhas | https://www.metro.sp.gov.br |
| GeoSampa | Dados geográficos SP | https://geosampa.prefeitura.sp.gov.br |

## Estrutura de Páginas (SEO)

Cada bairro gera múltiplas páginas:
- `/sp/pinheiros` — Página principal do bairro (score, resumo)
- `/sp/pinheiros-vs-vila-mariana` — Comparação entre bairros
- `/sp/bairros-mais-seguros` — Rankings temáticos
- `/sp/bairros-baratos-perto-do-metro` — Listas filtradas
- `/calculadora/custo-de-vida` — Ferramentas interativas

## Roadmap

### Fase 1 - MVP (Semanas 1-4)
- [ ] Coletar dados SSP-SP (criminalidade)
- [ ] Coletar dados FipeZap (preços)
- [ ] Coletar dados INEP (escolas)
- [ ] Criar score/nota por bairro (algoritmo simples)
- [ ] Gerar páginas estáticas pra 96 distritos de SP
- [ ] Deploy no Vercel/Cloudflare
- [ ] Submeter sitemap pro Google

### Fase 2 - Conteúdo (Semanas 5-8)
- [ ] Gerar páginas de comparação (top 50 pares)
- [ ] Criar rankings temáticos (segurança, preço, famílias)
- [ ] Adicionar calculadora de custo de vida
- [ ] Otimizar SEO (meta tags, schema markup, internal links)

### Fase 3 - Escala (Meses 3-6)
- [ ] Expandir pra Rio de Janeiro
- [ ] Expandir pra BH, Curitiba, Porto Alegre
- [ ] Aplicar pra Google AdSense
- [ ] Adicionar afiliados (QuintoAndar, Zap)
- [ ] Monitorar tráfego e ajustar conteúdo

## Monetização Estimada

| Visitas/mês | RPM (BR) | Receita/mês |
|-------------|----------|-------------|
| 10k | R$15-30 | R$150-300 |
| 50k | R$15-30 | R$750-1500 |
| 100k | R$20-40 | R$2000-4000 |
| 200k | R$20-40 | R$4000-8000 |

*RPM = receita por mil pageviews. Nicho imobiliário paga acima da média.*
