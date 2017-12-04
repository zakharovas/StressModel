from transform import encoding

def train_on_batch(model, syll_dictionary, batch, optimizer):
    encoded_batch = encoding.encode_text(batch)
    answer = model.predict()
