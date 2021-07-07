import pandas as pd  
import numpy as np

def start_pipeline(df):
    return df.copy()

def add_date(df, date):
    df['date_scraped'] = date
    return df

def clean_columns(df):
    cols = [x.strip() for x in list(df)]
    df.columns = cols
    
    return df

def filter_department(df, department=None):
    if department:
        df = df[df['department'].str.lower() == department]

    return df
    
def unique_name_key(df):
    """
        without any sort of "employee id" or key to lookup, the best we have is
        labeling people by first-m-last name. This works fine for just the GO, 
        however when used with all departments you run into some duplicates. 
    """
    df['uid'] = df['first'] + df['m'] + df['last']
    
    return df
    
def add_new_hires(df, clean_old=None):
    """
        last_quarter: all employees last quarter
        holdover:     a employee that started last quarter and is still on in recent quarter
        new:          a employee that started in the most recent quarter
    """
    if df.shape[0] < 1 and clean_old is not None: # quick fix to issue of lg office empty
        df.loc[-1, ['uid', 'difference', 'period']] = ['no employees', 0, 'recent quarter']

    if clean_old is None:
        df['period'] = 'last_quarter'
    else:
        holdover = [x for x in df['uid'].tolist() if x in clean_old['uid'].tolist()]
        new = [x for x in df['uid'].tolist() if x not in clean_old['uid'].tolist()]
        
        df.loc[df['uid'].isin(holdover), 'period'] = 'holdover'
        df.loc[df['uid'].isin(new), 'period'] = 'new'
        
    return df
    
def clean_column_names(df):
    cols = ['department', 'title', 'uid', '', 'termination']
    for col in cols:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace(r'^\s+$', np.nan, regex=True)
        df[col] = df[col].replace('', np.nan)
        
    return df
    
def remove_columns(df):
    remove = ['first', 'm', 'last']
    df = df.drop(columns=remove)
    
    remove = ['regular', 'overtime', 'other']
    df = df.drop(columns=remove)

    keep = [x for x in list(df) if x != '']
    return df[keep]

def order_columns(df):
    cols = [
        'uid',
        'title',
        'department',
        'total',
        'annual',
        'period',
        'fiscal_year',
        'date_scraped'
    ]
    
    if 'termination' in list(df):
        cols.insert(3, 'termination')
    
    return df[cols].sort_values(by='annual', ascending=False)
    

def clean_raw_pipeline(f, date, department=None, old_ids=None):
    df = pd.read_csv(f)

    return (df
        .pipe(start_pipeline)
        .pipe(add_date, date)
        .pipe(clean_columns)
        .pipe(unique_name_key)
        .pipe(clean_column_names)
        .pipe(filter_department, department)
        .pipe(add_new_hires, old_ids)
        .pipe(remove_columns)
        .pipe(order_columns)
    )

def fill_terminated(df):
    """
        For some reason a few people that were terminated last quarter were no longer listed
        as terminated. However their "total" pay hasn't changed so we fill the termination date
        with last quarters date.
    """
    df['termination'] = df.groupby(['uid'])['termination'].fillna(method='ffill')
    
    return df

def raise_table(df, department):
    current = df[df['period'] != 'last_quarter'].copy()
    prior = df[df['period'] == 'last_quarter'].copy()

    if 'no employees' in current['uid'].tolist():
        return df

    df_raises = df[df['termination'].isnull()]
    df_raises = df_raises.groupby(['uid', 'date_scraped'])['annual'].sum()
    diff = df_raises.groupby(['uid']).diff()
    pct_diff = df_raises.groupby(['uid']).pct_change()

    raises = pd.concat([df_raises, diff, pct_diff], axis=1)
    raises.columns = ['current_annual', 'difference', '%_diff']

    # get table of holdovers pay change
    raises = (raises
        .groupby('uid')
        .filter(lambda x: len(x) == 2)
        .dropna(axis=0, how='any')
        .reset_index()
        .sort_values(by='difference', ascending=False)
    )

    # join prior info and meta columns
    raises_table = raises.drop(columns=['date_scraped'])
    raises_table = raises_table.merge(current[['uid', 'title']], on='uid')

    renamer = {"annual": "prior_quarter", "title": "prior_title"}
    prior = prior[['uid', 'annual', 'title']].rename(columns=renamer)
    raises_table = raises_table.merge(prior, on='uid')

    col_order = ['uid', 'prior_title', 'title', 'prior_quarter', 'current_annual', 'difference', '%_diff']
    rt = raises_table[col_order].copy()

    rt.loc[rt['difference'] > 0, 'change'] = 'increase'
    rt.loc[rt['difference'] == 0, 'change'] = 'no_change'
    rt.loc[rt['difference'] < 0, 'change'] = 'decrease'

    rt = rt[rt['change'] != 'no_change']
    rt.to_csv(f'./data/clean/{department}/pay_changes.csv', index=False)

    return df

def summary_changes(df, department):
    new_hire = df[(df['period']=='new')].copy()
    new_hire = new_hire[['uid', 'title', 'annual', 'period', 'date_scraped']]

    termination = df[(df['period']!='last_quarter') & (df['termination'].notnull())].copy()
    termination = termination[['uid', 'title', 'annual', 'termination', 'date_scraped']]

    df1 = df[(df['period']=='last_quarter') & (df['termination'].isnull())]
    summary1 = {
        "total_employees": df1.shape[0],
        "highest_paid": df1['annual'].max(),
        "total_annual": df1['annual'].sum(),
        "median_annual": df1['annual'].median(),
        "missing_title": df1['title'].isnull().sum()
    }

    pay = pd.read_csv(f'./data/clean/{department}/pay_changes.csv')
    df2 = df[(df['period']!='last_quarter') & (df['termination'].isnull())]
    summary2 = {
        "total_employees": df2.shape[0],
        "highest_paid": df2['annual'].max(),
        "total_annual": df2['annual'].sum(),
        "median_annual": df2['annual'].median(),
        "missing_title": df2['title'].isnull().sum(),
        "terminations": termination.shape[0],
        "new_hires": new_hire.shape[0],
        "pay_increase": pay[pay['change']=='increase'].shape[0],
        "pay_decrease": pay[pay['change']=='decrease'].shape[0]
    }

    stats_df = pd.DataFrame({"prior_quarter": summary1, "current_quarter": summary2}).T
    stats_df.to_csv(f'./data/clean/{department}/summary.csv')

    print("\n" + f"{department} > " + ("-" * (145 - len(department))))
    print(stats_df.fillna(''))

    return df

def data_pipeline(files, department=None):
    if len(list(files)) > 2:
        print('[ERROR] currently only works for 2 most recent quarters.')
        return

    df1 = clean_raw_pipeline(files[0], files[0].stem[-10:], department)
    df2 = clean_raw_pipeline(files[1], files[1].stem[-10:], department, df1)
    df = pd.concat([df1, df2])

    return (df
        .pipe(start_pipeline)
        .reset_index(drop=True)
        .pipe(fill_terminated)
        .pipe(raise_table, department)
        .pipe(summary_changes, department)
    )