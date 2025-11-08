#!/usr/bin/env python3
"""
Document Processor - 文檔處理核心模組
整合 Docling, LangChain 等工具，提供統一的文檔處理介面

Author: Data Governance Team
Version: 1.0
Date: 2025-01-17
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re
import time

# 文檔處理
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 數據處理
import pandas as pd
import numpy as np


@dataclass
class DocumentMetadata:
    """
    標準化文檔元資料結構

    基於運算思維的抽象化設計
    """

    # 核心識別
    document_id: str
    filename: str
    title: str
    content_hash: str

    # 分類資訊
    category: str
    document_type: str
    year: Optional[int]

    # 內容特徵
    word_count: int
    char_count: int
    page_count: Optional[int]

    # 結構特徵
    has_abstract: bool
    has_references: bool
    has_tables: bool
    has_figures: bool

    # 品質指標
    quality_score: float
    extraction_confidence: float

    # 時間戳記
    created_at: str
    processed_at: str

    # 可選欄位
    keywords: Optional[List[str]] = None
    language: str = "en"
    authors: Optional[List[str]] = None

    def to_dict(self) -> Dict:
        """轉換為字典格式"""
        return asdict(self)


@dataclass
class ProcessingResult:
    """文檔處理結果"""

    success: bool
    content: Optional[str]
    metadata: Optional[DocumentMetadata]
    error: Optional[str] = None
    processing_time: float = 0.0


class DocumentProcessor:
    """
    文檔處理器主類

    整合多種文檔處理工具，提供統一介面
    基於運算思維的分解與模式識別設計
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化文檔處理器

        Args:
            config: 配置字典，可包含:
                - quality_threshold: 品質閾值
                - chunk_size: 分塊大小
                - chunk_overlap: 分塊重疊
        """
        self.config = config or {}

        # Docling 轉換器
        self.converter = DocumentConverter()

        # LangChain 分塊器
        self.chunker = RecursiveCharacterTextSplitter(
            chunk_size=self.config.get('chunk_size', 1000),
            chunk_overlap=self.config.get('chunk_overlap', 200),
            separators=["\n\n", "\n", "。", ".", " "]
        )

        # 品質閾值
        self.quality_threshold = self.config.get('quality_threshold', 0.7)

        # 處理統計
        self.stats = {
            'total_processed': 0,
            'success_count': 0,
            'failed_count': 0,
            'total_time': 0.0
        }

    def process_document(self, file_path: str) -> ProcessingResult:
        """
        處理單個文檔

        主流程：
        1. 提取內容（Docling）
        2. 分析結構
        3. 提取元資料
        4. 評估品質
        5. 返回結果

        Args:
            file_path: 文檔路徑

        Returns:
            ProcessingResult 物件
        """
        start_time = time.time()
        self.stats['total_processed'] += 1

        try:
            # Step 1: 提取內容
            content = self._extract_content(file_path)

            # Step 2: 分析結構
            structure_features = self._analyze_structure(content)

            # Step 3: 提取元資料
            metadata = self._extract_metadata(
                file_path,
                content,
                structure_features
            )

            # Step 4: 評估品質
            quality_score = self._assess_quality(metadata, content)
            metadata.quality_score = quality_score

            processing_time = time.time() - start_time
            self.stats['success_count'] += 1
            self.stats['total_time'] += processing_time

            return ProcessingResult(
                success=True,
                content=content,
                metadata=metadata,
                processing_time=processing_time
            )

        except Exception as e:
            processing_time = time.time() - start_time
            self.stats['failed_count'] += 1
            self.stats['total_time'] += processing_time

            return ProcessingResult(
                success=False,
                content=None,
                metadata=None,
                error=str(e),
                processing_time=processing_time
            )

    def _extract_content(self, file_path: str) -> str:
        """
        使用 Docling 提取文檔內容

        Args:
            file_path: 文檔路徑

        Returns:
            提取的文本內容
        """
        result = self.converter.convert(file_path)
        content = result.document.export_to_markdown()
        return content

    def _analyze_structure(self, content: str) -> Dict:
        """
        分析文檔結構特徵

        基於模式識別：論文通常有固定結構

        Args:
            content: 文檔內容

        Returns:
            結構特徵字典
        """
        features = {}

        # 檢測 Abstract
        features['has_abstract'] = bool(
            re.search(r'(?i)\babstract\b', content[:2000])
        )

        # 檢測 References
        features['has_references'] = bool(
            re.search(r'(?i)\breferences?\b', content)
        )

        # 檢測表格（簡化版）
        features['has_tables'] = content.count('|') > 10

        # 檢測圖片引用
        features['has_figures'] = bool(
            re.search(r'(?i)\b(figure|fig\.|圖)\s*\d+', content)
        )

        # 統計
        features['word_count'] = len(content.split())
        features['char_count'] = len(content)

        # 標題數量
        features['header_count'] = content.count('#')

        return features

    def _extract_metadata(self,
                         file_path: str,
                         content: str,
                         structure_features: Dict) -> DocumentMetadata:
        """
        提取文檔元資料

        Args:
            file_path: 檔案路徑
            content: 文檔內容
            structure_features: 結構特徵

        Returns:
            DocumentMetadata 物件
        """
        path = Path(file_path)

        # 生成文檔 ID
        doc_id = hashlib.md5(path.name.encode()).hexdigest()[:16]

        # 計算內容 hash
        content_hash = hashlib.sha256(
            content.encode() if content else b""
        ).hexdigest()[:16]

        # 從檔名提取年份
        year_match = re.match(r"(\d{4})", path.stem)
        year = int(year_match.group(1)) if year_match else None

        # 從路徑提取分類
        category = path.parent.name

        # 提取標題（從檔名）
        title = path.stem.replace('_', ' ')

        # 檢測文檔類型
        document_type = self._detect_document_type(content, structure_features)

        return DocumentMetadata(
            document_id=doc_id,
            filename=path.name,
            title=title,
            content_hash=content_hash,
            category=category,
            document_type=document_type,
            year=year,
            word_count=structure_features['word_count'],
            char_count=structure_features['char_count'],
            page_count=None,  # 可從 Docling 結果提取
            has_abstract=structure_features['has_abstract'],
            has_references=structure_features['has_references'],
            has_tables=structure_features['has_tables'],
            has_figures=structure_features['has_figures'],
            quality_score=0.0,  # 稍後計算
            extraction_confidence=0.85,
            created_at=datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            processed_at=datetime.now().isoformat(),
            language="en"
        )

    def _detect_document_type(self, content: str, features: Dict) -> str:
        """
        檢測文檔類型

        基於模式識別

        Args:
            content: 文檔內容
            features: 結構特徵

        Returns:
            文檔類型字符串
        """
        content_lower = content.lower()[:5000]  # 只看前 5000 字符

        # 論文特徵
        if features['has_abstract'] and features['has_references']:
            return "research_paper"

        # 技術文檔
        if any(keyword in content_lower for keyword in ['api', 'specification', 'implementation']):
            return "technical_doc"

        # 報告
        if any(keyword in content_lower for keyword in ['report', 'analysis', 'findings']):
            return "report"

        # 手冊
        if any(keyword in content_lower for keyword in ['manual', 'guide', 'tutorial']):
            return "manual"

        # 政策
        if any(keyword in content_lower for keyword in ['policy', 'compliance', 'regulation']):
            return "policy"

        return "general"

    def _assess_quality(self, metadata: DocumentMetadata, content: str) -> float:
        """
        評估文檔品質

        簡化版 - 基於結構完整性和內容長度

        Args:
            metadata: 元資料
            content: 文檔內容

        Returns:
            品質分數 (0-1)
        """
        score = 0.0

        # 基礎分 (40%)
        score += 0.4

        # 結構完整性 (30%)
        if metadata.has_abstract:
            score += 0.15
        if metadata.has_references:
            score += 0.15

        # 內容長度 (20%)
        if metadata.word_count >= 5000:
            score += 0.2
        elif metadata.word_count >= 2000:
            score += 0.15
        elif metadata.word_count >= 1000:
            score += 0.1

        # 結構豐富度 (10%)
        if metadata.has_tables or metadata.has_figures:
            score += 0.1

        return round(min(1.0, score), 2)

    def chunk_content(self, content: str, metadata: Optional[DocumentMetadata] = None) -> List[Dict]:
        """
        將內容分塊

        使用 LangChain RecursiveCharacterTextSplitter

        Args:
            content: 文檔內容
            metadata: 元資料（可選）

        Returns:
            分塊列表，每個包含 text 和 metadata
        """
        chunks = self.chunker.split_text(content)

        chunk_list = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "chunk_id": i,
                "char_count": len(chunk),
                "word_count": len(chunk.split())
            }

            # 附加文檔元資料
            if metadata:
                chunk_data["document_id"] = metadata.document_id
                chunk_data["source_file"] = metadata.filename
                chunk_data["category"] = metadata.category

            chunk_list.append(chunk_data)

        return chunk_list

    def batch_process(self,
                     file_paths: List[str],
                     show_progress: bool = True) -> List[ProcessingResult]:
        """
        批量處理文檔

        Args:
            file_paths: 檔案路徑列表
            show_progress: 是否顯示進度

        Returns:
            處理結果列表
        """
        results = []

        if show_progress:
            try:
                from tqdm import tqdm
                iterator = tqdm(file_paths, desc="Processing documents")
            except ImportError:
                iterator = file_paths
                print(f"Processing {len(file_paths)} documents...")
        else:
            iterator = file_paths

        for file_path in iterator:
            result = self.process_document(file_path)
            results.append(result)

            # 避免過度負載
            time.sleep(0.1)

        return results

    def get_stats(self) -> Dict:
        """
        獲取處理統計

        Returns:
            統計字典
        """
        stats = self.stats.copy()
        if stats['total_processed'] > 0:
            stats['success_rate'] = round(
                stats['success_count'] / stats['total_processed'] * 100,
                1
            )
            stats['avg_time'] = round(
                stats['total_time'] / stats['total_processed'],
                2
            )
        return stats

    def reset_stats(self):
        """重置統計"""
        self.stats = {
            'total_processed': 0,
            'success_count': 0,
            'failed_count': 0,
            'total_time': 0.0
        }


# ===== 輔助函數 =====

def scan_directory(directory: Path,
                   extensions: Optional[List[str]] = None) -> List[Path]:
    """
    掃描目錄，找出所有符合的文檔

    Args:
        directory: 目錄路徑
        extensions: 檔案副檔名列表（預設 ['.pdf', '.docx', '.txt']）

    Returns:
        檔案路徑列表
    """
    if extensions is None:
        extensions = ['.pdf', '.docx', '.txt', '.md']

    files = []
    for ext in extensions:
        files.extend(directory.rglob(f"*{ext}"))

    return sorted(files)


def results_to_dataframe(results: List[ProcessingResult]) -> pd.DataFrame:
    """
    將處理結果轉換為 DataFrame

    Args:
        results: 處理結果列表

    Returns:
        pandas DataFrame
    """
    data = []

    for result in results:
        if result.success and result.metadata:
            row = result.metadata.to_dict()
            row['processing_time'] = result.processing_time
            row['processing_success'] = True
        else:
            row = {
                'processing_success': False,
                'error': result.error,
                'processing_time': result.processing_time
            }

        data.append(row)

    return pd.DataFrame(data)


# ===== 示例使用 =====

if __name__ == "__main__":
    # 示例：處理單個文檔
    processor = DocumentProcessor(config={
        'quality_threshold': 0.75,
        'chunk_size': 1000
    })

    # 假設有一個測試檔案
    test_file = "../../papers/01_model_paradigm/2017_Transformer.pdf"

    if Path(test_file).exists():
        result = processor.process_document(test_file)

        if result.success:
            print(f"✅ 處理成功: {result.metadata.title}")
            print(f"   品質分數: {result.metadata.quality_score}")
            print(f"   字數: {result.metadata.word_count:,}")

            # 分塊
            chunks = processor.chunk_content(result.content, result.metadata)
            print(f"   分塊數: {len(chunks)}")
        else:
            print(f"❌ 處理失敗: {result.error}")

        # 顯示統計
        stats = processor.get_stats()
        print(f"\n📊 處理統計:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    else:
        print(f"測試檔案不存在: {test_file}")
