from deflock.engine.state import Campaign
from deflock.engine.scenes import SCENES, pick_scene


def resolve(campaign: Campaign, action: str):
    """
    Apply a player action and return (campaign, new_events).
    Slice 1: advance turn, log an event, pick next scene.
    No drift, no doctrines, no factions. Slice 2 onward.
    """
    scene = SCENES[campaign.current_scene]
    turn = campaign.turn

    if action == "comply":
        text = f"You {scene.compelled_action} {scene.compelled_object}. The flock watches."
    elif action == "refuse":
        text = f"You refuse. {scene.name} goes unattended."
    elif action == "social":
        text = f"You {scene.social_action} {scene.social_object}."
    elif action == "decree":
        text = "You withdraw to write. The flock waits outside."
    elif action == "purge":
        text = "You order the dissenters expelled."
    else:
        raise ValueError(f"unknown action: {action}")

    event = {"turn": turn, "kind": "action", "text": text}
    campaign.events.append(event)
    campaign.turn += 1

    if campaign.turn > campaign.max_turns:
        end = {"turn": campaign.turn, "kind": "system", "text": "The year has ended."}
        campaign.events.append(end)
        return campaign, [event, end]

    campaign.current_scene = pick_scene(campaign.seed, campaign.turn)
    campaign.next_scene = pick_scene(campaign.seed, campaign.turn + 1)
    campaign.herald_rumor = "Rumours drift in from the outer village."
    return campaign, [event]
