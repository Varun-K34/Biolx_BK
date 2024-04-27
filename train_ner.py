import random

from torch.optim import Adam
from torch.utils.data import DataLoader
from transformers import (get_linear_schedule_with_warmup,
                          BertForTokenClassification,
                          AutoTokenizer)

from data_utils.data_utils import *
from nn_utils.optimizers import get_optimizer_with_weight_decay
from nn_utils.trainer import BertTrainer

# https://github.com/cambridgeltl/MTL-Bioinformatics-2016/tree/master/data
DATA_TR_PATH = 'C:\\Users\\appuv\\backend1\\datasets\\iob2_train.tsv'
DATA_VAL_PATH = 'C:\\Users\\appuv\\backend1\\datasets\\iob2_devel.tsv'
DATA_TEST_PATH = None
SEED = 42

# MODEL
MODEL_NAME = 'allenai/scibert_scivocab_uncased'
MAX_LEN_SEQ = 128
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Optimization parameters
N_EPOCHS = 6
BATCH_SIZE = 8
BATCH_SIZE_VAL = 28
WEIGHT_DECAY = 0
LEARNING_RATE = 1e-4  # 2e-4
RATIO_WARMUP_STEPS = .1
DROPOUT = .3
ACUMULATE_GRAD_EVERY = 4
OPTIMIZER = Adam

# Seeds
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

# get data
training_set = read_data_from_file(DATA_TR_PATH)
val_set = read_data_from_file(DATA_VAL_PATH)

# Automatically extract labels and their indexes from data.
labels2ind, labels_count = get_labels(training_set + val_set)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Create loaders for datasets
training_set = NerDataset(dataset=training_set,
                          tokenizer=tokenizer,
                          labels2ind=labels2ind,
                          max_len_seq=MAX_LEN_SEQ)

val_set = NerDataset(dataset=val_set,
                     tokenizer=tokenizer,
                     labels2ind=labels2ind,
                     max_len_seq=MAX_LEN_SEQ)

dataloader_tr = DataLoader(dataset=training_set,
                           batch_size=BATCH_SIZE,
                           shuffle=True)

dataloader_val = DataLoader(dataset=val_set,
                            batch_size=BATCH_SIZE_VAL,
                            shuffle=False)

# Load model
nerbert = BertForTokenClassification.from_pretrained(MODEL_NAME,
                                                     hidden_dropout_prob=DROPOUT,
                                                     attention_probs_dropout_prob=DROPOUT,
                                                     num_labels=len(labels2ind),
                                                     id2label={str(v): k for k, v in labels2ind.items()})

# Prepare optimizer and schedule (linear warmup and decay)
optimizer = get_optimizer_with_weight_decay(model=nerbert,
                                            optimizer=OPTIMIZER,
                                            learning_rate=LEARNING_RATE,
                                            weight_decay=WEIGHT_DECAY)

training_steps = (len(dataloader_tr)//ACUMULATE_GRAD_EVERY) * N_EPOCHS
scheduler = get_linear_schedule_with_warmup(optimizer=optimizer,
                                            num_warmup_steps=training_steps * RATIO_WARMUP_STEPS,
                                            num_training_steps=training_steps)

# Trainer
trainer = BertTrainer(model=nerbert,
                      tokenizer=tokenizer,
                      optimizer=optimizer,
                      scheduler=scheduler,
                      labels2ind=labels2ind,
                      device=DEVICE,
                      n_epochs=N_EPOCHS,
                      accumulate_grad_every=ACUMULATE_GRAD_EVERY,
                      output_dir='C:\\Users\\appuv\\backend1\\datasets\\models')

# Train and validate model
trainer.train(dataloader_train=dataloader_tr,
              dataloader_val=dataloader_val)

# Test the model on test set if any
if DATA_TEST_PATH is not None:
    print(f"{'*'*40}\n\t\tEVALUATION ON TEST SET\n{'*'*40}")
    test_set = read_data_from_file(DATA_TEST_PATH)

    test_set = NerDataset(dataset=test_set,
                          tokenizer=tokenizer,
                          labels2ind=labels2ind,
                          max_len_seq=MAX_LEN_SEQ)

    dataloader_test = DataLoader(dataset=test_set,
                                 batch_size=BATCH_SIZE_VAL)

    trainer.evaluate(dataloader_test, verbose=True)

