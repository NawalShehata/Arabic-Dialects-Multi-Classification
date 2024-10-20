# preprocessing.py
import tnkeeh as tn
import re
import joblib

def predict_label(text):

    # Text preprocessing
    cleander = tn.Tnkeeh(remove_diacritics=True,
                     remove_html_elements=True,
                     remove_twitter_meta=True,
                     remove_links=True,
                     remove_english=True,
                     remove_repeated_chars=True,
                     remove_long_words=True,
                     normalize=True
                     )

    text = cleander.clean_raw_text(text)
    text = text[0]

    text = text.replace(r'[0-9٠-٩]', '')
    text = text.replace("؟", "")
    text = text.replace("@", "")
    text = text.replace("_", "")
    text = text.replace("-", "")

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    arabic_punctuation_pattern = r'[^\w\s\u0621-\u063A\u0641-\u064A]'
    text = re.sub(arabic_punctuation_pattern, '', text)

    text = re.sub(r'\s+', ' ', text).strip()

    # Load the model and the vectorizer
    clf_balance = joblib.load('models/logistic_regression_model.pkl')
    tfidf = joblib.load('models/tfidf_vectorizer.pkl')
    
    # Transform the input text
    text_transformed = tfidf.transform([text])
    
    # Predict the label
    predicted_label = clf_balance.predict(text_transformed)
    
    return predicted_label[0]
