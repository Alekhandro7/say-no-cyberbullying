import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import numpy
import re

from tensorflow.python.keras.layers import Dense, recurrent, Input,  Dropout, Embedding
from tensorflow.python.keras.models import Sequential
from keras._tf_keras.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.engine import data_adapter

def _is_distributed_dataset(ds):
    return isinstance(ds, data_adapter.input_lib.DistributedDatasetSpec)

data_adapter._is_distributed_dataset = _is_distributed_dataset

with open('test_positive.txt', 'r', encoding='utf-8') as f:
    texts_true=f.readlines()
    texts_true[0].replace('/ufeff', '')

with open('test_negative.txt', 'r', encoding='utf-8') as f:
    texts_false=f.readlines()
    texts_false[0].replace('/ufeff', '')

texts=texts_true+texts_false
count_true=len(texts_true)
count_false=len(texts_false)
total_lines=count_true+count_false
print(count_true, count_false, total_lines)

maxWordsCount=1000
tokenizer=Tokenizer(num_words=maxWordsCount, filters='!_@#$%^&*()-=+"№;:?*.,<>\t\n\r', lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts(texts)

dist=list(tokenizer.word_counts.items())
print(dist[:10])
print(texts[0][:100])

max_text_len=10
data=tokenizer.texts_to_sequences(texts)
data_pad=pad_sequences(data, maxlen=max_text_len)
print(data_pad)

print(list(tokenizer.word_index.items()))

X=data_pad
Y=np.array([[1, 0]]*count_true+[[0, 1]]*count_false)
print(X.shape, Y.shape)

indesec=numpy.random.choice(X.shape[0], size=X.shape[0], replace=False)
X=X[indesec]
Y=Y[indesec]

model=Sequential()
model.add(Embedding(maxWordsCount, 128, input_length=max_text_len))
model.add(recurrent.LSTM(128, return_sequences=True))
model.add(recurrent.LSTM(64))
model.add(Dense(2, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

history=model.fit(X, Y, batch_size=32, epochs=50)

reverse_word_map=dict(map(reversed, tokenizer.word_index.items()))

def sequence_to_text(list_of_indices):
    words=[reverse_word_map.get(letter) for letter in list_of_indices]
    return(words)

for i in open('chats.csv', 'r'):
    print(i)
    t=i.lower()
    data=tokenizer.texts_to_sequences([t])
    data_pad=pad_sequences(data, maxlen=max_text_len)
    print(sequence_to_text(data[0]))

rez=model.predict(data_pad)
print(rez, np.argmax(rez), sep='\n')
if np.argmax(rez)==1:
    print("Внимание, похоже на угрозу кибербуллинга!!!")
else:
    print("Похоже, что угроз не обнаружено. Хорошего вам дня;)")