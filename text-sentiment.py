import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re
#pip install mkdocs

turkish_characters = "a|b|c|ç|d|e|f|g|ğ|h|ı|i|j|k|l|m|n|o|ö|p|r|s|ş|t|u|ü|v|y|z|0-9"
data = pd.read_csv("data.tsv", header=0,
                   delimiter="\t", quoting=3)

data = data[['Review', 'Sentiment']]

data['Review'] = data['Review'].apply(lambda x: x.lower())
data['Review'] = data['Review'].apply((lambda x: re.sub('[^' + turkish_characters + '\s]', '', x)))

tokenizer = Tokenizer(split=' ', num_words=25000)
tokenizer.fit_on_texts(data['Review'].values)
X = tokenizer.texts_to_sequences(data['Review'].values)
X = pad_sequences(X, maxlen=400)

embed_dim = 128
lstm_out = 128

model = load_model("sentiment_3440_model.h5")

my_text = ["Muhteşem bir film"]

sequences = tokenizer.texts_to_sequences(my_text)
data = pad_sequences(sequences, maxlen=400)
predictions = model.predict(data)

if 0.45 < predictions[0][0] < 0.55:
    print('Nötr')
elif predictions[0][0] > predictions[0][1]:
    print("Negatif")
else:
    print("Pozitif")
