"""
AeroScan — Gerador de Mapa Interativo
Projeto FETIN 2026 — Equipe 49

Como usar:
  pip install folium pandas
  python gerar_mapa.py

O arquivo mapa_aeroscan.html será gerado na mesma pasta.
Abra no navegador para visualizar.
"""

import folium
import pandas as pd
import json
from folium.plugins import MarkerCluster, MiniMap, Fullscreen
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────
CENTRO_MAPA = [-22.2522, -45.7033]  # Centro da cidade
ZOOM_INICIAL = 15
ARQUIVO_SAIDA = "mapa_aeroscan.html"

# Caminhos dos arquivos de dados (mesma pasta do script)
BASE = Path(__file__).parent
CASOS_CSV    = BASE / "casos_dengue_mvp.csv"
FOCOS_CSV    = BASE / "focos_detectados_mvp.csv"
AREAS_CSV    = BASE / "areas_risco_mvp.csv"
GEOJSON_PATH = BASE / "marcadores_mapa_mvp.geojson"

# ─────────────────────────────────────────
# CORES E ÍCONES
# ─────────────────────────────────────────
COR_AREA = {
    "alto":  "#E74C3C",
    "medio": "#F39C12",
    "baixo": "#27AE60",
}

ICONE_FOCO = {
    "pneu":               ("tire",   "black",  "🔧"),
    "pool":               ("tint",   "blue",   "🏊"),
    "caixa_dagua_aberta": ("tint",   "blue",   "💧"),
    "terreno_baldio":     ("leaf",   "green",  "🌿"),
    "lixo_acumulado":     ("trash",  "gray",   "🗑️"),
}

# ─────────────────────────────────────────
# INICIALIZA O MAPA
# ─────────────────────────────────────────
print("🗺️  Iniciando mapa AeroScan...")

mapa = folium.Map(
    location=CENTRO_MAPA,
    zoom_start=ZOOM_INICIAL,
    tiles="OpenStreetMap",
)

Fullscreen(position="topright", title="Tela cheia").add_to(mapa)
MiniMap(toggle_display=True).add_to(mapa)

# ─────────────────────────────────────────
# GRUPOS DE CAMADAS
# ─────────────────────────────────────────
grupo_areas = folium.FeatureGroup(name="🟥 Áreas de Risco",              show=True)
grupo_casos = folium.FeatureGroup(name="🟠 Casos de Dengue",              show=True)
grupo_focos = folium.FeatureGroup(name="🔵 Focos Detectados pelo Drone",  show=True)

# ─────────────────────────────────────────
# 1. ÁREAS DE RISCO
# ─────────────────────────────────────────
print("📍 Adicionando áreas de risco...")

areas_df = pd.read_csv(AREAS_CSV)

