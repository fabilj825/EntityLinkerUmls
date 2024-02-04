├── ...
├── test                    # Test files (alternatively `spec` or `tests`)
│   ├── benchmarks          # Load and stress tests
│   ├── integration         # End-to-end, integration tests (alternatively `e2e`)
│   └── unit                # Unit tests
└── ...

# EntityLinkerUmls
unzip 2022AB-full/2022ab-1-meta.nlm \
unzip 2022AB-full/2022ab-otherks.nlm \
gunzip -c 2022AB/META/MRCONSO.RRF.*.gz > MRCONSO.RRF \
gunzip 2022AB/META/MRDEF.RRF.gz \

# Install and setup virtual env python
pip install virtualenv\
python<version> -m venv <virtual-environment-name>\
e.g:\
 mkdir projectA\
 cd projectA\
 python3.8 -m venv env\
source env/bin/activate\

# install requirements after source cmd
pip install -r requirements.txt\

# start jupyter
jupyter notebook

# run nb
preprocessing for creating dataframes from UMLS file\
spacy_knowledge_base for kb creation\
medmentions_and_training for dataset creation and training\

# current current status
Pipeline runs and training can be done. But loss not decreasing. Further inspection of preprocessing and KB are needed

