import pandas as pd
from pathlib import Path

class DataAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.path = Path(cfg['data_path'])

    def summarize(self, filters):
        df = pd.read_csv(self.path)
        # parse dates (dd-mm-yyyy or ISO)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        # handle NaNs
        df['spend'] = df['spend'].fillna(1)
        df['purchases'] = df['purchases'].fillna(0)
        # normalize campaign names (strip doublespaces)
        df['campaign_name'] = df['campaign_name'].astype(str).str.replace('_',' ').str.replace('  ',' ').str.strip()
        agg = df.groupby('campaign_name').agg({
            'spend':'sum','impressions':'sum','clicks':'sum','purchases':'sum','revenue':'sum'
        }).reset_index()
        agg['ctr'] = agg['clicks'] / agg['impressions'].replace(0,1)
        agg['roas'] = agg['revenue'] / agg['spend'].replace(0,1)
        daily = df.groupby('date').agg({'spend':'sum','revenue':'sum','impressions':'sum','clicks':'sum'}).reset_index()
        daily['roas'] = daily['revenue'] / daily['spend'].replace(0,1)
        return {'by_campaign': agg.to_dict(orient='records'),
                'daily': daily.to_dict(orient='records'),
                'raw_head': df.head(12).to_dict(orient='records')}