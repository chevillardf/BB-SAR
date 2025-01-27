# User Manual  

## Data preparation
### Fragment the chemical series into BBs
- You can use the jupyter notebook of the Lactam series [here](https://github.com/chevillardf/BB-SAR/blob/master/data/format_DORA_Lactam_bbs.ipynb) as template to fragment your own chemical series.
- Format the columns headers so they fit the current Molecules and BBs Models.

## Uploading data to the web application
### Upload your dataset to the web app
This part should be done by a proficient django developer, as adding your own chemical series will require to edit several files.
- bbs/models.py and molecules/models.py
- data/projects.json
- projects/management/commands/update_project_series.py
- utils/proj_settings

 ## Web application functions
