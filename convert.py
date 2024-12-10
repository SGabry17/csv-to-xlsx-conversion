import boto3
import pandas as pd
import io
import os
import sys

s3 = boto3.client('s3')

def main():
    src_bucket = os.environ.get('SRC_BUCKET')
    src_key = os.environ.get('SRC_KEY')
    dst_bucket = os.environ.get('DST_BUCKET')
    dst_key = os.environ.get('DST_KEY')

    if not src_bucket or not src_key or not dst_bucket or not dst_key:
        print("Faltan variables de entorno requeridas.")
        sys.exit(1)

    csv_obj = s3.get_object(Bucket=src_bucket, Key=src_key)
    csv_bytes = csv_obj['Body'].read()
    df = pd.read_csv(io.BytesIO(csv_bytes))

    xlsx_buffer = io.BytesIO()
    with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

    s3.put_object(Bucket=dst_bucket, Key=dst_key, Body=xlsx_buffer.getvalue())

if __name__ == "__main__":
    main()
