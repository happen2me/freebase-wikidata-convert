import pickle

from SPARQLWrapper import JSON, SPARQLWrapper
from tqdm import tqdm

sparql = SPARQLWrapper(
    "http://localhost:1234/api/endpoint/sparql"
)
sparql.setReturnFormat(JSON)

def queryFreebaseId(entity):
    sparql.setQuery(f"""
        SELECT DISTINCT ?fid WHERE {{
            <http://www.wikidata.org/entity/{entity}> <http://www.wikidata.org/prop/direct/P646> ?fid
        }}
        LIMIT 1
        """)
    try:
        ret = sparql.queryAndConvert()        
        r = ret["results"]["bindings"]
        if len(r) > 0:
            fid = r[0]["fid"]["value"]
            return fid
        return None
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    with open('id2entity.pkl', 'rb') as f:
        id2entity = pickle.load(f)
    
    fids = map(queryFreebaseId, tqdm(id2entity))
    fid2qid = {fid: qid for fid, qid in zip(fids, id2entity) if fid is not None}
    print("Found:", len(fid2qid))
    print(f"Not found: {len(id2entity) - len(fid2qid)} / {len(id2entity)}")
    
    with open('fid2qid.pkl', 'wb') as f:
        pickle.dump(fid2qid, f)
