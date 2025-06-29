# 🧠 Real-Time Semantic Segmentation (MobileNetV3 + DeepLabV3+)

This project implements a minimal and production-style semantic segmentation pipeline using a lightweight MobileNetV3 + DeepLabV3+ architecture, optimized for real-time performance and edge deployment. The pipeline is built entirely using **Jupyter Notebooks** for clear experimentation and reproducibility.

---

## 📁 Project Structure

```plaintext
.
├── finetune.ipynb          # Fine-tuning the base segmentation model
├── prunning.ipynb          # Structured convolutional pruning
├── test.ipynb              # Evaluation, benchmarking (mIoU, FPS, accuracy)
├── weights/                # Saved model checkpoints (base + pruned versions)
└── README.md               # This file

```
## 📦 Key Features

- ✅ Pretrained MobileNetV3 backbone (ImageNet)
- ✅ Fine-tuning with Pascal VOC 2012 dataset
- ✅ Structured model pruning using PyTorch
- ✅ Evaluation using Pixel Accuracy, Mean IoU, and FPS
- ❌ No ONNX export or quantization (not used in this version)

---

## 📊 Benchmark Results

| Model Variant          | Test Loss | Pixel Accuracy | Mean IoU | Total Time | FPS   |
|------------------------|-----------|----------------|----------|------------|-------|
| **Base (FP32)**        | 0.2578    | 91.59%         | 0.6609   | 44.60s     | 32.57 |
| **Pruned 0.1**         | 0.2689    | 91.42%         | 0.5931   | 37.17s     | 38.09 |
| **Pruned 0.2**         | 0.2876    | 90.83%         | 0.5794   | 38.17s     | 37.96 |
| **Pruned 0.3**         | 0.3793    | 88.39%         | 0.5363   | 38.86s     | 37.28 |
| **Pruned 0.4 (v1)**    | 0.7588    | 79.14%         | 0.4252   | 39.51s     | 36.67 |
| **Pruned 0.4 (v2)**    | 0.2975    | 91.20%         | 0.5833   | 38.49s     | 37.65 |

> 🔍 **Note:** Best trade-off between accuracy and speed appears at pruning levels 0.2 to 0.3. A re-run at 0.4 (v2) also gave strong results.

---

## 🛠️ Setup Instructions

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Download Pascal VOC 2012 dataset (automatically handled in notebooks if not found):
   - Structure: `./data/VOCdevkit/VOC2012/`

3. Launch Jupyter:
   ```bash
   jupyter lab
   ```

---

## 📌 How to Use

Run the notebooks in the following order:

1. `finetune.ipynb` – Fine-tune the base model
2. `prunning.ipynb` – Apply structured pruning to reduce FLOPs
3. `test.ipynb` – Evaluate different versions and compare mIoU, pixel accuracy, inference speed

---

## 📈 Future Work

- [ ] Add quantization-aware training
- [ ] Export to ONNX for cross-platform deployment
- [ ] Deploy on ARM-based edge devices (e.g., Raspberry Pi)
- [ ] Add result visualizations per model variant

---

## 📚 License

This project is released under the MIT License.
```

