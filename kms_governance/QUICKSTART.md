# KMS 資料治理系統 - 快速開始指南
## 5 分鐘上手教學

> 以 AI 論文集合 (papers/) 為範例場域

---

## 🚀 快速開始三步驟

### Step 1: 環境設定 (2 分鐘)

```bash
# 1. 進入專案目錄
cd d:\python_workspace\project_nlp\data_governance\kms_governance

# 2. 安裝依賴套件
pip install -r requirements.txt

# 3. 下載 spaCy 語言模型
python -m spacy download en_core_web_sm

# 4. 驗證安裝
python -c "import docling; print('✅ Docling OK')"
python -c "import langchain; print('✅ LangChain OK')"
```

### Step 2: 執行 Demo Notebook (2 分鐘)

```bash
# 啟動 Jupyter Lab
jupyter lab notebooks/04_end_to_end_demo.ipynb
```

然後在 Notebook 中執行所有 cells，你將看到：
- ✅ 掃描 31 篇 AI 論文
- ✅ 使用 Docling 提取內容
- ✅ 建立元資料目錄
- ✅ 品質評估報告
- ✅ 視覺化分析

### Step 3: 使用 Python API (1 分鐘)

```python
from pathlib import Path
from utils.document_processor import DocumentProcessor

# 初始化處理器
processor = DocumentProcessor(config={
    'quality_threshold': 0.75,
    'chunk_size': 1000
})

# 處理單篇論文
result = processor.process_document(
    "../../papers/01_model_paradigm/2017_Transformer.pdf"
)

if result.success:
    print(f"✅ 成功: {result.metadata.title}")
    print(f"   品質分數: {result.metadata.quality_score}")
    print(f"   字數: {result.metadata.word_count:,}")

    # 分塊處理
    chunks = processor.chunk_content(result.content)
    print(f"   分塊數: {len(chunks)}")
```

---

## 📂 目錄結構

```
kms_governance/
├── 📓 notebooks/               # Jupyter 教學筆記本
│   ├── 00_architecture_overview.ipynb
│   ├── 01_document_ingestion.ipynb
│   ├── 02_metadata_management.ipynb
│   ├── 03_quality_control.ipynb
│   └── 04_end_to_end_demo.ipynb ⭐
│
├── 🔧 utils/                   # 核心工具模組
│   ├── document_processor.py   ⭐
│   ├── metadata_extractor.py
│   ├── quality_assessor.py
│   └── lineage_tracker.py
│
├── ⚙️ configs/                 # 配置文件
│   ├── governance_policy.yaml  ⭐
│   ├── quality_thresholds.json
│   └── processing_rules.yaml
│
├── 📁 01_raw/                  # 原始文檔（指向 papers/）
├── 📁 02_processed/            # 處理後文檔
├── 📁 03_indexed/              # 索引層
├── 📁 04_metadata/             # 元資料層
├── 📁 05_quality/              # 品質報告
└── 📁 06_lineage/              # 血緣追蹤

⭐ = 重點檔案
```

---

## 💡 常見使用場景

### 場景 1: 批量處理論文資料夾

```python
from pathlib import Path
from utils.document_processor import (
    DocumentProcessor,
    scan_directory,
    results_to_dataframe
)

# 掃描目錄
papers_dir = Path("../../papers/01_model_paradigm")
files = scan_directory(papers_dir, extensions=['.pdf'])

print(f"找到 {len(files)} 篇論文")

# 批量處理
processor = DocumentProcessor()
results = processor.batch_process([str(f) for f in files])

# 轉為 DataFrame
df = results_to_dataframe(results)

# 儲存結果
df.to_csv("processed_papers.csv", index=False)

print(f"✅ 處理完成: {processor.get_stats()}")
```

### 場景 2: 品質過濾與報告

```python
import pandas as pd

# 載入處理結果
df = pd.read_csv("processed_papers.csv")

# 品質過濾
high_quality = df[df['quality_score'] >= 0.8]

print(f"高品質論文: {len(high_quality)}/{len(df)}")
print(f"平均品質分數: {df['quality_score'].mean():.3f}")

# 品質分布
print(df['quality_score'].describe())

# 輸出報告
report = {
    "total": len(df),
    "high_quality": len(high_quality),
    "avg_score": df['quality_score'].mean(),
    "median_score": df['quality_score'].median()
}

import json
with open("quality_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

### 場景 3: 建立文檔目錄資料庫

```python
import sqlite3
import pandas as pd

