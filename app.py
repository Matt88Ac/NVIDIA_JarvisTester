from flask import Flask, request
import grpc
import wikipedia as wiki
import numpy as np
# NLP proto
import jarvis_api.jarvis_nlp_core_pb2 as jcnlp
import jarvis_api.jarvis_nlp_core_pb2_grpc as jcnlp_srv
import jarvis_api.jarvis_nlp_pb2 as jnlp
import jarvis_api.jarvis_nlp_pb2_grpc as jnlp_srv

# ASR proto
import jarvis_api.jarvis_asr_pb2 as jasr
import jarvis_api.jarvis_asr_pb2_grpc as jasr_srv

# TTS proto
import jarvis_api.jarvis_tts_pb2 as jtts
import jarvis_api.jarvis_tts_pb2_grpc as jtts_srv
import jarvis_api.audio_pb2 as ja


import json
app = Flask(__name__)

channel = grpc.insecure_channel('localhost:50051')
jarvis_asr = jasr_srv.JarvisASRStub(channel)
jarvis_nlp = jnlp_srv.JarvisNLPStub(channel)
jarvis_tts = jtts_srv.JarvisTTSStub(channel)

def TTS(text):
    req = jtts.SynthesizeSpeechRequest()
    req.text = text
    req.language_code = "en-US"                    # currently required to be "en-US"
    req.encoding = ja.AudioEncoding.LINEAR_PCM     # Supports LINEAR_PCM, FLAC, MULAW and ALAW audio encodings
    req.sample_rate_hz = 22050                     # ignored, audio returned will be 22.05KHz
    req.voice_name = "ljspeech"                    # ignored

    resp = jarvis_tts.Synthesize(req)
    audio_samples = np.frombuffer(resp.audio, dtype=np.float32)
    return {'content':audio_samples.tolist(), 'sr':22050}

def q_and_a(question):
    wiki_articles = wiki.search(question)
    max_articles_combine = 3
    combined_summary = ""

    if len(wiki_articles) == 0:
        print("ERROR: Could not find any matching results in Wikipedia.")
    else:
        for article in wiki_articles[:min(len(wiki_articles), max_articles_combine)]:
            print(f"Getting summary for: {article}")
            combined_summary += "\n" + wiki.summary(article)
   
    req = jnlp.NaturalQueryRequest()

    req.query = question
    req.context = combined_summary
    resp = jarvis_nlp.NaturalQuery(req)

    print(f"Query: {question}")
    print(f"Answer: {resp.results[0].answer}")
    return resp.results[0].answer

        
def speech_to_text(data,sample_rate):
    req = jasr.RecognizeRequest()
    req.audio = data                                   # raw bytes
    req.config.encoding = ja.AudioEncoding.LINEAR_PCM     # Supports LINEAR_PCM, FLAC, MULAW and ALAW audio encodings
    req.config.sample_rate_hertz = sample_rate                     # Audio will be resampled if necessary
    req.config.language_code = "en-US"                    # Ignored, will route to correct model in future release
    req.config.max_alternatives = 1                       # How many top-N hypotheses to return
    req.config.enable_automatic_punctuation = True        # Add punctuation when end of VAD detected
    req.config.audio_channel_count = 1                    # Mono channel

    response = jarvis_asr.Recognize(req)
    asr_best_transcript = response.results[0].alternatives[0].transcript
    print("ASR Transcript:", asr_best_transcript)

    print("\n\nFull Response Message:")

    return asr_best_transcript

@app.route('/')
@app.route('/audio', methods=['POST'])
def index():
    data = json.loads(request.json)
    sr = int(data['sr'])
    content = bytes(data['content'])
#     print(content)
#     print(sr)
# Set up an offline/batch recognition request
    transcript = speech_to_text(content,sr)
    text = q_and_a(transcript)
    rv = TTS(text)
    return json.dumps(rv)

app.run(host='0.0.0.0')