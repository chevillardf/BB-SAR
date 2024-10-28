# BB-SAR

**BB-SAR** is a web application designed for analyzing structure-activity relationships (SAR) at the building block (BB) level. It facilitates data-driven decision-making in medicinal chemistry projects by focusing on a defined chemical series.

## Features
- Analyzes molecular properties using building blocks (BBs)
- Simplifies the data complexity and helps identify trends between molecular features and properties
- Provides an intuitive interface for medicinal chemists

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

## Upload your dataset
- Start Anaconda PowerShell and apply the same logic as Linux installation.