with open(GEOJSON_PATH, encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    if feature["properties"]["tipo"] == "area_risco":
        props = feature["properties"]
        nivel = props.get("nivel_risco", "baixo")
        cor   = COR_AREA.get(nivel, "#95A5A6")

        folium.GeoJson(
            feature,
            style_function=lambda x, c=cor: {
                "fillColor": c,
                "color": c,
                "weight": 2,
                "fillOpacity": 0.18,
                "dashArray": "5, 5",
            },
            tooltip=folium.Tooltip(
                f"<b>{props.get('nome', '')}</b><br>"
                f"Risco: <b>{nivel.upper()}</b><br>"
                f"Score: {props.get('score_risco', '—')}<br>"
                f"Prioridade drone: {props.get('prioridade_drone', '—')}",
                sticky=True,
            ),
        ).add_to(grupo_areas)

for _, row in areas_df.iterrows():
    nivel = row["nivel_risco"]
    cor   = COR_AREA.get(nivel, "#95A5A6")

    popup_html = f"""
    <div style="font-family:sans-serif;min-width:200px">
      <h4 style="margin:0 0 6px;color:{cor}">{row['nome_area']}</h4>
      <table style="font-size:13px;width:100%">
        <tr><td>📍 Bairro</td><td><b>{row['bairro']}</b></td></tr>
        <tr><td>⚠️ Nível de risco</td><td><b style="color:{cor}">{nivel.upper()}</b></td></tr>
        <tr><td>📊 Score</td><td><b>{row['score_risco']}</b></td></tr>
        <tr><td>🦟 Casos (14 dias)</td><td><b>{row['casos_ultimos_14_dias']}</b></td></tr>
        <tr><td>🔍 Focos detectados</td><td><b>{row['focos_detectados']}</b></td></tr>
        <tr><td>🚁 Prioridade drone</td><td><b>{row['prioridade_drone']}</b></td></tr>
      </table>
      <p style="font-size:12px;color:#666;margin-top:6px">{row['observacao']}</p>
    </div>
    """

    folium.Marker(
        location=[row["latitude_centro"], row["longitude_centro"]],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=f"Área {row['id_area']} — Score {row['score_risco']}",
        icon=folium.DivIcon(
            html=f"""
            <div style="
              background:{cor};color:white;
              border-radius:50%;width:32px;height:32px;
              display:flex;align-items:center;justify-content:center;
              font-weight:bold;font-size:13px;
              border:2px solid white;
              box-shadow:0 2px 6px rgba(0,0,0,0.3)
            ">{row['score_risco']}</div>
            """,
            icon_size=(32, 32),
            icon_anchor=(16, 16),
        ),
    ).add_to(grupo_areas)

print(f"  ✅ {len(areas_df)} áreas adicionadas")

# ─────────────────────────────────────────
# 2. CASOS DE DENGUE
# ─────────────────────────────────────────
print("🦟 Adicionando casos de dengue...")

casos_df = pd.read_csv(CASOS_CSV)
cluster_casos = MarkerCluster(name="Cluster casos").add_to(grupo_casos)

for _, row in casos_df.iterrows():
    confirmado = row["status"] == "confirmado"
    cor_caso   = "#E67E22" if confirmado else "#F1C40F"
    icone_caso = "exclamation-sign" if confirmado else "question-sign"

    popup_html = f"""
    <div style="font-family:sans-serif;min-width:180px">
      <h4 style="margin:0 0 6px;color:{cor_caso}">
        {'🦟 Caso Confirmado' if confirmado else '❓ Caso Suspeito'}
      </h4>
      <table style="font-size:13px;width:100%">
        <tr><td>🆔 ID</td><td><b>{row['id_caso']}</b></td></tr>
        <tr><td>📍 Bairro</td><td><b>{row['bairro']}</b></td></tr>
        <tr><td>📅 Data</td><td>{row['data_notificacao']}</td></tr>
        <tr><td>📌 Endereço</td><td>{row['endereco_aproximado']}</td></tr>
        <tr><td>Status</td><td><b style="color:{cor_caso}">{row['status'].upper()}</b></td></tr>
      </table>
    </div>
    """

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{row['id_caso']} — {row['status']} — {row['bairro']}",
        icon=folium.Icon(
            color="orange" if confirmado else "beige",
            icon=icone_caso,
            prefix="glyphicon",
        ),
    ).add_to(cluster_casos)

print(f"  ✅ {len(casos_df)} casos adicionados")

# ─────────────────────────────────────────
# 3. FOCOS DETECTADOS PELO DRONE
# ─────────────────────────────────────────
print("🚁 Adicionando focos detectados pelo drone...")

focos_df = pd.read_csv(FOCOS_CSV)

for _, row in focos_df.iterrows():
    tipo     = row["tipo_foco"]
    conf     = float(row["confianca_ia"])
    conf_pct = f"{conf*100:.0f}%"

    if conf >= 0.80:
        cor_conf   = "#2ECC71"
        nivel_conf = "Alta"
    elif conf >= 0.70:
        cor_conf   = "#F39C12"
        nivel_conf = "Média"
    else:
        cor_conf   = "#E74C3C"
        nivel_conf = "Baixa"

    emoji = ICONE_FOCO.get(tipo, ("map-marker", "blue", "📍"))[2]

    popup_html = f"""
    <div style="font-family:sans-serif;min-width:200px">
      <h4 style="margin:0 0 6px;color:#2980B9">🚁 Foco Detectado por Drone</h4>
      <table style="font-size:13px;width:100%">
        <tr><td>🆔 ID</td><td><b>{row['id_foco']}</b></td></tr>
        <tr><td>🔍 Tipo</td><td><b>{tipo.replace('_', ' ').title()}</b></td></tr>
        <tr><td>🤖 Classe IA</td><td>{row['classe_ia']}</td></tr>
        <tr><td>📊 Confiança IA</td><td>
          <b style="color:{cor_conf}">{conf_pct} ({nivel_conf})</b>
        </td></tr>
        <tr><td>📅 Data</td><td>{row['data_detectado']}</td></tr>
        <tr><td>📷 Imagem</td><td>{row['origem_imagem']}</td></tr>
        <tr><td>✅ Status</td><td>{row['status_verificacao'].upper()}</td></tr>
        <tr><td>📍 Área</td><td>{row['id_area']}</td></tr>
      </table>
    </div>
    """

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(popup_html, max_width=270),
        tooltip=f"{row['id_foco']} — {tipo.replace('_',' ').title()} — IA: {conf_pct}",
        icon=folium.DivIcon(
            html=f"""
            <div style="
              background:#2980B9;color:white;
              border-radius:8px;padding:4px 7px;
              font-size:16px;
              border:2px solid white;
              box-shadow:0 2px 6px rgba(0,0,0,0.35);
              white-space:nowrap
            ">{emoji}</div>
            """,
            icon_size=(36, 32),
            icon_anchor=(18, 16),
        ),
    ).add_to(grupo_focos)

