# simulation-fourier-reconstruction

## Getting started (with Binder)

Click on the Binder badge:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/shimming-toolbox/simulation-fourier-reconstruction/gc/jupyter-notebook)

Wait for Binder to finish building the environment (can take 5-10 minutes), then click on the Jupyter notebook (`Fourier-reconstruction_in_MRI.ipynb`).

**Warning:** After 10 minutes of inactivity, binder will stop working and you will have to launch it again.

## Getting started (on local station)

#### 1) You will need to [install miniconda](https://docs.conda.io/en/latest/miniconda.html) in order to set-up your python environment.

#### 2) Clone this GitHub repository on your computer:
```bash
git clone hhttps://github.com/shimming-toolbox/simulation-fourier-reconstruction.git
cd simulation-fourier-reconstruction
```
- For Windows user, you might need to [install git](https://git-scm.com/downloads) prior to clone the repository.
- If git clone is not working, you can download the zipped version of the repository and unzip it locally on your computer.

#### 3) Once miniconda is installed and the repository is cloned, run the following commands in order to create your virtual environment and start the jupyter notebook:

Then, run the following to create a virtual environment and start the notebook:

```bash
conda env create -f environment.yml # Only do it once in order to create the environment (might take a few minutes)

# Start the jupyter notebooks:
conda activate env-fourier  # Do it everytime you wish to run the notebook
jupyter notebook  
```

- Make sure that your prompt is currently on the `simulation-fourier-reconstruction` folder when you call the `environment.yml` file.
- For Windows user, you might need to type these commands in `Anaconda Prompt` if `cmd` does not recognize `conda`.
