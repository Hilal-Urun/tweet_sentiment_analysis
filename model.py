import numpy as np
import pandas as pd
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.models import load_model
from keras.utils.np_utils import to_categorical
import re
import glob

turkish_characters = "a|b|c|ç|d|e|f|g|ğ|h|ı|i|j|k|l|m|n|o|ö|p|r|s|ş|t|u|ü|v|y|z|0-9"
data = pd.read_csv("data/data.tsv", header=0, \
                    delimiter="\t", quoting=3)

data = data[['Review','Sentiment']]

# Veri Setinin temizlenmesi
data['Review'] = data['Review'].apply(lambda x: x.lower())
data['Review'] = data['Review'].apply((lambda x: re.sub('[^'+turkish_characters+'\s]','',x)))
    

# Veri setimizin işlenebilmesi için text verileri numaralara çevrilir, bunun için kerasın hazır tokenizer sınıfı kullanıldı
# Tokenizer sınıfı data içerisinde verilen cümleleri analiz eder ve kelimelerin sıklıklarını hesaplar
tokenizer = Tokenizer(split=' ',num_words=25000) #En sık geçen 25000 kelimeye odaklanıldı 

tokenizer.fit_on_texts(data['Review'].values) # Her bir kelimenin sıklığı hesaplanır
X = tokenizer.texts_to_sequences(data['Review'].values)
# Bütün metinler 400 sütundan oluşan bir dizi ile temsil edilecek. Kısa olanlara 0, uzun olanlar kesilir
X = pad_sequences(X,maxlen=400)


embed_dim = 128 #Her bir kelimenin temsil edileceği vektör boyutunu belirler. 
lstm_out = 128
def build_model():
    model = Sequential()
    model.add(Embedding(25000, embed_dim,input_length = X.shape[1], dropout=0.2))
    model.add(LSTM(lstm_out, dropout_U=0.2, dropout_W=0.2))
    model.add(Dense(2,activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    return model

# Çıktılarımızı kategorik hale getirdik. (Opsiyonel)
Y = pd.get_dummies(data['Sentiment']).values

# Verinin %80'i train, %20'si test verisi olacak şekilde ayrılır.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, random_state = 2)

model = build_model()
# Oluşturulan model train verileri ile eğitilir. Yapay Sinir Ağı eğitilmeye başlar.
# nb_epoch: İterasyon sayısı
model.fit(X_train, Y_train, nb_epoch = 3, batch_size=32, verbose = 2)
# Train verileri ile model eğitildikten sonra test dataları ile doğruluk oranlarına bakılır.
score = model.evaluate(X_test, Y_test, verbose = 2)
print("score: %.2f" % (score[1]))

# Save Model
#model.save("models/sentiment_3440_model.h5")

# Load Model. Daha önce eğitilmiş olan model. Veriseti yada model parametreleri değişirse
# bu model geçersiz olur. Eğitim işlemi uzun sürdüğü için ağı bir defa eğitip oluşan modeli kaydettim.
model = load_model("models/sentiment_3440_model.h5")
def readFile(filename):
    corpus_raw = u""
    print("Reading '{0}'...".format(filename))
    with codecs.open(filename, "r", "utf-8") as book_file:
        corpus_raw += book_file.read()
    return corpus_raw
my_text = " Bugün hava çok kötü!! "

# Verilen örnekler Tokenizer yapısı ile tam sayı dizisine dönüştürülür
# Daha sonra eğitilen modele sırayla verilerek anlam analizi sonuçları elde edilir.
# Her Cümlenin yüzde kaç olumlu ve olumsuz olduğuna dair bilgiler çıktı olarak verilir.
sequences = tokenizer.texts_to_sequences(my_text)
data = pad_sequences(sequences, maxlen=400)
predictions = model.predict(data)

print(predictions)
