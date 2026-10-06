## The essence

**How to install**
```bash
git clone https://github.com/Ksukskss/Aboba.git
```
Create a data directory:
```bash
cd Aboba && mkdir data && cd data
```
Download the SCARDEC database:
```bash
curl -C - -O http://scardec.projects.sismo.ipgp.fr/sourcefunction_archive_all.tar.bz2 && tar -xjf sourcefunction_archive_all.tar.bz2 && mv ALL_MOY_and_OPTI_2026_MAJ_till_31122024/ events/ && cd ../
```
Add data from the ISC:
```bash
python workflow/check.py #This creates a report file listing folders that lack ISC data. This may be useful for later verification. The next script uses this specific file to function.

python workflow/search_erorr_correction.py #This downloads the files from the ISC.
```



**Goal:** prepare a substrate for meaningful machine learning (ML) application in seismology - create a polished dataset of marco-seismicity with key earthquake parameters, source time functions (STF) and most importantly waveforms.

*Presentation*
https://docs.google.com/presentation/d/1Wcuf53iJRAo76x6a3W_sBSHDNKlveCVsDQSw0f55qwE/edit?slide=id.g3d20a583b4b_0_1#slide=id.g3d20a583b4b_0_1

*Core sources*: 
+ SCARDEC source time function database
   + http://scardec.projects.sismo.ipgp.fr/
+ ISC unified catalog macro-seismicity
   + https://www.isc.ac.uk/iscbulletin/search/catalogue/
   + Option to filter and download in CSV / QuakeML formats
+ FDSN metadata of various seimological networks
   + https://fdsn.org/networks/
+ ObsPy clients for downloading waveform data
   + https://docs.obspy.org/packages/autogen/obspy.clients.fdsn.client.Client.get_waveforms.html




## Glossary
+ [Source Time Function (STF)](analysis/definition/STF.md)


### HOW-TOs
+ Making a fresh setup
   ```bash
   # 0. Making a project folder to shack and hack inside it
   mkdir ~/project/
   cd ~/project
   # 1. Initializing UV package manager
   uv init
   # 2. Making virtual environment with Python 3.12 locally as .venv folder
   uv venv --clear --python 3.12 
   # 3. Activating to use it with command-line interface
   source .venv/bin/activate
   # 4. Adding necessary libraries
   uv add polars datasets scikit-learn torch obspy cartopy jupyter
   ```

### Discarded ideas (shitty dataset)
- https://huggingface.co/datasets/mnemoraorg/seismic-tsunami-event-linkage - датасет
- https://www.kaggle.com/datasets/ahmeduzaki/global-earthquake-tsunami-risk-assessment-dataset/code - куча тетрадок для этого же датасета на каггле (есть ли там полезные?)

### ML-courses stash
- https://developers.google.com/machine-learning/crash-course - структурированный курс от гугл по ml
- https://education.yandex.ru/handbook/ml - хэндбук от яндекс (база ml)
