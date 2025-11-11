# 整合性架構與設計文件 (Unified Architecture & Design Document) - TMF 知識上傳與治理自動化平台

---

**文件版本 (Document Version):** `v1.0`  
**最後更新 (Last Updated):** `2025-04-05`  
**主要作者 (Lead Author):** `RIVER.CHEN 陳殿河（技術架構師）`  
**審核者 (Reviewers):** `[架構委員會, DMS 知識治理組, 核心開發團隊]`  
**狀態 (Status):** `審核中 (In Review)`  

---

## 目錄 (Table of Contents)

- [整合性架構與設計文件 (Unified Architecture \& Design Document) - TMF 知識上傳與治理自動化平台](#整合性架構與設計文件-unified-architecture--design-document---tmf-知識上傳與治理自動化平台)
  - [目錄 (Table of Contents)](#目錄-table-of-contents)
  - [第 1 部分：架構總覽 (Architecture Overview)](#第-1-部分架構總覽-architecture-overview)
    - [1.1 C4 模型：視覺化架構](#11-c4-模型視覺化架構)
    - [1.2 DDD 戰略設計 (Strategic DDD)](#12-ddd-戰略設計-strategic-ddd)
    - [1.3 Clean Architecture 分層](#13-clean-architecture-分層)
    - [1.4 技術選型與決策](#14-技術選型與決策)
  - [第 2 部分：詳細設計 (Detailed Design)](#第-2-部分詳細設計-detailed-design)
    - [2.1 MVP 與模組優先級 (MVP \& Module Priority)](#21-mvp-與模組優先級-mvp--module-priority)
    - [2.2 核心功能：模組設計](#22-核心功能模組設計)
      - [**2.2.1 知識上傳服務 (KnowledgeUploadSvc)**](#221-知識上傳服務-knowledgeuploadsvc)
      - [**2.2.2 NLP 分析服務 (NLPAnalysisSvc)**](#222-nlp-分析服務-nlpanalysissvc)
      - [**2.2.3 品質評分引擎 (QualityEngineSvc)**](#223-品質評分引擎-qualityenginesvc)
      - [**2.2.4 知識熱點服務 (KnowledgeHeatmapSvc)**](#224-知識熱點服務-knowledgeheatmapsvc)
    - [2.3 非功能性需求設計 (NFRs Design)](#23-非功能性需求設計-nfrs-design)
  - [第 3 部分：附錄 (Appendix)](#第-3-部分附錄-appendix)
    - [A. 與現有系統整合說明](#a-與現有系統整合說明)
    - [B. 風險與緩解策略](#b-風險與緩解策略)
  - [文件總結](#文件總結)

---

**目的**: 本文件旨在將業務需求轉化為一個完整、內聚的技術藍圖。文件依序：
- 先呈現整體架構視角，建立共同語言與決策脈絡；
- 再深入模組與流程細節，說明如何落實核心能力；
- 最後補充整合介面與風險管理，確保執行階段有完整參考。

---

## 第 1 部分：架構總覽 (Architecture Overview)

*此部分關注系統的宏觀結構與指導原則，回答「系統由什麼組成？」以及「它們之間如何互動？」。*

### 1.1 C4 模型：視覺化架構

*我們使用 [C4 模型](https://c4model.com/) 來從不同層次視覺化軟體架構。*

*   **L1 - 系統情境圖 (System Context Diagram):**

    ```mermaid
    graph TD
        A[技術工程師] -->|上傳文件、標註關鍵字| B(TMF 知識上傳與治理平台)
        C[知識管理員] -->|審核、監控知識品質| B
        D[專案經理] -->|查詢知識熱點與缺口| B
        E[現有 TMF 平台] -->|單一登入、權限同步、知識儲存| B
        F[企業目錄 (AD/LDAP)] -->|使用者認證| B
        G[AI 模型服務 (內部)] -->|提供 NLP 分析與建議| B
    ```

    *描述本系統與外部使用者/系統的互動。本系統為 TMF 平台的增強模組，與現有 TMF 系統深度整合，並依賴企業認證系統與內部 AI 服務。*

*   **L2 - 容器圖 (Container Diagram):**

    ```mermaid
    graph TD
        subgraph "用戶端"
            WebApp[Web App - React.js]
        end

        subgraph "服務層"
            APIGateway[API Gateway - Spring Cloud Gateway]
            AuthSvc[認證服務 - Keycloak]
            KnowledgeUploadSvc[知識上傳服務]
            NLPAnalysisSvc[NLP 分析服務]
            QualityEngineSvc[品質評分引擎]
            KnowledgeHeatmapSvc[知識熱點服務]
            NotificationSvc[通知服務]
        end

        subgraph "數據與事件層"
            TMFDB[(TMF 知識資料庫 - PostgreSQL)]
            NLPModelDB[(NLP 模型參數庫 - MongoDB)]
            EventStore[(事件儲存 - Kafka)]
            Cache[(Redis - 緩存)]
        end

        WebApp --> APIGateway
        APIGateway --> AuthSvc
        APIGateway --> KnowledgeUploadSvc
        APIGateway --> NLPAnalysisSvc
        APIGateway --> QualityEngineSvc
        APIGateway --> KnowledgeHeatmapSvc
        APIGateway --> NotificationSvc

        KnowledgeUploadSvc --> TMFDB
        NLPAnalysisSvc --> NLPModelDB
        NLPAnalysisSvc --> TMFDB
        QualityEngineSvc --> TMFDB
        KnowledgeHeatmapSvc --> TMFDB
        KnowledgeUploadSvc --> EventStore
        QualityEngineSvc --> EventStore
        Cache --> APIGateway
        Cache --> KnowledgeHeatmapSvc
    ```

    *描述系統由哪些可部署單元組成。系統採用微服務架構，各服務獨立部署，共用 PostgreSQL 資料庫儲存知識主體，並使用 Kafka 處理異步事件，Redis 緩存熱點資料。*

*   **L3 - 元件圖 (Component Diagram):**

    *（選填，聚焦核心服務：KnowledgeUploadSvc）*

    ```mermaid
    graph TD
        subgraph "KnowledgeUploadSvc"
            UploadAPI[REST API Controller]
            FileParser[文件解析器 - PDF/DOCX]
            TextExtractor[文本提取器]
            KeywordExtractor[關鍵字提取器 - TF-IDF + BERT]
            DomainClassifier[領域分類器 - ML 模型]
            RuleEngine[規則引擎 - 知識品質檢查]
            Validator[資料驗證器]
            TMFAdapter[TMF 資料庫適配器]
            EventPublisher[事件發布器]
        end

        UploadAPI --> FileParser
        FileParser --> TextExtractor
        TextExtractor --> KeywordExtractor
        TextExtractor --> DomainClassifier
        TextExtractor --> RuleEngine
        KeywordExtractor --> Validator
        DomainClassifier --> Validator
        RuleEngine --> Validator
        Validator --> TMFAdapter
        Validator --> EventPublisher
        TMFAdapter --> TMFDB
        EventPublisher --> EventStore
    ```

    *針對核心上傳服務拆解其內部模組，展示從文件上傳到知識儲存的完整處理流程。*

### 1.2 DDD 戰略設計 (Strategic DDD)

*   **通用語言 (Ubiquitous Language):**

    | 詞彙 | 定義 |
    | :--- | :--- |
    | **知識文件 (Knowledge Artifact)** | 由技術人員上傳的技術文件，如設計規範、測試報告、Best Practice 等。 |
    | **應用領域 (Application Domain)** | 技術知識所屬的專業領域，如 `Firmware`, `Mechanical_Motor`, `EMI`。 |
    | **關鍵字 (Keyword)** | 能精準描述文件內容的技術術語，如 `PCB層數`, `BOM自動化`, `ESD防護`。 |
    | **品質評分 (Quality Score)** | 系統根據預設規則自動評估知識文件的完整性與規範性，分為 1~5 分。 |
    | **知識缺口 (Knowledge Gap)** | 某一應用領域下，上傳文件數量少於門檻或平均品質分數低於標準的狀態。 |
    | **治理 (Governance)** | 確保知識文件符合標準、可搜尋、可複用的流程與機制。 |

*   **限界上下文 (Bounded Contexts):**

    ```mermaid
    graph LR
        A[知識上傳上下文] -->|使用| B[知識儲存上下文]
        A -->|觸發事件| C[知識分析上下文]
        C -->|提供建議| A
        C -->|更新指標| D[知識熱點上下文]
        D -->|展示| E[使用者介面]
        B -->|提供資料| D
        F[認證上下文] -->|提供身份| A
        G[通知上下文] -->|發送提醒| A
    ```

    *識別並劃分不同的業務領域：*
    - **知識上傳上下文 (Knowledge Upload Context)**：處理文件上傳、格式驗證、自動標註。
    - **知識分析上下文 (Knowledge Analysis Context)**：執行 NLP 分析、領域分類、關鍵字提取。
    - **知識儲存上下文 (Knowledge Storage Context)**：與現有 TMF 資料庫互動，儲存與查詢知識主體。
    - **知識熱點上下文 (Knowledge Heatmap Context)**：聚合數據，生成可視化報告。
    - **認證上下文 (Authentication Context)**：由企業目錄提供使用者身份。
    - **通知上下文 (Notification Context)**：負責發送審核提醒、品質警告與知識缺口通知。

*各上下文之間透過明確定義的 API 與事件進行溝通。例如，知識上傳成功後，會透過 Kafka 發出 `KnowledgeUploadedEvent`，觸發知識分析上下文進行後續處理，避免緊耦合。防腐層（Anticorruption Layer）用於與現有 TMF 平台對接，確保內部模型不受外部系統變更影響 [[11]]。*

### 1.3 Clean Architecture 分層

*我們的系統遵循 Clean Architecture 原則，以確保關注點分離與測試性。*

*   **Domain Layer（領域層）**：  
    包含核心業務規則與實體，獨立於任何框架或外部系統。  
    - 實體（Entities）：`KnowledgeArtifact`, `DomainCategory`, `Keyword`  
    - 聚合（Aggregates）：`KnowledgeArtifact` 為根聚合，包含其標籤、品質評分、上傳者等相關資訊  
    - 領域服務（Domain Services）：`QualityScoringService`（計算知識文件品質分數的業務邏輯）  

*   **Application Layer（應用層）**：  
    包含應用程式特定的流程與用例，協調領域層與基礎設施層。  
    - 使用案例（Use Cases）：`UploadKnowledgeUseCase`, `AnalyzeKnowledgeUseCase`, `GenerateHeatmapUseCase`  
    - 輸入/輸出模型（DTOs）：`UploadRequest`, `AnalysisResult`, `HeatmapResponse`  
    - 介面（Interfaces）：`KnowledgeRepository`, `NLPAnalyzer`, `NotificationSender`（定義協定，由基礎設施層實現）  

*   **Infrastructure Layer（基礎設施層）**：  
    實現應用層定義的介面，與外部世界互動。  
    - 數據庫存取：`PostgreSQLKnowledgeRepository`（實作 `KnowledgeRepository`）  
    - NLP 實作：`BERTKeywordExtractor`（實作 `NLPAnalyzer`，呼叫內部 AI 模型服務）  
    - 外部系統整合：`TMFAdapter`（與現有 TMF 平台的 REST API 對接）  
    - 消息傳遞：`KafkaEventPublisher`（實作 `EventPublisher`）  
    - 通知服務：`EmailNotificationSender`（實作 `NotificationSender`）  

> *此分層設計確保業務邏輯不依賴於任何技術框架，未來若需更換資料庫或 NLP 引擎，僅需替換基礎設施層的實作，不影響核心業務。*

### 1.4 技術選型與決策

*   **技術棧 (Tech Stack):**

    | 層級 | 技術選型 | 選型理由 |
    | :--- | :--- | :--- |
    | **前端** | React.js + TypeScript + Ant Design | 成熟的元件生態，支援企業級 UI，與現有台達前端框架一致 |
    | **後端** | Java 17 + Spring Boot 3.x | 強大的企業支援、穩定的微服務生態、與台達現有 Java 技術體系兼容 |
    | **API 網關** | Spring Cloud Gateway | 支援路由、認證、限流，與 Spring 生態無縫整合 |
    | **認證** | Keycloak | 開源、支援 SSO 與 LDAP/AD 整合，符合台達企業安全標準 |
    | **資料庫** | PostgreSQL | 支援 JSONB 欄位儲存非結構化元數據，ACID 完整，適合知識圖譜型查詢 |
    | **模型儲存** | MongoDB | 靈活的文件結構，適合儲存 NLP 模型參數與分析結果 |
    | **事件總線** | Apache Kafka | 高吞吐、持久化、支援消費者群組，符合事件驅動架構需求 [[2]] |
    | **快取** | Redis | 低延遲、支援快取熱點查詢與會話管理 |
    | **NLP 引擎** | 內部微調 BERT 模型（基於 Hugging Face） | 基於台達內部技術文件微調，精準度高於通用模型，符合保密要求 |
    | **部署** | Docker + Kubernetes (EKS) | 支援自動擴展、滾動更新，符合雲原生標準 |

*   **架構決策記錄 (ADR):**

    *所有重大決策均記錄於獨立 ADR 文件中，並與本文件保持同步。關鍵決策摘要如下：*  
    - **ADR-001：選擇微服務而非單體架構**：因系統需支援高頻率的知識上傳與異步分析，微服務架構提供更好的獨立部署與擴展能力 [[2]]。  
    - **ADR-002：選擇 Kafka 而非 RabbitMQ**：因系統預期每日處理數萬筆知識事件，Kafka 的高吞吐與持久化特性更適合此場景 [[2]]。  
    - **ADR-003：使用內部微調 BERT 模型而非開源 API**：為確保技術文件的機密性與合規性，所有分析均在內部環境完成，避免資料外洩風險。  
    - **ADR-004：與現有 TMF 平台整合而非重建**：基於成本、使用者習慣與知識資產完整性考量，選擇深度整合而非替代。  

    **→ 參考: [架構決策記錄 (ADR)](../01_adr_template.md)**

> **小結**：第 1 部分界定了系統邊界、核心上下文與技術選型，是後續模組設計與交付優先順序的基礎。接下來的第 2 部分將沿著這些設計原則，說明各核心模組如何落地實作。

---

## 第 2 部分：詳細設計 (Detailed Design)

*此部分聚焦於「如何實現」，定義具體模組的行為、介面與資料流。*

### 2.1 MVP 與模組優先級 (MVP & Module Priority)

*基於商業價值與技術風險，我們將功能分為三個階段交付：*

| 階段 | 模組 | 優先級 | 目標 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **MVP (V1.0)** | 知識上傳服務 + 自動關鍵字建議 | 高 | 降低上傳時間 50% | 核心價值點，解決最痛點：手動標註耗時 |
| | 品質評分引擎 | 高 | 提升知識合格率至 80% | 自動化審核，減少人工負擔 |
| | 知識熱點地圖（基本版） | 中 | 識別前 5 大知識缺口領域 | 支援初步決策 |
| **Phase 2 (V1.1)** | 通知服務（郵件/系統通知） | 高 | 提升知識更新率 | 主動提醒使用者補強知識 |
| | 知識關聯推薦（基於相似文件） | 中 | 提高知識複用率 | 基於內容相似度推薦相關文件 |
| | 上傳問卷自動填補 | 中 | 減少重複輸入 | 從文件內容自動提取背景、效益 |
| **Phase 3 (V1.2)** | AI 智能搜尋（自然語言查詢） | 高 | 實現「問問題找知識」 | 集成 LLM，提供語意搜尋能力 |
| | 知識成熟度評估模型 | 高 | 量化知識資產價值 | 建立知識 KPI 與年度評估機制 |
| | 跨 BU 知識共享儀表板 | 低 | 推動知識協作文化 | 展示跨部門知識流動熱點 |

> *MVP 預計在 6 個月內完成，確保快速驗證價值並收集使用者回饋。*

### 2.2 核心功能：模組設計

*以下為 MVP 核心模組的詳細設計。*

#### **2.2.1 知識上傳服務 (KnowledgeUploadSvc)**

* **輸入**：PDF/DOCX 文件、上傳者資訊、應用領域（可選）  
* **處理流程**：  
  1. **文件解析**：使用 Apache Tika 解析文件內容，提取純文字。  
  2. **文本預處理**：移除頁眉/頁腳、表格轉文字、正則過濾無用符號。  
  3. **關鍵字提取**：呼叫 `NLPAnalysisSvc`，使用微調 BERT 模型進行實體識別（NER）與 TF-IDF 加權，輸出 Top 5 候選關鍵字。  
  4. **領域分類**：呼叫 `NLPAnalysisSvc`，使用分類模型判斷最可能的 3 個應用領域（如 `Firmware`, `EMI`, `Mechanical_Motor`），並提供置信度分數。  
  5. **品質評分**：呼叫 `QualityEngineSvc`，執行 5 項規則檢查：  
      - 摘要長度 ≥ 100 字  
      - 關鍵字數量 ≥ 3 個  
      - 機密等級已勾選（非「公開」）  
      - 有明確的「問題」與「解決方案」段落  
      - 文件名符合命名規範（`[BU]_[Type]_[Date]_[Title].pdf`）  
  6. **資料驗證與儲存**：若所有檢查通過，將文件內容、提取的關鍵字、領域、品質分數、元數據存入 PostgreSQL（TMFDB），並發布 `KnowledgeUploadedEvent` 至 Kafka。  
  7. **使用者介面回應**：在前端顯示建議的關鍵字與領域，供使用者確認或修改。若品質檢查失敗，則顯示具體錯誤訊息並阻止上傳。  

* **輸出**：上傳成功/失敗狀態、建議關鍵字、建議領域、品質評分、錯誤清單。  
* **介面定義**：  
  ```java
  public interface KnowledgeUploadService {
      UploadResult upload(KnowledgeUploadRequest request);
  }
  ```

#### **2.2.2 NLP 分析服務 (NLPAnalysisSvc)**

* **角色**：獨立微服務，專注於自然語言處理，供多個上游服務呼叫。  
* **技術實現**：  
  - 使用 Hugging Face Transformers 庫，基於 `bert-base-chinese` 模型，在台達內部 50,000 篇技術文件上進行微調。  
  - 訓練任務：  
      - **實體識別 (NER)**：識別技術術語（如 `PCB`, `ESD`, `BOM`）  
      - **領域分類**：將文件分類至 20 個預定義技術領域  
  - **輸入**：純文字內容（≤ 5000 字）  
  - **輸出**：JSON 格式，包含 `keywords: [string]`, `domains: [{name: string, confidence: float}]`  
* **效能**：單次分析延遲 ≤ 800ms（在 4 vCPU 環境下）。  
* **模型更新**：每月自動重新訓練，使用新上傳的高品質文件作為正樣本，提升準確率。  

#### **2.2.3 品質評分引擎 (QualityEngineSvc)**

* **核心邏輯**：基於規則引擎（Drools）實現，可動態更新規則而無需重啟服務。  
* **評分規則範例**：  
  ```java
  rule "Summary Length Check"
      when
          $artifact : KnowledgeArtifact( summary.length < 100 )
      then
          $artifact.addQualityIssue("摘要長度不足，建議至少100字");
  end

  rule "Confidentiality Check"
      when
          $artifact : KnowledgeArtifact( confidentiality == Confidentiality.PUBLIC )
      then
          $artifact.addQualityIssue("機密等級未設定，請選擇非公開等級");
  end
  ```
* **最終品質分數**：`5 - (違規項目數 × 0.5)`，最低為 1 分。  
* **輸出**：`QualityScore`（1~5）與 `QualityIssues`（清單）供前端展示。  

#### **2.2.4 知識熱點服務 (KnowledgeHeatmapSvc)**

* **功能**：聚合全平台知識數據，生成可視化報告。  
* **資料來源**：從 PostgreSQL 定期（每小時）讀取 `KnowledgeArtifact` 表，計算：  
  - 各應用領域的文件總數  
  - 各領域的平均品質分數  
  - 每月上傳趨勢  
* **輸出**：REST API 提供 JSON 格式熱點數據：  
  ```json
  {
    "domains": [
      {
        "name": "Firmware",
        "count": 182,
        "avgQuality": 4.2,
        "isGap": False
      },
      {
        "name": "EMI",
        "count": 8,
        "avgQuality": 2.1,
        "isGap": true
      }
    ],
    "trend": [
      {"month": "2025-03", "uploads": 156},
      {"month": "2025-04", "uploads": 189}
    ]
  }
  ```
* **前端展示**：使用 ECharts 繪製熱力圖與趨勢折線圖，並以紅色標示「知識缺口」領域（數量 < 10 且平均分 < 2.5）。  

### 2.3 非功能性需求設計 (NFRs Design)

*以下設計確保系統滿足第 2 部分定義的 NFRs。*

| NFR 分類 | 設計實現 |
| :--- | :--- |
| **性能** | - 使用 Redis 緩存熱點知識熱點數據，減少資料庫查詢。<br>- NLP 分析服務部署於獨立 Kubernetes HPA（水平擴展），根據 Kafka 消費者滯後量自動擴容。<br>- API 延遲目標：`Upload` ≤ 1.5s, `Heatmap` ≤ 300ms。 |
| **可擴展性** | - 所有微服務均無狀態設計，可透過 Kubernetes 水平擴展。<br>- Kafka 主題按 `domain` 分區，支援未來新增技術領域。<br>- 資料庫使用分庫分表策略（按 `bu_id`），支援未來 10 倍資料量。 |
| **可用性** | - 核心服務部署於 3 個可用區（AZ），負載均衡器實現跨區流量分發。<br>- 資料庫每日全備份 + 每 15 分鐘 binlog 備份，RPO < 5 分鐘，RTO < 20 分鐘。<br>- 所有服務具備健康檢查與自動重啟機制。 |
| **安全性** | - 所有 API 透過 OAuth 2.0 + JWT 驗證，權限基於 RBAC（角色：工程師、管理員、審核員）。<br>- 文件上傳至 S3 儲存桶，並啟用服務端加密（SSE-S3）。<br>- NLP 模型訓練與推理均在內部私有雲環境執行，禁止任何外部連線。 |
| **合規性** | - 所有使用者資料與文件內容儲存於台灣境內伺服器，符合《個資法》與台達內部資訊安全規範。 |
| **可維護性** | - 所有服務具備標準化日誌（JSON 格式，送至 ELK Stack）。<br>- 使用 OpenTelemetry 進行分散式追蹤，可追蹤單一上傳請求的完整鏈路。<br>- 每個微服務提供 Swagger UI 文件與 Prometheus 監控指標。 |

> **小結**：第 2 部分落實了「誰做什麼」的細節，並將 NFR 要求轉化為可執行的設計準則。第 3 部分將這些模組拉回企業既有環境，說明如何與外部系統協作並管控風險。

---

## 第 3 部分：附錄 (Appendix)

### A. 與現有系統整合說明

| 整合點 | 方式 | 說明 |
| :--- | :--- | :--- |
| **使用者認證** | LDAP/AD 集成 | 透過 Keycloak 與台達企業目錄同步，無需獨立帳號。 |
| **知識儲存** | REST API + 資料庫直連 | 知識上傳服務透過 `TMFAdapter` 將資料寫入現有 TMF 的 `knowledge_artifact` 資料表，確保資料一致性。 |
| **通知系統** | 內部郵件平台 | 通知服務透過台達內部 SMTP 服務發送郵件，與現有通知機制統一。 |

### B. 風險與緩解策略

| 風險 | 說明 | 緩解策略 |
| :--- | :--- | :--- |
| **NLP 模型準確率不足** | 初期關鍵字建議錯誤率高，使用者不信任 | - 開放使用者「修正建議」功能，並回饋至訓練資料庫。<br>- 定期進行 A/B 測試，確認新模型提升幅度後再上線。 |
| **事件堆積造成延遲** | Kafka 消費端異常導致知識分析延遲 | - 監控 `lag` 指標並設定自動擴容策略。<br>- 提供手動重處理流程，確保重要文件可優先處理。 |
| **跨系統整合風險** | TMF 平台 API 版本更新造成介面不相容 | - 透過防腐層隔離版本差異。<br>- 與 TMF 團隊建立發版同步機制，提前驗證介面變更。 |

---

## 文件總結

- **架構視角**：定義了邊界、上下文與技術決策，為團隊建立共同語言。  
- **設計視角**：詳述 MVP 模組與 NFR 對應作法，確保交付節奏與品質指標清楚。  
- **落地視角**：整理整合點與風險緩解策略，避免執行階段出現溝通落差。

此文件可作為開發、測試、營運等跨部門協作時的參考主軸，後續若有設計更新，請同步維護本文件與對應 ADR。