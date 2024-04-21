import spacy
from spacy import displacy


nlp = spacy.load("zh_core_web_sm")
# nlp = spacy.load("en_core_web_sm")           # load package "en_core_web_sm"
# nlp = spacy.load("/path/to/en_core_web_sm")  # load package from a directory
#
# doc = nlp("This is a sentence.")

import zh_core_web_sm
nlp = zh_core_web_sm.load()
doc = nlp("北京分行自营贷款，上海分行自营存款。下属最多的五个分行，五个机构")
print([(w.text, w.pos_) for w in doc])

#词性标注
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

#可视化工具
# displacy.serve(doc, style="dep")
displacy.serve(doc, style="ent")