# Misinformation_Baselines

Misinformation detection is one of the major problems that the Natural Language Processing community is faced with. Research in this area to curb the spread of fake news is of prime importance. In this project, I implement baselines models for three stance detection misinformation datasets.

## Datasets

### ByteDance Dataset -

ByteDance dataset has been released by ByteDance (A China-based global Internet technology company) as the competition dataset of Task: Fake News Classification. The training dataset consists of 320,767 news pairs with 3 class labels, i.e., agreed, disagreed, and unrelated. The testing dataset contains 80,126 news pairs without any labels. These news pairs are available in both Chinese and English.

### Fake News Challenge-1 Dataset

Fake News Challenge-1 has provided this dataset and derived from Emergent (a digital journalism project for rumor debunking). There are 49,972 headline-body pairs in total, with stances labeled by expert journalists. FNC1 dataset has a headline and a body text pair, either from the same news article or from two different articles, and the corresponding stance labels Agrees, Disagrees, Discusses, Unrelated.

### Covid-Stance Dataset -

This is a stance detection dataset that includes user-generated content on Twitter in the context of COVID-19. It is a collection of approximately 14 thousand tweets. It contains manually annotated opinions of the tweet initiators regarding the use of “chloroquine” and “hydroxychloroquine” to prevent or treat COVID-19. The instances of this dataset have three different classes as Neutral, Against, and Favor.

## Baselines

### Siamese BiLSTM + LSTM -

Siamese LSTMs are used since, in each dataset we have a source target pair and we observe that the Siamese (Shared weights) give better learning as compared to separate LSTMs.

### MultiChannel CNNs + LSTM -

MultiChannel CNNs are used to capture local features in the input and proved effective in various NLP tasks (apart from their applications in traditional computer vision). The features generated from the CNNs and LSTMs are added and then fed to a dense layer for the final classification.


## Method

### Word Features only -
With the above two models we only use the word level embeddings obtained from Glove 300d as the initial embeddings.

### Word + Sentence Level -
Here, along with the word representations, we generate the sentence level representations using BERT(BiDirectional Encoding Representations from Transformers). The two features have separate encoders and the representation obtained from these encoders if fused and passed to the dense layer for the final classification.

## References

1. [ByteDance Dataset](https://www.kaggle.com/wsdmcup)
2. [FNC1 Dataset](https://github.com/FakeNewsChallenge/fnc-1)
3. [Covid-Stance Dataset](https://www.sciencedirect.com/science/article/pii/S235234092031283X)
4. [Siamese LSTMs](https://www.researchgate.net/publication/307558687_Siamese_Recurrent_Architectures_for_Learning_Sentence_Similarity)
5. [MultiChannel CNNs](https://machinelearningmastery.com/develop-n-gram-multichannel-convolutional-neural-network-sentiment-analysis/)
6. [BERT](https://arxiv.org/abs/1810.04805)
