import os
import pandas as pd
import logging
from datetime import datetime

# Configure Logging
logging.basicConfig(
            filename='etl.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    logging.info("ETL job started")

    # Read CSV
    df = pd.read_csv("sales.csv")

    logging.info(f"Original rows: {len(df)}")


    # Clean column names 
    df.columns = df.columns.str.lower().str.replace(" ","_")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove nulls 
    df = df.dropna()

    logging.info("fCleaned rows: {len(df)}")

    # Example transformation
    if 'sales_amount' in df.columns:
       df['sales_amount'] = df['sales_amount'].astype(float)

    # Timestamp output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = f"sales_clean_{timestamp}.csv"

    # Save output 
    df.to_csv(output_file, index=False)

    # Upload to S3
    s3_bucket = "kevin-data-engineering-lab-2026"

    upload_command = (
            f"aws s3 cp {output_file} "
            f"s3://{s3_bucket}/processed/"
    )

    os.system(upload_command)

    logging.info(f"Uploaded {output_file} to S3")

    logging.info(f"Saved cleaned file: {output_file}")
    
    print(f"ETL Successful: {output_file}")

except Exception as e:
    logging.error(f"ETL failed: {str(e)}")
    print(f"ETL failed.  Check logs.")


