import json
import random
from dataclasses import dataclass, field, asdict
from typing import List, Optional


TRAITS = [
    "ZEALOUS", "GLUTTONOUS", "ABSTINENT", "SKEPTICAL", "DEVOUT",
    "SOCIABLE", "SOLITARY", "COWARD", "BLOODTHIRSTY", "MOURNFUL",
    "PROUD", "LOYAL", "DOUBTFUL", "DISLOYAL",
]

FIRST_NAMES = [
    "Sara", "Elias", "Miriam", "Jonah", "Ada", "Caleb", "Hannah",
    "Silas", "Ruth", "Amos", "Leah", "Gideon", "Naomi", "Tobias",
    "Esther", "Pietro", "Marta", "Luca", "Oda", "Ewan",
]


@dataclass
class Follower:
    id: str
    name: str
    age: int
    trait: str
    zeal: int
    comfort: int
    obedience: int
    faction: Optional[str] = None
    knowledge: List[str] = field(default_factory=list)
    memory: List[str] = field(default_factory=list)


@dataclass
class Campaign:
    id: str
    seed: int
    turn: int
    max_turns: int
    zeal_pool: int
    comfort_pool: int
    strain: int
    flock_size: int
    followers: List[Follower]
    doctrines: List[dict] = field(default_factory=list)
    events: List[dict] = field(default_factory=list)
    current_scene: Optional[str] = None
    next_scene: Optional[str] = None
    herald_rumor: Optional[str] = None
    violations_log: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        d["followers"] = [Follower(**f) for f in d["followers"]]
        return cls(**d)


def _make_followers(rng: random.Random, n: int) -> List[Follower]:
    followers = []
    for i in range(n):
        followers.append(Follower(
            id=f"f{i:03d}",
            name=rng.choice(FIRST_NAMES),
            age=rng.randint(16, 68),
            trait=rng.choice(TRAITS),
            zeal=rng.randint(35, 65),
            comfort=rng.randint(35, 65),
            obedience=rng.randint(40, 70),
        ))
    return followers


def new_campaign(seed: int) -> Campaign:
    rng = random.Random(seed)
    followers = _make_followers(rng, rng.randint(8, 14))
    return Campaign(
        id=f"c{seed:08x}",
        seed=seed,
        turn=1,
        max_turns=12,
        zeal_pool=sum(f.zeal for f in followers),
        comfort_pool=sum(f.comfort for f in followers),
        strain=0,
        flock_size=len(followers),
        followers=followers,
    )
