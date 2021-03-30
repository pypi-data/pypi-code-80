import pywikibot
import pandas as pd
import requests
from itertools import chain
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from SPARQLWrapper import SPARQLWrapper, JSON
from sentence_transformers import SentenceTransformer, util, models, losses
import torch
import re
import random
from tqdm import tqdm
from pprint import pprint


class synonym_finder():
    '''
    Synonym finder class
    '''
    def __init__(self, bert_model = 'nli-bert-base'):
        self.model_name = bert_model
        self.model=None
        
    def rerank(self,target_w, outputs_w, thr = 0.7):
        if self.model ==None:
            self.model = SentenceTransformer(self.model_name)
        outputs_w = [re.sub('_',' ',x) for x in outputs_w]
        outputs_df = pd.DataFrame(data = {'concept':outputs_w})
        outputs_emb = self.model.encode(outputs_w)
        target_emb = self.model.encode(target_w)
        cs = util.pytorch_cos_sim(target_emb, outputs_emb)[0]
        cs = cs.cpu()

        #We use torch.topk to find the highest N scores
        top_res = torch.topk(cs, k=len(outputs_w))
        inds = list(top_res[1].numpy())
        headT = outputs_df.iloc[inds].copy()
        headT["score"] = list(top_res[0].numpy())
        headT = headT[headT.score>thr]
        return headT.concept.tolist()
    
    
    def get_synonyms(self,term=None,source = "wikidata", thr = 0):
        '''
        Return synonyms and related keywords
        '''
        if source=='wikidata':
            try:
                site = pywikibot.Site('en', 'wikipedia')
                page = pywikibot.Page(site, term)
                item = pywikibot.ItemPage.fromPage(page)
                outputs = item.aliases['en']
                 ##### filter ####
                outputs = [x for x in outputs if term.lower() not in x.lower()]
                return outputs
            except Exception as e:
                print(e)
        elif source=='conceptnet':
            try:
                response = requests.get("http://api.conceptnet.io/related/c/en/"+term+"?filter=/c/en&limit=50")
                res_dict = response.json()
                synonyms_df = pd.DataFrame(res_dict['related'])
                synonyms_df['@id'] = synonyms_df['@id'].apply(lambda x : x.split('/')[-1])
                outputs = synonyms_df['@id'].tolist()
                if thr == 0:
                    return outputs
                else:
                    return self.rerank(term,outputs,thr = thr)
            except Exception as e:
                print(e)
        elif source=='wordnet':
            try:
                synonyms = wordnet.synsets(term)
                lemmas = list(set(chain.from_iterable([word.lemma_names() for word in synonyms])))
                return lemmas
            except Exception as e:
                print(e)
        elif source=='dbpedia':
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setQuery('select ?link ?olink ?label where { ?link rdfs:label "' +str(term)+'"@en. ?olink  dbo:wikiPageRedirects ?link. ?olink rdfs:label ?label FILTER(lang(?label ) = "en")}')
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            outputs = []
            for result in results["results"]["bindings"]:
                outputs.append(result["label"]["value"])
                
            ##### filter ####
            outputs = [x for x in outputs if term.lower() not in x.lower()]

            if thr ==0:
                return outputs
            else:
                return self.rerank(term,outputs, thr = thr)

        def word_lemmatizer(self, text):
            lem_text = [WordNetLemmatizer().lemmatize(i) for i in text]
            return lem_text

        def word_stemmer(self, text):
            stem_text = [PorterStemmer().stem(i) for i in text]
            return stem_text
