#!/usr/bin/env python3
"""
Paper Download Script
Download all papers mentioned in course_content.md
"""

import os
import time
from pathlib import Path
from typing import Dict, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Paper metadata structure - Total: 33 papers
PAPERS: List[Dict] = [
    # 🧩 Model Paradigm Shift (11 papers)
    {
        "category": "01_model_paradigm",
        "year": "2004",
        "name": "Brook_for_GPUs",
        "url": "https://dl.acm.org/doi/pdf/10.1145/1015706.1015800",
        "type": "pdf",
        "note": "ACM paywall - requires institutional access"
    },
    {
        "category": "01_model_paradigm",
        "year": "2012",
        "name": "AlexNet",
        "url": "https://proceedings.neurips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf",
        "type": "pdf"
    },
    {
        "category": "01_model_paradigm",
        "year": "2014",
        "name": "Seq2Seq",
        "arxiv_id": "1409.3215",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2015",
        "name": "Knowledge_Distillation",
        "arxiv_id": "1503.02531",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2015",
        "name": "ResNet",
        "arxiv_id": "1512.03385",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2017",
        "name": "Transformer",
        "arxiv_id": "1706.03762",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2017",
        "name": "AlphaGo_Zero",
        "url": "https://www.nature.com/articles/nature24270.pdf",
        "type": "pdf",
        "note": "Nature paywall - may require subscription"
    },
    {
        "category": "01_model_paradigm",
        "year": "2017",
        "name": "MoE",
        "arxiv_id": "1701.06538",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2021",
        "name": "LoRA",
        "arxiv_id": "2106.09685",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2022",
        "name": "Chain_of_Thought",
        "arxiv_id": "2201.11903",
        "type": "arxiv"
    },
    {
        "category": "01_model_paradigm",
        "year": "2022",
        "name": "ReAct",
        "arxiv_id": "2210.03629",
        "type": "arxiv"
    },

    # ⚙️ Infrastructure & Data (5 papers - The Bitter Lesson is a blog post, not downloadable PDF)
    {
        "category": "02_infrastructure",
        "year": "2019",
        "name": "ZeRO",
        "arxiv_id": "1910.02054",
        "type": "arxiv"
    },
    {
        "category": "02_infrastructure",
        "year": "2020",
        "name": "Scaling_Laws",
        "arxiv_id": "2001.08361",
        "type": "arxiv"
    },
    {
        "category": "02_infrastructure",
        "year": "2022",
        "name": "LAION_5B",
        "arxiv_id": "2210.08402",
        "type": "arxiv"
    },
    {
        "category": "02_infrastructure",
        "year": "2023",
        "name": "RefinedWeb",
        "arxiv_id": "2306.01116",
        "type": "arxiv"
    },
    {
        "category": "02_infrastructure",
        "year": "2024",
        "name": "MegaScale",
        "arxiv_id": "2402.15627",
        "type": "arxiv"
    },

    # 🗣 Language Models (8 papers)
    {
        "category": "03_language_models",
        "year": "2013",
        "name": "Word2Vec",
        "arxiv_id": "1301.3781",
        "type": "arxiv"
    },
    {
        "category": "03_language_models",
        "year": "2016",
        "name": "Google_NMT",
        "arxiv_id": "1609.08144",
        "type": "arxiv"
    },
    {
        "category": "03_language_models",
        "year": "2018",
        "name": "GPT_1",
        "url": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf",
        "type": "pdf"
    },
    {
        "category": "03_language_models",
        "year": "2018",
        "name": "BERT",
        "arxiv_id": "1810.04805",
        "type": "arxiv"
    },
    {
        "category": "03_language_models",
        "year": "2019",
        "name": "GPT_2",
        "url": "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf",
        "type": "pdf"
    },
    {
        "category": "03_language_models",
        "year": "2020",
        "name": "GPT_3",
        "arxiv_id": "2005.14165",
        "type": "arxiv"
    },
    {
        "category": "03_language_models",
        "year": "2022",
        "name": "InstructGPT",
        "arxiv_id": "2203.02155",
        "type": "arxiv"
    },
    {
        "category": "03_language_models",
        "year": "2024",
        "name": "TULU_3",
        "arxiv_id": "2407.15541",
        "type": "arxiv"
    },

    # 🖼 Multimodal Models (8 papers)
    {
        "category": "04_multimodal",
        "year": "2014",
        "name": "DeepVideo",
        "url": "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42455.pdf",
        "type": "pdf",
        "note": "CVPR 2014"
    },
    {
        "category": "04_multimodal",
        "year": "2014",
        "name": "Two_Stream_CNN",
        "arxiv_id": "1406.2199",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2015",
        "name": "GAN",
        "arxiv_id": "1406.2661",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2020",
        "name": "DDPM",
        "arxiv_id": "2006.11239",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2020",
        "name": "ViT",
        "arxiv_id": "2010.11929",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2021",
        "name": "CLIP",
        "arxiv_id": "2103.00020",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2022",
        "name": "Stable_Diffusion",
        "arxiv_id": "2112.10752",
        "type": "arxiv"
    },
    {
        "category": "04_multimodal",
        "year": "2022",
        "name": "DiT",
        "arxiv_id": "2212.09748",
        "type": "arxiv"
    },
]


