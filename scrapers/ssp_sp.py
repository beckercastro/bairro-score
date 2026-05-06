"""
BairroScore - Scraper SSP-SP
Coleta dados de criminalidade por município do portal de transparência da SSP-SP.

O portal usa ASP.NET com ViewState/EventValidation (postback).
Precisamos simular a navegação: selecionar crime → ano → mês → extrair tabela.

URL: http://www.ssp.sp.gov.br/transparenciassp/Consultas.aspx
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import time

BASE_URL = "http://www.ssp.sp.gov.br/transparenciassp/Consultas.aspx"

# Tipos de crime disponíveis no portal
CRIMES = {
    "homicidio_doloso": "Homicicio",  # sim, é com typo no portal
    "latrocinio": "Latrocinio",
    "furto_veiculo": "FurtoVeiculo",
    "roubo_veiculo": "RouboVeiculo",
    "furto_celular": "FurtoCelular",
    "roubo_celular": "RouboCelular",
}


def get_viewstate(soup):
    """Extrai __VIEWSTATE e __EVENTVALIDATION do HTML"""
    vs = soup.find("input", {"id": "__VIEWSTATE"})
    ev = soup.find("input", {"id": "__EVENTVALIDATION"})
    return {
        "__VIEWSTATE": vs["value"] if vs else "",
        "__EVENTVALIDATION": ev["value"] if ev else "",
    }


def scrape_ssp_municipio(crime_key, ano, mes, municipio_filter="Cotia"):
    """
    Scrapa dados da SSP-SP pra um crime/ano/mês específico.
    Retorna DataFrame com dados por município.
    """
    crime_name = CRIMES[crime_key]
    ano_str = str(ano)[-2:]  # últimos 2 dígitos
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    
    # Step 1: GET inicial pra pegar ViewState
    print(f"  [1/4] Acessando portal SSP-SP...")
    r = session.get(BASE_URL, timeout=30)
    soup = BeautifulSoup(r.content, "html.parser")
    state = get_viewstate(soup)
    
    # Step 2: POST selecionando o crime
    print(f"  [2/4] Selecionando crime: {crime_key}...")
    data = {
        "__EVENTTARGET": f"ctl00$cphBody$btn{crime_name}",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": state["__VIEWSTATE"],
        "__EVENTVALIDATION": state["__EVENTVALIDATION"],
        "ctl00$cphBody$hdfExport": "",
    }
    r = session.post(BASE_URL, data=data, timeout=30)
    soup = BeautifulSoup(r.content, "html.parser")
    state = get_viewstate(soup)
    time.sleep(1)
    
    # Step 3: POST selecionando o ano
    print(f"  [3/4] Selecionando ano: {ano}...")
    data = {
        "__EVENTTARGET": f"ctl00$cphBody$lkAno{ano_str}",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": state["__VIEWSTATE"],
        "__EVENTVALIDATION": state["__EVENTVALIDATION"],
        "ctl00$cphBody$filtroDepartamento": "0",
        "ctl00$cphBody$hdfExport": "",
    }
    r = session.post(BASE_URL, data=data, timeout=30)
    soup = BeautifulSoup(r.content, "html.parser")
    state = get_viewstate(soup)
    time.sleep(1)
    
    # Step 4: POST selecionando o mês
    print(f"  [4/4] Selecionando mês: {mes}...")
    data = {
        "__EVENTTARGET": f"ctl00$cphBody$lkMes{mes}",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": state["__VIEWSTATE"],
        "__EVENTVALIDATION": state["__EVENTVALIDATION"],
        "ctl00$cphBody$filtroDepartamento": "0",
        "ctl00$cphBody$hdfExport": "",
    }
    r = session.post(BASE_URL, data=data, timeout=30)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # Extrair tabela
    table = soup.find("table", {"id": "ctl00_cphBody_grdListBO"})
    if not table:
        print(f"  ⚠️  Tabela não encontrada. Portal pode ter mudado.")
        return None
    
    rows = []
    for tr in table.find_all("tr")[1:]:  # skip header
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells and len(cells) >= 2:
            rows.append(cells)
    
    if not rows:
        print(f"  ⚠️  Nenhum dado encontrado.")
        return None
    
    df = pd.DataFrame(rows)
    print(f"  ✅ {len(rows)} registros encontrados")
    
    # Filtrar por município se especificado
    if municipio_filter:
        df_filtered = df[df.apply(lambda row: municipio_filter.lower() in " ".join(row.astype(str)).lower(), axis=1)]
        if not df_filtered.empty:
            print(f"  📍 {len(df_filtered)} registros pra {municipio_filter}")
            return df_filtered
    
    return df


def collect_cotia_data():
    """Coleta todos os crimes disponíveis pra Cotia no último ano"""
    results = {}
    ano = 2025
    
    for crime_key in CRIMES:
        print(f"\n{'='*50}")
        print(f"Coletando: {crime_key} ({ano})")
        print(f"{'='*50}")
        
        monthly_data = []
        for mes in range(1, 13):
            try:
                df = scrape_ssp_municipio(crime_key, ano, mes, "Cotia")
                if df is not None:
                    monthly_data.append({"mes": mes, "dados": df.to_dict()})
            except Exception as e:
                print(f"  ❌ Erro mês {mes}: {e}")
            time.sleep(2)  # rate limiting
        
        results[crime_key] = monthly_data
    
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("BairroScore - Scraper SSP-SP")
    print("Testando coleta pra Cotia/SP")
    print("=" * 60)
    
    # Teste com um único crime/mês pra validar
    print("\n🧪 Teste: Homicídio doloso, Jan/2025, Cotia")
    try:
        df = scrape_ssp_municipio("homicidio_doloso", 2025, 1, "Cotia")
        if df is not None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'ssp_sp')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'teste_cotia.csv')
            df.to_csv(output_path, index=False)
            print(f"\n💾 Salvo em: {output_path}")
        else:
            print("\n⚠️  Scraper não retornou dados.")
            print("   Possíveis causas:")
            print("   - Portal SSP-SP mudou a estrutura")
            print("   - Netskope/proxy bloqueando a conexão")
            print("   - Portal requer JavaScript (precisa Selenium)")
            print("\n   Alternativa: usar dados consolidados do SEADE")
            print("   https://repositorio.seade.gov.br/")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("   O portal SSP-SP pode precisar de Selenium.")
        print("   Vamos tentar fonte alternativa (SEADE/dados abertos).")
