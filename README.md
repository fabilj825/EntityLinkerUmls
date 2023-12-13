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
