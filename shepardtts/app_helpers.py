"""Helper functions for ShepardTTS Gradio web interface."""

from __init__ import __version__

title = "ShepardTTS"

description = """

<br/>

This demo is currently running a fine-tuned version of **XTTS v2.0.3**. <a href="https://huggingface.co/coqui/XTTS-v2">XTTS</a> is a multilingual text-to-speech and voice-cloning model. It has been fine-tuned on game data from Mass Effect 2 and Mass Effect 3. Speaker embeddings are generated from available game samples. See the GitHub repository for more information.

<br/>

This server has limited computing power (CPU-bound). Multi-sentence texts can take up to a minute or more to generate.

<br/>
"""

links = f"""

|                                 |                                         |
| ------------------------------- | --------------------------------------- |
| **Source code and README**      | [GitHub](https://github.com/Darwinkel/ShepardTTS) |
| **Current running version**     | {__version__} |

"""

examples = [
    [
        "I'm Commander Shepard, and this is my favorite store on the Citadel.",
        "ME2_f-player_f-Shepard",
    ],
    [
        "I'm Commander Shepard, and this is my favorite store on the Citadel.",
        "ME2_m-player_m-Shepard",
    ],
    [
        "I don't know if the Reapers understand fear, but you killed one of them. They have to respect that.",
        "ME2_m-global_illusive_man-nor_illusive_man",
    ],
    [
        "Worried about my qualifications? I can crush a mech with my biotics or shoot its head off at a hundred yards. Take your pick.",
        "ME2_m-hench_vixen-procer_miranda",
    ],
    [
        "Lots of ways to help people. Sometimes heal patients; sometimes execute dangerous people. Either way helps.",
        "ME2_m-hench_professor",
    ],
    [
        "Christian Bible, the Gospel of Mark, chapter five, verse nine. We acknowledge this as an appropriate metaphor. We are Legion, a terminal of the geth. We will integrate into Normandy.",
        "ME2_m-hench_geth",
    ],
    [
        "I enjoy the sight of humans on their knees. That is a joke.",
        "ME2_m-hench_ai",
    ],
    [
        "The problem is that war isn't orderly. And the enemy is never predictable. Even the most experienced veteran is going to find themselves in situations they haven't trained for.",
        "ME2_m-cithub_anderson",
    ],
    [
        "I'm Garrus Vakarian, and this is now my favorite spot on the Citadel.",
        "ME2_m-hench_garrus",
    ],
    [
        "We've seen these before, Shepard. Dragon's Teeth, your people call them. The geth used them on Eden Prime.",
        "ME2_m-hench_tali",
    ],
    [
        "I spent two years mourning you. So if we're going to try this, I need to know that you're always coming back.",
        "ME3_m-hench_liara",
    ],
    [
        "That assassin should be embarrassed. A terminally ill drell kept him from reaching his target.",
        "ME3_m-global_thane",
    ],
    [
        "Stand amongst the ashes of a trillion dead souls and ask the ghosts if honor matters.",
        "ME3_m-hench_prothean",
    ],
    [
        "Want me to call the Council and hang up on them? For old times' sake.",
        "ME3_m-global_joker",
    ],
]
