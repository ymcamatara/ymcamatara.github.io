# YMCA Matara Website - User Guide (v2.0)

A complete guide for managing the YMCA Matara website with the automated news system.

---

## 📁 Project Structure

```
ymca-matara/
├── index.html          ← Landing page (About YMCA Matara)
├── news.html           ← News list with filters (auto-generated)
├── build_site.py       ← Python automation script
└── news/               ← Your programme folders go here
    └── [programme-name]/
        ├── info.json       ← Metadata (title, date, description)
        ├── article.md      ← Full content in Markdown
        ├── photo1.jpg      ← Media files (optional)
        └── index.html      ← Auto-generated
```

---

## 🚀 Quick Start: Adding a New Programme

### Step 1: Create a Folder

Create a new folder inside `news/` with a descriptive name:

```
news/youth-leadership-camp-2024/
news/football-tournament/
news/community-cleanup-drive/
```

### Step 2: Create info.json

Create `info.json` inside your folder with this format:

```json
{
  "title": "Youth Leadership Camp 2024",
  "date": "2024-12-15",
  "description": "Two-day leadership training with 50 participants."
}
```

| Field | Description |
|-------|-------------|
| `title` | Programme name (displayed on cards and page header) |
| `date` | Event date in `YYYY-MM-DD` format (used for sorting and filtering) |
| `description` | Short summary shown on the programme card |

### Step 3: Create article.md

Create `article.md` with your full content using Markdown:

```markdown
We successfully hosted our annual Youth Leadership Camp!

## Programme Highlights
- Leadership workshops
- Team-building activities
- Public speaking training

## Results
**Winners:** Team Alpha

Thank you to all participants!
```

**Supported Markdown:**
- `## Headings` (use ## for main sections)
- `- Bullet lists`
- `1. Numbered lists`
- `**Bold text**`
- `*Italic text*`
- `> Blockquotes`
- `---` Horizontal rules

### Step 4: Add Photos & Videos (Optional)

Drop your media files directly into the folder:

```
news/football-tournament/
├── info.json
├── article.md
├── opening-ceremony.jpg
├── trophy-presentation.jpg
└── match-highlights.mp4
```

**Supported formats:**
- **Images:** .jpg, .jpeg, .png, .gif, .webp, .svg
- **Videos:** .mp4, .webm, .mov

### Step 5: Run the Build Script

```bash
py build_site.py
```

You should see:
```
==================================================
  YMCA Matara Website Builder v2.0
==================================================

[*] Scanning for programmes...
    Found 2 programme(s)

[*] Generating news.html with filters...
    [OK] Created: news.html

[*] Generating programme pages...
    [OK] Created: news/football-tournament/index.html
         3 media file(s) included

[+] Build complete!
```

### Step 6: Preview Locally

```bash
py -m http.server 8000
```

Open: **http://localhost:8000**

### Step 7: Deploy to GitHub

```bash
git add .
git commit -m "Added football tournament programme"
git push
```

---

## 🔍 Using the Filter Feature

The News page includes **Year** and **Month** filter dropdowns:

1. **Year Filter**: Automatically populated with years from your programmes
2. **Month Filter**: January through December
3. **"All" Options**: Show all programmes regardless of date

When no programmes match your filter selection, a "No programmes found" message appears.

---

## 📋 Common Tasks

### Editing a Programme

1. Navigate to the programme folder: `news/programme-name/`
2. Edit `info.json` to change title, date, or description
3. Edit `article.md` to change the content
4. Run `py build_site.py`
5. Commit and push

### Deleting a Programme

1. Delete the entire folder: `news/programme-name/`
2. Run `py build_site.py`
3. Commit and push

---

## 🔧 First-Time GitHub Pages Setup

### 1. Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it: `ymca-matara`
3. Set to **Public**
4. Create repository

### 2. Push Your Code

```bash
cd ymca-matara
git init
git add .
git commit -m "Initial commit: YMCA Matara website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ymca-matara.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Repository → **Settings** → **Pages**
2. Source: **main** branch
3. Click **Save**

Your site: `https://YOUR-USERNAME.github.io/ymca-matara/`

---

## ❓ Troubleshooting

### "markdown library not found"

```bash
pip install markdown
```

### Programme not appearing

- Check `info.json` exists and is valid JSON
- Verify date format is `YYYY-MM-DD`
- Run `py build_site.py` again

### Images not showing

- Check file extensions are lowercase
- Ensure files are in the programme folder
- Avoid special characters in filenames

---

*Last updated: January 2026*
