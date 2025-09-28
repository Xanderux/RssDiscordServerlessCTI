# RSS to Discord Bot (via GitHub Actions)

This project automatically fetches articles from RSS feeds and posts them to a Discord channel via webhook — every hour — using GitHub Actions.

## How to Set It Up (in 4 Steps)

### 1. Fork this Repository
Click the **Fork** button on GitHub to create your own copy of the project.

---

### 2. Create a Discord Webhook
On your Discord server:
1. Go to **Server Settings** → **Integrations** → **Webhooks**
2. Click **New Webhook**
3. Choose a channel
4. Copy the **Webhook URL**

You’ll need this in the next step.

---

### 3. Add the Webhook as a GitHub Secret

In your newly forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Use:
   - **Name:** `DISCORD_WEBHOOK_URL`
   - **Value:** _paste your Discord webhook URL_

Save it 

---

### 4. Create `feeds.txt` at the project root

At the root of your forked repo, create a file named: `feeds.txt`

Add **one RSS feed URL per line**, for example:
```commandline
https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v
https://blog.sekoia.io/feed/
```

Commit and push the file.

---

## How It Works

- The GitHub Action runs **every hour**
- It reads RSS feeds from `feeds.txt`
- If a new article appears, it posts:
  - Title
  - Link
  - Publication date
- Messages are sent to your Discord channel via the webhook
- Already sent articles are tracked in `sent_urls.txt` (auto-committed)

---

## Manually Trigger the Workflow

You can also run it manually:
- Go to **Actions** in your GitHub repo
- Select the workflow
- Click **“Run workflow”**

---

## Need to Add or Remove Feeds Later?

Just edit `feeds.txt`, commit, and the workflow will use the updated list.

---

## ✅ That’s it!

Once you've completed the four steps, the bot works automatically — no hosting, no server, no cron jobs.  
If you need help or improvements, feel free to open an issue!
