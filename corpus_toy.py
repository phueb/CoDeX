from typing import List
from cached_property import cached_property
import random
from itertools import cycle


class ToyCorpus:
    """
    create a collection of documents,
     each consisting of a string where artificial nouns are followed by a non-noun (other).
    example document: "n1 o5 n34 o82 n93 o3 n45 o11".
    the documents are sorted because:
     1. the population from which nouns are sampled is gradually increased
     2. the probability that only a select population of non-nouns can occur after a noun is gradually decreased

     these two constraints result in an ordered collection of documents,
     where the conditional entropy of nouns given the probability distribution over non-nouns decreases,
     while the joint entropy of nouns and non-nouns increases.
    """

    def __init__(self,
                 num_docs: int = 32,
                 doc_size: int = 100_000,
                 num_types: int = 4096,
                 num_nouns: int = 512,
                 divisor: int = 2,  # the larger, the more constrained are non-nouns
                 min_nouns: int = 100,
                 doc_offset: int = 0,  # the larger, the faster the noun population reaches its maximum
                 fragmented_control: bool = False,  # split nouns in 2 categories
                 ) -> None:
        self.num_docs = num_docs
        self.doc_size = doc_size
        self.num_types = num_types
        self.num_nouns = num_nouns
        self.min_nouns = min_nouns
        self.doc_offset = doc_offset
        self.fragmented_control = fragmented_control

        self.nouns = [f'n{i:0>6}' for i in range(self.num_nouns)]
        self.others = [f'o{i:0>6}' for i in range(self.num_types - self.num_nouns)]

        # a smaller set of non-nouns (non-nouns are preferentially sampled from this population in early documents)
        self.limited_others = [o for o in self.others if float(o[1:]) % divisor == 0]

        # TODO test - some nouns occur with on set of others and others occur with another
        lo1 = [o for o in self.others if float(o[1:]) % 2 == 0]
        lo2 = [o for o in self.others if float(o[1:]) % 2 != 0]
        los = cycle([lo1, lo2])
        self.noun2limited_others = {noun: next(los) for noun in self.nouns}

        print('Initialized ToyCorpus with number of limited non-nouns:', len(self.limited_others))

    @cached_property
    def docs(self) -> List[str]:
        res = [self.doc(i) for i in range(self.num_docs)]
        return res

    def doc(self,
            doc_id,
            ) -> str:

        assert 0 <= self.doc_offset <= self.num_docs

        # gradually increase noun population across consecutive documents
        limit = self.num_nouns * ((doc_id + self.doc_offset) / self.num_docs)
        nouns = self.nouns[:int(max(self.min_nouns, limit + 1))]

        # probability of constraining population of non-nouns
        prob = doc_id / self.num_docs

        # sample
        res = ''
        for n in range(self.doc_size):
            # sample noun randomly
            noun = random.choice(nouns)

            # sample next-word from one of two population (this keeps overall type frequency the same)
            if self.fragmented_control and doc_id != 0:  # nouns fall into exactly 2 sub-categories
                other = random.choice(self.noun2limited_others[noun])
            # sample next-word - sometimes from a limited population
            elif random.random() < prob:
                other = random.choice(self.limited_others)
            # no strategic sampling
            else:
                other = random.choice(self.others)
            res += f'{noun} {other} '  # whitespace after each
        return res