# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 專案概述

這是一個關於**企業級檢索增強生成系統 (Enterprise RAG)** 的教學專案，著重於資料治理、文檔處理與知識管理。專案包含兩大核心部分：

1. **AI 論文收集系統** - 收集並整理 AI 發展史上的 36 篇關鍵論文
2. **企業知識治理課程教材** - 教授如何建立企業級的文檔處理與知識管理系統

---

## 專案架構

```
data_governance/
├── download_papers.py          # 論文下載腳本
├── course_content.md           # 36篇論文清單與摘要
├── requirements.txt            # Python 依賴套件
├── papers/                     # 下載的論文 PDF 檔案
│   ├── 01_model_paradigm/      # 模型范式變遷 (11篇)
│   ├── 02_infrastructure/      # Infra與資料變遷 (5篇)
│   ├── 03_language_models/     # 語言模型發展 (8篇)
│   └── 04_multimodal/          # 多模態模型發展 (8篇)
└── ch1_document_governance/    # 第1章教材
    └── lectures/               # 課程講義
        ├── 01_enterprise_knowledge_governance.md  # 企業知識治理
        ├── 01_document_processing_fundamentals.md # 文檔處理基礎
        └── 01_docops_pipeline_design.md           # DocOps 管線設計
```

---

## 常用指令

### 環境設置

```bash
# 安裝依賴
pip install -r requirements.txt

# 驗證安裝
python -c "import requests; print('OK')"
```

### 論文下載系統

```bash
# 下載所有論文 (自動跳過已存在的檔案)
python download_papers.py

# 檢查論文收集狀態
ls -lR papers/

# 查看下載統計
python download_papers.py | grep -E "(OK|SKIP|FAIL)"
```

**重要說明**：
- 腳本會自動創建分類目錄
- 已下載的檔案會被跳過
- 每次請求間隔 1 秒，避免伺服器封鎖
- 某些論文需要機構訪問權限 (如 ACM, Nature)

---

## 核心設計模式

### 1. 論文下載系統 (`download_papers.py`)

**設計原則**：
- **冪等性**: 重複執行腳本不會重複下載已存在的檔案
- **容錯性**: 單一論文下載失敗不影響其他論文
- **可追溯性**: 每個論文都有完整的元數據 (來源、年份、分類)

**關鍵元件**：

```python
# 論文結構設計
PAPERS = [
    {
        "category": "01_model_paradigm",  # 分類目錄
        "year": "2017",                   # 發表年份
        "name": "Transformer",            # 論文簡稱
        "arxiv_id": "1706.03762",        # arXiv ID (自動生成下載URL)
        "type": "arxiv"                   # 類型: arxiv 或 pdf
    }
]
```

**下載流程**：
1. 檢查檔案是否已存在 → 存在則跳過
2. 根據 `type` 決定下載來源 (arXiv 或直接 PDF URL)
3. 使用 `requests.Session` 處理重試機制
4. 串流下載避免記憶體溢出
5. 記錄下載狀態 (成功/跳過/失敗)

**擴展方式**：
- 新增論文：在 `PAPERS` 列表中加入新的字典
- 新增分類：創建新的 `category` 名稱
- 處理付費牆：在 `note` 欄位記錄手動下載說明

### 2. 課程教材系統 (`ch1_document_governance/`)

**教學內容層次**：

```
第1章：數據治理基礎
├── 理論層 (enterprise_knowledge_governance.md)
│   ├── 知識熵增定律與數學模型
│   ├── 文檔生命週期管理理論
│   └── 品質評估框架 (ISO 25012)
│
├── 工程層 (document_processing_fundamentals.md)
│   ├── Docling 深度整合
│   ├── 語義分塊算法
│   └── 元數據自動提取
│
└── 實踐層 (docops_pipeline_design.md)
    ├── 企業級 DocOps 管線
    ├── 品質監控系統
    └── 案例分析
```

**設計哲學**：
- **理論與實踐結合**: 每個理論模型都配有完整的 Python 實作
- **生產級程式碼**: 所有範例程式碼可直接用於生產環境
- **數學嚴謹性**: 使用 LaTeX 數學公式精確定義概念
- **品質優先**: 強調文檔品質評估與持續改進

---

## 技術棧與工具選型

### Python 套件

| 套件 | 用途 | 選型理由 |
|------|------|----------|
| `requests` | HTTP 請求 | 標準庫，穩定可靠 |
| `urllib3` | 底層 HTTP | 提供重試機制 |
| `docling` (教材中) | PDF 處理 | IBM 出品，準確率 95%+ |
| `sentence-transformers` | 語義嵌入 | SOTA 模型，支援多語言 |
| `spacy` | NLP 處理 | 工業級 NLP 工具 |

### 檔案命名規範

**論文檔案**: `YYYY_PaperName.pdf`
```
2017_Transformer.pdf
2018_BERT.pdf
2022_Stable_Diffusion.pdf
```

**教材檔案**: `章節編號_主題_類型.md`
```
01_enterprise_knowledge_governance.md   # 01章_企業知識治理
01_document_processing_fundamentals.md  # 01章_文檔處理基礎
```

---

## 程式碼風格指南

### 資料結構設計

**使用 TypedDict 或 dataclass 明確定義結構**：

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class DocumentMetadata:
    """標準化文檔元數據結構"""
    document_id: str
    title: str
    authors: List[str]
    created_date: Optional[datetime]
    document_type: str
    quality_score: float
```

### 錯誤處理模式

```python
# 推薦: 細緻的錯誤處理與回報
try:
    result = download_paper(paper, base_dir, session)
    if result == "success":
        success_count += 1
    elif result == "skip":
        skipped_count += 1
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 403:
        print(f"[SKIP] Access denied - institutional access required")
    else:
        print(f"[FAIL] HTTP {e.response.status_code}")
