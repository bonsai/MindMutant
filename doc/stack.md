# Technology Stack

| Category | Technology | Usage |
|----------|------------|-------|
| **Lang** | Python 3.9+ | |
| **GA** | Python (Custom) | 個体管理、進化エンジンの構築（独自実装） |
| **NLP** | spaCy | `ja_core_news_md` モデルを使用したベクトル演算 |
| **Math** | NumPy (<2) | ベクトル計算（互換性のためv1系に固定） |
| **Data** | JSON | 世代データ管理 (data/g{N}/*.json) |
| **Viz** | HTML5/JS | `wordcrowd.html` によるタグクラウド表示 |