import evaluate
import numpy as np
import pandas as pd
from datasets import Dataset
from setfit import SetFitModel, SetFitTrainer

test_df = pd.read_csv('./data/hoc/test.tsv', sep='\t')
train_df = pd.read_csv('./data/hoc/train.tsv', sep='\t')

LABELS = ['activating invasion and metastasis', 'avoiding immune destruction',
          'cellular energetics', 'enabling replicative immortality', 'evading growth suppressors',
          'genomic instability and mutation', 'inducing angiogenesis', 'resisting cell death',
          'sustaining proliferative signaling', 'tumor promoting inflammation']


# Convert labels to hotvec multilabel format (similar to scikit-learn)
def hotvec_multilabel(true_df):
    data = {}

    for i in range(len(true_df)):
        true_row = true_df.iloc[i]

        key = true_row['index']

        data[key] = set()

        if not pd.isna(true_row['labels']):
            for l in true_row['labels'].split(','):
                data[key].add(LABELS.index(l))

    y_hotvec = []
    for k, (true) in data.items():
        t = [0] * len(LABELS)
        for i in true:
            t[i] = 1

        y_hotvec.append(t)

    y_hotvec = np.array(y_hotvec)

    return y_hotvec


model = SetFitModel.from_pretrained(
    "sentence-transformers/paraphrase-mpnet-base-v2",
    multi_target_strategy="multi-output",  # one-vs-rest; multi-output; classifier-chain
)

multilabel_f1_metric = evaluate.load("f1", "multilabel")
multilabel_accuracy_metric = evaluate.load("accuracy", "multilabel")


# f1/accuracy sentence level
def compute_metrics(y_pred, y_test):
    return {
        "f1": multilabel_f1_metric.compute(predictions=y_pred, references=y_test, average="micro")["f1"],
        "accuracy": multilabel_accuracy_metric.compute(predictions=y_pred, references=y_test)["accuracy"],
    }


eval_dataset = Dataset.from_dict({"text": test_df['sentence'], "label": hotvec_multilabel(test_df)})
train_dataset = Dataset.from_dict({"text": train_df['sentence'], "label": hotvec_multilabel(train_df)})

trainer = SetFitTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    metric=compute_metrics,
    num_iterations=5,
)

trainer.train()
metrics = trainer.evaluate()
print(metrics)