# 載入元資料
df = pd.read_csv("processed_papers.csv")

# 連接 SQLite
conn = sqlite3.connect("04_metadata/document_catalog.db")

# 寫入資料庫
df.to_sql('documents', conn, if_exists='replace', index=False)

# 查詢範例
query = """
SELECT filename, category, year, quality_score
FROM documents
WHERE quality_score >= 0.8
ORDER BY year DESC
"""

results = pd.read_sql(query, conn)
print(results)

conn.close()
```

---

## 🎯 關鍵配置

### 調整品質閾值

編輯 `configs/governance_policy.yaml`:

```yaml
quality_control:
  thresholds:
    minimum_score: 0.70   # 最低接受分數
    target_score: 0.85    # 目標分數
```

### 調整分塊參數

```yaml
document_processing:
  chunking:
    chunk_size: 1000      # 調整分塊大小
    chunk_overlap: 200    # 調整重疊大小
```

---

## 📊 檢視結果

### 元資料目錄

```bash
# SQLite 資料庫
sqlite3 04_metadata/document_catalog.db

# 查看所有文檔
SELECT * FROM documents LIMIT 5;

# 依分類統計
SELECT category, COUNT(*), AVG(quality_score)
FROM documents
GROUP BY category;
```

### 品質報告

```bash
# JSON 報告
cat 05_quality/governance_report.json | python -m json.tool
```

---

## 🔧 進階功能

### 1. 自訂文檔處理器

```python
class CustomProcessor(DocumentProcessor):
    def _assess_quality(self, metadata, content):
        # 自訂品質評估邏輯
        score = super()._assess_quality(metadata, content)

        # 加入自訂規則
        if "important_keyword" in content:
            score += 0.1

        return min(1.0, score)
```

### 2. 整合向量資料庫（準備 RAG）

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 處理文檔
processor = DocumentProcessor()
result = processor.process_document("paper.pdf")

# 分塊
chunks = processor.chunk_content(result.content, result.metadata)

# 向量化
embeddings = OpenAIEmbeddings()
texts = [c['text'] for c in chunks]
metadatas = [{'source': c['source_file']} for c in chunks]

# 建立向量資料庫
vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    persist_directory="03_indexed/vector_index"
)
```

### 3. 血緣追蹤

```python
# 記錄處理歷史
import json
from datetime import datetime

lineage_record = {
    "document_id": result.metadata.document_id,
    "source_file": result.metadata.filename,
    "processed_at": datetime.now().isoformat(),
    "transformations": [
        {"step": "content_extraction", "tool": "docling"},
        {"step": "chunking", "tool": "langchain"},
        {"step": "quality_assessment", "score": result.metadata.quality_score}
    ]
}

# 儲存血緣記錄
with open(f"06_lineage/{result.metadata.document_id}.json", "w") as f:
    json.dump(lineage_record, f, indent=2)
```

---

## 🐛 疑難排解

### 問題 1: Docling 安裝失敗

```bash
# 確認 Python 版本 (需要 3.11+)
python --version

# 升級 pip
python -m pip install --upgrade pip

# 重新安裝
pip install --no-cache-dir docling
```

### 問題 2: 記憶體不足

```python
# 批次處理時設定較小的批次大小
processor = DocumentProcessor()

# 分批處理
batch_size = 5
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    results = processor.batch_process(batch)
    # 處理結果...
```

### 問題 3: PDF 提取失敗

```python
# 使用備用方案
try:
    result = processor.process_document(file_path)
except Exception as e:
    print(f"Docling 失敗，嘗試 PyPDF: {e}")

    # 使用 PyPDF 作為備用
    from pypdf import PdfReader
    reader = PdfReader(file_path)
    content = "".join(page.extract_text() for page in reader.pages)
```

---

## 📚 下一步學習

1. **完整教學**: 閱讀 `notebooks/00_architecture_overview.ipynb`
2. **理論基礎**: 參考 `../ch1_document_governance/lectures/`
3. **API 文檔**: 查看 `docs/api_reference.md`
4. **最佳實踐**: 閱讀 `docs/governance_guide.md`

---

## 🤝 技術支援

- **Issues**: GitHub Issues
- **文檔**: [KMS Governance Docs](./README.md)
- **範例**: `notebooks/` 目錄

---

**版本**: v1.0
**更新**: 2025-01-17
**作者**: Data Governance Team
