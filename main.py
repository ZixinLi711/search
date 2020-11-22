from flask import Flask, render_template

app = Flask(__name__)
@app.route('/search/<keyword>')
def searchByKeyword(keyword):
    num,result = search(keyword)
    return render_template("page.html",title=search,result=result,keyword=keyword,num=num)


from whoosh.index import create_in
from whoosh.fields import *
import os.path
import os
def search(keyword):
     schema = Schema(id = ID(stored=True), submitter = TEXT(stored=True),
                     authors = TEXT(stored=True), title = TEXT(stored=True),
                     comments = TEXT(stored=True), journal_ref=TEXT(stored=True),
                     doi=ID(stored=True),report_no=TEXT(stored=True),
                     categories= TEXT(stored=True),license= TEXT(stored=True),
                     abstract= TEXT(stored=True),versions=TEXT(stored=True),
                     update_date=TEXT(stored=True), authors_parsed= TEXT(stored=True))

     if not os.path.exists("index"):
         os.mkdir("index")
     ix = create_in("index", schema)
     writer = ix.writer()
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
         results = searcher.search(q,limit=None)
         list = []
         print(len(results))
         for r in results:
             list.append(dict(r))
         return len(list),list



if __name__ == '__main__':
     app.run()


