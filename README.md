# BB-SAR
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Python](https://img.shields.io/badge/License-GNU_GPL_v3.0-red)

**BB-SAR** is a web application designed for analyzing structure-activity relationships (SAR) at the building block (BB) level. It facilitates data-driven decision-making in medicinal chemistry projects by focusing on a defined **chemical series**.
![bb-sar_toc](https://github.com/user-attachments/assets/5ea529d9-af3b-4741-89b9-56e804bad3a7)

## Table of Contents

- [Features](#features)
- [License](#license)
- [Installation](#installation)
- [Utilisation](#utilisation)
  
## Features
- :mag: Analyzes biological/physicochemical properties from the BB perspective.
- :bar_chart: Simplifies the data complexity and helps identify trends between molecular features and properties.
- :sparkles: Provides an intuitive interface for medicinal chemists.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

## Installation

### Prerequisites
- Python 3.10+
- Conda package manager
- Git

### Linux

#### 1. Clone the repository
```bash
cd /path/to/your/directory
git clone https://github.com/chevillardf/BB-SAR.git
cd BB-SAR
```

#### 2. Create and activate the conda environment
```bash
conda env create -f data/py310.yml
conda activate py310
```

#### 3. Start the application
```bash
python manage.py runserver
```

#### 4. Access the web app
- Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Default Password: `yourPassword` (can be edited in `bb-sar/settings.py`)

### Windows
- Install Anaconda by following the instructions [here](https://docs.anaconda.com/anaconda/install/windows/).
- Start Anaconda PowerShell and apply the same logic as Linux installation.

## Utilisation
### Fragment the chemical series into BBs
- You can use the jupyter notebook of the Lactam series [here](https://github.com/chevillardf/BB-SAR/blob/master/data/format_DORA_Lactam_bbs.ipynb) as template to fragment your own chemical series.
- Format the columns headers so they fit the current Molecules and BBs Models.

### Upload your dataset to the web app
This part should be done by a proficient django developer, as adding your own chemical series will require to edit several files.
- bbs/models.py and molecules/models.py
- data/projects.json
- projects/management/commands/update_project_series.py
- utils/proj_settings

## Utilisation
