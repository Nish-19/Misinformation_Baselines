## Generating BERT Representations

We use BERT (Bidirectional Encoder Representations from Transformers) a generalized Language Model to obtain sentence/ paragraph level representations of the source/ target of the stance detection datasets.

We extract the 768 dimensional representation of the [CLS] token for each source/ target and use this along with the word level features for the final classification.

## Different BERT Embeddings

1. Standard BERT - Trained on the Wikipedia dataset.
2. [BioClinicalBERT](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT) - Trained on database containing electronic health records from ICU patients at the Beth Israel Hospital in Boston, MA.
3. [CovidSciBERT](https://huggingface.co/lordtt13/COVID-SciBERT) - Trained on scientific papers from the CORD-19 corpus.

## Running

Run python bert_new.py for getting the BERT representations of the dataset.

Comment/ Uncomment appropriate lines from 76 - 96 for choosing the appropriate BERT model and the respective tokenizer

Change the line 122 of the code to the path of the trainset.

Change the line 129 of the code to the path of the testset.
