import json
import urllib.request
import sys
import os
from datetime import datetime

def send_discord_notification(posts_data):
    """生成されたバズ投稿案をDiscordに通知する"""
    webhook_url = "https://discord.com/api/webhooks/1474967648365183218/ywMzNWNMvo-m4pTbcHTbUYhQLyiYfGmTMJihp19rf8t-0E5-CrgVrTazCvAE-izyUzJK"
    
    # GitHubのファイルURLを構築
    repo_base = "https://github.com/kodaiyamada1996-droid/x_post/blob/main"
    file_url = f"{repo_base}/output/{posts_data['filename']}"
    
    # 類型の絵文字マッピング
    type_emojis = {
        "有益まとめ": "📚",
        "体験談": "📖",
        "共感ツイート": "🤝",
        "逆張り・意見系": "💡"
    }
    
    emoji = type_emojis.get(posts_data.get("type", ""), "📝")
    
    # メッセージ構築
    content = f"🐦 **Xバズ投稿案が生成されました！**\n\n"
    content += f"{emoji} **類型**: {posts_data.get('type', '不明')}\n"
    content += f"🎯 **テーマ**: {posts_data.get('theme', '不明')}\n"
    
    if posts_data.get("episode"):
        content += f"📎 **参照エピソード**: {posts_data['episode']}\n"
    
    content += f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    content += f"📂 [GitHubで確認する]({file_url})\n"
    content += "\n---\n\n"
    
    # 各投稿案を追加
    for i, post in enumerate(posts_data.get("posts", []), 1):
        content += f"**案{i}** ({len(post)}文字)\n"
        content += f"```\n{post}\n```\n\n"
    
    data = json.dumps({"content": content}).encode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request(webhook_url, data=data, headers=headers)
    
    try:
        urllib.request.urlopen(req)
        print("✅ Discord notification sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}", file=sys.stderr)
        sys.exit(1)

def send_reminder():
    """毎日のリマインダー通知を送る"""
    webhook_url = "https://discord.com/api/webhooks/1474967648365183218/ywMzNWNMvo-m4pTbcHTbUYhQLyiYfGmTMJihp19rf8t-0E5-CrgVrTazCvAE-izyUzJK"
    
    content = "⏰ **Xバズ投稿の時間です！**\n\n"
    content += "Antigravity で `/generate-buzz-post` を実行してください 🐦\n"
    content += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    data = json.dumps({"content": content}).encode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request(webhook_url, data=data, headers=headers)
    
    try:
        urllib.request.urlopen(req)
        print("✅ Reminder sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send reminder: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Notify:   python notify_discord.py notify <json_file>")
        print("  Reminder: python notify_discord.py reminder")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "reminder":
        send_reminder()
    elif command == "notify":
        if len(sys.argv) < 3:
            print("Usage: python notify_discord.py notify <json_file>")
            sys.exit(1)
        json_file = sys.argv[2]
        with open(json_file, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
        send_discord_notification(posts_data)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
