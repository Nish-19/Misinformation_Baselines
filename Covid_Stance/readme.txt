CS_Baseline.ipynb is the python notebook for running the baselines of siamese lstm and multichannel cnn + lstm on the bytedance dataset

CS_bert.ipynb is the python script for running baselines of siamese lstm and multichannel cnn using additional BERT representations (on sentence level) along with word representations taken from Glove 300d.

The results are tabulated below

+-------------------------+----------------------+--------------+------------------+----------+
| Model                   | Embeddings           | FOR F1 score | AGAINST F1 score | Accuracy |
+-------------------------+----------------------+--------------+------------------+----------+
| Siamese BiLSTM + LSTM   | Glove                | 0.87         | 0.79             | 83.92    |
| (Only Word)             |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| MultiChannel CNN + LSTM | Glove                | 0.88         | 0.81             | 85.16    |
| (Only Word)             |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| Siamese BiLSTM + LSTM   | Glove + BERT         | 0.87         | 0.80             | 83.96    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| MultiChannel CNN + LSTM | Glove + BERT         | 0.88         | 0.81             | 85.44    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| Siamese BiLSTM + LSTM   | Glove + BioBERT      | 0.86         | 0.81             | 83.52    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| MultiChannel CNN + LSTM | Glove + BioBERT      | 0.87         | 0.82             | 84.64    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| Siamese BiLSTM + LSTM   | Glove + CovidSciBERT | 0.88         | 0.81             | 85.16    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+
| MultiChannel CNN + LSTM | Glove + CovidSciBERT | 0.88         | 0.82             | 85.64    |
| (Word + Sentence)       |                      |              |                  |          |
+-------------------------+----------------------+--------------+------------------+----------+