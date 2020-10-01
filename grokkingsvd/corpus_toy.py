from typing import List
from cached_property import cached_property
import random


class ToyCorpus:
    """
    create a collection of documents,
     each consisting of a string where artificial nouns are followed by a non-noun (other).
    example document: "n1 o5 n34 o82 n93 o3 n45 o11".
    the documents are sorted because:
     1. the population from which nouns are sampled is gradually increased
     2. the population from which non-nouns are sampled is gradually increased

     these two constraints result in an ordered collection of documents,
     where the conditional entropy of nouns given the probability distribution over non-nouns decreases,
     while the joint entropy of nouns and non-nouns increases.
    """

    def __init__(self,
                 num_docs: int = 32,
                 doc_size: int = 50_000,
                 num_types: int = 4096,
                 doc_offset: int = 0,  # the larger, the faster the noun population reaches its maximum
                 increase_noun_types: bool = True,  # whether to gradually introduce new nouns
                 increase_other_types: bool = False,  # whether to gradually introduce new others
                 ) -> None:
        self.num_docs = num_docs
        self.doc_size = doc_size
        self.num_types = num_types
        self.doc_offset = doc_offset
        self.increase_noun_types = increase_noun_types
        self.increase_other_types = increase_other_types

        self.num_nouns = num_types // 2
        self.num_others = num_types // 2
        self.min_nouns = self.num_nouns // 2
        self.min_others = self.num_others // 2
        assert self.num_nouns + self.num_others == self.num_types

        self.nouns = [f'n{i:0>6}' for i in range(self.num_nouns)]
        self.others = [f'o{i:0>6}' for i in range(self.num_others)]

    @cached_property
    def docs(self) -> List[str]:
        res = [self.doc(i) for i in range(self.num_docs)]
        return res

    def doc(self,
            doc_id,
            ) -> str:

        assert 0 <= self.doc_offset <= self.num_docs

        # gradually increase noun population across consecutive documents from which to sample
        if self.increase_noun_types:
            limit = self.num_nouns * ((doc_id + self.doc_offset) / self.num_docs)
            nouns = self.nouns[:int(max(self.min_nouns, limit + 1))]
        else:
            nouns = self.nouns

        # gradually increase non-noun/other population across consecutive documents from which to sample
        if self.increase_other_types:
            limit = self.num_others * ((doc_id + self.doc_offset) / self.num_docs)
            others = self.others[:int(max(self.min_others, limit + 1))]
        else:
            others = self.others

        # sample
        res = ''
        for n in range(self.doc_size):
            noun = random.choice(nouns)
            other = random.choice(others)
            res += f'{noun} {other} '  # whitespace after each

        return res
