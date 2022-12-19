#!/usr/bin/env python3

import numpy as np
import pyaudio
import sys
import time

dtypes = {
        pyaudio.paUInt8:np.uint8,
        pyaudio.paInt8:np.int8,
        pyaudio.paInt16:np.int16,
        pyaudio.paInt32:np.int32,
        }
maxamps = {
        pyaudio.paUInt8:2**8 - 1,
        pyaudio.paInt8:2**8 - 1,
        pyaudio.paInt16:2**16 - 1,
        pyaudio.paInt32:2**32 - 1,
        }

audio = pyaudio.PyAudio()
rate = 48000
fmt = pyaudio.paInt16
dtype = dtypes[fmt]
maxamp = maxamps[fmt]
dur = 0.25
out = audio.open(rate=rate,
                 channels=1,
                 format=fmt,
                 output=True,
                 )

freq = 440
rawarrs = []
freqs = []
t = np.arange(0, dur, 1/rate)
for _ in range(240):
    freqs.append(freq)
    rawarrs.append(maxamp * 0.1 * np.cos(freq * 2 * np.pi * t))
    freq *= 1.5
    if freq > 880: freq /= 2
rawarrs = np.vstack(rawarrs)
try:
    out.start_stream()
    time.sleep(1)

    arrs = dtype(rawarrs)
    print("now playing!", file=sys.stderr)
    for _ in range(len(rawarrs)):
        print("pulse", _, freqs[_], file=sys.stderr)
        out.write(arrs[_,:])
        out.write(np.zeros(int(dur * rate), dtype))

    #print("chord!", file=sys.stderr)
    #out.write(dtype(np.sum(arrs, axis=0)))
finally:
    out.stop_stream()
    out.close()
    audio.terminate()
    print("Exited cleanly", file=sys.stderr)
