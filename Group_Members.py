import requests
import json
group = '523659444473997'
total = []
url = "https://graph.facebook.com/"+group+"/members?fields=email,name"

while True:
    try:
        payload = {}
        headers = {
            'Authorization': 'Bearer DQVJzY0dfMlJuMjltNG1aNW5sNmNtQVhoVGlsYlhwdnhIcnJsUkYtTGJ6dS05VWJqeF9WNG9NSVA4TjlmSEZAsVjEwRnNhYkVDUkJzWEJDQTJUZA1ZAXUXVoTUZAGS21nbEt0QVpJczZAtb3cyajd0YnlwZADlndGJJbS1vYzJpb1pFNGRmRlhDSVlGWThwYjlGYTRnWWpXckNVaEVmR1dZANkJHaEVodU5oVHZASbk1RRVBmbVhLbzg0T2JSRmZAiRkIxTDBEX2E2VGRJS0tPa25fR2JMNAZDZD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        responseJson = json.loads(response.text)
        for append in responseJson['data']:
            file_object = open('Group_Members.txt', 'a')
            encoded_string = append['name'].encode("iso-8859-1", "ignore")
            append['name'] = encoded_string.decode("iso-8859-1", "ignore")
            file_object.write(append['email'] + ';' + append['name'] + '\n')
            print(append['email'])
            file_object.close()
        url = responseJson['paging']['next']
    except:
        break

print('Fin')