import sys
import json
import argparse
from pathlib import Path
from src.pipeline import data_pipeline

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--departments', dest='departments', required=False, nargs='+', default=[],
                    help='choose departments: [bhddh, ccri, uri, dot, doh, corrections]')
parser.add_argument('-a', '--all', dest='all', required=False, action="store_true",
                    help='collects all departments')

args = parser.parse_args()

with open('./data/files/departments.json', 'r') as f:
    depart_lookup = json.load(f)

if args.all:
    args.departments = list(depart_lookup.keys())
    print(args.departments)


if __name__ == "__main__":
    files = list(Path('./data/raw/').glob('*.csv'))

    if not len(sys.argv) > 1:
        print('ERROR: No arguments passed')
        print('type -a (--all) for a breakdown of all departments')
        print('type -d (--departments) followed by the abbreviation [bhddh, ccri, uri, dot]')
        print('visit https://github.com/SmirkyGraphs/ri-campaign-finance for a full list of departments')
    
    for department in args.departments:
        if department not in depart_lookup.keys():
            print(f'[ERROR] {department} is not an acceptable department, skipping')
            continue
        else:
            dep = depart_lookup[department]

        Path(f'./data/clean/{dep}/').mkdir(parents=True, exist_ok=True)
        df = data_pipeline(files, dep)
        df.to_csv(f'./data/clean/{dep}/payroll_clean.csv', index=False)
        df[df['termination'].notnull()].to_csv(f'./data/clean/{dep}/terminations.csv', index=False)
        df[df['period']=='new'].to_csv(f'./data/clean/{dep}/new_hires.csv', index=False)