import requests
import base64
import time

def callService(file_path):

    with open(file_path, "rb") as img_file:
        image = base64.b64encode(img_file.read()).decode('utf-8')

        headers = {
            'content-type': 'application/json'
        }

        payload = {
            'image': image
        }

        r = requests.post('http://localhost:7071/api/classify', json=payload, headers=headers)
        r = r.json()    

        checkUrl = r["statusQueryGetUri"]

        print(checkUrl)

        keepChecking = True
        output = None
        while keepChecking:
            time.sleep(1)
            r = requests.get(checkUrl, headers=headers)
            r = r.json()

            if r["runtimeStatus"] == "Completed":
                keepChecking = False
                output = r["output"]
                
        print(output)



callService('images/bald-eagle.jpg')

callService('images/Bernese-Mountain-Dog-Temperament-long.jpg')

callService('images/penguin.jpg')
callService('images/dog.jpg')