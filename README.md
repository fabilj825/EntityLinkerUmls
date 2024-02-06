### clone project
git clone  https://github.com/fabilj825/EntityLinkerUmls
### Install and setup virtual env python
pip install virtualenv \
python<version> -m venv <virtual-environment-name> \
e.g: \
python3 -m venv env \
source env/bin/activate \

### install requirements after source cmd
cd EntityLinkerUmls \
pip install -r requirements.txt \
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_lg-0.5.3.tar.gz \
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_ner_bc5cdr_md-0.5.3.tar.gz \
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_scibert-0.5.3.tar.gz \
python -m ipykernel install --user --name=env
### unzip trained models
1. in biobert/named-entity-recognition/output/all -> our trained BIOBERT NER \
2. in NERdemo/output/ -> our trained NER for Medmentions \
3. in models -> our NEL with Scispacy Large \

After unzipping you can decide if you want to train based on our scripts, or use inference_all_models.ipynb to test the unzipped models on MedMentions.
### copy MRCONSO and MRDEF to umlsfiles
Due to licenses it is not allowed to provide these files. Please copy them into the umlsfiles folder for running reprocessingUMLS.ipynb 
### jupyter nb
start jupyter with: \
jupyter notebook

### run inference with our models

Run inference in different combinations with inference_all_models.ipynb. We included some trained models (see unzipping) to show the basic functionality. 

### train on our scripts
If you want to train from scratch, either use the three afterwards mentioned jupyter notebooks or train the NER models with the CLI interface of Spacy. Biobert should be run on GPU, so maybe just use the delivered checkpoint because it is time consuming. \
NERdemo, wandBSweep should be run local with command line. See according README. They create NER models \
Run preprocessingUMLS.ipynb -> spacy_knowledge_base.ipynb -> medmentions_and_training.ipynb in that order to create KB and a model with scispacy NER and own EL. THe EL can be used to create pipelines with the NER models trained with NERdemo, Biobert or wandBSweep




