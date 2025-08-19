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
