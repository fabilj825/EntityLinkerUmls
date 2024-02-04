
from typing import Optional, NamedTuple, List, Iterator, Dict, Tuple
from typing import Optional, Callable, Iterable, Iterator
import spacy
from spacy.training import Example
import warnings

from spacy.training import Corpus, Example
from spacy.language import Language

import os



"""
Utilities for working with the local dataset cache.
"""

import os

from pathlib import Path
from typing import Optional



# @spacy.registry.readers("MyCorpus.v1")
# def create_docbin_reader(file: Path) -> Callable[["Language"], Iterable[Example]]:
#     return partial(read_files, file)


# def read_files(file: Path, nlp: "Language") -> Iterable[Example]:
#     # we run the full pipeline and not just nlp.make_doc to ensure we have entities and sentences
#     # which are needed during training of the entity linker
#     with nlp.select_pipes(disable="entity_linker"):
#         doc_bin = DocBin().from_disk(file)
#         docs = doc_bin.get_docs(nlp.vocab)
#         for doc in docs:
#             yield Example(nlp(doc.text), doc)
class MedMentionEntity(NamedTuple):
    start: int
    end: int
    mention_text: str
    mention_type: str
    umls_id: str


class MedMentionExample(NamedTuple):
    title: str
    abstract: str
    text: str
    pubmed_id: str
    entities: List[MedMentionEntity]


def med_mentions_example_iterator(filename: str) -> Iterator[MedMentionExample]:
    """
    Iterates over a Med Mentions file, yielding examples.
    """
    with open(filename, "r", encoding="utf-8") as med_mentions_file:
        lines = []
        for line in med_mentions_file:
            line = line.strip()
            if line:
                lines.append(line)
            else:
                yield process_example(lines)
                lines = []
        # Pick up stragglers
        if lines:
            yield process_example(lines)


def process_example(lines: List[str]) -> MedMentionExample:
    """
    Processes the text lines of a file corresponding to a single MedMention abstract,
    extracts the title, abstract, pubmed id and entities. The lines of the file should
    have the following format:
    PMID | t | Title text
    PMID | a | Abstract text
    PMID TAB StartIndex TAB EndIndex TAB MentionTextSegment TAB SemanticTypeID TAB EntityID
    ...
    """
    pubmed_id, _, title = [x.strip() for x in lines[0].split("|", maxsplit=2)]
    _, _, abstract = [x.strip() for x in lines[1].split("|", maxsplit=2)]

    entities = []
    for entity_line in lines[2:]:
        _, start, end, mention, mention_type, umls_id = entity_line.split("\t")
        mention_type = mention_type.split(",")[0]
        entities.append(
            MedMentionEntity(int(start), int(end), mention, mention_type, umls_id)
        )
    return MedMentionExample(
        title, abstract, title + " " + abstract, pubmed_id, entities
    )

def select_subset_of_overlapping_chain(
    chain: List[Tuple[int, int, str]]
) -> List[Tuple[int, int, str]]:
    """
    Select the subset of entities in an overlapping chain to return by greedily choosing the
    longest entity in the chain until there are no entities remaining
    """
    sorted_chain = sorted(chain, key=lambda x: x[1] - x[0], reverse=True)
    selections_from_chain: List[Tuple[int, int, str]] = []
    chain_index = 0
    # dump the current chain by greedily keeping the longest entity that doesn't overlap
    while chain_index < len(sorted_chain):
        entity = sorted_chain[chain_index]
        match_found = False
        for already_selected_entity in selections_from_chain:
            max_start = max(entity[0], already_selected_entity[0])
            min_end = min(entity[1], already_selected_entity[1])
            if len(range(max_start, min_end)) > 0:
                match_found = True
                break

        if not match_found:
            selections_from_chain.append(entity)

        chain_index += 1

    return selections_from_chain


