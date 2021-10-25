# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['zenodo_url_to_data_url', 'get_audio_data', 'show_info', 'plot_waveform', 'plot_melspec', 'play_audio',
           'show_audio']

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

def show_info(waveform, sample_rate):
    print(f"Shape: {tuple(waveform.shape)}, Dtype: {waveform.dtype}, Duration: {waveform.numpy().shape[-1]/sample_rate} s")
    print(f"Max: {waveform.max().item():6.3f},  Min: {waveform.min().item():6.3f}, Mean: {waveform.mean().item():6.3f}, Std Dev: {waveform.std().item():6.3f}")

def plot_waveform(waveform, sample_rate, ax=None, xlim=None, ylim=[-1,1]):
    "Waveform plot, from https://pytorch.org/tutorials/beginner/audio_preprocessing_tutorial.html"
    if ax is None: fig, ax = plt.subplots()
    waveform = waveform.numpy()
    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate
    for c in range(num_channels):
        label = f'Channel {c+1}' if num_channels > 1 else ''
        ax.plot(time_axis, waveform[c], linewidth=1, label=label)
    ax.grid(True)
    if ylim: ax.set_ylim(ylim)
    ax.title.set_text('Waveform')
    ax.set_xlabel('Time (s)')
    if num_channels > 1: ax.legend()
    if ax is None: plt.show(block=False)

def plot_melspec(waveform, sample_rate, ax=None, ref=np.max, vmin=-70, vmax=2):
    "Mel-spectrogram plot, from librosa documentation"
    if ax is None: fig, ax = plt.subplots()
    M = librosa.feature.melspectrogram(y=waveform.numpy()[0], sr=sample_rate)
    M_db = librosa.power_to_db(M, ref=ref)
    img = librosa.display.specshow(M_db, y_axis='mel', x_axis='time', ax=ax, sr=sample_rate, vmin=vmin, vmax=vmax)
    ax.set(title='Mel spectrogram display (Channel 0)')
    plt.colorbar(img, ax=ax, format="%+2.f dB")
    if ax is None: plt.show(block=False)

def play_audio(waveform, sample_rate):
    "From torchaudio preprocessing tutorial"
    waveform = waveform.numpy()
    num_channels, num_frames = waveform.shape
    if num_channels == 1:
        display(Audio(waveform[0], rate=sample_rate))
    elif num_channels == 2:
        display(Audio((waveform[0], waveform[1]), rate=sample_rate))
    else:
        raise ValueError("Waveform with more than 2 channels are not supported.")

def show_audio(waveform, sample_rate, info=True, play=True, waveform_plot=True, melspec_plot=True):
    "This display routine is an amalgam of the torchaudio tutorial and the librosa documentation:"
    if info: show_info(waveform, sample_rate)
    if play: play_audio(waveform, sample_rate)
    ncols = waveform_plot + melspec_plot
    if ncols > 0:
        fig, ax = plt.subplots(nrows=1, ncols=ncols, figsize=(ncols*6,4))
        if waveform_plot: plot_waveform(waveform, sample_rate, ax=ax[0])
        if melspec_plot: plot_melspec(waveform, sample_rate, ax=ax[1], ref=500) # ref=500 is a bit arbitrary but works good