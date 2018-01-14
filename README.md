# StreamoutProcessor

## General Description
Takes raw sdhcal binaries (slcio files with collection of `RU_XDAQ`) and transform them to Raw SDHCAL hits (slcio files with collection of `DHCALRawHits`)
It's a simple port from Laurent Mirabito's Streamout code to a Marlin processor

> /!\ When running on lxplus you probably want to setup a python virtualenv to ensure all library/python version are present/uptodate
You need python>=2.7.10 and pyyaml library, see section [Setting a proper environment](#Setting-a-proper-environment)

## Running the processor
Once you are happy with the configuration file (see section [General configuration](#General-configuration)):
```bash
    python pyMarlin.py config_streamout # Note the missing .py at the end of the config file
```
## General configuration

## Grid submission

If you want to send job on the grid, add ganga to your pythonPath :

```bash
    export PYTHONPATH=$PYTHONPATH:/cvmfs/ganga.cern.ch/Ganga/install/LATEST/python
```

Modify the config file you want to use (default is config_streamout.py) and make sure `runOnGrid` is set to `True`.

```
```
## Setting a proper environment
Source your environment (source init_ilcsoft.sh for example)
```bash
    virtualenv -p `which python` /Path/To/Your/Project/venv # Ensure you use the correct Python version not the ols system one(2.6.6)
    source /Path/To/Your/Project/venv/bin/activate
    # Update python installation
    pip install --upgrade pip
    pip install --upgrade setuptools
    pip install pyyaml
```
