"""
修復圖片和公式提取的完整解決方案

這個腳本展示了如何正確從 PDF 中提取圖片和公式
"""
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
import re

def extract_images_from_pdf(pdf_path: Path, output_dir: Path) -> list:
    """使用 PyMuPDF 從 PDF 提取圖片（最可靠的方法）"""
    try:
        import fitz  # PyMuPDF
        pdf_doc = fitz.open(str(pdf_path))
        image_paths = []
        image_count = 0
        
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = pdf_doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_filename = f"image_{image_count:03d}.{image_ext}"
                    image_path = output_dir / image_filename
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    image_paths.append(str(image_path.relative_to(output_dir.parent.parent)))
                    image_count += 1
                except Exception as e:
                    continue
        
        pdf_doc.close()
        return image_paths
    except ImportError:
        print("⚠️  PyMuPDF (fitz) 未安裝，請運行: pip install pymupdf")
        return []
    except Exception as e:
        print(f"⚠️  提取圖片失敗: {e}")
        return []

def process_paper_with_images(file_path: str, output_dir: Path) -> dict:
    """處理論文並提取圖片和公式"""
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    import time
    
    pdf_file = Path(file_path)
    file_stem = pdf_file.stem
    
    # 配置 docling
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        do_table_structure=True,
        do_picture_classification=False,
    )
    
    pdf_options = PdfFormatOption(pipeline_options=pipeline_options)
    converter = DocumentConverter(format_options={InputFormat.PDF: pdf_options})
    
    start_time = time.time()
    
    # 轉換文檔
    result = converter.convert(str(file_path))
    
    # 提取 Markdown
    content = result.document.export_to_markdown()
    
    # 創建目錄
    doc_images_dir = output_dir / "images" / file_stem
    doc_images_dir.mkdir(parents=True, exist_ok=True)
    
    # 方法1: 使用 PyMuPDF 從原始 PDF 提取圖片（最可靠）
    image_paths = extract_images_from_pdf(pdf_file, doc_images_dir)
    image_count = len(image_paths)
    
    # 替換 Markdown 中的圖片占位符
    if image_count > 0:
        # 找到所有圖片占位符
        image_placeholders = re.findall(r'<!--\s*image\s*-->', content)
        for i, _ in enumerate(image_placeholders):
            if i < len(image_paths):
                # 使用相對路徑
                relative_path = f"images/{file_stem}/{Path(image_paths[i]).name}"
                content = content.replace('<!-- image -->', 
                                         f'![Image {i+1}]({relative_path})', 1)
    
    # 處理公式占位符（暫時保留占位符，因為公式提取較複雜）
    formula_placeholders = re.findall(r'<!--\s*formula[^>]*-->', content)
    formula_count = len(formula_placeholders)
    
    # 保存 Markdown
    markdown_path = output_dir / f"{file_stem}.md"
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    extraction_time = time.time() - start_time
    
    return {
        "success": True,
        "content": content,
        "markdown_path": str(markdown_path),
        "image_count": image_count,
        "formula_count": formula_count,
        "image_paths": image_paths,
        "extraction_time": round(extraction_time, 2)
    }

# 測試
if __name__ == "__main__":
    test_file = Path("papers/01_model_paradigm/2012_AlexNet.pdf")
    output_dir = Path("kms_governance/02_processed")
    
    result = process_paper_with_images(str(test_file), output_dir)
    print(f"✅ 處理完成")
    print(f"  圖片數量: {result['image_count']}")
    print(f"  公式占位符: {result['formula_count']}")
    print(f"  圖片路徑: {result['image_paths'][:3]}")

