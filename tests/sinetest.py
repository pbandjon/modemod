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
out = audio.open(rate=rate,
                 channels=1,
                 format=fmt,
                 output=True,
                 )
try:
    out.start_stream()
    time.sleep(1)

    t = np.arange(0, 1, 1/rate)
    rawarrs = np.vstack([
            maxamp * 0.1 * np.cos(440 * 2 * np.pi * t),
            maxamp * 0.1 * np.cos(554 * 2 * np.pi * t),
            maxamp * 0.1 * np.cos(660 * 2 * np.pi * t),
            ])
    arrs = dtype(rawarrs)
    print("now playing!", file=sys.stderr)
    for _ in range(3):
        print("pulse", _, file=sys.stderr)
        out.write(arrs[_,:])
        out.write(np.zeros(rate, dtype))

    print("chord!", file=sys.stderr)
    out.write(dtype(np.sum(arrs, axis=0)))
finally:
    out.stop_stream()
    out.close()
    audio.terminate()
    print("Exited cleanly", file=sys.stderr)
