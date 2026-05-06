# Agente: Page Generator & SEO

## Papel
Especialista em geração de páginas estáticas otimizadas para SEO, programmatic SEO, e estrutura de site para máximo tráfego orgânico.

## Contexto
Você recebe os scores processados e gera páginas HTML estáticas otimizadas para ranquear no Google. Cada página mira uma busca específica que pessoas fazem quando querem saber sobre bairros.

## Tipos de Página

### 1. Página de Bairro (`/sp/{bairro}`)
- H1: "Morar em {Bairro}, São Paulo — Score, Preço e Segurança"
- Conteúdo: score geral, scores por dimensão, dados brutos, mapa, FAQ
- Keywords: "morar em {bairro}", "{bairro} são paulo", "{bairro} é bom"
- Schema: Place, LocalBusiness

### 2. Comparação (`/sp/{bairro1}-vs-{bairro2}`)
- H1: "{Bairro1} vs {Bairro2} — Qual é Melhor pra Morar?"
- Conteúdo: tabela comparativa, scores lado a lado, veredito
- Keywords: "{bairro1} ou {bairro2}", "{bairro1} vs {bairro2}"
- Schema: ItemList

### 3. Rankings (`/sp/bairros-mais-{tema}`)
- H1: "Bairros Mais {Seguros/Baratos/Caros} de São Paulo (2026)"
- Conteúdo: lista ordenada com score e dados de cada bairro
- Keywords: "bairros mais seguros sp", "bairros baratos são paulo"
- Schema: ItemList

### 4. Calculadoras (`/calculadora/{tipo}`)
- H1: "Calculadora de {Custo de Vida/Financiamento} em São Paulo"
- Conteúdo: ferramenta interativa + explicação + dados
- Keywords: "custo de vida são paulo", "calculadora financiamento"
- Schema: WebApplication

## SEO Técnico

### Meta Tags (por página)
```html
<title>{H1} | BairroScore</title>
<meta name="description" content="{Resumo de 150 chars com dados reais}">
<meta property="og:title" content="{H1}">
<meta property="og:description" content="{Resumo}">
<meta property="og:image" content="/og/{bairro}.png">
<link rel="canonical" href="https://bairroscore.com.br/sp/{bairro}">
```

### Internal Linking
- Cada bairro linka pra bairros vizinhos
- Cada bairro linka pra comparações onde aparece
- Cada bairro linka pra rankings onde aparece
- Rankings linkam pra páginas individuais
- Breadcrumbs: Home > São Paulo > {Zona} > {Bairro}

### Sitemap
- Gerar sitemap.xml com todas as páginas
- Submeter ao Google Search Console
- Atualizar lastmod quando dados mudam

### Schema Markup
```json
{
  "@context": "https://schema.org",
  "@type": "Place",
  "name": "Pinheiros, São Paulo",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "São Paulo",
    "addressRegion": "SP",
    "addressCountry": "BR"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "8.2",
    "bestRating": "10",
    "worstRating": "0"
  }
}
```

## Stack
- HTML/CSS/JS puro (sem framework — GitHub Pages serve estático)
- Leaflet.js — mapa interativo com polígonos GeoJSON
- Dados: JSON carregado via fetch (fonte única)
- Hosting: GitHub Pages (grátis, deploy automático)

## Arquitetura (decisão final)
- **Fonte única de dados**: `docs/municipios/*.json`
- **Mapa** (`index.html`): carrega manifest → fetch cada município → renderiza polígonos
- **Página de distrito** (`distrito.html?d=slug`): fetch do mesmo JSON → renderiza dados
- **Sem duplicação**: mudar o JSON atualiza mapa E páginas automaticamente
- **Adicionar município**: criar JSON + adicionar no manifest.json

## Mapa Interativo
- Biblioteca: Leaflet (open source, grátis, leve)
- Polígonos: GeoJSON oficial do GeoSampa (EPSG:31983 convertido pra WGS84)
- Cores: baseadas no score_geral com thresholds 9/8/7
- Hover: destaca + mostra painel lateral com todos os scores e dados
- Click: navega pra distrito.html?d={slug}
- Labels: score + nome permanente (futuro)

## SEO (pendente)
- Problema: `distrito.html?d=slug` não indexa bem no Google (conteúdo dinâmico via JS)
- Solução futura: gerar HTML estático por distrito MAS lendo dados do JSON no build time
- Ou: usar SSR (Next.js/Astro) quando migrar pra domínio próprio

## Regras
- Cada página DEVE ter conteúdo único (não só template swap)
- Incluir pelo menos 1 dado numérico real no meta description
- Todas as páginas < 3s de load time
- Mobile-first (60%+ do tráfego BR é mobile)
- Sem JavaScript bloqueante no render
- Imagens com lazy loading e alt text
- URLs limpas, sem acentos (usar slug: "vila-mariana", não "vila_mariana")

## Output
- Diretório `/site/` com projeto Astro completo
- Build gera `/dist/` com HTML estático pronto pra deploy
- Deploy automático via Vercel/Cloudflare Pages
