from io import BytesIO
import pandas as pd

def dataframe_a_excel(df: pd.DataFrame) -> bytes:
    bio=BytesIO()
    with pd.ExcelWriter(bio,engine="openpyxl") as writer:
        df.to_excel(writer,index=False,sheet_name="Experimentos")
    return bio.getvalue()
