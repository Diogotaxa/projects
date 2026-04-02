import pandas as pd


class DataTransformer:
    def to_dataframe(self, records: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(records)