print(f"  ✅ {len(focos_df)} focos adicionados")

# ─────────────────────────────────────────
# 4. MONTA MAPA
# ─────────────────────────────────────────
grupo_areas.add_to(mapa)
grupo_casos.add_to(mapa)
grupo_focos.add_to(mapa)

folium.LayerControl(collapsed=False).add_to(mapa)

# ─────────────────────────────────────────
# 5. LEGENDA
# ─────────────────────────────────────────
legenda_html = """
<div style="
  position:fixed;bottom:30px;left:15px;z-index:1000;
  background:white;border-radius:10px;
  padding:12px 16px;
  box-shadow:0 2px 10px rgba(0,0,0,0.2);
  font-family:sans-serif;font-size:12px;
  max-width:200px;
">
  <b style="font-size:13px">🚁 AeroScan</b><br>
  <span style="color:#666;font-size:11px">Detecção de focos de dengue</span>
  <hr style="margin:8px 0;border-color:#eee">
  <b>Áreas de Risco</b><br>
  <span style="color:#E74C3C">■</span> Alto &nbsp;
  <span style="color:#F39C12">■</span> Médio &nbsp;
  <span style="color:#27AE60">■</span> Baixo<br><br>
  <b>Casos de Dengue</b><br>
  🟠 Confirmado &nbsp; 🟡 Suspeito<br><br>
  <b>Focos (Drone + IA)</b><br>
  🔧 Pneu &nbsp; 🏊 Piscina<br>
  💧 Caixa d'água &nbsp; 🗑️ Lixo<br><br>
  <b>Confiança da IA</b><br>
  <span style="color:#2ECC71">■</span> Alta (≥80%) &nbsp;
  <span style="color:#F39C12">■</span> Média<br>
  <span style="color:#E74C3C">■</span> Baixa (&lt;70%)
</div>
"""
mapa.get_root().html.add_child(folium.Element(legenda_html))

# ─────────────────────────────────────────
# 6. TÍTULO
# ─────────────────────────────────────────
titulo_html = """
<div style="
  position:fixed;top:10px;left:50%;transform:translateX(-50%);
  z-index:1000;background:white;border-radius:8px;
  padding:8px 20px;
  box-shadow:0 2px 8px rgba(0,0,0,0.2);
  font-family:sans-serif;text-align:center;
">
  <span style="font-size:15px;font-weight:600">🚁 AeroScan MVP</span>
  <span style="font-size:12px;color:#666;margin-left:8px">Mapa de Focos de Dengue</span>
</div>
"""
mapa.get_root().html.add_child(folium.Element(titulo_html))

# ─────────────────────────────────────────
# 7. SALVA
# ─────────────────────────────────────────
saida = Path(__file__).parent.parent / ARQUIVO_SAIDA
mapa.save(str(saida))

print(f"\n{'='*50}")
print(f"✅ Mapa gerado com sucesso!")
print(f"📁 Arquivo: {saida}")
print(f"\n📊 Resumo:")
print(f"   🟥 Áreas de risco:   {len(areas_df)}")
print(f"   🟠 Casos de dengue:  {len(casos_df)}")
print(f"   🔵 Focos detectados: {len(focos_df)}")
print(f"\n👉 Abra o arquivo no navegador para visualizar!")
print(f"{'='*50}")
