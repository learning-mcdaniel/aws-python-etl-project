
GOAL:  Build an actual ETL pipeline using Python
	1. Pull raw CSV data from S3
	2. Process it with Python
	3. Create cleaned output file
	4. Upload processed file back to S3

ARCHITECTURE:

	Local/S3 Raw Data -> Python ETL Script on EC2 -> Processed Clean Data -> Upload back to S3


Step 1:  Connect to EC2 and create a working directory called data-project

> ssh -i kevin-aws-key.ppk ec2-user@18.224.94.114
Warning: Permanently added '18.224.94.114' (ECDSA) to the list of known hosts.
X11 forwarding request failed on channel 0
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
Last login: Mon May 11 18:15:10 2026 from 67.175.178.49
[ec2-user@ip-172-31-43-205 ~]$ pwd
/home/ec2-user
[ec2-user@ip-172-31-43-205 ~]$ ll
total 68412
drwxr-xr-x. 3 ec2-user ec2-user       78 May  7 18:36 aws
-rw-r--r--. 1 ec2-user ec2-user 70000082 May 11 18:19 awscliv2.zip
-rw-r--r--. 1 ec2-user ec2-user    51523 May  8 21:13 product_sales_dataset.csv
[ec2-user@ip-172-31-43-205 ~]$ mkdir data-project
[ec2-user@ip-172-31-43-205 ~]$ cd data-project/


Step 2:  Pull CSV file from S3

[ec2-user@ip-172-31-43-205 data-project]$ aws s3 ls
2026-05-08 20:27:05 kevin-data-engineering-lab-2026
[ec2-user@ip-172-31-43-205 data-project]$ aws s3 cp s3://kevin-data-engineering-lab-2026/raw/product_sales_dataset.csv .
download: s3://kevin-data-engineering-lab-2026/raw/product_sales_dataset.csv to ./product_sales_dataset.csv
[ec2-user@ip-172-31-43-205 data-project]$ ls
product_sales_dataset.csv
[ec2-user@ip-172-31-43-205 data-project]$ mv product_sales_dataset.csv sales.csv


Step 3:  Create Python ETL Script

[ec2-user@ip-172-31-43-205 data-project]$ nano etl_sales.py
[ec2-user@ip-172-31-43-205 data-project]$ cat etl_sales.py
import pandas as pd

# Read raw CSV
df = pd.read_csv("sales.csv")

print("Original Data:")
print(df.head())

# Basic cleaning
df.columns = df.columns.str.lower().str.replace(" ","_")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with null values
df = df.dropna()

# Example transformation
if 'sales_amount' in df.columns:
   df['sales_amount'] = df['sales_amount'].astype(float)

# Save cleaned file
output_file = "sales_clean.csv"
df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")

[ec2-user@ip-172-31-43-205 data-project]$

[ec2-user@ip-172-31-43-205 data-project]$ ll
total 56
-rw-r--r--. 1 ec2-user ec2-user   536 May 11 20:33 etl_sales.py
-rw-r--r--. 1 ec2-user ec2-user 51523 May  8 21:13 sales.csv


Step 4:  Install Pandas

[ec2-user@ip-172-31-43-205 data-project]$ sudo dnf install python3-pip -y
Last metadata expiration check: 2:21:03 ago on Mon May 11 18:16:12 2026.
Dependencies resolved.
==============================================================================================================================================================================================================
 Package                                             Architecture                              Version                                                   Repository                                      Size
==============================================================================================================================================================================================================
Installing:
 python3-pip                                         noarch                                    21.3.1-2.amzn2023.0.17                                    amazonlinux                                    1.8 M
Installing weak dependencies:
 libxcrypt-compat                                    x86_64                                    4.4.33-7.amzn2023                                         amazonlinux                                     92 k

Transaction Summary
==============================================================================================================================================================================================================
Install  2 Packages

