"""Defines some mappings from speaker ids to characters accross games."""

SPEAKER_MAPPINGS = {
    # ME2
    "m-player_m-Shepard": "Broshep",
    "f-player_f-Shepard": "Femshep",
    # ME3
    "m-Shepard": "Broshep",
    "f-Shepard": "Femshep",
    # Thane
    "m-hench_assassin": "Thane",
    "m-hench_assassin-citasl_thane_follow": "Thane",
    "m-global_thane": "Thane",
    # "m-radio_thane": "Thane",
    # Tali
    "m-hench_tali": "Tali",
    "m-hench_tali-profre_tali": "Tali",
    # "m-radio_tali": "Tali",
    # Legion
    "m-hench_geth": "Legion",
    # "m-gth002_gethprime": "Legion",  # Technically a geth prime
    "m-global_legion": "Legion",
    # "m-gthleg_first_geth": "Legion",  # Technically recorded Geth
    # "m-radio_legion": "Legion",
    # Conrad Verner
    "m-twrhub_imposter_conrad": "ConradVerner",
    "m-citund_conradverner": "ConradVerner",
    # Garrus Vakarian
    "m-hench_garrus": "Garrus",
    # "m-hench_garrus-omggra_garrus_sniper": "Garrus",
    # EDI
    "m-hench_edi": "EDI",
    "m-hench_ai": "EDI",
    # "m-radio_edi": "EDI",
    # Javik
    "m-hench_prothean": "Javik",
    "m-hench_ prothean": "Javik",
    # Mordin Solus
    "m-global_mordin": "Mordin",
    "m-hench_professor": "Mordin",
    # "m-hench_professor-hench_radio_professor": "Mordin",
    # "m-radio_mordin": "Mordin",
    # Kasumi Goto
    "m-hench_thief": "Kasumi",
    "m-hench_thief-hench_saboteur": "Kasumi",
    "m-cit_kasumi": "Kasumi",
    # "m-cit_radio_kasumi": "Kasumi",
    # Jack
    "m-hench_convict": "Jack",
    "m-global_jack": "Jack",
    # Grunt
    "m-hench_grunt": "Grunt",
    "m-global_grunt": "Grunt",
    # "m-radio_grunt": "Grunt",
    # Zaeed
    "m-global_zaeed": "Zaeed",
    "m-hench_veteran": "Zaeed",
    # Liara T'Soni
    # "m-liara": "Liara",
    "m-hench_liara": "Liara",
    # "m-liara-pronor_liara": "Liara",
    # "m-radio_liara": "Liara",
    # Miranda Lawson
    "m-hench_vixen": "Miranda",
    "m-hench_vixen-procer_vixen": "Miranda",
    "m-hench_vixen-procer_miranda": "Miranda",
    "m-global_miranda": "Miranda",
    # "m-radio_global_miranda": "Miranda",
    # Ashley Williams
    "m-hench_ashley": "Ashley",
    # "m-horcr1_ashley": "Ashley",
    # "m-horcr1_ashley-pronor_ash": "Ashley",
    # James Vega
    "m-hench_marine": "James",
    # "m-radio_marine": "James",
    # "m-radio_james": "James",
    # Kaidan Alenko
    "m-hench_kaidan": "Kaidan",
    # "m-horcr1_kaidan": "Kaidan",
    # "m-horcr1_kaidan-pronor_kaidan": "Kaidan",
    # Anderson
    "m-global_anderson": "Anderson",
    "m-cithub_anderson": "Anderson",
    "m-cithub_anderson-citprs_anderson": "Anderson",
    # "m-radio_anderson": "Anderson",
    # "m-radio_global_anderson": "Anderson",
    # Samara and Morinth posing as Samara
    "m-global_samara": "Samara",
    "m-hench_mystic": "Samara",
    "m-hench_mystic-hench_mystic_as_vampire": "Samara",
    "m-hench_mystic-twrmwa_mystic_warrior": "Samara",
    # Jacob Taylor
    "m-global_jacob": "Jacob",
    "m-hench_leading": "Jacob",
    # "m-radio_jacob": "Jacob",
    # Joker
    "m-hench_joker": "Joker",
    "m-global_joker": "Joker",
    # "m-radio_joker": "Joker",
    # Wrex
    "m-krohub_wrex": "Wrex",
    "m-global_wrex": "Wrex",
    # "m-radio_wrex": "Wrex",
    # Gabby and Ken
    "m-nor_engineer_female": "Gabby",
    "m-cithub_gabby": "Gabby",
    "m-nor_engineer_male": "Ken",
    "m-cithub_ken": "Ken",
    # Karin Chakwas
    "m-nor_doctor": "Chakwas",
    "m-nor_doctor-endgm2_chakwas": "Chakwas",
    # Urdnot Wreav
    "m-global_wreav": "Wreav",
    # "m-radio_wreav": "Wreav",
    # The Illusive Man
    "m-global_illusive_man": "IllusiveMan",
    "m-global_illusive_man-nor_illusive_man": "IllusiveMan",
    "m-global_illusive_man-procer_illusive_man": "IllusiveMan",
    # Armando-Owen Bailey
    "m-global_bailey": "Bailey",
    # Kelly Chambers
    "m-nor_yeoman-endgm2_yeoman": "KellyChambers",
    "m-nor_yeoman": "KellyChambers",
    "m-nor_yeoman-endgm2_chambers": "KellyChambers",
}


def get_character(raw: str) -> str:
    """Get the character name from an identifier."""
    # Return proper name if found, otherwise return the input
    return SPEAKER_MAPPINGS.get(raw, raw)