def remove_overlapping_entities(
    sorted_spacy_format_entities: List[Tuple[int, int, str]]
) -> List[Tuple[int, int, str]]:
    """
    Removes overlapping entities from the entity set, by greedilytaking the longest
    entity from each overlapping chain. The input list of entities should be sorted
    and follow the spacy format.
    """
    spacy_format_entities_without_overlap = []
    current_overlapping_chain: List[Tuple[int, int, str]] = []
    current_overlapping_chain_start = 0
    current_overlapping_chain_end = 0
    for i, current_entity in enumerate(sorted_spacy_format_entities):
        current_entity = sorted_spacy_format_entities[i]
        current_entity_start = current_entity[0]
        current_entity_end = current_entity[1]

        if len(current_overlapping_chain) == 0:
            current_overlapping_chain.append(current_entity)
            current_overlapping_chain_start = current_entity_start
            current_overlapping_chain_end = current_entity_end
        else:
            min_end = min(current_entity_end, current_overlapping_chain_end)
            max_start = max(current_entity_start, current_overlapping_chain_start)
            if min_end - max_start > 0:
                current_overlapping_chain.append(current_entity)
                current_overlapping_chain_start = min(
                    current_entity_start, current_overlapping_chain_start
                )
                current_overlapping_chain_end = max(
                    current_entity_end, current_overlapping_chain_end
                )
            else:
                selections_from_chain = select_subset_of_overlapping_chain(
                    current_overlapping_chain
                )

                current_overlapping_chain = []
                spacy_format_entities_without_overlap.extend(selections_from_chain)
                current_overlapping_chain.append(current_entity)
                current_overlapping_chain_start = current_entity_start
                current_overlapping_chain_end = current_entity_end

    spacy_format_entities_without_overlap.extend(
        select_subset_of_overlapping_chain(current_overlapping_chain)
    )

    return sorted(spacy_format_entities_without_overlap, key=lambda x: x[0])

def read_full_med_mentions(
    directory_path: str,
    label_mapping: Optional[Dict[str, str]] = None,
    span_only: bool = False,
    spacy_format: bool = True,
    use_umls_ids: bool = True,
):

    expected_names = [
        "corpus_pubtator.txt",
        "corpus_pubtator_pmids_all.txt",
        "corpus_pubtator_pmids_dev.txt",
        "corpus_pubtator_pmids_test.txt",
        "corpus_pubtator_pmids_trng.txt",
    ]

    corpus = os.path.join(directory_path, expected_names[0])
    examples = med_mentions_example_iterator(corpus)

    train_ids = {
        x.strip()
        for x in open(os.path.join(directory_path, expected_names[4]))
    }
    dev_ids = {
        x.strip()
        for x in open(os.path.join(directory_path, expected_names[2]))
    }
    test_ids = {
        x.strip()
        for x in open(os.path.join(directory_path, expected_names[3]))
    }

    train_examples = []
    dev_examples = []
    test_examples = []
    #non_overlapping=[]
    for example in examples:
        spacy_format_entities = [
            (
                x.start,
                x.end,
                x.umls_id,
            )
            for x in example.entities
        ]
        spacy_format_entities = remove_overlapping_entities(
            sorted(spacy_format_entities, key=lambda x: x[0])
        )
        # spacy_format_entities=sorted(spacy_format_entities, key=lambda x: x[0])
        
        # for i,ent in enumerate(spacy_format_entities):
        #     start=ent[0]
        #     if i==0:
        #         old_end=ent[1]
        #         continue
        #     if start < old_end:
        #         print("overlap")
        #         print(start)
        #         print(old_end)
        #         print(ent[2])
        #         continue
        #     old_end=ent[1]
        #     non_overlapping.append(ent)
        # start=0
        # old_end=0

        spacy_example = (example.text, {"entities": spacy_format_entities})
        if example.pubmed_id in train_ids:
            train_examples.append(spacy_example if spacy_format else example)

        elif example.pubmed_id in dev_ids:
            dev_examples.append(spacy_example if spacy_format else example)

        elif example.pubmed_id in test_ids:
            test_examples.append(spacy_example if spacy_format else example)

    return train_examples, dev_examples, test_examples

@spacy.registry.readers("med_mentions_reader")
def med_mentions_reader(
    directory_path: str, split: str
) -> Callable[[Language], Iterator[Example]]:
    train, dev, test = read_full_med_mentions(
        directory_path, label_mapping=None, span_only=True, spacy_format=True
    )

    def corpus(nlp: Language) -> Iterator[Example]:
        if split == "train":
            original_examples = train
        elif split == "dev":
            original_examples = dev
        elif split == "test":
            original_examples = test
        else:
            raise Exception(f"Unexpected split {split}")

        for original_example in original_examples:
            doc = nlp.make_doc(original_example[0])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                spacy_example = Example.from_dict(doc, original_example[1])
            yield spacy_example

    return corpus


