# generate_bash_config.py

import yaml
import sys

yaml_file = sys.argv[1]

# Load the config file
with open(yaml_file, 'r') as f:
    config = yaml.safe_load(f)

# Open the bash config file for writing
with open('corpora_config.sh', 'w') as f:
    if 'german' in config['corpora']:
        GERMAN_CORPORA = config['corpora']['german']
        # Write the German corpora array
        f.write('GERMAN_CORPORA=(' + ' '.join(f'"{corpus}"' for corpus in GERMAN_CORPORA) + ')\n')
    if 'english' in config['corpora']:
        ENGLISH_CORPORA = config['corpora']['english']   
        # Write the English corpora array
        f.write('ENGLISH_CORPORA=(' + ' '.join(f'"{corpus}"' for corpus in ENGLISH_CORPORA) + ')\n')
