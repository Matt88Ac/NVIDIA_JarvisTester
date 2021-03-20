import soundfile as sf
import sounddevice as sd
import sys
import queue
import numpy as np
import io
import os
import json
import requests
import time

q = queue.Queue()
fname = 'new_file.wav'
sr = 44100
server_ip = '54.87.118.144'


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def is_silent(snd_data: np.ndarray):
    return np.abs(snd_data).max() < 10 ** -2


def record(path, sample_rate, channels=1):
    if path in os.listdir():
        os.remove(path)
    try:
        with sf.SoundFile(path, mode='x', samplerate=sample_rate, channels=channels, subtype=None) as file:
            i = 0
            silent = 0
            key = input('Press a key to start recording: ')
            time.sleep(0.5)
            with sd.InputStream(samplerate=sample_rate, device=0, channels=channels, callback=callback):
                print(f"Ask me a question: ")
                try:
                    while True:
                        to_write = q.get()
                        if not is_silent(to_write):
                            silent = 0
                        else:
                            silent += 1
                            if silent == 10 and i > 10:
                                break
                        file.write(to_write)
                        i += 1
                except RuntimeError as re:
                    print(f"{re}. If recording was stopped by the user, then this can be ignored")

    except RuntimeError:
        print('error')


record(fname, sr)
with io.open(fname, 'rb') as file:
    content = file.read()

os.remove(fname)
print('waiting for an answer...')
to_send = {'content': list(content), 'sr': sr}
to_send = json.dumps(to_send)

out = requests.post(f'http://{server_ip}:5000/audio', json=to_send)
content = json.loads(out.content)
sr = int(content['sr'])
content = np.array(content['content'])
sd.play(content, sr, blocking=True)
sf.write('ourfile.wav', content, samplerate=sr)
