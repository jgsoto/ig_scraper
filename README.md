# 📊 Instagram Scraper & Analytics Tool

A Python-based tool to scrape Instagram profile data and perform basic engagement and behavior analysis.

---

## 🚀 Features

* 🔍 Scraping:

  * Profile (followers, basic info)
  * Posts (likes, comments, views)
  * Followers
  * Following

* 📊 Analytics:

  * Total and average engagement
  * Engagement rate (views & followers)
  * Top-performing posts
  * Content consistency
  * Benford’s Law analysis

* 🧠 Interactive system:

  * CLI menu
  * Select what to scrape
  * Control how much data to fetch

---

## 🗂️ Project Structure

```
project/
│
├── main.py            # Main menu / entry point
├── browser.py         # Playwright setup
├── perfil.py          # Profile scraper
├── posts.py           # Posts scraper (GraphQL)
├── followers.py       # Followers & following scraper
├── engagement.py      # Metrics & analysis
├── cookies.py         # Cookie loader
│
└── data/              # (Optional) output files
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright

```bash
playwright install
```

---

## ▶️ Usage

Run the program:

```bash
python main.py
```

### Menu options:

```
1. Profile
2. Posts
3. Followers
4. Following
5. All
6. Engagement
7. Benford Analysis
0. Exit
```

---

## 📊 Engagement Metrics

The system calculates:

* **Total Engagement** → likes + comments
* **Average Engagement per post**
* **Engagement Rate (views):**

  ```
  engagement / views
  ```
* **Engagement Rate (followers):**

  ```
  engagement / followers
  ```

---

## 📁 Output

Data is automatically saved as:

```
<username>_data.json
```

Example:

```json
{
  "perfil": {...},
  "posts": [...],
  "followers": [...],
  "following": [...],
  "engagement": {...},
  "benford": {...}
}
```

---

## ⚠️ Important Notes

* Instagram frequently changes its internal API.
* Heavy usage may lead to:

  * rate limits
  * checkpoints
  * temporary blocks

### Recommended:

* Use valid cookies
* Limit request frequency
* Avoid aggressive scraping


---

## 📄 License

This project is for educational purposes only.

---

## 👨‍💻 Author

Developed by José Soto