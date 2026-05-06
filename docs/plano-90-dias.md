# Plano 30-60-90 dias

## Semana 1-2: Coleta de Dados

### Tarefas
1. Scraper SSP-SP (criminalidade por distrito/mês)
   - Fonte: http://www.ssp.sp.gov.br/estatistica/dados-mensais
   - Dados: roubos, furtos, homicídios por distrito
   - Output: CSV com distrito, tipo_crime, quantidade, mês

2. Scraper FipeZap (preço m² por bairro)
   - Fonte: https://fipezap.zapimoveis.com.br
   - Dados: preço médio venda e aluguel por bairro
   - Output: CSV com bairro, preco_venda_m2, preco_aluguel_m2

3. Dados INEP (escolas)
   - Fonte: microdados INEP (download direto)
   - Dados: nota IDEB por escola, geolocalização
   - Output: CSV com escola, nota, lat, lng, distrito

4. Dados de transporte
   - Metrô: estações com lat/lng (manual ou API)
   - Calcular distância de cada bairro à estação mais próxima

### Entregável
- Pasta `/data/raw/` com todos os CSVs brutos
- Pasta `/data/processed/` com dados limpos e normalizados

## Semana 3-4: Score + Geração de Páginas

### Algoritmo de Score (v1 - simples)
```
score_seguranca = normalizar(inverso(crimes_per_capita), 0-10)
score_preco = normalizar(inverso(preco_m2), 0-10)  # mais barato = nota maior
score_escolas = normalizar(media_ideb_distrito, 0-10)
score_transporte = normalizar(inverso(distancia_metro), 0-10)

score_geral = (seguranca * 0.3) + (preco * 0.2) + (escolas * 0.25) + (transporte * 0.25)
```

### Geração de páginas
- Template: página de bairro com scores, dados, mapa
- Gerar 96 páginas (1 por distrito de SP)
- Gerar 10 rankings temáticos ("mais seguros", "mais baratos", etc)
- Gerar 20 comparações populares ("Pinheiros vs Vila Madalena")

### Stack
- Astro ou Next.js (SSG) — gera HTML estático
- Tailwind CSS pra estilo
- Chart.js ou similar pra gráficos
- Deploy: Vercel (grátis pra sites estáticos)

### Entregável
- Site funcional com ~130 páginas
- Deploy em produção
- Sitemap.xml submetido ao Google Search Console

## Semana 5-8: SEO + Conteúdo

### SEO técnico
- Meta title e description únicos por página
- Schema markup (Place, LocalBusiness)
- Internal linking (cada bairro linka pra vizinhos e comparações)
- Open Graph tags pra compartilhamento social
- Core Web Vitals otimizados (site estático = rápido)

### Conteúdo adicional
- 1 parágrafo editorial único por bairro (pode usar AI + revisão)
- Seção "Perguntas frequentes" por bairro
- Gerar mais 50 comparações
- Criar 5 calculadoras (custo de vida, financiamento, aluguel vs compra)

### Entregável
- ~300 páginas indexadas
- Primeiras impressões no Google Search Console

## Mês 3-4: Tráfego + Monetização

### Monitoramento
- Google Search Console: impressões, cliques, posição média
- Google Analytics: pageviews, tempo na página, bounce rate
- Identificar quais páginas estão rankeando e dobrar nelas

### Monetização
- Aplicar Google AdSense (requisito: conteúdo original, ~30 páginas)
- Se tráfego > 10k/mês: testar Ezoic (sem mínimo rígido)
- Se tráfego > 50k/mês: aplicar Mediavine (paga 3-5x mais que AdSense)

### Expansão
- Adicionar Rio de Janeiro (mesmas fontes de dados)
- Adicionar mais calculadoras
- Criar blog com artigos longos ("Guia completo pra morar em Pinheiros")

## Mês 5-6: Escala

- 3-4 cidades cobertas
- 1000+ páginas indexadas
- Meta: 50-100k pageviews/mês
- Receita: R$1-4k/mês em ads
- Avaliar afiliados de imobiliárias
