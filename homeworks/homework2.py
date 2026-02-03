import pandas as pd
from pathlib import Path
from datetime import datetime
from prefect import flow, task

# Task 1: Extract - Download and decompress data
@task(name="extract")
def extract(taxi: str, year: int, month: int) -> str:
    """
    Extract taxi data for given parameters.
    Returns the path to the uncompressed CSV file.
    """
    file = f"{taxi}_tripdata_{year:04d}-{month:02d}.csv"
    # Download logic here
    return file

# Task 2: Transform - Read and process data
@task(name="transform")
def transform(file: str) -> pd.DataFrame:
    """Read CSV and perform transformations"""
    df = pd.read_csv(file)
    return df

# Task 3: Load - Store results
@task(name="load")
def load(df: pd.DataFrame, taxi: str, year: int, month: int):
    """Store processed data"""
    output_file = f"{taxi}_tripdata_{year:04d}-{month:02d}_processed.parquet"
    df.to_parquet(output_file)
    return output_file

# Main Flow
@flow(name="taxi-data-pipeline")
def taxi_pipeline(taxi: str, year: int, month: int):
    """Main orchestration flow"""
    raw_file = extract(taxi, year, month)
    df = transform(raw_file)
    result = load(df, taxi, year, month)
    return result

# For scheduled execution
if __name__ == "__main__":
    # Run with specific parameters for homework questions
    taxi_pipeline(taxi="yellow", year=2020, month=12)