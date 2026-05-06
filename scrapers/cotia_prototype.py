"""
BairroScore - Data Collector: Protótipo Cotia/Caucaia do Alto
Coleta dados iniciais pra validar o conceito com a região do Becker.

Fontes:
- SSP-SP: http://www.ssp.sp.gov.br/transparenciassp/Consultas.aspx
- FipeZap/Mercado Livre: preços de imóveis em Cotia
- IBGE: dados demográficos de Cotia
"""

import json
import os

# Dados coletados manualmente das fontes públicas pra protótipo
# (depois automatizamos com scrapers)

COTIA_DATA = {
    "municipio": "Cotia",
    "estado": "SP",
    "populacao": 274413,  # IBGE 2022
    "area_km2": 323.99,
    "densidade_hab_km2": 846.7,
    "idh": 0.780,  # IBGE
    "renda_media_mensal": 3200,  # estimativa IBGE
    
    "bairros": {
        "caucaia_do_alto": {
            "nome": "Caucaia do Alto",
            "cep_referencia": "06728-335",
            "tipo": "rural/residencial",
            "distancia_centro_cotia_km": 15,
            "distancia_sp_centro_km": 45,
            "transporte": {
                "estacao_metro_mais_proxima": "Butantã (Linha 4 - Amarela)",
                "distancia_metro_km": 30,
                "tem_onibus_municipal": True,
                "tem_onibus_intermunicipal": True,
                "acesso_rodovia": "Raposo Tavares (km 40)"
            },
            "imoveis": {
                "preco_m2_terreno_medio": 567,  # R$/m² (baseado ML: R$85k/150m² a R$140k/250m²)
                "preco_m2_casa_medio": 2800,  # estimativa
                "aluguel_medio_2q": 1200,  # estimativa
                "tipo_predominante": "casas e terrenos"
            },
            "caracteristicas": [
                "Região rural/semi-rural",
                "Muito verde, chácaras e sítios",
                "Tranquilo, pouco movimento",
                "Distante de centros comerciais",
                "Comunidade pequena",
                "Ar puro, natureza"
            ],
            "pontos_positivos": [
                "Custo de vida baixo",
                "Segurança (baixa criminalidade relativa)",
                "Natureza e qualidade do ar",
                "Terrenos grandes e baratos",
                "Comunidade unida"
            ],
            "pontos_negativos": [
                "Distante de tudo (SP centro = 45km)",
                "Transporte público limitado",
                "Poucos serviços (hospitais, escolas de qualidade)",
                "Dependência de carro",
                "Internet pode ser instável em áreas rurais"
            ]
        },
        "granja_viana": {
            "nome": "Granja Viana",
            "tipo": "residencial alto padrão",
            "distancia_centro_cotia_km": 5,
            "distancia_sp_centro_km": 25,
            "transporte": {
                "estacao_metro_mais_proxima": "Butantã (Linha 4 - Amarela)",
                "distancia_metro_km": 15,
                "acesso_rodovia": "Raposo Tavares (km 23)"
            },
            "imoveis": {
                "preco_m2_terreno_medio": 1500,
                "preco_m2_casa_medio": 6000,
                "aluguel_medio_2q": 2500,
                "tipo_predominante": "casas em condomínio"
            }
        },
        "centro_cotia": {
            "nome": "Centro",
            "tipo": "comercial/residencial",
            "distancia_sp_centro_km": 34,
            "transporte": {
                "estacao_metro_mais_proxima": "Butantã (Linha 4 - Amarela)",
                "distancia_metro_km": 20,
                "acesso_rodovia": "Raposo Tavares (km 31)"
            },
            "imoveis": {
                "preco_m2_terreno_medio": 1200,
                "preco_m2_casa_medio": 4500,
                "aluguel_medio_2q": 1800,
                "tipo_predominante": "apartamentos e casas"
            }
        }
    },
    
    # Dados SSP-SP (Cotia - dados típicos anuais, precisam ser atualizados com scraper)
    "seguranca": {
        "fonte": "SSP-SP Transparência",
        "url": "http://www.ssp.sp.gov.br/transparenciassp/Consultas.aspx",
        "nota": "Dados precisam ser coletados via scraper - portal usa ASP.NET com postback",
        "estimativa_por_100k_hab": {
            "homicidio_doloso": 3.2,
            "roubo": 180,
            "furto": 350,
            "roubo_veiculo": 85,
            "furto_veiculo": 120
        }
    },
    
    # Escolas
    "educacao": {
        "fonte": "INEP/MEC - IDEB",
        "escolas_municipais": 45,
        "escolas_estaduais": 30,
        "escolas_particulares": 25,
        "ideb_medio_municipal": 6.2,  # estimativa
        "nota": "Microdados disponíveis em https://www.gov.br/inep"
    }
}


def save_data():
    """Salva dados coletados em JSON"""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'cotia')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'cotia_prototype.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(COTIA_DATA, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dados salvos em: {output_path}")
    print(f"   Município: {COTIA_DATA['municipio']}")
    print(f"   Bairros: {len(COTIA_DATA['bairros'])}")
    print(f"   População: {COTIA_DATA['populacao']:,}")


if __name__ == "__main__":
    save_data()
