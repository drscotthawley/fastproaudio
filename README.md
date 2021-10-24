# fastproaudio
> End-to-end audio with fastai.


## Idea behind this repo

`fastaudio` focuses on spectrograms. `fastai` use cases tend to focus on classification. We need to go beyond those. Instead we'll focus on two things:

1. autoregressive prediction in the time domain. We'll use an LSTM -- essentially adapting the language model lessons

2.  audio-to-audio processing/translation (e.g. audio effects). We'll use stacked 1D convolutions like a U-Net

(you probably noticed already that task #1 could be in task #2, for the case of translating to audio shifted ahead by one sample.)

#### "How many channels of audio are we going to use?"
 That's up to the dataset!  We'll try our best to assume that it's just mono.

#### "What other fastai datatypes/projects are relevant?"
 There are three packages that are relevant for sequence modeling:

1.  `fastaudio`, as we mentioned, is only for spectrogram classification. The `AudioBlock` makes batches using an entire audio file which then gets converted to spectrograms.  Instead, we want to progressively grab sequences of audio samples and as (uniform-length) chunks.

2. The [Time Series Prediction](https://timeseriesai.github.io/tsai/) package is relevant, but the only time series output it seems to support is ["univariate forecasting"](https://timeseriesai.github.io/tsai/#Univariate-Forecasting).  Nope. 
3. Language Modeling, e.g. Chapters [10](https://github.com/fastai/fastbook/blob/master/10_nlp.ipynb) and [12](https://github.com/fastai/fastbook/blob/master/12_nlp_dive.ipynb) from fastbook. Yea, that's the closest. We can treat the audio samples as if they were word vectors/embeddings: just make the tokenizer and numericalize methods to be no-ops (or we could use mu-law encoding).  Nice thing is the dimensionality of the embeddings is just equal to how many channels of audio you have. 
   
We'll use *some* of fastaudio but we'll also liberally rewrite/overwrite whatever we want.

...And this may not be useful to more than a few core people. We'll see. ;-) 

## Install

`pip install fastproaudio`

## How to use

Workin' on it! 
