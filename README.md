# 🐦 Xバズ投稿自動生成ツール

Antigravity ワークフローで、Xでバズりそうな投稿文を生成し、GitHub に保存して Discord に通知するツールです。

## 📋 機能

- **4つのコンテンツ類型に対応**: 有益まとめ・体験談・共感ツイート・逆張り/意見系
- **体験談DB連携**: `saas-blog-writer` の42エピソードを参照
- **ネタDB**: 50テーマをストック（使用回数の少ないものを優先選定）
- **1回の実行で3パターン**の投稿案を生成
- **重複回避**: 過去の生成ログと比較
- **GitHub保存 + Discord通知**

## 🚀 使い方

### 投稿案を生成

Antigravity で以下のワークフローを実行:

```
/generate-buzz-post
```

### 処理フロー

1. テーマを自動選定（or ユーザー指定）
2. Antigravity が3パターンの投稿案を生成
3. `output/YYYY-MM-DD_buzz-post.md` に保存
4. GitHub に push
5. Discord に通知

### リマインダー通知（手動設定する場合）

毎日決まった時間にDiscordリマインダーを送りたい場合：

```bash
python3 scripts/notify_discord.py reminder
```

macOS の `launchd` で定期実行する場合は、以下の plist を作成:

```bash
# ~/Library/LaunchAgents/com.x-post.reminder.plist を作成後:
launchctl load ~/Library/LaunchAgents/com.x-post.reminder.plist
```

## 📁 ファイル構成

```
x_post/
├── README.md
├── .agent/
│   └── workflows/
│       └── generate-buzz-post.md   # ワークフロー定義
├── data/
│   ├── persona.json                # ペルソナ設定
│   ├── neta_db.json                # ネタDB（50テーマ）
│   └── generation_log.json         # 生成ログ
├── scripts/
│   └── notify_discord.py           # Discord通知
└── output/
    └── YYYY-MM-DD_buzz-post.md     # 生成された投稿案
```

## 📊 データ参照

体験談データは以下のファイルを直接参照:
- `/Users/kodaiyamada/develop/saas-blog-writer/data/experience_database.md`