Total download size: 1.9 M
Installed size: 11 M
Downloading Packages:
(1/2): libxcrypt-compat-4.4.33-7.amzn2023.x86_64.rpm                                                                                                                          2.5 MB/s |  92 kB     00:00
(2/2): python3-pip-21.3.1-2.amzn2023.0.17.noarch.rpm                                                                                                                           21 MB/s | 1.8 MB     00:00
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                                          15 MB/s | 1.9 MB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                                                                      1/1
  Installing       : libxcrypt-compat-4.4.33-7.amzn2023.x86_64                                                                                                                                            1/2
  Installing       : python3-pip-21.3.1-2.amzn2023.0.17.noarch                                                                                                                                            2/2
  Running scriptlet: python3-pip-21.3.1-2.amzn2023.0.17.noarch                                                                                                                                            2/2
  Verifying        : libxcrypt-compat-4.4.33-7.amzn2023.x86_64                                                                                                                                            1/2
  Verifying        : python3-pip-21.3.1-2.amzn2023.0.17.noarch                                                                                                                                            2/2

Installed:
  libxcrypt-compat-4.4.33-7.amzn2023.x86_64                                                             python3-pip-21.3.1-2.amzn2023.0.17.noarch

Complete!
[ec2-user@ip-172-31-43-205 data-project]$ pip3 --version
pip 21.3.1 from /usr/lib/python3.9/site-packages/pip (python 3.9)
[ec2-user@ip-172-31-43-205 data-project]$ pip3 install pandas
Defaulting to user installation because normal site-packages is not writeable
Collecting pandas
  Downloading pandas-2.3.3-cp39-cp39-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.8 MB)
     |████████████████████████████████| 12.8 MB 5.9 MB/s
Collecting python-dateutil>=2.8.2
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
     |████████████████████████████████| 229 kB 67.7 MB/s
Collecting tzdata>=2022.7
  Downloading tzdata-2026.2-py2.py3-none-any.whl (349 kB)
     |████████████████████████████████| 349 kB 65.2 MB/s
Requirement already satisfied: pytz>=2020.1 in /usr/lib/python3.9/site-packages (from pandas) (2022.7.1)
Collecting numpy>=1.22.4
  Downloading numpy-2.0.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (19.5 MB)
     |████████████████████████████████| 19.5 MB 70.5 MB/s
Requirement already satisfied: six>=1.5 in /usr/lib/python3.9/site-packages (from python-dateutil>=2.8.2->pandas) (1.15.0)
Installing collected packages: tzdata, python-dateutil, numpy, pandas
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
awscli 2.33.15 requires python-dateutil<=2.9.0,>=2.1, but you have python-dateutil 2.9.0.post0 which is incompatible.
Successfully installed numpy-2.0.2 pandas-2.3.3 python-dateutil-2.9.0.post0 tzdata-2026.2


Step 5:  Run ETL Script

[ec2-user@ip-172-31-43-205 data-project]$ python3 etl_sales.py
Original Data:
   Product_ID  Product_Name Category  Price_USD  Quantity_Sold  sales_amount  Order_Date Customer_City
0        1001      Lipstick   Beauty         26              7           182  2025-01-24       Karachi
1        1002        Jacket  Fashion        254              6          1524  2026-04-01      Peshawar
2        1003    Gym Gloves   Sports         30             10           300  2025-11-05      Peshawar
3        1004  History Book    Books         45              6           270  2026-01-05        Lahore
4        1005   Tennis Ball   Sports        401              1           401  2025-11-28        Quetta
Cleaned data saved to sales_clean.csv
[ec2-user@ip-172-31-43-205 data-project]$ ll
total 112
-rw-r--r--. 1 ec2-user ec2-user   536 May 11 20:33 etl_sales.py
-rw-r--r--. 1 ec2-user ec2-user 51520 May 11 20:35 sales.csv
-rw-r--r--. 1 ec2-user ec2-user 53520 May 11 20:38 sales_clean.csv


Step 6:  Upload Processed DAta to S3

[ec2-user@ip-172-31-43-205 data-project]$ aws s3 ls
2026-05-08 20:27:05 kevin-data-engineering-lab-2026
[ec2-user@ip-172-31-43-205 data-project]$ aws s3 cp sales_clean.csv s3://kevin-data-engineering-lab-2026/processed/
upload: ./sales_clean.csv to s3://kevin-data-engineering-lab-2026/processed/sales_clean.csv
[ec2-user@ip-172-31-43-205 data-project]$ aws s3 ls s3://kevin-data-engineering-lab-2026/processed/
2026-05-08 20:28:14          0
2026-05-11 20:40:40      53520 sales_clean.csv
[ec2-user@ip-172-31-43-205 data-project]$

