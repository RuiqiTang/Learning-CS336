import token


def text2idx(text):
    tokens=text.encode("utf-8")
    tokens=list(map(int,tokens))
    return tokens

class stat_dict:
    def __init__(self,ids):
        self.ids=ids
        self.counts={}
        for pair in zip(ids,ids[1:]):
            self.counts[pair]=self.counts.get(pair,0)+1
    
    def return_sorted_dict(self):
        return sorted(((v,k) for k,v in self.counts.items()),reverse=True)

    def return_top_pair(self):
        top_pair=max(self.counts,key=self.counts.get)
        return top_pair

def merge(ids,pair,idx):
    '''Use symbolic `idx` to replace pair'''
    newidx=[]
    i=0
    while i<len(ids):
        if i<len(ids)-1 and ids[i]==pair[0] and ids[i+1]==pair[1]:
            newidx.append(idx)
            i+=2
        else:
            newidx.append(ids[i])
            i+=1
    return newidx

def decode(ids,vocab):
    # given idx -> Python string
    tokens=b"".join(vocab[idx] for idx in ids)
    text=tokens.decode("utf-8",errors="replace")
    return text

def get_stats(tokens):
    return

merges=dict()

def encode(text):
    tokens=list(text.encoding('utf-8'))
    while len(tokens)>2:     #Merge Bits
        stats=get_stats(tokens)
        pair=min(stats,key=lambda p:merges.get(p,fload("inf"))) #TODO: Conduct merges
        if pair not in merges:
            break   # nothing else can be merged
        idx=merges[pair]
        tokens=merge(tokens,pair,idx)
    return tokens
