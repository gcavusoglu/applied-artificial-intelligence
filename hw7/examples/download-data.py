import itertools

from datasets import load_dataset
from huggingface_hub import login

login(token="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")

streamed_dataset = load_dataset("umutertugrul/turkish-hospital-medical-articles", streaming=True)

# 1. Grab the raw underlying stream
raw_stream = next(iter(streamed_dataset.values()))

# 2. Safely take UP TO 100 items without crashing
data_list = list(itertools.islice(raw_stream, 100))

print(f"Successfully retrieved {len(data_list)} rows without downloading the full dataset.")
print([data['title'] for data in data_list])
print(len(data_list))
