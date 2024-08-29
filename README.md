# Archiving Files

This repository contains scripts for archiving old files (such as recordings or faxes) stored by Telnyx.

## Archiving Old Faxes

Telnyx retains files sent or received via its Programmable Faxes service for 30 days, after which they are automatically deleted. To preserve these files, the repository provides a script (fax_archiving_script.py) to archive them from Telnyx storage.

### Preparation Steps

Before using the script, follow these steps:

1. **API Key Configuration:**
Provide your Telnyx API key in the script on line 8. Refer to the [Telnyx API documentation](https://developers.telnyx.com/docs/development#obtain-your-api-keys) for instructions on how to obtain your API key.
   
2. **Bucket Setup:**
Set up a bucket in Telnyx's distributed storage to hold the archived files. Follow the [Telnyx Cloud Storage Quick Start Guide](https://developers.telnyx.com/docs/cloud-storage/quick-start) for detailed instructions. 
   
3. **Bucket Configuration:**
In the script, specify the following details:
- bucket name (line 9)
- and region (line 10)

4. **Install Dependencies:**
Install the required boto3 library using pip:  
```bash
  pip install boto3
```
###Running the Script

To run the script, use the following command:

```
python3 fax_archiving_script.py
```