except Exception as e:
    print(f"[FAIL] Unexpected error: {str(e)}")
```

### 非同步處理模式

教材中的企業級程式碼使用 `async/await`：

```python
async def process_enterprise_document(self, file_path: str) -> Dict:
    """處理企業文檔的完整流程"""
    # 階段1: 文檔解析
    conversion_result = await self._convert_document(file_path)
    # 階段2: 質量評估
    quality_assessment = await self._assess_document_quality(conversion_result)
    # 階段3: 結構化提取
    structured_content = await self._extract_structured_content(conversion_result)
    return result
```

---

## 關鍵數學模型

### 1. 知識熵增定律 (Knowledge Entropy)

```
S_knowledge = -Σ p_i log p_i
dS_knowledge/dt > 0  (無治理情況下)
```

**意義**: 沒有持續治理的知識系統，可用性必然衰退

### 2. 文檔品質函數 (Quality Function)

```
Q(doc) = w1·Accuracy + w2·Relevance + w3·Timeliness + w4·Completeness
```

**權重配置** (基於 ISO 25012):
- Accuracy: 0.3
- Relevance: 0.25
- Timeliness: 0.25
- Completeness: 0.2

### 3. 語義邊界檢測 (Semantic Boundary)

```
Boundary(i) = LocalMin(Sim(s_i, s_{i+1}))
```

**應用**: 智能文檔分塊，避免打斷語義連貫的段落

---

## 開發工作流程

### 新增論文到收集系統

1. 確認論文資訊 (年份、標題、來源)
2. 在 `PAPERS` 列表中新增條目：
   ```python
   {
       "category": "03_language_models",
       "year": "2024",
       "name": "New_Paper_Name",
       "arxiv_id": "2401.12345",  # 或使用 "url" 欄位
       "type": "arxiv"
   }
   ```
3. 執行下載腳本驗證
4. 更新 `papers/README.md` 統計資訊

### 開發新的文檔處理功能

1. **先寫測試資料**: 準備範例 PDF/DOCX 檔案
2. **定義資料結構**: 使用 `dataclass` 或 `TypedDict`
3. **實作核心邏輯**: 遵循 async/await 模式
4. **加入品質評估**: 每個處理步驟都要有品質指標
5. **撰寫文檔**: 使用數學公式說明演算法原理

---

## 品質標準

### 文檔處理準確率

| 元件 | 目標準確率 | 測試方法 |
|------|-----------|---------|
| PDF 文字提取 | ≥95% | 與人工標註比對 |
| 表格結構識別 | ≥92% | 結構完整性檢查 |
| 版面理解 | ≥89% | 閱讀順序正確性 |
| 元數據提取 | ≥85% | 欄位完整性驗證 |

### 論文下載系統 SLA

- **成功率**: ≥90% (排除付費牆論文)
- **重試機制**: 最多 3 次
- **超時設定**: 30 秒/檔案
- **速率限制**: 1 秒/請求

---

## 常見問題與解決方案

### Q1: 論文下載失敗 (403 錯誤)

**原因**: 某些期刊需要機構訪問權限 (如 ACM, Nature)

**解決方案**:
1. 透過學校或公司的圖書館系統存取
2. 使用 Google Scholar 尋找開放版本
3. 查看作者個人網站或 ResearchGate

### Q2: Docling 處理大型 PDF 時記憶體不足

**解決方案**:
```python
# 使用分頁處理
pdf_options = PdfFormatOption(
    max_file_size="100MB",      # 限制檔案大小
    timeout=300,                # 5分鐘超時
    enable_optimizations=True   # 啟用記憶體優化
)
```

### Q3: 語義分塊結果不理想

**調整參數**:
```python
self.similarity_threshold = 0.3  # 降低閾值 → 更多分塊
self.min_chunk_size = 100        # 最小分塊大小
self.max_chunk_size = 1500       # 最大分塊大小
self.overlap_ratio = 0.1         # 重疊比例
```

---

## 專案擴展方向

### 短期目標
- [ ] 完成第 2-5 章教材撰寫
- [ ] 新增論文摘要自動生成功能
- [ ] 實作完整的 DocOps 管線範例程式碼

### 長期目標
- [ ] 建立互動式 Jupyter Notebook 教學環境
- [ ] 開發企業級 RAG 系統參考實作
- [ ] 整合向量資料庫與檢索系統
- [ ] 提供 Docker 容器化部署方案

---

## 參考資料

### 核心論文
- Vaswani et al. (2017) - "Attention Is All You Need" (Transformer 架構)
- Devlin et al. (2018) - "BERT: Pre-training of Deep Bidirectional Transformers"
- Brown et al. (2020) - "Language Models are Few-Shot Learners" (GPT-3)

### 技術文檔
- [Docling Documentation](https://github.com/DS4SD/docling) - IBM 文檔處理工具
- ISO/IEC 25012:2008 - 資料品質標準
- [arXiv API Documentation](https://arxiv.org/help/api) - 論文下載 API

### 課程相關
- CS785 - 企業級檢索增強生成系統
- 第 0 章 (先修): 數據治理基礎概念
- 第 1 章: 知識資產的系統化管理

---

## 授權與引用

本專案為教學用途，程式碼遵循 MIT 授權。論文版權歸原作者所有。

**引用論文時請使用原始出處**：
```bibtex
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and ...},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}
```

---

**最後更新**: 2025-01-06
**維護者**: 數據治理研究團隊
**課程編號**: CS785 - 企業級檢索增強生成系統
