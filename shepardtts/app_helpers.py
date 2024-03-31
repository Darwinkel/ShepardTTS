"""Helper functions for ShepardTTS Gradio web interface."""

from .__version__ import __version__

title = "ShepardTTS"

description = """

<br/>

This demo is currently running a fine-tuned version of **XTTS v2.0.3**.
<a href="https://huggingface.co/coqui/XTTS-v2">XTTS</a> is a multilingual text-to-speech and voice-cloning model.
It has been fine-tuned on game data from Mass Effect 2 and Mass Effect 3.
Speaker embeddings are generated from available game samples.
The number in front of each speaker indicates the amount of audio samples it was calibrated on.
See the GitHub repository for more information.

<br/>

This server has limited computing power (CPU-bound).
Multi-sentence texts can take up to a minute or more to generate.

<br/>

Most voices perform best when narrating medium-length sentences with medium-length words.
They tend to produce garbage and artifacts when confronted with very short words and sentences,
 excessive punctuation, and abbreviations.
Sentences which are too long tend to cause hallucinations.
As a rule of thumb: provide text input such that it could have reasonably occurred in the games.
The more out-of-domain - and unnatural - the text input, the lower the chances of a good narration.

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
        "46_ME2-f_player_f_Shepard-twrhub_main_contact_d_dlg",
        # 31_ME2-f_player_f_Shepard-twrasa_pinnacle_assassin_d_dlg
        # 35_ME2-f_player_f_Shepard-omgpra_mordin_d_dlg
        # 38_ME2-f_player_f_Shepard-norcv_starter_h_dlg
        # 24_ME2-f_player_f_Shepard-norlm_relationship_02_dlg
    ],
    [
        "I'm Commander Shepard, and this is my favorite store on the Citadel.",
        "70_ME2-m_player_m_Shepard-nor_yeoman_d_dlg",
        # 32_ME3-m_Shepard-citprs_cat3_ashjoins_m_dlg
        # ME2-m_player_m_Shepard-quatll_admiraldove1_d_dlg
        # 29_ME3-m_Shepard-kro002_salarianalt_bye_m_dlg
        # 14_ME2-m_player_m_Shepard-norlm_relationship_02_dlg
    ],
    [
        "I don't know if the Reapers understand fear, but you killed one of them. They have to respect that.",
        "31_ME2-m_global_illusive_man-norcr1_debriefing_d_dlg",
    ],
    [
        "Worried about my qualifications? "
        "I can crush a mech with my biotics or shoot its head off at a hundred yards. "
        "Take your pick.",
        "42_ME2-m_hench_vixen-norvx_relationship_03_h_dlg",
        # 24_ME2-m_hench_vixen-procer_vixen_intro_d_dlg
        # 40_ME2-m_hench_vixen-norvx_starter_h_dlg"
    ],
    [
        "Lots of ways to help people. Sometimes heal patients; sometimes execute dangerous people. Either way helps.",
        "28_ME2-m_hench_professor-norpr_relationship_00_h_dlg",
        # 28_ME2-m_hench_professor-norpr_relationship_00_h_dlg
        # 43_ME2-m_hench_professor-norpr_relationship_03_h_dlg
        # 41_ME2-m_hench_professor-norpr_loyalty_01_h_dlg
        # 41_ME2-m_hench_professor-kroprl_protege_d_dlg
        # 36_ME2-m_hench_professor-kroprl_deadkrogan_h_dlg
    ],
    [
        "Christian Bible, the Gospel of Mark, chapter five, verse nine. "
        "We acknowledge this as an appropriate metaphor. "
        "We are Legion, a terminal of the geth. "
        "We will integrate into Normandy.",
        "29_ME2-m_hench_geth-norgt_relationship03_h_dlg",
        # 31_ME2-m_hench_geth-norgt_relationship00_h_dlg
    ],
    [
        "I enjoy the sight of humans on their knees. That is a joke.",
        "25_ME2-m_hench_ai-endgm2_huddle_03a_d_dlg",
        # 27_ME3-m_Owner-norhen_edi_investigate_d_dlg
    ],
    [
        "The problem is that war isn't orderly. "
        "And the enemy is never predictable. "
        "Even the most experienced veteran is going to find themselves in situations they haven't trained for.",
        "14_ME2-m_cithub_anderson_citprs_anderson-citprs_council_d_dlg",
    ],
    [
        "I'm Garrus Vakarian, and this is now my favorite spot on the Citadel.",
        "27_ME2-m_hench_garrus-citgrl_window_tgr_dlg",
        # 32_ME2-m_hench_garrus-norgr_relationship_03_h_dlg
        # 37_ME2-m_hench_garrus-omggra_garrus_intro_d_dlg
        # 35_ME2-m_hench_garrus-norgr_relationship_00_h_dlg
    ],
    [
        "We've seen these before, Shepard. Dragon's Teeth, your people call them. The geth used them on Eden Prime.",
        "41_ME2-m_hench_tali-nortl_relationship_03_h_dlg",
        # 35_ME2-m_hench_tali-nortl_relationship_04_h_dlg
        # 32_ME2-m_hench_tali-nortl_loyalty_02_h_dlg
    ],
    [
        "I spent two years mourning you. So if we're going to try this, I need to know that you're always coming back.",
        "121_ME2-m_liara-twrhub_main_contact_d_dlg",
        # 58_ME3-m_hench_liara-cat002_monastery_objects_b_dlg
    ],
    [
        "That assassin should be embarrassed. A terminally ill drell kept him from reaching his target.",
        "66_ME2-m_hench_assassin-noras_starter_h_dlg",
        # 40_ME2-m_hench_assassin-noras_loyalty01_h_dlg
    ],
    [
        "Stand amongst the ashes of a trillion dead souls and ask the ghosts if honor matters.",
        "32_ME3-m_hench_prothean-cat002_monastery_objects_b_dlg",
    ],
    [
        "Want me to call the Council and hang up on them? For old times' sake.",
        "78_ME3-m_Owner-nor_joker_bridge_d_dlg",
        # 8_ME3-m_global_joker-cat003_nor_warning_v_dlg
    ],
    [
        "By the Code, I will serve you, Shepard. Your choices are my choices. "
        "Your morals are my morals. "
        "Your wishes are my code.",
        "45_ME2-m_hench_mystic-normw_loyalty_02_h_dlg",
        # 33_ME2-m_hench_mystic-normw_relationship_03_h_dlg
        # 45_ME2-m_hench_mystic-normw_loyalty_01_h_dlg
        # 49_ME3-m_Owner-citprs_samara_d_dlg
    ],
    [
        "I wanted to travel the stars, tending the wounds of tough soldiers with piercing eyes and sensitive souls. "
        "Turns out military life isn't quite as romantic as I'd imagined.",
        "17_ME3-m_Owner-cithub_doctor_recruit_d_dlg",
        # 55_ME2-m_nor_doctor-nor_doctor_d_dlg
    ],
    [
        "If there was ever a reason I studied psychology, it was to help people at a time like this.",
        "153_ME2-m_nor_yeoman-nor_yeoman_d_dlg",
        # 22_ME2-m_nor_yeoman-nor_yeoman_a_dlg
    ],
    [
        "You'll have to make him scream a little. He's not going to tell you everything just 'cause you ask.",
        "42_ME3-m_Owner-citwrd_rp1_bailey_d_dlg",
        # 20_ME3-m_global_bailey-cat003_wrapup_bailey_d_dlg
        # 22_ME3-m_Owner-citwrd_rp1_bailey_ph2_d_dlg
        # 18_ME3-m_global_bailey-cat003_csec_baileylogin_d_dlg
        # 18_ME3-m_Owner-citwrd_aria3_bailey_d_dlg
    ],
    [
        "We finally get out here, and the final frontier was already settled. "
        "And the residents don't even seem impressed by the view. Or the dangers.",
        "35_ME2-m_horcr1_kaidan-horcr1_kaidan_end_d_dlg",
        # 11_ME3-m_hench_kaidan-cat002_enter_building_m_dlg
    ],
    [
        "I can't tell the aliens from the animals.",
        "17_ME3-m_hench_ashley-cat002_monastery_objects_b_dlg",
        # 35_ME2-m_horcr1_ashley-horcr1_ash_end_d_dlg
        # 52_ME3-m_Owner-citprs_ash_char_moment_m_dlg
        # 31_ME3-m_Owner-citprs_ash_talk1_d_dlg
    ],
]
