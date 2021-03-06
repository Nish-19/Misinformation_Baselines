# -*- coding: utf-8 -*-
"""BD_BERT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-tBcv7tBWm7h75rXdD4oussAkcjDdgo2
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x
import tensorflow as tf
print(tf.__version__)

# All general imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer 

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, Reshape, Conv2D, MaxPool2D, Concatenate, Flatten, Dropout, Dense, Bidirectional, GlobalAveragePooling1D, GRU, GlobalMaxPooling1D, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import LSTM, GRU, Conv1D, MaxPool1D, Activation, Add

from tensorflow.keras.models import Model, Sequential

from tensorflow.keras.layers import Dense, Input, Embedding, Dropout, Activation, Conv1D, Softmax
from tensorflow.keras import initializers, regularizers, constraints, optimizers, layers
from tensorflow.keras import backend as K

from tensorflow.keras.callbacks import EarlyStopping

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score
import io, os, gc

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

#################### Importing ByteDance Datasets ####################
# Train set
train_df = pd.read_csv('../data/train_bd.csv')
print(train_df.columns)
le = LabelEncoder()
train_df['bd_label'] = le.fit_transform(train_df['bd_label'])
train_df.head()

# Test set
test_df = pd.read_csv('../data/test_merged_bd.csv')
print(test_df.columns)
test_df['bd_label'] = le.transform(test_df['bd_label'])
test_df.head()

pre_bert_bd = np.load("bd/pre_bert_fbd.npy")
hyp_bert_bd = np.load("bd/hyp_bert_fbd.npy")
print('Premise', pre_bert_bd.shape)
print('Hypothesis', hyp_bert_bd.shape)

pre_bert_bd_test = np.load("bd/pre_bert_test_fbd.npy")
hyp_bert_bd_test = np.load("bd/hyp_bert_test_fbd.npy")
print('Premise', pre_bert_bd_test.shape)
print('Hypothesis', hyp_bert_bd_test.shape)

train_lst_1 = train_df['title1_en'].tolist()
print(len(train_lst_1))
train_lst_1[:5]
train_lst_2 = train_df['title2_en'].tolist()
print(len(train_lst_2))
uq_tr_1 = list(set(train_lst_1))
uq_tr_2 = list(set(train_lst_2))
print(len(uq_tr_1))
print(len(uq_tr_2))
train_merged = uq_tr_1 + uq_tr_2
print('Train Length is', len(train_merged))
train_merged[:5]
test_lst_1 = test_df['title1_en'].tolist()
test_lst_2 = test_df['title2_en'].tolist()
uq_ts_1 = list(set(test_lst_1))
uq_ts_2 = list(set(test_lst_2))
test_merged = uq_ts_1 + uq_ts_2
print('Test merged', len(test_merged))
total_dataset = train_merged + test_merged
print('Dataset length is', len(total_dataset))

# Defining the tokenizer
def get_tokenizer(vocabulary_size):
  print('Training tokenizer...')
  tokenizer = Tokenizer(num_words= vocabulary_size)
  tweet_text = []
  print('Read {} Sentences'.format(len(total_dataset)))
  tokenizer.fit_on_texts(total_dataset)
  return tokenizer

# For getting the embedding matrix
def get_embeddings():
  print('Generating embeddings matrix...')
  embeddings_file = '../data/glove.6B.300d.txt'
  embeddings_index = dict()
  with open(embeddings_file, 'r', encoding="utf-8") as infile:
    for line in infile:
      values = line.split()
      word = values[0]
      vector = np.asarray(values[1:], "float32")
      embeddings_index[word] = vector
	# create a weight matrix for words in training docs
  vocabulary_size = len(embeddings_index)
  embeddinds_size = list(embeddings_index.values())[0].shape[0]
  print('Vocabulary = {}, embeddings = {}'.format(vocabulary_size, embeddinds_size))
  tokenizer = get_tokenizer(vocabulary_size)
  embedding_matrix = np.zeros((vocabulary_size, embeddinds_size))
  considered = 0
  total = len(tokenizer.word_index.items())
  for word, index in tokenizer.word_index.items():
    if index > vocabulary_size - 1:
      print(word, index)
      continue
    else:
      embedding_vector = embeddings_index.get(word)
      if embedding_vector is not None:
        embedding_matrix[index] = embedding_vector
        considered += 1
  print('Considered ', considered, 'Left ', total - considered)			
  return embedding_matrix, tokenizer, embeddings_index

def get_data(tokenizer, MAX_LENGTH, input_df):
  print('Loading data')
  X1, X2, Y = [], [], []
  X1 = input_df['title1_en'].tolist()
  X2 = input_df['title2_en'].tolist()
  Y = input_df['bd_label'].tolist()  
  assert len(X1) == len(X2) == len(Y)
  sequences_1 = tokenizer.texts_to_sequences(X1)
  sequences_2 = tokenizer.texts_to_sequences(X2)
  X1 = pad_sequences(sequences_1, maxlen=MAX_LENGTH)
  X2 = pad_sequences(sequences_2, maxlen=MAX_LENGTH)
  Y = np.array(Y)
  return X1, X2, Y

embedding_matrix, tokenizer, embeddings_index = get_embeddings()

MAX_LENGTH = 20
# read ml data
X1, X2, Y = get_data(tokenizer, MAX_LENGTH, train_df)

X1_test, X2_test, Y_test = get_data(tokenizer, MAX_LENGTH, test_df)

encoder = LabelBinarizer()#convertes into one hot form
encoder.fit(Y)
Y_enc = encoder.transform(Y)
print(Y_enc)

# Considering everything as it is
reduced_X1 = X1
reduced_X2 = X2
reduced_train_labels = train_df['bd_label'].values
reduced_X1_test = X1_test
reduced_X2_test = X2_test
reduced_test_labels = test_df['bd_label'].values
reduced_test_weights = test_df['Weight'].values

print(type(reduced_train_labels))
print(reduced_train_labels.shape)
encoder = LabelBinarizer()#convertes into one hot form
encoder.fit(reduced_train_labels)
Y_enc = encoder.transform(reduced_train_labels)
Y_enc_test = encoder.transform(reduced_test_labels)
print(Y_enc)
print(Y_enc_test)

y_train = tf.keras.utils.to_categorical(reduced_train_labels)
print(y_train)
y_test = tf.keras.utils.to_categorical(reduced_test_labels)
print(y_test)

from sklearn.model_selection import train_test_split
VALIDATION_RATIO = 0.1
RANDOM_STATE = 9527
x1_train, x1_val, \
x2_train, x2_val, \
pre_train_bert, pre_val_bert, \
hyp_train_bert, hyp_val_bert, \
y_train, y_val = \
    train_test_split(
        reduced_X1, reduced_X2, 
        pre_bert_bd, hyp_bert_bd,
        y_train,
        test_size=VALIDATION_RATIO, 
        random_state=RANDOM_STATE
)

print("Training Set")
print("-" * 10)
print(f"x1_train: {x1_train.shape}")
print(f"x2_train: {x2_train.shape}")
print(f"y_train : {y_train.shape}")

print("-" * 10)
print(f"x1_val:   {x1_val.shape}")
print(f"x2_val:   {x2_val.shape}")
print(f"y_val :   {y_val.shape}")
print("-" * 10)
print("Test Set")

NUM_CLASSES = 3

MAX_SEQUENCE_LENGTH = 20

NUM_LSTM_UNITS = 150

MAX_NUM_WORDS = embedding_matrix.shape[0]

NUM_EMBEDDING_DIM = embedding_matrix.shape[1]

# BERT + Normal Grand Model

NUM_LSTM_UNITS = 150

top_input_wd = Input(
    shape=(MAX_SEQUENCE_LENGTH, ), 
    dtype='int32')
bm_input_wd = Input(
    shape=(MAX_SEQUENCE_LENGTH, ), 
    dtype='int32')

embedding_layer = Embedding(
    MAX_NUM_WORDS, NUM_EMBEDDING_DIM)
top_embedded_wd = embedding_layer(
    top_input_wd)
bm_embedded_wd = embedding_layer(
    bm_input_wd)

source_lstm_wd = Bidirectional(LSTM(NUM_LSTM_UNITS, return_sequences=True, recurrent_dropout = 0.3))
shared_lstm_wd = Bidirectional(LSTM(NUM_LSTM_UNITS, activation='tanh', recurrent_dropout = 0.3))
top_source_wd = source_lstm_wd(top_embedded_wd)
bm_source_wd = source_lstm_wd(bm_embedded_wd)

source_comb_wd = concatenate(
    [top_source_wd, bm_source_wd],
    axis=-1
    )
lstm_ops_wd = shared_lstm_wd(source_comb_wd)   # 300D vector


top_input_bt = Input(
    shape=(768, ), 
    dtype='float32')
bm_input_bt = Input(
    shape=(768, ), 
    dtype='float32')


top_embedded_bt = Reshape((1, 768, ))(top_input_bt)
bm_embedded_bt = Reshape((1, 768, ))(bm_input_bt)

source_lstm_bt = Bidirectional(LSTM(NUM_LSTM_UNITS, return_sequences=True, recurrent_dropout = 0.3))
shared_lstm_bt = Bidirectional(LSTM(NUM_LSTM_UNITS, activation='tanh', recurrent_dropout = 0.3))
top_source_bt = source_lstm_bt(top_embedded_bt)
bm_source_bt = source_lstm_bt(bm_embedded_bt)

source_comb_bt = concatenate(
    [top_source_bt, bm_source_bt],
    axis=-1
    )
lstm_ops_bt = shared_lstm_bt(source_comb_bt)  #300D vector

# Bert and Normal Combination

comb_features_bd = Add()([lstm_ops_wd, lstm_ops_bt])

pre_bd = Dense(
    units=64, 
    activation='tanh',
    name = 'pre_bd')(comb_features_bd)

predictions_bd = Dense(
    units=NUM_CLASSES, 
    activation='softmax',
    name = 'bd')(pre_bd)

model = Model(
    inputs=[top_input_wd, bm_input_wd, top_input_bt, bm_input_bt], 
    outputs=predictions_bd)

model.summary()

from tensorflow.keras.optimizers import Adam
lr = 1e-3
opt = Adam(lr=lr, decay=lr/50)
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

BATCH_SIZE = 4096
NUM_EPOCHS = 50
stop = [EarlyStopping(monitor='val_loss', patience=0.001)]
history = model.fit(x=[x1_train, x2_train, pre_train_bert, hyp_train_bert],
                    y=y_train,
                    batch_size=BATCH_SIZE,
                    epochs=NUM_EPOCHS,
                    validation_data=(
                      [x1_val, x2_val, pre_val_bert, hyp_val_bert], 
                      y_val
                    ),
                    shuffle=True,
                    callbacks=stop,
          )

from sklearn import metrics
from sklearn.metrics import classification_report
predictions = model.predict(
    [X1_test, X2_test, pre_bert_bd_test, hyp_bert_bd_test])

y_pred = [idx for idx in np.argmax(predictions, axis=1)]
#print(y_pred)
print('Accuracy is')
print(metrics.accuracy_score(reduced_test_labels, y_pred, sample_weight = reduced_test_weights)*100)
print(classification_report(reduced_test_labels, y_pred, target_names = ['agreed', 'disagreed', 'unrelated'], sample_weight = reduced_test_weights))

# Model 2
NUM_LSTM_UNITS = 128

print('Getting Text CNN model...')
filter_sizes = [2, 3, 5]
num_filters = 128	#Hyperparameters 32,64,128; 0.2,0.3,0.4
drop = 0.4

top_input = Input(
    shape=(MAX_SEQUENCE_LENGTH, ), 
    dtype='int32')
bm_input = Input(
    shape=(MAX_SEQUENCE_LENGTH, ), 
    dtype='int32')

embedding_layer = Embedding(
    MAX_NUM_WORDS, NUM_EMBEDDING_DIM)
top_embedded = embedding_layer(
    top_input)
bm_embedded = embedding_layer(
    bm_input)
reshape = Reshape((MAX_SEQUENCE_LENGTH, NUM_EMBEDDING_DIM, 1))(top_embedded)
reshape_1 = Reshape((MAX_SEQUENCE_LENGTH, NUM_EMBEDDING_DIM, 1))(bm_embedded)
conv_0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], NUM_EMBEDDING_DIM),  padding='valid', kernel_initializer='normal',  activation='relu')(reshape)
conv_1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], NUM_EMBEDDING_DIM),  padding='valid', kernel_initializer='normal',  activation='relu')(reshape_1)
maxpool_0 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(conv_0)
maxpool_1 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(conv_1)
concatenated_tensor = Concatenate(axis=1)([maxpool_0, maxpool_1])
flatten = Flatten()(concatenated_tensor)
dropout = Dropout(drop)(flatten)

top_input_bt = Input(
    shape=(768, ), 
    dtype='float32')
bm_input_bt = Input(
    shape=(768, ), 
    dtype='float32')


top_embedded_bt = Reshape((1, 768, ))(top_input_bt)
bm_embedded_bt = Reshape((1, 768, ))(bm_input_bt)

source_lstm_bt = Bidirectional(LSTM(NUM_LSTM_UNITS, return_sequences=True, recurrent_dropout = 0.3))
shared_lstm_bt = Bidirectional(LSTM(NUM_LSTM_UNITS, activation='tanh', recurrent_dropout = 0.3))
top_source_bt = source_lstm_bt(top_embedded_bt)
bm_source_bt = source_lstm_bt(bm_embedded_bt)

source_comb_bt = concatenate(
    [top_source_bt, bm_source_bt],
    axis=-1
    )
lstm_ops_bt = shared_lstm_bt(source_comb_bt)  #256D vector

# comb_features_cs = concatenate(
#     [dropout+lstm_ops_bt, dropout-lstm_ops_bt, dropout*lstm_ops_bt],
#     axis=-1
#     )

comb_features_bd = Add()([dropout, lstm_ops_bt]) 

predictions = Dense(units=NUM_CLASSES, activation='sigmoid')(comb_features_bd)

model = Model(
    inputs=[top_input, bm_input, top_input_bt, bm_input_bt], 
    outputs=predictions)
model.summary()

from tensorflow.keras.optimizers import Adam
lr = 1e-3
opt = Adam(lr=lr, decay=lr/50)
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

BATCH_SIZE = 512
NUM_EPOCHS = 50
stop = [EarlyStopping(monitor='val_loss', patience=0.001)]
history = model.fit(x=[x1_train, x2_train, pre_train_bert, hyp_train_bert],
                    y=y_train,
                    batch_size=BATCH_SIZE,
                    epochs=NUM_EPOCHS,
                    validation_data=(
                      [x1_val, x2_val, pre_val_bert, hyp_val_bert], 
                      y_val
                    ),
                    shuffle=True,
                    callbacks=stop,
          )

from sklearn import metrics
from sklearn.metrics import classification_report
predictions = model.predict(
    [X1_test, X2_test, pre_bert_bd_test, hyp_bert_bd_test])

y_pred = [idx for idx in np.argmax(predictions, axis=1)]
#print(y_pred)
print('Accuracy is')
print(metrics.accuracy_score(reduced_test_labels, y_pred, sample_weight = reduced_test_weights)*100)
print(classification_report(reduced_test_labels, y_pred, target_names = ['agreed', 'disagreed', 'unrelated'], sample_weight = reduced_test_weights))