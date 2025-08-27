import json
import requests


class NotionClient:

    def __init__(self, token, database_id) -> None:
        self.database_id = database_id

        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16"
        }

    # create page
    def create_page(self, description, date, due_date, status):
        create_url = 'https://api.notion.com/v1/pages'

        data = {
        "parent": { "database_id": self.database_id },
        "properties": {
            "Description": {
                "title": [
                    {
                        "text": {
                            "content": description
                        }
                    }
                ]
            },

            "Date": {
                "date": {
                            "start": date,
                            "end": None
                        }
            },

            "Due Date" : {
                "date": {
                            "start" : due_date,
                            "end": None
                        }
            },

            "Status": {
                "checkbox" : status
                
            }
        }}

        data = json.dumps(data)
        res = requests.post(create_url, headers=self.headers, data=data)
        print(res.status_code)
        return res
    

    # read page
    def read_page(self):
        query_url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        res = requests.post(query_url, headers=self.headers)
        pages = res.json().get("results", [])   
        return pages


    # update page
    def update_page(self, page_id, status):
        update_url = f'https://api.notion.com/v1/pages/{page_id}'
        data = {
            "properties": {
                "Status": {
                    "checkbox": status
                }
            }
        }
        data = json.dumps(data)
        res = requests.patch(update_url, headers=self.headers, data=data)
        print(res.status_code)
        return res

    # delete page
    def delete_page(self, page_id):
        delete_url = f'https://api.notion.com/v1/pages/{page_id}'
        data = {"archived": True}
        res = requests.patch(delete_url, headers=self.headers,data=json.dumps(data))
        return res