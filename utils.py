import tempfile
import os
import pydub
import scipy
import scipy.io.wavfile

def read_mp3(file_path, as_float = True):
    """
    Read an MP3 File into numpy data.
    :param file_path: String path to a file
    :param as_float: Cast data to float and normalize to [-1, 1]
    :return: Tuple(rate, data), where
        rate is an integer indicating samples/s
        data is an ndarray(n_samples, 2)[int16] if as_float = False
            otherwise ndarray(n_samples, 2)[float] in range [-1, 1]
    """

    path, ext = os.path.splitext(file_path)
    assert ext=='.mp3'
    mp3 = pydub.AudioSegment.from_mp3(file_path)
    _, path = tempfile.mkstemp()
    mp3.export(path, format="wav")
    rate, data = scipy.io.wavfile.read(path)
    os.remove(path)
    if as_float:
        data = data/(2**15)
    return rate, data

def normalize_impulse(imp_data):
    abs_data = abs(imp_data)
    data = imp_data / sum(abs_data)
    return data

def normalize_impulse_max(imp_data):
    abs_data = abs(imp_data)
    data = imp_data / abs_data.max()
    data[0] = 1
    return data