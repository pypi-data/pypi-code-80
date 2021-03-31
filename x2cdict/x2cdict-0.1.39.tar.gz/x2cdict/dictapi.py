from x2cdict.google import GoogleVocabDict, GooglePhraseDict
from x2cdict.qishe import QisheVocabDict

class VocabDict:
  """
  It combines qishe and google voacb api
  """

  def __init__(self, from_lang, to_lang="cn"):
    self.from_lang, self.to_lang = from_lang, to_lang
    self.google_api = GoogleVocabDict(from_lang, to_lang)
    self.qishe_api = QisheVocabDict(from_lang, to_lang)

  def search(self, w, pos, google=True):
    result = self.qishe_api.search_with_pos(w, pos)
    if result == None:
      result = self.google_api.search(w, pos) if google else None
    return result

  def search_without_pos(self, w, google=True):
    result = self.qishe_api.search_without_pos(w)
    if result == None:
      result = self.google_api.search(w, pos) if google else None
    return result


class PhraseDict:
  """
  Google API to translate phrase 
  """

  def __init__(self, from_lang, to_lang="cn"):
    self.from_lang, self.to_lang = from_lang, to_lang
    self.google_api = GooglePhraseDict(from_lang, to_lang)

  def search(self, p):
    result = self.google_api.search(p)
    return result
