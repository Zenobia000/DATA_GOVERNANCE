以下是完整 36 篇論文的整理版表格（依你指定的四大分群）。
引用次數為截至 2025 年模型記憶中之大致估計值。

---

## 🧩 模型的范式變遷

| 年份   | 論文名稱                                                            | 出處                 | 引用次數 (估) | 摘要                           | 主要貢獻            |
| ---- | --------------------------------------------------------------- | ------------------ | -------- | ---------------------------- | --------------- |
| 2004 | Brook for GPUs: Stream Computing on Graphics Hardware           | ACM SIGGRAPH / TOG | ≈ 1.9 k  | 將 GPU 抽象成可程式化流處理單元。          | 開啟 GPGPU 時代。    |
| 2012 | ImageNet Classification with Deep CNNs (AlexNet)                | NeurIPS 2012       | ≈ 145 k  | GPU 訓練 CNN 突破 ImageNet 準確率。  | 深度學習時代開端。       |
| 2014 | Sequence to Sequence Learning with Neural Networks              | NeurIPS 2014       | ≈ 70 k   | Encoder–Decoder 架構翻譯任務。      | 序列轉換基石。         |
| 2015 | Distilling the Knowledge in a Neural Network                    | arXiv 1503.02531   | ≈ 17 k   | 以 soft label 進行知識蒸餾。         | 模型壓縮典範。         |
| 2015 | Deep Residual Learning for Image Recognition (ResNet)           | CVPR 2016          | ≈ 200 k  | 殘差連接解決梯度消失。                  | 使超深網路可行。        |
| 2017 | Attention Is All You Need                                       | NeurIPS 2017       | ≈ 320 k  | 全自注意力架構取代 RNN。               | Transformer 誕生。 |
| 2017 | Mastering the Game of Go without Human Knowledge (AlphaGo Zero) | Nature 2017        | ≈ 25 k   | 自我博弈 + MCTS 學習棋藝。            | 強化學習無人示範典範。     |
| 2017 | Outrageously Large Neural Networks (Sparsely-Gated MoE)         | arXiv 1701.06538   | ≈ 3.8 k  | 稀疏 Mixture-of-Experts 降低計算量。 | 巨模型稀疏化開端。       |
| 2021 | LoRA: Low-Rank Adaptation of Large Language Models              | arXiv 2106.09685   | ≈ 8 k    | 低秩矩陣微調 LLM。                  | 輕量化微調主流。        |
| 2022 | Chain-of-Thought Prompting Elicits Reasoning in LLMs            | arXiv 2201.11903   | ≈ 7 k    | 展示 LLM 推理步驟。                 | 推理型 prompt 奠基。  |
| 2022 | ReAct: Synergizing Reasoning and Acting in LLMs                 | arXiv 2210.03629   | ≈ 2.5 k  | 結合推理與行動。                     | Agent 結構雛形。     |

---

## ⚙️ Infra 與資料的變遷

| 年份          | 論文名稱                                                             | 出處               | 引用次數 (估) | 摘要                  | 主要貢獻              |
| ----------- | ---------------------------------------------------------------- | ---------------- | -------- | ------------------- | ----------------- |
| 2018 / 2019 | The Bitter Lesson                                                | R. Sutton Blog   | ≈ 3 k    | 主張計算勝於人類先驗。         | AI 長期哲學指引。        |
| 2019        | ZeRO: Memory Optimizations Toward Training Trillion Param Models | arXiv 1910.02054 | ≈ 5.8 k  | 分散式梯度與參數切分。         | 支撐 DeepSpeed。     |
| 2020        | Scaling Laws for Neural Language Models                          | arXiv 2001.08361 | ≈ 7.4 k  | 性能與模型規模呈冪律關係。       | LLM scaling 理論基礎。 |
| 2022        | LAION-5B: Open Large-Scale Image-Text Dataset                    | arXiv 2210.08402 | ≈ 2.2 k  | 58 億圖文對 CLIP 過濾。    | 開源多模態資料集革命。       |
| 2023        | RefinedWeb: High-Quality Massive Web Corpus                      | arXiv 2306.01116 | ≈ 0.3 k  | 清洗 Common Crawl 語料。 | 高質文本工程範例。         |
| 2024        | MegaScale: Scaling LLM Training to >10 000 GPUs                  | arXiv 2402.15627 | ≈ 0.15 k | 萬卡訓練監控與容錯。          | 超大規模訓練實踐。         |

