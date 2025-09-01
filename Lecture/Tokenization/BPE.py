'''
    Ref:
    - https://zhuanlan.zhihu.com/p/1925690164627374951
'''
from heapq import merge
import os 

from collections import Counter
from pathlib import Path 
import token
from typing import Dict,List,Tuple

Token=int 
Subword=bytes
Pair=[int,int]

class BPETokenizer:
    def __init__(
        self,
        vocab:Dict[int,Subword]|None=None,
        merges:List[Pair]|None=None,
        special_tokens:List[str]|None=None
    ) -> None:
        self.vocab=Dict[int,Subword]=vocab or {}
        self.merges:List[Pair]=merges or {}

        # Process:special tokens
        self.special_tokens:List[str]=special_tokens or []
        self.special_token_to_id:Dict[str,Token]={}
        self.id_to_special_token:Dict[Token,str]={}
        for token in self.special_tokens:   # Ensure special tokens has been inserted into vocab
            self._add_special_token(token)

        # Reverse dict
        self._inv_vocab:Dict[Subword,int]={b:i for i,b in self.vocab.items()}
    
    def encode(
        self,
        string:str
    )->List[Token]:
        '''
            String -> Token id
        '''
        # Special cases
        if string in self.special_token_to_id:
            return [self.special_token_to_id[string]]
        
        # 1. Split into bytes
        indices=[self._inv_vocab[bytes(b)] for b in string.encode('utf-8')]
        # 2. Merge pairs
        for pair in self.merges:
            indices=self.merge(indices,pair,self.pair_to_id(pair))
        return indices
    
    def decode(
        self,
        indices:List[Token]
    )->str:
        '''
            Token id -> String
        '''
        if not indices:
            return ""
        parts:List[str]=[]
        for token_id in indices:
            if token_id in self.id_to_special_token:    # 1. Process Special Tokens
                parts.append(self.id_to_special_token[token_id])
            else:   # 2. Change token_id to str
                parts.append(self.vocab[token_id].decode('utf-8',errors='replace'))
        return "".join(parts)
    
    def train_from_files(
        self,
        file_path:str|Path,
        target_vocab_size:int=30000
    )->None:
        # 1. Read text
        text=Path(file_path).read_text(encoding='utf-8')

        # 2. Ensure byte-level base vocab exists
        if not self.vocab:
            for b in sorted(set(text.encode('utf-8'))):
                self.add_token(bytes([b]))
        return
    
    def add_token(self,subword:Subword)->Token:
        '''
            Add subword to vocab
            return token_id
        '''
        if subword in self._inv_vocab:
            return self._inv_vocab[subword]
        idx=len(self.vocab)
        self.vocab[idx]=subword
        self._inv_vocab[subword]=idx
        return idx

    @staticmethod
    def merge(
        indices:List[Token],
        pair:Pair,
        new_index:Token
    )->List[Token]:
        new_indices:List[Token]=[]
        i=0
        while i<len(indices):
            if i+1<len(indices) and indices[i]==pair[0] and indices[i+1] == pair[1]:
                new_indices.append(new_index)
                i+=2
            else:
                new_indices.append(indices[i])
                i+=1
        return new_indices
        
