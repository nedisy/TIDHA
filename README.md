# TIDHA
**Time Domain Hydrodynamic Analysis**

See the [documentation](https://nedisy.github.io/TIDHA/).

## Background
This project is created mainly to make a python code for hydrodynamic analysis. Most codes I found that works with hydrodynamic analysis use Fortran which I don't understand.

## Components
Curretly this only contain first order time series solver that use `scipy.integrate.solve_ivp`. The acceleration is formulated explicitly following [Vessel theory: Impulse response and convolution](https://www.orcina.com/webhelp/OrcaFlex/Content/html/Vesseltheory,Impulseresponseandconvolution.htm). The excitation force also calculated independently from the vessel movement at the moment. Pile force is one of the special force in this project. It is defined by the effect of individual pile reaction due to pile movement to the rigid body as a whole.

## Usage
To use this project at the current state, follows steps below to run the example file:
1. Install python, version 3.11. Check if your system already have python installed by opening terminal/command prompt and run `python`. The terminal will give your python version or error if it haven't been installed yet.
2. Open terminal in the current directory. Windows users can open terminal in the current directory by opening context menu with shift + right click in the current directory windows explorer.
3. Create virtual environment by running belows command on the terminal: `python -m venv .`. The command should work for any python version above 3.3.
4. Activate the environment in the terminal by running: `Scripts\activate`.
5. Install libraries for the virtual environment by running following command: `pip install -r requirements.txt`
6. Run the `run.bat` file by double clicking for windows or convert this to sh file for linux user. 

The script will run the python script in the `examples\dummy_pontoon\run.py`. You can copy the content of `dummy_pontoon` folder to new `cases\your_analysis_case` folder as the template and modify it. Note that you have to provide `your_analysis_case\Wamit_file` that contains solved BEM case accroding to your vessel geometry. You can use free hydrodyamic BEM solver like HAMS or NEMOH and convert your data to Wamit format using BEMRosetta or BEMIO. After moving your analysis folders you have to put the folder path into the run.bat in order for it to be able to run. You can run the cases in batch by including them in the bat file. Your bat file will looks like this:

```
Scripts\python.exe cases\pontoon0deg\run.py
Scripts\python.exe cases\pontoon45deg\run.py
Scripts\python.exe cases\pontoon90deg\run.py
pause
```

## No Virtual Environment
You can run the code without virtual environment as long as all dependencies are instaled in your current system. It is not recomennded as it can potentially cause conflic of dependencies.
