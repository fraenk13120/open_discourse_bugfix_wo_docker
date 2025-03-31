# Python

The python service processes and creates the election periods 1-19 from the open-discourse data. To my knowledge, the Bundestag has changed their APIs, thats why the original setup does not function anymore. Here is a setup without the use of docker, the code relys on the open-discourse skripts, but edited. The Output are several .csv files. Added progressbar and some tools for troubleshooting.

## Please check:
- in the 01_processing/01_downloading_raw_data.py if the URLs for the .zip files are still working
- The MPs database is not yet working, there is work needed in the MP-Sections (primarly downloading the data)
- The paths in definitions/path_definitions.py
- sometimes in `sh setup.sh`  the virtual environment does not activate, if so do it manually (with the commands from the file)
- the requirements in requirements.txt are dependent on python3.11, if you use another version make sure the functionality is the same


## Folders

- The `data` folder contains all of the cached data
- The `logs` folder contains the logs which are generated in the `build.sh` script
- The `src` folder contains all of the python scripts. More infornmation on these can be found in the [README in src](./src/README.md)

## Commands

- To setup the python environment, please run `sh setup.sh`
- To build the open-discourse data, please run `sh build.sh`
- for initial setup run setup.py as well
- you can use the viewpkl.py file (in helper functions) to get insight which data is stored in the pickle-files
