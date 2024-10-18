# BB-SAR

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

## Installation

### Linux

#### Clone the repository
```
cd /wherever/your/programs/are/
git clone https://github.com/chevillardf/BB-SAR.git
cd BB-SAR
```

#### Create and activate the conda environment
```
conda env create -f data/py310.yml
conda activate py310
```

#### Start the application
```
python manage.py runserver
```

#### Access the webapp
- Open your web browser and go to http://127.0.0.1:8008/
- Password = yourPassword (can be edited in bb-sar/settings.y)

### Windows
- Install anaconda by following the instructions [here](https://docs.anaconda.com/anaconda/install/windows/)
- Start Anaconda power shell and apply the same logic as Linux installation
