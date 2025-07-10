import sys
import pickle
import string
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# NLTK setup
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Preprocessing
def clean_text(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

# Spam indicators
spam_keywords = [
    

    "win", "prize", "free", "verify", "click", "blocked", "₹", "gift", "now",
    "claim", "link", "account", "suspended", "offer", "urgent", "congratulations",
    "selected", "lottery", "redeem", "pay", "reward", "kyc", "loan", "credit",
    "cash", "atm", "approved", "emi", "limit", "personal", "instant"

]

class ScamClassifier(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡YB SCAM CLASSIFIER⚡")
        self.setGeometry(100, 100, 850, 600)
        self.setStyleSheet("background-color: #000000;")
        self.initUI()

    def initUI(self):
        title = QLabel("⚡ YB SCAM CLASSIFIER ⚡")
        title.setFont(QFont("Consolas", 26, QFont.Bold))
        title.setStyleSheet("color: #ffe600; padding: 15px;")
        title.setAlignment(Qt.AlignCenter)

        instruction = QLabel("💬 Enter your message:")
        instruction.setFont(QFont("Consolas", 13, QFont.Bold))
        instruction.setStyleSheet("color: #00ff88;")
        instruction.setAlignment(Qt.AlignCenter)

        self.textEdit = QTextEdit()
        self.textEdit.setFont(QFont("Consolas", 12))
        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff88;
                border: 2px solid #00ff88;
                padding: 10px;
            }
        """)

        self.resultLabel = QLabel("")
        self.resultLabel.setFont(QFont("Consolas", 16, QFont.Bold))
        self.resultLabel.setStyleSheet("""
            QLabel {
                color: #00ff88;
                border: 2px solid #ffe600;
                padding: 15px;
            }
        """)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setWordWrap(True)

        scanBtn = QPushButton("🧠 SCAN MESSAGE")
        scanBtn.setFont(QFont("Consolas", 12, QFont.Bold))
        scanBtn.setStyleSheet("""
            QPushButton {
                color: #00ff88;
                background-color: #000000;
                border: 2px solid #00ff88;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #003300;
            }
        """)
        scanBtn.clicked.connect(self.analyze_text)

        resetBtn = QPushButton("↺ RESET FIELD")
        resetBtn.setFont(QFont("Consolas", 12, QFont.Bold))
        resetBtn.setStyleSheet("""
            QPushButton {
                color: #00ff88;
                background-color: #000000;
                border: 2px solid #00ff88;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #330000;
            }
        """)
        resetBtn.clicked.connect(self.clear_text)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(scanBtn)
        btnLayout.addWidget(resetBtn)

        footer = QLabel("~ powered by AI | spam detection + reason engine ~")
        footer.setFont(QFont("Consolas", 9))
        footer.setStyleSheet("color: #007700;")
        footer.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(instruction)
        layout.addWidget(self.textEdit)
        layout.addLayout(btnLayout)
        layout.addWidget(self.resultLabel)
        layout.addWidget(footer)

        self.setLayout(layout)

    def analyze_text(self):
        text = self.textEdit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "⚠ Warning", "Please enter a message.")
            return

        cleaned = clean_text(text)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)
        score = model.decision_function(vector)[0]
        confidence = round(100 / (1 + math.exp(-abs(score))), 2)

        # Find matching spam keywords
        matched = [word for word in spam_keywords if word in cleaned]

        # Format reason
        reason_text = f"\n\nDetected keywords: {matched}" if matched else "\n\nNo suspicious keywords found."

        if prediction[0] == 1:
            final_text = f"🛑 SPAM DETECTED ({confidence}% confidence){reason_text}"
            color = "#ff3333"
        else:
            final_text = f"✅ SAFE MESSAGE ({confidence}% confidence){reason_text}"
            color = "#00ff88"

        self.show_result(final_text, color)

    def show_result(self, text, color):
        self.resultLabel.setStyleSheet(f"""
            color: {color};
            border: 2px solid #ffe600;
            padding: 15px;
        """)
        self.resultLabel.setText("")
        self.full_text = text
        self.current_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._typewriter)
        self.timer.start(25)

    def _typewriter(self):
        if self.current_index <= len(self.full_text):
            self.resultLabel.setText(self.full_text[:self.current_index])
            self.current_index += 1
        else:
            self.timer.stop()

    def clear_text(self):
        self.textEdit.clear()
        self.resultLabel.clear()

# Run GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScamClassifier()
    window.show()
    sys.exit(app.exec_())
