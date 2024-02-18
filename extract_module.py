import boto3
import time


s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
bucket_name = 'ericsson-project-uddipan-1803'

def upload_and_extract_text(pdf_file):
        pdf_file_key = f'uploads/{pdf_file.filename}'
        s3_client.upload_fileobj(pdf_file, bucket_name, pdf_file_key)

        response = textract_client.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': pdf_file_key}}
        )
        
        job_id = response['JobId']

        while True:
            result = textract_client.get_document_text_detection(JobId=job_id)
            status = result['JobStatus']
            
            if status == 'SUCCEEDED':
                break
            elif status == 'FAILED' or status == 'PARTIAL_SUCCESS':
                return status, "File upload and text extraction failed."

            time.sleep(5)  

        extracted_text = ''
        for item in result['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text += item['Text'] + '\n'
        
        return status, extracted_text