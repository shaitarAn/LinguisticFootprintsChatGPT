# generate_bash_config.py

from config import GERMAN_CORPORA, ENGLISH_CORPORA

# Open the bash config file for writing
with open('corpora_config.sh', 'w') as f:
    # Write the German corpora array
    f.write('GERMAN_CORPORA=(' + ' '.join(f'"{corpus}"' for corpus in GERMAN_CORPORA) + ')\n')
    
    # Write the English corpora array
    f.write('ENGLISH_CORPORA=(' + ' '.join(f'"{corpus}"' for corpus in ENGLISH_CORPORA) + ')\n')
