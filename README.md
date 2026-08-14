# 🚁 AeroScan — Drone + IA para Detecção de Focos de Dengue

> Projeto FETIN 2026 — Equipe 49  
> Detecção automática de focos de dengue (piscinas e pneus) via drone com visão computacional YOLOv8.

---

## 📊 Resultados do Modelo

| Métrica | Valor | Meta |
|---------|-------|------|
| **mAP@50** | **95.6%** | 60% ✅ |
| Precision | 91.2% | — |
| Recall | 92.3% | — |
| mAP@50-95 | 64.8% | — |

> Treinado com 6.749 imagens aéreas em 50 épocas usando YOLOv8, com 2 classes: `pool` e `tire`.

---

## 🎯 O Problema e a Solução

O Brasil registra milhões de casos de dengue por ano. A identificação manual de focos — piscinas abandonadas e pneus com água parada — é lenta, cara e depende de agentes de saúde indo casa a casa.

O AeroScan é um sistema de drone com IA que sobrevoa áreas de risco e detecta automaticamente esses focos em imagens aéreas, gerando um mapa interativo para as equipes de saúde priorizarem as vistorias.

---

## 🗂️ Estrutura do Repositório

```
FETIN/
├── datasets/
│   └── unified/           ← Dataset unificado (6.749 imagens)
│       ├── train/
│       ├── valid/
│       ├── test/
│       └── data.yaml
├── runs/
│   └── drone_v1/
│       └── weights/
│           └── best.pt    ← Modelo treinado ⭐
├── dashboard/
│   └── mapa_aeroscan.html ← Mapa interativo de focos
├── demo.py                ← Script de demo com câmera ao vivo
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Rodar em Qualquer PC

**Pré-requisitos:** Python 3.9+ → [python.org](https://python.org) | Git → [git-scm.com](https://git-scm.com)

```bash
# 1. Clonar o repositório
git clone https://github.com/RanderDLemos/FETIN.git
cd FETIN

# 2. Instalar dependências
pip install -r requirements.txt
```

### Demo com câmera ao vivo
```bash
python demo.py
```
Aponte a câmera para imagens aéreas de piscinas ou pneus — o modelo detecta e mostra as caixinhas em tempo real. Pressione `Q` para sair ou `S` para salvar um screenshot.

### Detecção em imagem ou vídeo
```python
from ultralytics import YOLO

model = YOLO('runs/drone_v1/weights/best.pt')

results = model.predict('sua_imagem.jpg', conf=0.25)  # imagem
results = model.predict('video_drone.mp4', conf=0.25, save=True)  # vídeo
```

---

## 🗺️ Mapa Interativo

Visualiza em tempo real as áreas de risco, casos confirmados de dengue e focos detectados pelo drone.

Acesse: [Link do GitHub Pages após publicação]

---

## 📦 Fontes do Dataset

| Dataset | Classe |
|---------|--------|
| pool-images/pool-detection-kmqaa | `pool` |
| swimming-pools/swimming-pools-detection | `pool` |
| piscina-piloto/swimming-pool-detection | `pool` |
| king-mongkut-.../tire-x4hgu | `tire` |
| testwheel/wheeltester | `tire` |

---

## 🔁 Como Retreinar

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(
    data='datasets/unified/data.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    name='drone_v1',
    flipud=0.5,
    fliplr=0.5,
    degrees=45,
    scale=0.5,
)
```

> ⚠️ Requer GPU. Use o Google Colab (T4 gratuita) — tempo estimado: 30–40 minutos.

---

## 🔒 Privacidade e LGPD

Todas as imagens passam por anonimização automática antes de serem armazenadas. Rostos são detectados e borrados em tempo real — nenhum dado biométrico é salvo ou transmitido.

---

## 🛠️ Tecnologias

- [YOLOv8](https://github.com/ultralytics/ultralytics) — Detecção de objetos
- [Roboflow](https://roboflow.com) — Gerenciamento de datasets
- [OpenCV](https://opencv.org) — Processamento de imagem
- [Folium](https://python-visualization.github.io/folium/) — Mapa interativo
- [Python 3.10](https://python.org)

---

## 👥 Equipe

| Nome | GitHub |
|------|--------|
| Rander D. Lemos | [@RanderDLemos](https://github.com/RanderDLemos) |
| [Adicionar membros] | — |
