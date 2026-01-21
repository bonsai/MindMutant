# MindMutant

遺伝的アルゴリズム（GA）と自然言語処理（NLP）を融合させた、新規アイデア生成エンジン。
既存の概念（単語）を「遺伝子」と見なし、交差・突然変異・淘汰のプロセスを経て、予期せぬ新しいコンセプトを進化させます。

## 🚀 概要

「アイデアとは既存の要素の新しい組み合わせである」
MindMutant はこの定義を生物学的シミュレーションとして実装しました。

- **進化**: 単語同士が交配し、新たな「子供」が生まれます。
- **評価**: 意外性（Novelty）と意味の繋がり（Coherence）でアイデアを評価。
- **ライフサイクル**: 世代（G）を重ね、優秀なアイデアだけが生き残ります。

## 🛠 技術スタック

- **Core**: Python 3.9+
- **Algorithm**: DEAP (Evolutionary Computation)
- **NLP**: spaCy (Vector & Similarity)
- **UI**: Streamlit

## 📦 セットアップ

```bash
# クローン
git clone https://github.com/bonsai/MindMutant.git
cd MindMutant

# 依存パッケージのインストール
pip install -r requirements.txt
python -m spacy download en_core_web_md

# アプリケーション起動
streamlit run app.py
```

## 📂 ディレクトリ構成

- `gen/`: コアロジック (GA, NLP, Fitness)
- `data/`: ドメイン定義とキーワード (JSON)
- `app.py`: Streamlit エントリーポイント
- `task.md`: 開発タスク管理
- `adr.md`: アーキテクチャ・仕様詳細
