# Version A: 
### Install and setup virtual env python
pip install virtualenv \
python<version> -m venv <virtual-environment-name> \
e.g: \
 mkdir projectA \
 cd projectA \
 python3.8 -m venv env \
source env/bin/activate \

### install requirements after source cmd
pip install -r requirements.txt

### unzip trained models
1. in biobert/named-entity-recognition/output/all -> our trained BIOBERT NER \
2. in NERdemo/output/ -> our trained NER for Medmentions \
3. in models -> our NEL with Scispacy Large \

### train on our scripts

NERdemo, wandBSweep should be run local with command line. See according README. They create NER models \
Run preprocessingUMLS.ipynb -> spacy_knowledge_base.ipynb -> medmentions_and_training.ipynb in that order to create KB and a model with scispacy NER and own EL. 

### run inference with our models

Run inference in different combinations with inference_all_models.ipynb.


