## The essence
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


## Current focus
+ [ ] Design a function to match source time function and event parameters from the SCARDEC database with information from the ISC unified catalog
   + [X] Create a function to request event_ID from ISC based on the specified date interval
         + /workflow/isc_req_id.py — script takes the start time,the end time and displays relevant event_IDs. Works in the terminal.
   + [X] Create a function to save xmls from ISC based on the specified ID
         + /workflow/isc_req_xml.py — script uses isc_req_id.py to get IDs for a certain period, sends a request to ISC for each ID, and saves the files in .xml format
   + [ ] Create a function to parse and convert .xml files to .csv
   + [ ] Design a function that will summarize the previous functions for a specific event from SCARDEC catalog
    
### Progress journal (log?)
+ [ ] Get used to seismological notation
+ [ ] Get a good grasp on deconvolution (find the perfect GIF!)
   +  https://www.youtube.com/watch?v=KuXjwB4LzSA
+ [ ] Explore more information abouts SCARDEC steps
   + [x] Sort csv 
   + [x] [Plot](src/visualization.py) specific earthquake:
      ![2011 Mw=8.8 Tohoku](2011-03-11-05-46-24.NEAR-EAST-COAST-OF-HONSHU.Mw-9-0.png)
+ [x] Extract STF database and find the optimal format
   + CSV table with columns: ...
+ [x] Download STF database and figure out its structure (!2025-11-25)
   + `/ALL_MOY_and_OPTI_2025_MAJ_till_31122023/FCTs_yymmdd_hhmmss_locate/` contains moy(avarage), opt(optimal) files and .png image of the focal mechanism
+ [x] Read the core article: ***2016* - A new database of source time functions (STFs) extracted from the SCARDEC method** *by Martin Vallée & Vincent Douet* 
   + `analysis/exploration/2016.Vallee+Douet.STF-database.Els-PEPI`
   + [Summary](analysis/exploration/2016.Vallee+Douet.STF-database.Els-PEPI.md)
   + [Full](https://www.sciencedirect.com/science/article/abs/pii/S0031920116300735) - requires subscription (-> gitIgnored!)
+ [x] Setup the enviroment (!2025-11-23)

+ [ ] Watch some anime to get a grasp on the earthquake phenomena ^!^
   + [x] "The Wind Rises" (風立ちぬ - *Kaze Tachinu*) by Hayao Miyazaki (2013, Studio Ghibli)
   + [ ] "Suzume" (すずめの戸締まり - *Suzume no Tojimari*) by Makoto Shinkai (2022, 	
CoMix Wave Films)



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
