def dataset_summary(df):

    summary = {
        "Rows": df.shape[0],"\n"
        "Columns": df.shape[1],"\n"
        "Missing Values": df.isnull().sum().to_dict(),"\n"
        "Data Types": df.dtypes.astype(str).to_dict()
    }

    return summary