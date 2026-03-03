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
4. さらに、関連する他のエピソードも複数ピックアップし、記事の厚みを出す素材にする
5. `generation_log.json` を確認し、過去30日以内に同じテーマで生成していないか確認

**ユーザーに確認**: 選定したテーマ、コンテンツ類型、使用するエピソード一覧を提示し、OKか聞く。ユーザーがテーマを指定した場合はそれに従う。

---

## Step 2: 素材確認・質問

1. 選定したテーマに必要な体験談素材が `experience_database.md` に十分あるか確認する
2. **素材が足りない場合**: ユーザーに質問してエピソードを引き出す
3. **有益情報（ノウハウ・データ等）が必要な場合**: Web検索でリサーチし、方向性をユーザーに事前確認する

---

## Step 3: 長文ポストの生成

`persona.json` の設定に **完全に従って** 、Xの長文ポスト（ロングフォーム）を **1本** 作成する。

### 投稿のボリューム・形式

- **2,000〜5,000文字** を目安（ブログ記事と遜色ないボリューム）
- 体験談を密に盛り込み、読者をファン化させるストーリーテリング
- Xの長文ポスト機能（最大25,000文字）を活用

### 構造

1. **フック**（冒頭2〜3行）: スクロールを止めさせる導入
2. **導入**: 自己紹介 + この投稿で伝えたいことの概要
3. **本文**: 体験談を中心に、複数のエピソード・具体的な数字を交えて深く展開
4. **学び・教訓**: 読者が持ち帰れるポイントを整理
5. **締め**: 読者への応援メッセージ

### 必ず守るルール

- 口調は **穏やか**、偉そうぶらない
- 語尾は「〜だと思う」「〜なんだよね」「〜してみて」のような柔らかい口語体
- 自分の実体験をベースにする（リアリティが命）
- 一文は短めに。改行を多用して読みやすく
- 具体的な数字・状況・感情を入れる
- 箇条書きや区切り線（───）で構造化
- 失敗談も正直に書く → 信頼とファン化につながる
- **リンクは含めない**
- 末尾にハッシュタグ（最大3個）

---

## Step 4: ユーザー確認

生成した長文ポストをユーザーに提示し確認してもらう。
修正希望があれば対応する。OKが出たら次へ。

---

## Step 5: 出力と保存

1. 今日の日付でファイルを作成する

出力先: `/Users/kodaiyamada/develop/x_post/output/YYYY-MM-DD_buzz-post.md`

以下のフォーマットで出力する：

```markdown
# Xバズ投稿案 — YYYY-MM-DD

- **類型**: [選定した類型]
- **テーマ**: [選定したテーマ]
- **参照エピソード**: [使用した全エピソード]
- **文字数**: [文字数]

---

[投稿本文]
```

2. `generation_log.json` を更新する
3. `neta_db.json` の該当テーマの `used_count` を +1 する

---

## Step 6: GitHubに保存

変更をGitHubにコミット＆プッシュする：

```bash
cd /Users/kodaiyamada/develop/x_post && git add -A && git commit -m "バズ投稿: [テーマの要約]" && git push origin main
```

---

## Step 7: Discord通知

生成結果をDiscordに通知する：

```bash
cd /Users/kodaiyamada/develop/x_post && python3 scripts/notify_discord.py notify /tmp/buzz_post_notify.json
```

通知用JSONは `/tmp/buzz_post_notify.json` に保存してから実行。

---

## 完了

ユーザーはDiscordやGitHubで記事を確認し、Xに投稿する。
