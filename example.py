import requests
import numpy as np
import pandas as pd

from em_aligner import EMAligner


if __name__ == '__main__':
    # Load sample data from the ACL SIGMORPHON 2022 Shared Task on Grapheme-to-Phoneme Conversion
    data_url = "https://raw.githubusercontent.com/sigmorphon/2022G2PST/main/data/target_languages/ita_train.tsv"
    data = requests.get(data_url, allow_redirects=False)
    grapheme_phoneme_pairs = data.text.split("\n")
    grapheme_phoneme_pairs = [
        grapheme_phoneme_pair.strip() for grapheme_phoneme_pair in grapheme_phoneme_pairs
        if grapheme_phoneme_pair.strip()
    ]
    grapheme_phoneme_pairs = [grapheme_phoneme_pair.split("\t") for grapheme_phoneme_pair in grapheme_phoneme_pairs]
    graphemes, phonemes = zip(*grapheme_phoneme_pairs)

    graphemes = [g.strip() for g in graphemes]
    phonemes = [p.strip().split() for p in phonemes]

    # Instantiate & Train Aligner
    aligner = EMAligner(max_source_ngram=2, max_target_ngram=2, epochs=10)
    aligner.fit(source=graphemes, target=phonemes)

    # Align Graphemes to Phonemes using the trained model
    alignments = aligner.align(source=graphemes, target=phonemes)

    # Print an example
    source_alignment, target_alignment = alignments[2]
    source_alignment = [" ".join(source_ngram) for source_ngram in source_alignment]
    target_alignment = [" ".join(target_ngram) for target_ngram in target_alignment]
    print(pd.DataFrame(data=np.array([source_alignment, target_alignment])))

    # Save model
    aligner.save("./saved_model")
