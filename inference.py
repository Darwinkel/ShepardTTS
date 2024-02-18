"""CLI file for rendering a single piece of text. Note: you should prefer Gradio."""

import time

import numpy as np
import torch
from torchaudio.io import StreamWriter

from utils import load_checkpoint, normalize_line

model = load_checkpoint()

SPEAKER = "Femshep"

gpt_cond_latent = torch.load(f"mean_character_embeddings/{SPEAKER}_gpt_cond_latent.pt")
speaker_embedding = torch.load(f"mean_character_embeddings/{SPEAKER}_speaker_embedding.pt")


line = "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals. I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire United States armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the United States, and your IP is being traced right now. So you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways. And that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps. I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo."

print("Inference...")
out = model.inference(
    normalize_line(line),
    "en",
    gpt_cond_latent,
    speaker_embedding,
    top_k=30,
    top_p=0.5,
    temperature=0.6,
    enable_text_splitting=True,
)

waveform = torch.tensor([])
quarter_second_pause = torch.tensor(np.zeros(24000 // 4), dtype=torch.float32)
for sentence in out["wav"]:
    waveform = torch.cat((waveform, quarter_second_pause, sentence, quarter_second_pause))

# Write compressed opus ogg
s = StreamWriter(dst=f"out_individual/{int(time.time())}_{SPEAKER}.ogg")
s.add_audio_stream(sample_rate=24000, num_channels=1, encoder="opus")
with s.open():
    s.write_audio_chunk(0, waveform.unsqueeze(1))
