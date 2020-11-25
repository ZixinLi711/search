from flask import Flask, render_template
import time

app = Flask(__name__)
@app.route('/search/<keyword>')
def searchByKeyword(keyword):
     num,result = search(keyword)
     return render_template("page.html",title=search,result=result,keyword=keyword,num=num)

from whoosh.index import create_in
from whoosh.fields import *
import os.path
import os
from whoosh.analysis import StemmingAnalyzer
def search(keyword):
     stem_ana = StemmingAnalyzer(cachesize=-1)
     schema = Schema(id = ID(stored=True), title = TEXT(stored=True,analyzer=stem_ana),abstract= TEXT(stored=True,analyzer=stem_ana))

     if not os.path.exists("index"):
         os.mkdir("index")
     ix = create_in("index", schema)
     writer = ix.writer(procs=4, multisegment=True, limitmb=2048)


     import json
     with open('arxiv-metadata-oai-snapshot.json') as f:
         for line in f.readlines():
             data = json.loads(line)
             # In order to save the storing space, I only index id,title and abstract.
             writer.add_document(id=data["id"], title=data["title"], abstract=data["abstract"])

     writer.commit()
     from whoosh.qparser import QueryParser,MultifieldParser
     with ix.searcher() as searcher:
         q = MultifieldParser({"title","abstract"},ix.schema).parse(keyword)
         results = searcher.search(q,limit=None )
         # results = searcher.collector(collapse="deep learning", collapse_limit = 3)
         list = []
         print(len(results))
         print(time.process_time())
         for r in results:
              if not list.__contains__(r):
                list.append(dict(r))
         return len(list),list



if __name__ == '__main__':
     app.run(port=8081)


