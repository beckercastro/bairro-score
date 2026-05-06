"""
BairroScore - Scoring Engine
Calcula scores 0-10 por bairro baseado nos dados coletados.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_FILE = os.path.join(DATA_DIR, 'raw', 'cotia', 'cotia_dados_consolidados.json')
OUTPUT_DIR = os.path.join(DATA_DIR, 'processed')


def load_data():
    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def score_seguranca(data):
    """
    Score de segurança baseado na taxa de crimes por 100k hab.
    Compara com média do estado de SP.
    Escala: 0 (muito perigoso) a 10 (muito seguro)
    """
    taxas = data['seguranca']['taxas_por_100k_hab']
    media_sp_hom = data['seguranca']['comparativo_estado']['media_sp_homicidio_100k']
    
    # Peso por gravidade
    score_hom = max(0, 10 - (taxas['homicidio_doloso'] / media_sp_hom) * 5)
    score_roubo = max(0, 10 - (taxas['roubo'] / 500) * 10)  # 500/100k = nota 0
    score_furto = max(0, 10 - (taxas['furto'] / 1000) * 10)  # 1000/100k = nota 0
    
    # Média ponderada
    score = (score_hom * 0.5) + (score_roubo * 0.3) + (score_furto * 0.2)
    return round(min(10, max(0, score)), 1)


def score_custo(bairro_data):
    """
    Score de custo (mais barato = nota maior).
    Referência: m² mais caro da região (Granja Viana) = nota 1
    """
    preco = bairro_data['preco_m2_casa']
    # Escala: R$1000/m² = 10, R$7000/m² = 1
    score = 10 - ((preco - 1000) / (7000 - 1000)) * 9
    return round(min(10, max(1, score)), 1)


def score_educacao(data):
    """Score de educação baseado no IDEB médio. IDEB 7+ = nota 10, IDEB 4 = nota 4"""
    ideb = data['educacao']['ideb_medio']
    score = (ideb / 7.0) * 10
    return round(min(10, max(0, score)), 1)


def score_transporte(dist_metro_km):
    """Score de transporte baseado na distância ao metrô. 0km=10, 40km=1"""
    score = 10 - ((dist_metro_km / 40) * 9)
    return round(min(10, max(1, score)), 1)


def calculate_scores():
    data = load_data()
    
    seg_score = score_seguranca(data)
    edu_score = score_educacao(data)
    
    bairros_scores = {}
    
    for bairro_key, bairro_data in data['imoveis']['bairros'].items():
        # Distância ao metrô por bairro
        dist_metro = {
            'caucaia_do_alto': 35,
            'granja_viana': 15,
            'centro': 20,
            'jardim_da_gloria': 22,
            'parque_sao_george': 23,
        }
        
        custo = score_custo(bairro_data)
        transp = score_transporte(dist_metro.get(bairro_key, 25))
        
        # Score geral: ponderado
        geral = (seg_score * 0.30) + (custo * 0.20) + (edu_score * 0.25) + (transp * 0.25)
        
        bairros_scores[bairro_key] = {
            "nome": bairro_key.replace('_', ' ').title(),
            "municipio": "Cotia",
            "score_geral": round(geral, 1),
            "scores": {
                "seguranca": seg_score,
                "custo": custo,
                "educacao": edu_score,
                "transporte": transp
            },
            "dados": {
                "preco_m2_casa": bairro_data['preco_m2_casa'],
                "preco_m2_terreno": bairro_data['preco_m2_terreno'],
                "aluguel_medio_2q": bairro_data['aluguel_medio_2q'],
                "distancia_metro_km": dist_metro.get(bairro_key, 25),
                "tipo_predominante": bairro_data['tipo_predominante']
            }
        }
    
    return bairros_scores


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    scores = calculate_scores()
    
    output_path = os.path.join(OUTPUT_DIR, 'cotia_scores.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("BairroScore - Scoring Engine")
    print("=" * 60)
    print(f"\n📊 Scores calculados pra {len(scores)} bairros de Cotia:\n")
    
    # Ordenar por score geral
    sorted_bairros = sorted(scores.items(), key=lambda x: x[1]['score_geral'], reverse=True)
    
    print(f"{'Pos':<4} {'Bairro':<22} {'Geral':<7} {'Seg':<5} {'$':<5} {'Edu':<5} {'Transp':<6}")
    print("-" * 60)
    
    for i, (key, s) in enumerate(sorted_bairros, 1):
        print(f"{i:<4} {s['nome']:<22} {s['score_geral']:<7} "
              f"{s['scores']['seguranca']:<5} {s['scores']['custo']:<5} "
              f"{s['scores']['educacao']:<5} {s['scores']['transporte']:<6}")
    
    print(f"\n💾 Salvo em: {output_path}")


if __name__ == "__main__":
    main()
