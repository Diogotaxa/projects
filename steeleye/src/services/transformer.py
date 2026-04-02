import pandas as pd


class DataTransformer:
    def to_dataframe(self, records: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(records)
        
        # Count lowercase 'a' in the fullname
        df['a_count'] = df['FinInstrmGnlAttrbts.FullNm'].fillna('').str.count('a')
        
        # Add Yes or No flag
        df['contains_a'] = df['a_count'].apply(lambda x: 'YES' if x > 0 else 'NO')
        
        return df