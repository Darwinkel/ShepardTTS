# ShepardTTS

[ShepardTTS](https://shepardtts.darwinkel.net) is a free and open-source fine-tuned [XTTS v2.0.3](https://docs.coqui.ai/en/latest/models/xtts.html) model, trained on paired dialogue/audio samples from the Mass Effect 2 and Mass Effect 3 base games.

Pull requests, feature requests, and discussions are welcome!

If you are a researcher, and you want access to the public ShepardTTS deployment, contact me.

## Usage notes
Most voices perform best when narrating medium-length sentences with medium-length words. They tend to produce garbage and artifacts when confronted with very short words and sentences, excessive punctuation, and abbreviations. Sentences which are too long tend to cause hallucinations. As a rule of thumb: provide text input such that it could have reasonably occurred in the games. The more out-of-domain - and unnatural - the text input, the lower the chances of a good narration.

![This paragraph is a good example of appropriate text input.](/examples/1708512151_ME2_f-player_f-Shepard.ogg)

## Deployment
GitHub Actions automatically produces a fresh image on every push to the `main` branch. See `docker-compose.example.yml` on how it can be deployed.

## History (and other experiments)
I initially [fine-tuned SpeechT5](https://huggingface.co/learn/audio-course/chapter6/fine-tuning), but the results were disappointing. That model very frequently produced garbage and/or hallucinated output for most voices. Interestingly, it also had a very strong bias towards female speakers. 

## Dataset
After dumping dialogue strings with the Legendary Explorer and dumping audio samples with Gibbed's ME2/ME3 extractor, you can use `create_dataset.py` to align and filter the two. This transforms the dialogue-audio pairs into a HuggingFace dataset, which it then exports into the [ljspeech](https://github.com/coqui-ai/TTS/tree/dev/recipes/ljspeech) format. 

You can then proceed to train the model, and create character embeddings when it finishes training.

The audio samples and dialogue strings are extremely clean. The audio has a sample rate of 24000Hz (downsampled to 22050 for training). The dialogue strings are corrupted in some cases (issue with the Legendary Explorer?).

## Training 
Trained for 12 epochs on a RTX 3060 with 12GB VRAM. Took about 14 hours. Judging from the eval loss, this is roughly the point where it starts overfitting. See `train.py` for the used parameters.

## Future work
See [the project board](https://github.com/users/Darwinkel/projects/2).

GPU inference with DeepSpeed is ~20x faster (minutes to seconds), but renting GPU's is very expensive. Do we have a generous sponsor in the audience perhaps?


## Ethical (and legal) statement
There are probably copyright issues with a generative model trained on game files. More importantly, I'm not sure how the voice actors feel about their voice being cloned. Do not use ShepardTTS for commercial or harmful purposes. This software is a labor of love built for the Mass Effect fan community.

Due to these legal and ethical issues, I will not distribute the game files nor the model checkpoint at this time. Dump and fine-tune yourself.

### Risks
Voice cloning technology has been around for a couple of years. Hand-picked audio samples with commercial-grade voice models likely produce better audio than ShepardTTS. Furthermore, waveforms produced by this model are easily recognizable as such just by visual inspection, as it always produces (some) characteristic artifacts.

The access to the public deployment is highly restricted, and as such there is no straightforward way to use the system such that it hurts the interests of the original voice actors.

All things considered, this software should not produce additional harm beyond what already exists.

## License
The model and its output: [Coqui Public Model License (CPML)](https://coqui.ai/cpml)

The code: [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Acknowledgements
- [Coqui for their amazing XTTS v2.0.3 model](https://docs.coqui.ai/en/latest/models/xtts.html);
- [Mass Effect Legendary Explorer](https://github.com/ME3Tweaks/LegendaryExplorer) to dump the dialogue strings;
- [Gibbed's](http://svn.gib.me/public/masseffect3/trunk/Gibbed.MassEffect3.AudioExtract/) [AudioExtractor](http://mod.gib.me/masseffect2/audioextract_rev27.zip) to bulk-export audio files from ME2 and ME3;
- [Gradio](https://www.gradio.app/), [HuggingFace](https://huggingface.co/coqui/XTTS-v2), and [HuggingFace Spaces](https://huggingface.co/spaces/coqui/xtts), for inspiration regarding the deployment of this model.