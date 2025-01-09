def bit_error_rate(original, extracted):
    min_len = min(len(original), len(extracted))
    errors = sum(1 for o, e in zip(original[:min_len], extracted[:min_len]) if o != e)
    return errors / min_len * 100

def normalized_correlation(original, extracted):
    min_len = min(len(original), len(extracted))
    original_bits = np.array(list(map(int, original[:min_len])))
    extracted_bits = np.array(list(map(int, extracted[:min_len])))
    return np.dot(original_bits, extracted_bits) / (np.linalg.norm(original_bits) * np.linalg.norm(extracted_bits))

