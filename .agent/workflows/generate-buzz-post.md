---
description: Xでバズりそうな投稿案を3パターン生成し、GitHubに保存してDiscordに通知する
---

# /generate-buzz-post ワークフロー

// turbo-all

## 事前準備

以下のファイルを読み込んでコンテキストを把握する：
- `/Users/kodaiyamada/develop/x_post/data/persona.json` — ペルソナ設定・口調・NG事項
- `/Users/kodaiyamada/develop/x_post/data/neta_db.json` — ネタDB（50テーマ）
- `/Users/kodaiyamada/develop/x_post/data/generation_log.json` — 過去の生成ログ（重複回避用）
- `/Users/kodaiyamada/develop/saas-blog-writer/data/experience_database.md` — 体験談データベース

---

## Step 1: テーマ選定

1. `neta_db.json` から **使用回数（used_count）が少ない** テーマを優先してピックアップする
2. コンテンツ類型のウェイトを考慮する：
   - 有益まとめ: 35%
   - 体験談: 35%
   - 共感ツイート: 15%
   - 逆張り・意見系: 15%
3. 選定したテーマに `related_ep` がある場合は、`experience_database.md` から該当エピソードの詳細を取得
4. `generation_log.json` を確認し、過去30日以内に同じテーマで生成していないか確認

**ユーザーに確認**: 選定したテーマとコンテンツ類型を提示し、OKか聞く。ユーザーがテーマを指定した場合はそれに従う。

---

## Step 2: 投稿案の生成

`persona.json` の設定に **完全に従って** 、3パターンのX投稿案を生成する。

### 必ず守るルール

- **280文字以内**（Xの日本語文字数上限）
- 口調は **穏やか**、偉そうぶらない
- 語尾は「〜だと思う」「〜なんだよね」「〜してみて」のような柔らかい口語体
- 自分の実体験をベースにする
- 絵文字は **1〜2個まで**
- ハッシュタグは **最大2個**（#転職 #SaaS営業 等）
- **リンクは含めない**
- 改行を適度に使って読みやすく

### 類型別の書き方

**有益まとめ:**
- 冒頭に「これ知らない人多すぎる」のようなフックを入れる
- 箇条書きで3〜5個のポイントを整理
- 最後に「保存しておいて」等のCTAを軽く

**体験談:**
- 「正直に言います」等の冒頭で引きを作る
- Before → 転機 → After の構造
- 具体的な数字や状況を入れてリアリティを出す
- 最後に学びを1行で

**共感ツイート:**
- 短文でテンポ良く
- 「わかる人にはわかる」空気感
- リプで「わかる！」と言いたくなる内容

**逆張り・意見系:**
- 常識に対して「実はそうじゃない」という切り口
- 攻撃的にならず穏やかに本質を突く
- 最後に提案型で締める

---

## Step 3: 出力と保存

1. 今日の日付でファイルを作成する

出力先: `/Users/kodaiyamada/develop/x_post/output/YYYY-MM-DD_buzz-post.md`

以下のフォーマットで出力する：

```markdown
# Xバズ投稿案 — YYYY-MM-DD

- **類型**: [選定した類型]
- **テーマ**: [選定したテーマ]
- **参照エピソード**: [あれば]

---

## 案1

[投稿文]

---

## 案2

[投稿文]

---

## 案3

[投稿文]
```

2. `generation_log.json` を更新する：
   - `generated` 配列に新しいエントリを追加
   - フォーマット:
```json
{
  "date": "YYYY-MM-DD",
  "type": "類型",
  "theme": "テーマ",
  "theme_id": 1,
  "episode": "EP-XXX",
  "filename": "YYYY-MM-DD_buzz-post.md"
}
```
   - `last_updated` を更新

3. `neta_db.json` の該当テーマの `used_count` を +1 する

**ユーザーに確認**: 生成された3案を提示し、修正希望があれば対応する。OKが出たら次へ。

---

## Step 4: GitHubに保存

変更をGitHubにコミット＆プッシュする：

```bash
cd /Users/kodaiyamada/develop/x_post && git add -A && git commit -m "バズ投稿案: [テーマの要約]" && git push origin main
```

---

## Step 5: Discord通知

生成結果をDiscordに通知する。まず通知用のJSONファイルを一時作成し、通知スクリプトを実行する：

```bash
cd /Users/kodaiyamada/develop/x_post && python3 scripts/notify_discord.py notify /tmp/buzz_post_notify.json
```

通知用JSONは以下の形式で `/tmp/buzz_post_notify.json` に保存してから実行：
```json
{
  "type": "類型",
  "theme": "テーマ",
  "episode": "EP-XXX",
  "filename": "YYYY-MM-DD_buzz-post.md",
  "posts": ["案1の本文", "案2の本文", "案3の本文"]
}
```

---

## 完了

これでワークフロー完了。ユーザーはDiscordに届いた投稿案を見て、気に入ったものをXに投稿する。
