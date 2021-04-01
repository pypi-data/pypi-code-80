from intentBox.container import IntentBox
from os.path import expanduser, join
from os import listdir, walk


class CollisionDetector:
    def __init__(self, config=None):
        self.config_core = config or {}
        self.box = IntentBox()
        self._skills_map = {}
        self.load_skills()

    @property
    def skills_config(self):
        return self.config_core.get("skills", {"csm": {"directory": "skills"}})

    @property
    def skills_path(self):
        data_dir = self.config_core.get("data_dir", expanduser("~/chatterbox"))
        return expanduser(join(data_dir, self.skills_config["csm"]["directory"]))

    @property
    def blacklisted_skills(self):
        return self.skills_config.get("blacklisted_skills", [])

    def load_skills(self):
        # TODO live monitor
        for skill_folder in listdir(self.skills_path):
            for base, folders, files in walk(join(self.skills_path, skill_folder)):
                for f in files:
                    if f.endswith(".voc"):
                        name = skill_folder + ":" + f.split(".")[0]
                        self._skills_map[name] = skill_folder
                        # TODO this is very limiting but works for the standard listen block
                        self.box.register_adapt_intent_from_file(name, join(base, f))
                    elif f.endswith(".rx"):
                        self._skills_map[f] = skill_folder
                        self.box.register_adapt_regex_from_file(join(base, f))
                    elif f.endswith(".intent"):
                        name = skill_folder + ":" + f.split(".")[0]
                        self._skills_map[name] = skill_folder
                        self.box.register_padatious_intent_from_file(name, join(base, f))
                    elif f.endswith(".entity"):
                        self.box.register_padatious_entity_from_file(f, join(base, f))

    def triggered_skills(self, utterance, min_conf=0.5):
        utterance = utterance.strip() # spaces should not mess with exact matches
        intents = self.box.intent_scores(utterance)
        for idx, intent in enumerate(intents):
            intents[idx].pop("utterance")
            intents[idx]["skill"] = self._skills_map.get(intents[idx]["intent_type"])
            intents[idx]["intent_name"] = intents[idx].pop("intent_type").split(":")[-1]
            if intent["conf"] < min_conf:
                intents[idx] = None
        return [i for i in intents if i]



if __name__ == "__main__":
    c = CollisionDetector()

    print(c.triggered_skills("what is your ip address"))
    print(c.triggered_skills("lower volume"))
    print(c.triggered_skills("say that again"))
    print(c.triggered_skills("what did i say"))

    """
    [{'skill': 'ip_address', 'conf': 1.0, 'entities': {}, 'intent_name': 'intent_name2Intent', 'intent_engine': 'padatious'}]
    [{'skill': 'volume', 'conf': 1.0, 'entities': {}, 'intent_name': 'intent_name3Intent', 'intent_engine': 'padatious'}]
    [{'intent_name': 'say_that_again', 'entities': {'again:say_that_again': 'say that again'}, 'skill': 'again', 'conf': 1.0, 'intent_engine': 'adapt'}]
    [{'intent_name': 'what_did_i_say', 'entities': {'again:what_did_i_say': 'what did i say'}, 'skill': 'again', 'conf': 1.0, 'intent_engine': 'adapt'}]
    """
