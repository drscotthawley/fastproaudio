# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['zenodo_url_to_data_url', 'get_audio_data', 'show_audio']

# Cell

#from fastai.vision.all import *
from fastai.data.all import *
#from subprocess import Popen, PIPE
import pyzenodo3
import torchaudio
import librosa
import librosa.display
from IPython.display import Audio

#from zipfile import ZipFile

# some data urls
URLs.AUDIOMDPI = 'https://zenodo.org/record/3562442'
URLs.MARCO = URLs.AUDIOMDPI  # just a shorthand alias I'm more likely to remember
URLs.SIGNALTRAIN_LA2A_1_1 = 'https://zenodo.org/record/3824876'
URLs.SIGNALTRAIN_LA2A_REDUCED = 'http://hedges.belmont.edu/data/SignalTrain_LA2A_Reduced.tgz'

# Cell
def zenodo_url_to_data_url(url):
    #%pip install pyzenodo3 -q
    zen = pyzenodo3.Zenodo()
    record = url.split('/')[-1]
    return zen.get_record(record).data['files'][0]['links']['self']

# Cell

# extract_func no longer supported  in untar_data, so zipfile stuff is unused
# thanks KevinB for the zip_extract! https://forums.fast.ai/t/generalizing-untar-data-to-also-work-with-zips/53741/14?u=drscotthawley
#def zip_extract(fname, dest):
#    zipfile.ZipFile(fname, mode='r').extractall(dest)

def get_audio_data(url):
    if ('zenodo' in url.lower()):
        url = zenodo_url_to_data_url(url)
    if '.zip' in url[-5:]:
        return untar_data(url)#, extract_func=zip_extract) #
    else:
        return untar_data(url)

# Cell
def show_audio(waveform, sample_rate):
    "This display routine is an amalgam of the torchaudio tutorial and the librosa documentation:"

    # print stats:
    print("Shape:", tuple(waveform.shape), "Dtype:", waveform.dtype)
    print(f"Max: {waveform.max().item():6.3f},  Min: {waveform.min().item():6.3f}, Mean: {waveform.mean().item():6.3f}, Std Dev: {waveform.std().item():6.3f}")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    # waveform, from https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html
    for c in range(num_channels):
        label = f'Channel {c+1}' if num_channels > 1 else ''
        ax[0].plot(time_axis, waveform[c], linewidth=1, label=label)
    ax[0].grid(True)
    ax[0].title.set_text('Waveform')
    if num_channels > 1: ax[0].legend()

    # mel spectrogram  for channel_0, code from librosa documentation
    y, sr = waveform[0], sample_rate
    M = librosa.feature.melspectrogram(y=y, sr=sr)
    M_db = librosa.power_to_db(M, ref=np.max)
    img = librosa.display.specshow(M_db, y_axis='mel', x_axis='time', ax=ax[1])
    ax[1].set(title='Mel spectrogram display')
    fig.colorbar(img, ax=ax[1], format="%+2.f dB")
    plt.show()

    # play audio
    if num_channels == 1:
        display(Audio(waveform[0], rate=sample_rate))
    elif num_channels == 2:
        display(Audio((waveform[0], waveform[1]), rate=sample_rate))
    else:
        raise ValueError("Waveform with more than 2 channels are not supported.")
