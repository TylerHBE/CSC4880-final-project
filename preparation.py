# from raid.utils import load_data
import pandas as pd
from pathlib import Path

def load_ghostbuster_data(out_path: str = "./data/output/ghostbuster-data.xlsx", reread: bool = False) -> pd.DataFrame:
    """
    Load the Ghostbuster dataset from the subrepository.

    Returns:
        pd.DataFrame: A DataFrame containing the Ghostbuster dataset.
    """

    if Path(out_path).exists() and not reread:
        return pd.read_excel(out_path)

    main_path = "./data/ghostbuster-data"  # Adjust the path as necessary
    data_paths = ["wp", "reuter", "essay", "other"]  # List of subdirectories to load data from
    human_data = ["human"]

    df = pd.DataFrame()  # Initialize an empty DataFrame to hold the combined data

    root = Path(main_path)
    for data_path in data_paths:
        full_path = root / data_path
        if full_path.exists():
            # Load the data by reading each text file in the directory and inserting the contents into a DataFrame
            for file in full_path.rglob("*.txt"):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # The sub_path is the parent directory of the file, which indicates the model or source of the text in the ghostbuster dataset
                    subpath_str = str(file.parts[-2])  # Convert sub_path to string for DataFrame
                    df = pd.concat([df, pd.DataFrame({'text': [content], 'model': [subpath_str], 'source-index': [file], 'human': [subpath_str in human_data]})], ignore_index=True)
        else:
            print(f"Warning: {full_path} does not exist. Skipping this directory.")
    df.to_excel(out_path, index=False)
    return df

def load_raid_bench_data(out_path: str = "./data/output/raid-bench-data.xlsx", reread: bool = False) -> pd.DataFrame:
    #return load_data()
    pass  # Placeholder while downloading the raid-bench data.

def prepare(out_path: str = "./data/output/combined-data.xlsx", reread: bool = False) -> pd.DataFrame:
    """
    Prepare the dataset and return the prepared DataFrame.
    """

    if Path(out_path).exists() and not reread:
        return pd.read_excel(out_path)

    ghostbuster_df = load_ghostbuster_data()
    raid_bench_df = load_raid_bench_data()

    combined_df = pd.concat([ghostbuster_df, raid_bench_df], ignore_index=True)
    combined_df.to_excel(out_path, index=False)

    return combined_df

print(prepare().head())