
import wave
import audioop

def rmsSplits(
        filename,
        splitsPerSecond = 10):
    """
    take a WAV audio, splits into chunks and for every chunk
    return the rms (audio intensity of that chunk)

    return List[int], 
    where 
        len(List[int]) = length in seconds of audio * splitsPerSecond
    """
    wav = wave.open("mozart17jan.wav")
    totalFrames = wav.getnframes()
    frameRate = wav.getframerate()
    lengthSeconds = totalFrames / frameRate

    """
    averageRMS = audioop.rms(
                wav.readframes(totalFrames), wav.getsampwidth())
    wav.rewind()
    """

    # detect average of sound every tenth of a second
    splits = int(totalFrames / (frameRate / splitsPerSecond))
    rms = []
    for i in range(splits):
        _rms = audioop.rms(
                wav.readframes(int(totalFrames / splits)), wav.getsampwidth()
                )
        """
        if rms > averageRMS:
            print("Sound in {} split is {}, higher than average {}".format(
                i, rms, averageRMS))
        """

        rms.append(_rms)
    return rms
