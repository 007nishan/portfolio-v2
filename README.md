# Nishan's Portfolio Website

Flask-based portfolio website showcasing my journey to becoming an Amazon Business Analyst.

## Features

- 📊 141 Daily Coding Challenges (Sep 2025 - Feb 2026)
- 🐍 Python Learning Journey
- 🗄️ SQL Mastery Progress
- 🤖 Machine Learning Path
- 💼 Professional Portfolio

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Images

Copy all challenge images to `static/images/`:

```bash
mkdir -p static/images
cp /mnt/project/*.jpg static/images/
```

### 3. Run Locally

```bash
python app.py
```

Visit: http://localhost:5000

## Project Structure

```
portfolio/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── home.html        # Homepage
│   ├── challenges.html  # Daily challenges
│   ├── sql.html         # SQL journey
│   ├── python.html      # Python journey
│   ├── ml.html          # ML journey
│   └── about.html       # About me
└── static/              # Static files
    ├── css/            # Custom styles
    ├── js/             # JavaScript
    └── images/         # Challenge images
```

## Deployment Options

### Option 1: PythonAnywhere (FREE)
1. Sign up at pythonanywhere.com
2. Upload code
3. Set Python version to 3.10+
4. Configure WSGI file
5. Done!

### Option 2: Render (FREE)
1. Push code to GitHub
2. Connect Render to repo
3. Deploy automatically
4. Free SSL included

### Option 3: Vercel (FREE)
1. Install vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
4. Done!

## TODO

- [ ] Add individual challenge detail pages
- [ ] Integrate chatbot (Gemini API)
- [ ] Add SQL journey page
- [ ] Add Python journey page
- [ ] Add ML journey page
- [ ] Add About page with contact form
- [ ] Connect GitHub API for code links
- [ ] Add analytics tracking

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** Bootstrap 5, Jinja2
- **Hosting:** PythonAnywhere/Render/Vercel (FREE)
- **Future:** Gemini API chatbot, Cal.com scheduling

## Contact

- GitHub: [yourusername]
- LinkedIn: [yourprofile]
- Email: your.email@example.com

---

**Status:** In Development
**Last Updated:** February 15, 2026
