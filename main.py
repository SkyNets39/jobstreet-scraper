from crawler import scrape_classification
import pandas as pd
import config

if __name__ == "__main__":
    data_dict = scrape_classification()

    df = pd.DataFrame(data_dict)
    df.to_csv(config.OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("Saved", len(df), "jobs to", config.OUTPUT_CSV)
