import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.blob_trigger(arg_name="blob", path="test/{name}", connection="ravendra565137442_STORAGE")
@app.send_grid_output(arg_name="sendgrid_msg", api_key_setting="AzureWebJobsSendGridApiKey")
def blob_trigger_send_email(blob: func.InputStream, sendgrid_msg: func.Out[str], name: str):
    logging.info(f"Blob trigger processed blob: {name}, size: {blob.length} bytes")

    email_content = f"A new blob was uploaded or updated.\n\nName: {name}\nSize: {blob.length} bytes"

    message = {
        "personalizations": [{
            "to": [{"email": "user@contoso.com"}]
        }],
        "subject": "Azure Blob Storage Notification",
        "content": [{
            "type": "text/plain",
            "value": email_content
        }]
    }

    sendgrid_msg.set(json.dumps(message))
