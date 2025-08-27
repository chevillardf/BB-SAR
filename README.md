# BB-SAR
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Python](https://img.shields.io/badge/License-GNU_GPL_v3.0-red)
[![Docs](https://img.shields.io/badge/docs-User%20Manual-brightgreen)](MANUAL.md)
[![Demo](https://img.shields.io/badge/demo-online-brightgreen)](https://bb-sar.onrender.com/)


**BB-SAR** is a web application designed for analyzing structure-activity relationships (SAR) at the building block (BB) level. It facilitates data-driven decision-making in medicinal chemistry projects by focusing on a defined **chemical series**.

For a detailed explanation of the BB-SAR method and its applications in medicinal chemistry, please refer to the [article](https://pubs.acs.org/doi/10.1021/acs.jcim.4c02121)

The minimal webapp demo can be accessed [on render](https://bb-sar.onrender.com)

![bb-sar_toc](https://github.com/user-attachments/assets/5ea529d9-af3b-4741-89b9-56e804bad3a7)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [License](#license)
  
## Features
- :mag: Analyzes biological/physicochemical properties from the BB perspective.
- :bar_chart: Simplifies the data complexity and helps identify trends between molecular features and properties.
- :sparkles: Provides an intuitive interface for medicinal chemists.

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
conda env create -f data/py311.yml
conda activate py311
```

#### 3. Start the application
```bash
python manage.py runserver
```

#### 4. Access the web app
- Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Windows
- Install Anaconda by following the instructions [here](https://docs.anaconda.com/anaconda/install/windows/).
- Start Anaconda PowerShell and apply the same logic as Linux installation.

## Utilisation
For detailed usage instructions, see the [User Manual](./MANUAL.md). 

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.