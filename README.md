# BeamDashboardX
This project generates a Beam DashBoard for Photon (X-ray) plans in a web browser as a read-only report with advanced visualizations.  It uses PyESAPI with Plotly running in streamlit via the default web browser (tested with Chrome and Edge).  This project is available as a compiled release (courtesy of PyInstaller and GitHub Actions) to be downloaded from the [releases](https://github.com/Varian-MedicalAffairsAppliedSolutions/MAAS-BeamDashboardX/releases) section and then the .zip file is to be extracted into the "System Scripts" directory on your Eclipse system (no Python environment needs to be installed there).  The project aims to bring modern interactive plotting tools to the Eclipse platform leveraging PyESAPI and Streamlit to build a bridge between the Eclipse data model and Plotly (or any other python plotting library of your choice).

## Example report (images are dynamic with mouseover, clickable and interactive)

![image](https://github.com/user-attachments/assets/ef94e4c5-962c-40e1-a295-f6d791c1ae5d)
![image](https://github.com/user-attachments/assets/54151595-b8e0-49d9-aa97-29a72b3aa27c)
![image](https://github.com/user-attachments/assets/2948bd46-c8cf-4ac0-9784-b65bf21c997a)
![image](https://github.com/user-attachments/assets/6cc78475-0c5a-49b9-ae83-36396ac12001)
![image](https://github.com/user-attachments/assets/46236c04-6bd4-45e8-9337-b70b76ec9973)

## Installation Quickstart Guide 
Afte downloading the .zip file from the release and moving it to where Eclipse can acccess, right click select "properties" and unblock (if blocked)<br>
![unblockdownloadedzip](https://github.com/user-attachments/assets/568df1ac-f3bb-479f-b82c-99033203c6e0)

Extract contents from the downloaded release .zip into the Systems Scripts directory (2 files and streamlit_runner directory are created)
![image](https://github.com/user-attachments/assets/6980ee6e-1225-4975-b753-017f57e0de3c)

Launch BeamDashboardX.cs from the system scripts directory
![image](https://github.com/user-attachments/assets/2a34de6f-a24f-4524-bbba-10c47e68e18e)

Streamlit runner console will first appear (leave this open)
![image](https://github.com/user-attachments/assets/0372c2c5-6fa6-46ef-848d-64005946bc6a)

Then the streamlit runner will launch the system default browser and build + display the BeamDashboardX interactive report <br>
-close browser window and streamlit runner console when finished

## Known Issues
* Streamlit is multi-threaded, and ESAPI only supports access from a single thread. Until a workaround is found, this means any access to PyESAPI should only happen once in an isolated function decorated with `@streamlit.cache_data`

## Development quick start
To run this code as a developer with a local python environment:
1. Create a virtual python environment within the project folder named `venv`:
  <br> `py.exe -m venv venv`
1. Activate python environment in `venv` folder:
  <br> `.\venv\Scripts\activate`
1. Update pip (obligatory):
  <br> `py.exe -m pip install --upgrade pip`
1. Install dependencies:
  <br> `pip install -r .\requirements.txt`
1. Install Jupyter Notebook and dependencies for PlotLy (latest version without multithreading):
  <br> `pip install jupyter chart_studio`
1. Update expiration date:
  <br> `py.exe .\make_expiration.py`
1. Launch BeamDashboardX.cs file from Eclipse Scripts menu.
1. To use Jupyter Notebook to prototype with Eclipse data in Python:
    1. `jupyter notebook`
    1. Be sure to have your default web browser set to Google Chrome or Edge.
    1. Open ScratchPad.ipynb for examples.