def create_session() -> requests.Session:
    """Create session with retry strategy"""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Set user agent to avoid blocking
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    return session


def download_paper(paper: Dict, base_dir: Path, session: requests.Session) -> str:
    """
    Download a single paper

    Args:
        paper: Paper metadata dict
        base_dir: Base directory for downloads
        session: Requests session

    Returns:
        Status string: "success", "skip", or "fail"
    """
    # Create category directory
    category_dir = base_dir / paper["category"]
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = f"{paper['year']}_{paper['name']}.pdf"
    filepath = category_dir / filename

    # Skip if already downloaded
    if filepath.exists():
        print(f"[OK] Already exists: {filename}")
        return "skip"

    # Determine download URL
    if paper["type"] == "arxiv":
        url = f"https://arxiv.org/pdf/{paper['arxiv_id']}.pdf"
    elif paper["type"] == "pdf":
        url = paper["url"]
    else:
        print(f"[FAIL] Unknown type for: {filename}")
        return "fail"

    # Download with progress
    try:
        print(f"[DOWN] Downloading: {filename} ...")
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()

        # Check if it's actually a PDF
        content_type = response.headers.get("content-type", "")
        if "pdf" not in content_type.lower() and not url.endswith(".pdf"):
            print(f"[WARN] {filename} might not be a PDF (content-type: {content_type})")

        # Write to file
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[OK] Downloaded: {filename} ({filepath.stat().st_size // 1024} KB)")
        return "success"

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"[SKIP] Access denied (403): {filename} - may require institutional access")
            print(f"       Manual download: {url}")
            return "skip"
        else:
            print(f"[FAIL] HTTP error {e.response.status_code} for {filename}")
            return "fail"
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Failed to download {filename}: {str(e)}")
        return "fail"
    except Exception as e:
        print(f"[FAIL] Unexpected error for {filename}: {str(e)}")
        return "fail"


def main():
    """Main execution function"""
    print("=" * 60)
    print("Paper Downloader - AI Evolution: 36 Papers Collection")
    print("=" * 60)
    print()

    # Setup base directory
    base_dir = Path(__file__).parent / "papers"
    base_dir.mkdir(exist_ok=True)

    # Create session
    session = create_session()

    # Statistics
    total = len(PAPERS)
    success = 0
    failed = 0
    skipped = 0

    # Download each paper
    for idx, paper in enumerate(PAPERS, 1):
        print(f"\n[{idx}/{total}] {paper['name']}")

        result = download_paper(paper, base_dir, session)

        if result == "success":
            success += 1
        elif result == "skip":
            skipped += 1
        else:
            failed += 1

        # Be polite to servers
        time.sleep(1)

    # Summary
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total papers: {total}")
    print(f"[OK] Successfully downloaded: {success}")
    print(f"[SKIP] Already existed: {skipped}")
    print(f"[FAIL] Failed: {failed}")
    print()
    print(f"Papers saved to: {base_dir.absolute()}")
    print()

    # Show directory structure
    print("Directory structure:")
    for category in sorted(base_dir.iterdir()):
        if category.is_dir():
            files = list(category.glob("*.pdf"))
            print(f"  {category.name}/ ({len(files)} papers)")
            for file in sorted(files):
                print(f"    - {file.name}")


if __name__ == "__main__":
    main()
