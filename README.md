# Version A: 
### Install and setup virtual env python
pip install virtualenv\
python<version> -m venv <virtual-environment-name>\
e.g:\
 mkdir projectA\
 cd projectA\
 python3.8 -m venv env\
source env/bin/activate\

### install requirements after source cmd
pip install -r requirements.txt\

NERdemo, wandBSweep should be run local with command line. See according README. \
medmentions_and_training.ipynb, preprocessingUMLS.ipynb and spacy_knowledge_base.ipynb can be run either local or in Colab. But one must change the Paths accordingly and ommit the command for including google drive. For the notebooks it is recommended to use Colab. See Version B.

# Version B: 
Copy MedMentions-master, dataframes, knowledgebase and the three notebooks in a folder in the base directory of Google drive named UMLS.
Set paths to the files and the notebook can be run. The recommended order is:
preprocessingUMLS.ipynb
spacy_knowledge_base.ipynb
medmentions_and_training.ipynb

