# Many-to-Many Aligner

This repository contains a Python implementation of the many-to-many aligner proposed
by [1].
The aligner was proposed to align graphemes to phonemes as a preprocessing step
in order to learn grapheme-to-phoneme conversion models.

The aligner learns to align graphemes to phonemes from a provided set of (grapheme, phoneme)
pairs. Alignment probabilities are learned by Expectation Maximisation (EM).

The main innovation of many-to-many aligners is that they allow alignment of grapheme
n-grams to phoneme n-grams.
Previous work mostly used 1-to-1 alignments, i.e. only single graphemes were aligned to
single phonemes.
However, this an unrealistic assumption for most languages.
For example, consider the word "phoenix" with IPA /'fiːnɪks'.
Here, the alignments should be

| ph  | oe  | n   | i   | x   |
|-----|-----|-----|-----|-----|
| 'f  | iː  | n   | ɪ   | ks  |

while any 1-to-1 alignment would be implausible.

## Usage
### Instantiation
The main class `EMAligner` is in `em_aligner.py`.
It takes the following parameters:
  * `max_source_ngram`: The maximum n-gram length of grapheme n-grams that may be aligned
  * `max_target_ngram`: The maximum n-gram length of phoneme n-grams that may be aligned
  * `normalisation_mode`: Choices are:
    * `"conditional"`: Learns a distribution over phoneme n-grams for each grapheme n-gram
      individually
    * `"joint"`: Learns a joint distribution of grapheme n-grams and phoneme n-grams
  * `many2many`: Whether to allow grapheme n-grams of length >= 2 to be aligned to phoneme
    n-grams of length >= 2. If `False`, only 1-to-many and many-to-1 alignments are allowed
  * `allow_delete_graphemes`: If `True`, allows grapheme n-grams to not be aligned
     to any phoneme n-gram. In edit operation terminology, this corresponds to Deletion
  * `allow_delete_phonemes`: If `True`, allows phoneme n-grams to not be aligned
     to any grapheme n-gram.
  * `epochs`: Number of iterations of the EM-Algorithm.

Please note that memory complexity is number of source n-grams times number of target
n-grams. Therefore, setting `max_source_ngram` or `max_target_ngram` may result in
performance issues.

### Training
Once the aligner is instantiated, it can be trained by calling
`aligner.fit(source=source, target=target)`
where `source` is a list of strings representing the graphemes and `target` is a nested list
where each phoneme sequence is represented by a list containing phonemes as strings.

### Alignment
The method `align(source, target)` can be used to align graphemes and phonemes.
Arguments are required to have identical format like arguments to the `fit` method.
Return format is a list of (aligned graphemes, aligned phonemes) tuples, where both
aligned graphemes and aligned phonemes are nested lists of equal length.
Each sublist contains the aligned n-gram at the corresponding position.

### Saving and Loading Models
Models can be saved by calling `aligner.save(path)`.
`path` is a string specifying where to save the model to.
The model is saved in two files called, one called `parameters.pickle` containing the
aligner's arguments, and one called `parameters.npy` containing the aligner's learned
parameters.
Models can be loaded by calling `EMAligner.load(path)` where `path` is a string
specifying a location containing a file called `parameters.pickle` and a file
called `parameters.npy` created by  saving a trained aligner model.



## References
[1] Sittichai Jiampojamarn, Grzegorz Kondrak, and Tarek Sherif. 2007. 
    Applying Many-to-Many Alignments and Hidden Markov Models to Letter-to-Phoneme
    Conversion. In Human Language Technologies 2007: The Conference of the North
    American Chapter of the Association for Computational Linguistics; Proceedings
    of the Main Conference, pages 372–379, Rochester, New York. Association for
    Computational Linguistics.