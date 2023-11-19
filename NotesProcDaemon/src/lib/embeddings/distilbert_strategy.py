import numpy as np
import torch
from transformers import DistilBertModel, DistilBertTokenizer
from .abs_strategy import EmbeddingStrategy


CHECKPOINT = 'distilbert-base-uncased'
BATCH_SIZE = 4

EMBEDDING_SIZE = 768


class DistilBertStrategy(EmbeddingStrategy):

    def __init__(self):
        self._model = DistilBertModel.from_pretrained(CHECKPOINT)
        self._tokenizer = DistilBertTokenizer.from_pretrained(CHECKPOINT)

    def encode(self, text: str | list[str]) -> np.ndarray:
        if type(text) is not list:
            text = [text]

        batched_text = [text[i:i+BATCH_SIZE] for i in range(0, len(text), BATCH_SIZE)]

        input_batches = [
            self._tokenizer(text_batch, return_tensors='pt', padding=True)
            for text_batch in batched_text
        ]

        embeddings = np.zeros((len(text), EMBEDDING_SIZE))
        with torch.no_grad():
            for idx, input_batch in enumerate(input_batches):
                outputs = self._model(**input_batch)
                batch_embeddings = outputs.last_hidden_state.index_select(-2, torch.tensor(0)).squeeze(-2)
                embeddings[idx:idx+BATCH_SIZE] = batch_embeddings

        np_embeddings = np.array(embeddings)

        return np_embeddings