---

## 🗣 語言模型的發展

| 年份   | 論文名稱                                                                   | 出處                 | 引用次數 (估) | 摘要                      | 主要貢獻                |
| ---- | ---------------------------------------------------------------------- | ------------------ | -------- | ----------------------- | ------------------- |
| 2013 | Efficient Estimation of Word Representations (Word2Vec)                | arXiv 1301.3781    | ≈ 95 k   | 連續詞向量表徵。                | 詞嵌入時代開啟。            |
| 2016 | Google Neural Machine Translation (GNMT)                               | arXiv 1609.08144   | ≈ 14 k   | 全 seq2seq 翻譯系統。         | NMT 產業化。            |
| 2018 | Improving Language Understanding by Generative Pre-Training (GPT-1)    | OpenAI Report      | ≈ 11 k   | 無監督預訓練 + 監督微調。          | 預訓練範式開端。            |
| 2018 | BERT: Pre-training of Deep Bidirectional Transformers                  | NAACL 2019         | ≈ 130 k  | 雙向 Transformer MLM 預訓練。 | NLP 基準全面超越。         |
| 2019 | Language Models are Unsupervised Multitask Learners (GPT-2)            | OpenAI Tech Report | ≈ 40 k   | 大規模 Transformer 零樣本泛化。  | Few/Zero-shot 展示。   |
| 2020 | Language Models are Few-Shot Learners (GPT-3)                          | arXiv 2005.14165   | ≈ 30 k   | 175 B 參數少樣本學習。          | Prompt Learning 確立。 |
| 2022 | Training LLMs to Follow Instructions with Human Feedback (InstructGPT) | arXiv 2203.02155   | ≈ 8 k    | SFT + RM + PPO。         | RLHF 對齊開端。          |
| 2024 | TULU 3: Instruction Tuning at Scale                                    | arXiv 2407.15541   | ≈ 50     | SFT + DPO + RLVR 全開源。   | 後訓練 pipeline 新標竿。   |

---

## 🖼 多模態模型的發展

| 年份      | 論文名稱                                                                            | 出處                          | 引用次數 (估) | 摘要                          | 主要貢獻                   |
| ------- | ------------------------------------------------------------------------------- | --------------------------- | -------- | --------------------------- | ---------------------- |
| 2014    | Large-Scale Video Classification with CNNs (DeepVideo)                          | CVPR 2014                   | ≈ 5.5 k  | CNN 應用於影片分類。                | 視覺跨入時序領域。              |
| 2014    | Two-Stream CNNs for Action Recognition in Videos                                | NeurIPS 2014                | ≈ 12 k   | 影像與光流雙路網路。                  | 動作辨識里程碑。               |
| 2015    | Generative Adversarial Networks (GAN)                                           | NeurIPS 2014 paper pub 2015 | ≈ 60 k   | 生成器-判別器 博弈。                 | 生成式模型革命。               |
| 2020    | Denoising Diffusion Probabilistic Models (DDPM)                                 | NeurIPS 2020                | ≈ 23 k   | 逐步去噪生成影像。                   | Diffusion 主流誕生。        |
| 2020    | An Image is Worth 16×16 Words (ViT)                                             | ICLR 2021                   | ≈ 55 k   | 將 Transformer 應用於圖像。        | Vision Transformer 開端。 |
| 2021    | CLIP: Learning Transferable Visual Models from Language Supervision             | ICML 2021                   | ≈ 40 k   | 文字-圖像對比學習。                  | 多模態表徵主流。               |
| 2021-22 | High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion) | arXiv 2112.10752            | ≈ 10 k   | 潛變量空間高效生成。                  | 開放式影像生成革命。             |
| 2022    | DiT: Diffusion Models Beat GANs on Image Synthesis                              | arXiv 2212.09748            | ≈ 2 k    | Transformer 為骨幹的 Diffusion。 | 統一 Diffusion 架構。       |

---

### ✅ 摘要整理小結

* **模型的范式變遷**：從 GPU → CNN → Transformer → LLM 推理化。
* **Infra 與資料**：從 硬體與分散訓練 到 資料治理。
* **語言模型**：從 詞向量 到 RLHF 對齊。
* **多模態**：從 影像 到 跨語意生成。


