import pandas as pd
import string
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

nltk.download('stopwords')

# 1. Load original dataset
df = pd.read_csv("spam.csv", encoding='latin-1')[['v1', 'v2']]
df.columns = ['label', 'text']
df = df[df['label'].isin(['ham', 'spam'])]

# 2. Add custom spam messages
custom_spam = [
    "Your ATM card has been blocked. Click here to reactivate immediately.",
    "Congratulations! You’ve won a free smartphone. Claim now at http://fakeprize.com",
    "URGENT: Your SBI account has been suspended. Click to verify.",
    "Win ₹1,00,000 cash prize. Just reply YES now!",
    "Your UPI service is disabled. Complete eKYC now to continue using services.",
    "Final notice: Your electricity bill is overdue. Pay now or disconnection will occur.",
    "Verify your PAN card immediately to avoid penalties.",
    "HDFC alert: Netbanking blocked due to inactivity. Reactivate now.",
    "Your EMI card is approved for ₹3,00,000. Click to verify details.",
    "Congratulations! ₹500000 personal loan approved. Confirm now.",
    "Your EMI offer is ready. Tap here to activate your ₹2 lakh limit."
    " Your EMI Card with 300000/- Limit is approved. Please verify your details now."
    "We noticed an unusual transaction. Call 1800-000-0000 to verify.",
    "आपका PF account deactivate hone ja raha hai. Login now to stop.",
    "Claim your FREE $100 Amazon voucher here!",
    "आप Lucky draw ke winner hain. ₹10,000 ka prize jeet chuke hain!",
    "Congratulations! You’ve won a MacBook Pro. Click to claim.",
    "Flipkart offer: ₹5000 cashback valid only for 10 minutes!",
    "Free fuel for 3 months. Register now!",
    "iPhone 15 giveaway! Register here and win.",
    "आपको ₹1000 ka recharge mila hai. Activate karein abhi.",
    "You've been selected for an Apple Watch. Confirm now!",
    "Win a BMW by filling this survey: http://scamsite.com/survey",
    "Pay ₹10 and get ₹200 recharge. Only today!",
    "Your Chase account has been locked. Click to resolve immediately.",
    "SBI se sandesh: Aapka ATM block ho gaya hai. Verify karein turant.",
    "Dear customer, you’ve received a payment of $800. Check here: http://fraudurl.com",
    "Bank of America alert: Suspicious login detected. Secure account now.",
    "आपका PAN card suspend ho gaya hai. Click karein verify karne ke liye.",
    "Your credit card statement is overdue. Clear balance to avoid penalty.",
    "KYC pending hai. Click karein apna eKYC update karne ke liye.",
    "Netflix subscription expired. Update card details to continue.",
    "WhatsApp backup failed. Tap here to fix.",
    "Paytm alert: Login from unknown device. Secure your wallet.",
    "LinkedIn: Your profile will be suspended. Last warning!",
    "Airtel warning: Account closure in 12 hours without recharge.",
    "Your FedEx delivery is held. Pay $3.99 clearance fee.",
    "आपका parcel customs me phasa hai. ₹50 pay karein release karne ke liye.",
    "Amazon package delayed. Confirm address urgently.",
    "Your shipment needs KYC clearance. Upload now.",
    "Delivery attempt failed. Click to reschedule.",
    "Courier returned to sender. Pay to redeliver.",
    "Parcel from Flipkart is ready. Click for tracking.",
    "You have 1 new package. Open link to confirm.",
    "Order #99781 failed due to unpaid charges. Pay now.",
    "Earn $1000 per week from home. No experience needed!",
    "Work from home job offer. Apply now and get ₹15,000 bonus.",
    "Life insurance offer closing soon. Buy now for ₹1/day.",
    "Loan approved! Click to disburse ₹50,000 instantly.",
    "Instant cash loan, no documents required. Tap here.",
    "You are shortlisted for TCS. Submit fee ₹499 to confirm.",
    "LIC se message: Policy expired. Renew abhi.",
    "Axis Bank loan offer: EMI ₹999 only. Apply today.",
    "Job confirmed. Pay ₹199 for processing.",
    "Join WFH company and earn ₹5000 daily."
]

# 3. Add to dataset
df = pd.concat([df, pd.DataFrame({'label': ['spam'] * len(custom_spam), 'text': custom_spam})], ignore_index=True)

# 4. Text Cleaning
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [ps.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

df['transformed'] = df['text'].apply(transform)

# 5. TF-IDF with ngram
tfidf = TfidfVectorizer(ngram_range=(1, 2))
X = tfidf.fit_transform(df['transformed'])

# 6. Encode labels
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
df = df.dropna()
y = df['label']

# 7. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# 8. Train model
model = LinearSVC()
model.fit(X_train, y_train)

# 9. Save model and vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

# 10. Accuracy
print("✅ Train Accuracy:", model.score(X_train, y_train))
print("✅ Test Accuracy :", model.score(X_test, y_test))
