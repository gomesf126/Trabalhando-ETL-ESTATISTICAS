from src.transform.features import criar_pipeline
from src.transform.features import CLEANING, ENGINEERING

def pipeline(df):
    return (
        df #CLEANING
        .pipe(criar_pipeline, CLEANING)
           #ENGINEERING
        .pipe(criar_pipeline, ENGINEERING)
    )