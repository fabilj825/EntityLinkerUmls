"""Convert entity annotation from spaCy v2 TRAIN_DATA format to spaCy v3
.spacy format."""
import srsly
import typer
import warnings
from pathlib import Path
import json

import spacy
from spacy.tokens import DocBin


def convert(lang: str, input_path: Path, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    fileData=(Path.cwd() / input_path )
    skip=0
    with fileData.open("r", encoding="utf8") as jsonfile:
        for line in jsonfile:
            example = json.loads(line)
            doc = nlp.make_doc(example[0])
            ents = []
            for start, end, label in example[1]["entities"]:
                span = doc.char_span(start, end, label=label)
                if span is None:
                    skip=skip+1
                    #msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(example[0])}\n"
                    #warnings.warn(msg)
                else:
                    ents.append(span)
            
            doc.ents = ents
            db.add(doc)
    print(skip)
    db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(convert)
