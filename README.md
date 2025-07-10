
# ⚡ YB Scam Classifier GUI ⚡

A stylish desktop application built with **PyQt5** to detect **scam or spam messages** using machine learning and keyword analysis.  
It uses an AI model trained on labeled messages to identify spam, highlight reasons, and show confidence scores.

---

## 🧠 Features

- 🔍 **Spam Detection** using a trained ML model (`model.pkl`)
- 💬 **Text Preprocessing** with NLTK (stopwords + stemming)
- ⚠️ **Keyword Flagging** (e.g., "loan", "win", "verify")
- 🎨 **Animated Matrix-style UI** (green/black theme)
- ✅ **Typewriter Effect** to display detection results
- 🔁 **Reset Button** to clear input/output

---

## 🖼️ Preview

> Input your message in the text box → Click `🧠 SCAN MESSAGE` → Result shows below with spam reason and confidence.

---

## 🛠️ Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install pyqt5 nltk
```

---

## 📁 Files

| File Name             | Description                          |
|-----------------------|--------------------------------------|
| `scam_classifier_gui.py` | Main PyQt5 GUI script                |
| `model.pkl`           | Trained ML classification model      |
| `vectorizer.pkl`      | Fitted vectorizer (e.g., TfidfVectorizer) |
| `README.md`           | Project documentation (this file)    |

---

## 🚀 How to Run

1. Ensure `model.pkl` and `vectorizer.pkl` are in the same folder.
2. Then run the app using:

```bash
python scam_classifier_gui.py
```

---

## 🔒 How It Works

1. Cleans the input message (punctuation, stopwords, stemming)
2. Transforms text using `vectorizer.pkl`
3. Predicts class (spam/safe) using `model.pkl`
4. Highlights matched **spam keywords**
5. Displays confidence score with animated output

---

## ✅ Example Safe Message

```
Your order #456-123456 has been shipped. Track it for delivery details.
```

## 🛑 Example Spam Message

```
Congratulations! You won ₹2 lakh. Click here to claim your prize now!
```

---

## 📌 Notes

- You must have an internet connection the first time to download NLTK stopwords.
- Make sure to use the correct `.pkl` files (same ones used during training).

---

## 👨‍💻 Author

**YB**  
Made with ❤️ using Python and AI
