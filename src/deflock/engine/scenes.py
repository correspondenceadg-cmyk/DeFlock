from dataclasses import dataclass
from typing import List
import random


@dataclass
class Scene:
    id: str
    name: str
    prose_variants: List[str]
    compelled_action: str
    compelled_object: str
    conditions: List[str]
    social_action: str
    social_object: str
    withdrawable: bool
    sacrificeable: bool
    weight: float = 1.0


SCENES = {
    "feast_new_moon": Scene(
        id="feast_new_moon",
        name="The Feast of the New Moon",
        prose_variants=[
            "The table is set under the new moon. The elder lifts a cup.",
            "Smoke rises from the fire. The flock waits with hands open.",
            "A goat has been slaughtered and the wine poured. The elder beckons.",
        ],
        compelled_action="eat", compelled_object="flesh",
        conditions=["on new moons"],
        social_action="speak", social_object="with the elder",
        withdrawable=True, sacrificeable=True, weight=1.5,
    ),
    "sabbath_dispute": Scene(
        id="sabbath_dispute",
        name="The Sabbath Dispute",
        prose_variants=[
            "A field lies half-harvested. The flock looks to you. It is the day of rest.",
            "The ox has thrown a shoe. The others wait for your word.",
        ],
        compelled_action="work", compelled_object="the field",
        conditions=["on the day of rest"],
        social_action="pray", social_object="with the flock",
        withdrawable=False, sacrificeable=False,
    ),
    "stranger_door": Scene(
        id="stranger_door",
        name="The Stranger at the Door",
        prose_variants=[
            "A traveller stands at the gate. The flock watches.",
            "Someone knocks. They are not of this place.",
        ],
        compelled_action="speak", compelled_object="with the stranger",
        conditions=["in the presence of outsiders"],
        social_action="give", social_object="alms without speaking",
        withdrawable=False, sacrificeable=False,
    ),
    "funeral": Scene(
        id="funeral",
        name="The Funeral",
        prose_variants=[
            "A body lies on the bier. The mourners wait for your hand.",
            "The grave is open. The widow does not look at you.",
        ],
        compelled_action="touch", compelled_object="the dead",
        conditions=["while in grief"],
        social_action="speak", social_object="a blessing",
        withdrawable=False, sacrificeable=True,
    ),
    "sick_bed": Scene(
        id="sick_bed",
        name="The Sick Bed",
        prose_variants=[
            "A child lies feverish. The mother holds the door open.",
            "The old man's breathing is shallow. The room smells of sweat.",
        ],
        compelled_action="touch", compelled_object="the sick",
        conditions=["while sick"],
        social_action="pray", social_object="over the sick",
        withdrawable=True, sacrificeable=False,
    ),
    "marriage_alliance": Scene(
        id="marriage_alliance",
        name="The Marriage Alliance",
        prose_variants=[
            "A neighbouring elder offers their daughter. The flock waits.",
            "The terms are read aloud. A union would settle the border.",
        ],
        compelled_action="marry", compelled_object="the outsider",
        conditions=["when married"],
        social_action="speak", social_object="terms instead",
        withdrawable=False, sacrificeable=True,
    ),
    "elders_council": Scene(
        id="elders_council",
        name="The Elders' Council",
        prose_variants=[
            "The elders are seated. They wait for you to speak.",
            "The room is quiet. All eyes are on the head of the table.",
        ],
        compelled_action="speak", compelled_object="a ruling",
        conditions=["always"],
        social_action="speak", social_object="a ruling",
        withdrawable=False, sacrificeable=False,
    ),
    "blood_rite": Scene(
        id="blood_rite",
        name="The Blood Rite",
        prose_variants=[
            "The beast is bound. The knife is in your hand.",
            "Blood is on the stones already. The flock chants.",
        ],
        compelled_action="touch", compelled_object="blood",
        conditions=["on feast days"],
        social_action="pray", social_object="over the offering",
        withdrawable=False, sacrificeable=True,
    ),
    "childrens_lesson": Scene(
        id="childrens_lesson",
        name="The Children's Lesson",
        prose_variants=[
            "The children are seated in rows. They are waiting to be taught.",
            "A small hand tugs at your sleeve. The others watch.",
        ],
        compelled_action="touch", compelled_object="the children",
        conditions=["always"],
        social_action="give", social_object="a coin and a word",
        withdrawable=True, sacrificeable=False,
    ),
    "alone_hour": Scene(
        id="alone_hour",
        name="The Alone Hour",
        prose_variants=[
            "The fire is low. No one is watching. The cup is at your elbow.",
            "The day's work is done. You are alone with your thoughts.",
        ],
        compelled_action="drink", compelled_object="wine",
        conditions=["when alone"],
        social_action="pray", social_object="instead",
        withdrawable=True, sacrificeable=False,
    ),
    "grief_encounter": Scene(
        id="grief_encounter",
        name="The Grief Encounter",
        prose_variants=[
            "A widow sits at her door. She has not eaten in three days.",
            "The young man's father has died. He begs you to sit with him.",
        ],
        compelled_action="fast", compelled_object="with the grieving",
        conditions=["while in grief"],
        social_action="eat", social_object="to comfort them",
        withdrawable=True, sacrificeable=False,
    ),
    "wandering_preacher": Scene(
        id="wandering_preacher",
        name="The Wandering Preacher",
        prose_variants=[
            "A preacher has arrived with a new doctrine. He asks to be heard.",
            "A man in ragged robes speaks of a god you have never named.",
        ],
        compelled_action="speak", compelled_object="with them",
        conditions=["in the presence of outsiders"],
        social_action="give", social_object="a coin and a blessing",
        withdrawable=True, sacrificeable=False,
    ),
}


def pick_scene(seed: int, turn: int) -> str:
    """Deterministic scene pick from (seed, turn). Real scheduler lands in Slice 5."""
    rng = random.Random(seed * 1000 + turn)
    ids = list(SCENES.keys())
    weights = [SCENES[i].weight for i in ids]
    return rng.choices(ids, weights=weights, k=1)[0]


def scene_prose(scene_id: str, seed: int, turn: int) -> str:
    scene = SCENES[scene_id]
    rng = random.Random(seed * 2000 + turn * 7 + 17)
    return rng.choice(scene.prose_variants)
