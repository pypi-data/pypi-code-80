import requests


# TODO localization
COREFERENCE_INDICATORS_EN = ["he", "she", "it", "they", "them", "these", "whom",
                             "whose", "who", "its", "it's", "him", "her", "we",
                             "us"]


def tokenize(text):
    # very simple, tokenize punctuation
    punct = [".", ",", "", "-", "!", "?"]
    for p in punct:
        text = text.replace(p, " " + p + " ")
    return [w for w in text.split(" ") if w.strip()]


def replace_coreferences(text, smart=True, nlp=None):
    if smart:
        words = tokenize(text)
        should_solve = False
        for indicator in COREFERENCE_INDICATORS_EN:
            if indicator in words:
                should_solve = True
                break
        if not should_solve:
            return text
    solver = CoreferenceSolver(nlp)
    solved = solver.replace_coreferences(text)
    if solved == text:
        return solver.replace_coreferences_with_context(text)
    return solved


class CoreferenceSolver:
    nlp = None
    cache = {}
    contexts = {}
    prev_sentence = ""
    prev_solved = ""

    def __init__(self, nlp=None, lang="en-us"):
        # TODO localize
        if nlp:
            self.bind(nlp)

    @staticmethod
    def extract_replacements(original, solved):
        a = original.lower()
        b = solved.lower()
        chunk = a.split(" ")
        chunk2 = b.split(" ")
        replaced = {}
        index_map = {}
        # extract keys
        indexes = []
        for idx, w in enumerate(chunk):
            if w not in chunk2:
                indexes.append(idx)
                replaced[idx] = []
                index_map[idx] = w
        i2 = 0
        for i in indexes:
            o = chunk[i:]
            s = chunk2[i + i2:]
            if len(o) == 1:
                # print(o[0], "->", " ".join(s), i)
                replaced[i].append(" ".join(s))
                continue
            for idx, word in enumerate(o):
                if word not in s:
                    chunk3 = s[idx:]
                    for idx2, word2 in enumerate(chunk3):
                        if word2 in o and not replaced[i]:
                            chunk3 = s[:idx2]
                            i2 += len(chunk3) - 1
                            # print(word, "->", " ".join(chunk3), i)
                            replaced[i].append(" ".join(chunk3))
        bucket = {}
        for k in replaced:
            if index_map[k] not in bucket:
                bucket[index_map[k]] = []
            bucket[index_map[k]] += replaced[k]
        return bucket

    @classmethod
    def bind(cls, nlp):
        CoreferenceSolver.nlp = nlp

    @classmethod
    def replace_coreferences(cls, text):
        cls.prev_sentence = text
        if text in cls.cache:
            solved = cls.cache[text]
        else:
            try:
                # offline, using neuralcoref
                if cls.nlp is not None:
                    doc = cls.nlp(text)
                    solved = doc._.coref_resolved
                else:
                    # mix both services
                    # neuralcoref catches "it", which cogcomp fails
                    # London was founded by the Romans, who named london Londinium.
                    # cogcomp catches "who did X", which neural coref fails
                    # It was founded by the Romans, the Romans named it Londinium.

                    solved = cls.cogcomp_coref_resolution(text) or text
                    solved = cls.neuralcoref_demo(solved)

                cls.cache[text] = solved
            except Exception as e:
                cls.prev_solved = text
                return text
        extracted = cls.extract_replacements(text, solved)
        for pronoun in extracted:
            if len(extracted[pronoun]) > 0:
                cls.contexts[pronoun] = extracted[pronoun][-1]
        cls.prev_solved = solved
        return solved

    @staticmethod
    def neuralcoref_demo(text):
        try:
            params = {"text": text}
            r = requests.get("https://coref.huggingface.co/coref",
                             params=params).json()
            text = r["corefResText"] or text
        except Exception as e:
            pass
        return text

    @staticmethod
    def cogcomp_coref_resolution(text):
        try:
            data = CoreferenceSolver._cogcomp_demo(text)
            links = data["links"]
            node_ids = {}
            replace_map = {}
            for n in data["nodes"]:
                node_ids[int(n["id"])] = n["name"]
            for l in links:
                # only replace some stuff
                if node_ids[l["target"]].lower() not in COREFERENCE_INDICATORS_EN:
                    continue
                replace_map[node_ids[l["target"]]] = node_ids[l["source"]]
            for r in replace_map:
                text = text.replace(r, replace_map[r])
            return text
        except Exception as e:
            return text

    @staticmethod
    def _cogcomp_demo(text):
        url = "https://cogcomp.org/demo_files/Coref.php"
        data = {"lang": "en", "text": text}
        r = requests.post(url, json=data)
        return r.json()

    @classmethod
    def replace_coreferences_with_context(cls, text):

        if text in cls.cache:
            solved = cls.cache[text]
        else:
            new_text = cls.prev_solved + "; " + text
            try:
                # offline, using spacy
                if cls.nlp is not None:
                    doc = cls.nlp(new_text)
                    solved = doc._.coref_resolved
                else:
                    solved = cls.cogcomp_coref_resolution(new_text) or new_text
                    solved = cls.neuralcoref_demo(solved)

                solved = solved.replace(cls.prev_solved + "; ", "").strip()
                cls.cache[new_text] = solved
                cls.cache[text] = solved
            except Exception as e:
                cls.prev_solved = text
                return text
        extracted = cls.extract_replacements(text, solved)
        for pronoun in extracted:
            if len(extracted[pronoun]) > 0:
                cls.contexts[pronoun] = extracted[pronoun][-1]
        cls.prev_sentence = text
        cls.prev_solved = solved
        return solved

