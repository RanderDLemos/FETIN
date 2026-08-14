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

> Treinado com 6.749 imagens aéreas em 50 épocas usando YOLOv8.

---

## 🎯 O Problema

O Brasil registra milhões de casos de dengue por ano. A identificação manual de focos — piscinas abandonadas e pneus com água parada — é lenta, cara e depende de agentes de saúde indo casa a casa. Em surtos, a capacidade humana não acompanha a velocidade de proliferação do mosquito.

## 💡 A Solução

O AeroScan é um sistema de drone equipado com câmera e inteligência artificial que sobrevoa áreas de risco e detecta automaticamente focos do mosquito *Aedes aegypti* em imagens aéreas, gerando um mapa interativo para as equipes de saúde priorizarem as vistorias.

---

## 🤖 Classes Detectadas

| Classe | Descrição |
|--------|-----------|
| `pool` | Piscinas vistas de cima (vista aérea) |
| `tire` | Pneus abandonados |
| `car-tire` | Pneus em terrenos e quintais |

---

## 🗂️ Estrutura do Repositório

```
FETIN/
├── datasets/
│   └── unified/          ← Dataset unificado (6.749 imagens)
│       ├── train/
│       ├── valid/
│       ├── test/
│       └── data.yaml
├── runs/
│   └── drone_v1/
│       └── weights/
│           └── best.pt   ← Modelo treinado ⭐
├── dashboard/
│   └── mapa_aeroscan.html ← Mapa interativo de focos
├── demo.py               ← Script de demo com câmera ao vivo
├── requirements.txt      ← Dependências do projeto
└── README.md
```

---

## ⚙️ Como Rodar em Qualquer PC

### Pré-requisitos

- Python 3.9 ou superior → [python.org](https://python.org)
- Webcam ou câmera USB
- Git → [git-scm.com](https://git-scm.com)

### 1. Clonar o repositório

```bash
git clone https://github.com/RanderDLemos/FETIN.git
cd FETIN
```

### 2. Instalar dependências

```bash
pip install ultralytics opencv-python
```

Ou usando o arquivo de requisitos:

```bash
pip install -r requirements.txt
```

### 3. Rodar a demo com câmera ao vivo

```bash
python demo.py
```

Uma janela vai abrir com a câmera em tempo real. Aponte para imagens aéreas de piscinas ou pneus — o modelo detecta e mostra as caixinhas coloridas com a porcentagem de confiança.

**Teclas:**
- `Q` → fechar a demo
- `S` → salvar screenshot da detecção atual

### 4. Rodar detecção em uma imagem específica

```python
from ultralytics import YOLO

model = YOLO('runs/drone_v1/weights/best.pt')
results = model.predict('sua_imagem.jpg', conf=0.25)
results[0].show()   # exibe com as detecções
results[0].save()   # salva como arquivo
```

### 5. Rodar detecção em um vídeo

```python
from ultralytics import YOLO

model = YOLO('runs/drone_v1/weights/best.pt')
results = model.predict('video_drone.mp4', conf=0.25, save=True)
```

---

## 🗺️ Mapa Interativo

O mapa mostra em tempo real:
- 🔴 Áreas de alto risco
- 🟠 Casos confirmados de dengue
- 🔵 Focos detectados pelo drone

Acesse: [Link do GitHub Pages após publicação]

---

## 📦 Dataset

Fontes utilizadas para treinamento:

| Dataset | Tipo | Imagens |
|---------|------|---------|
| pool-images/pool-detection-kmqaa | Piscinas aéreas | — |
| swimming-pools/swimming-pools-detection | Piscinas aéreas | — |
| piscina-piloto/swimming-pool-detection | Piscinas aéreas | — |
| king-mongkut-.../tire-x4hgu | Pneus | — |
| testwheel/wheeltester | Pneus | — |
| **Total unificado** | — | **6.749 imagens** |

---

## 🔁 Como Retreinar o Modelo

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # modelo base

model.train(
    data='datasets/unified/data.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    name='drone_v1',
    # Augmentações para imagens aéreas de drone:
    flipud=0.5,
    fliplr=0.5,
    degrees=45,
    scale=0.5,
)
```

> ⚠️ O retreino requer GPU. Use o Google Colab (T4 gratuita) — tempo estimado: 30–40 minutos.

---

## 🔒 Privacidade e LGPD

Todas as imagens capturadas pelo drone passam por anonimização automática antes de serem armazenadas. Rostos e dados pessoais identificáveis são detectados e borrados em tempo real. Nenhuma imagem com dado biométrico é salva ou transmitida.

---

## 🛠️ Tecnologias

- [YOLOv8](https://github.com/ultralytics/ultralytics) — Detecção de objetos
- [Roboflow](https://roboflow.com) — Gerenciamento de datasets
- [OpenCV](https://opencv.org) — Processamento de imagem
- [Folium](https://python-visualization.github.io/folium/) — Mapa interativo
- [Python 3.10](https://python.org)

---

## 👥 Equipe

Projeto FETIN 2026 — Equipe 49

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos no contexto da FETIN 2026.
