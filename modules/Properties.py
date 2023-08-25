class Properties:
    def title(self, column_name, labels):
        return {
            column_name: {
                "title": [
                    {
                        "text": {
                            "content": label
                        }
                    } for label in labels
                ]
            }
        }

    def text(self, column_name, *contents):
        return {
            column_name: {
                "rich_text": [
                    {
                        "text": {
                            "content": content
                        }
                    } for content in contents
                ]
            }
        }

    def checkbox(self, column_name, boolean: bool):
        return {
            column_name: {
                "checkbox": boolean
            }
        }

    def number(self, column_name):
        return {
            column_name: {
                "number": 1999
            }
        }

    def select(self, column_name, label):
        return {
            column_name: {
                "select": {
                    "name": label
                }
            }
        }

    def multi_select(self, column_name, *labels):
        return {
            column_name: {
                "multi_select": [{
                    "name": label
                } for label in labels]
            }
        }

    def date(self, column_name, start, end):
        # testing on future
        return {
            column_name: {
                "date": {
                    "start": "2022-08-05",
                    "end": "2022-08-10"
                }
            }
        }

    def url(self, column_name, url_address):
        return {
            column_name: {
                "url": url_address
            }
        }

    def email(self, column_name, email_address):
        return {
            column_name: {
                "email": email_address
            }
        }

    def phone(self, column_name, phone_number):
        return {
            column_name: {
                "phone_number": phone_number
            }
        }

    def people(self, column_name):
        # testing on future
        return {
            column_name: {
                "people": [
                    {
                        "id": "4af42d2d-a077-4808-b4f7-e960a93fd945"
                    }
                ]
            }
        }

    def relation(self, column_name):
        # testing on future
        return {
            column_name: {
                "relation": [
                    {
                        "id": "fbb0a7f2-413e-4728-adbf-281ab14f0c33"
                    }
                ]
            }
        }

    def column(self, database_raw, column_name):
        values = []
        database = database_raw["results"]

        for row_raw in database:
            row_content = row_raw["properties"][column_name]

            if "title" in row_content:
                values.append([content["text"]["content"] if content is not None else None for content in row_content["title"]])

            if "rich_text" in row_content:
                values.append([content["text"]["content"] if content is not None else None for content in row_content["rich_text"]])

            if "checkbox" in row_content:
                values.append(row_content["checkbox"] if row_content["checkbox"] is not None else None)

            if "number" in row_content:
                values.append(row_content["number"] if row_content["number"] is not None else None)

            if "select" in row_content:
                try:
                    values.append(row_content["select"]["name"] if row_content["select"]["name"] is not None else None)
                except:
                    values.append("")

            if "multi_select" in row_content:
                values.append([content["name"] if content is not None else None for content in row_content["multi_select"]])

            if "date" in row_content:
                try:
                    values.append([row_content["date"]["start"] if row_content["date"]["start"] is not None else None, row_content["date"]["end"] if row_content["date"]["end"] is not None else None])
                except:
                    values.append([None,None])

            if "url" in row_content:
                values.append(row_content["url"] if row_content["url"] is not None else None)

            if "email" in row_content:
                values.append(row_content["email"] if row_content["email"] is not None else None)

            if "phone_number" in row_content:
                values.append(row_content["phone_number"] if row_content["phone_number"] is not None else None)

            if "people" in row_content:
                values.append([content["id"] if content is not None else None for content in row_content["people"]])

            if "relation" in row_content:
                values.append([content["id"] if content is not None else None for content in row_content["relation"]])

        return values
    
    def has(self, database_raw, column_name, *matches):
        ids = []
        database = database_raw["results"]

        for row_raw in database:
            row_content = row_raw["properties"][column_name]
            row_id = row_raw["id"]

            if "title" in row_content:
                if any(
                    content["text"]["content"] == match
                    for content in row_content["title"]
                    if content is not None
                    for match in matches
                ):
                    ids.append(row_id)

            if "rich_text" in row_content:
                if any(
                    content["text"]["content"] == match
                    for content in row_content["rich_text"]
                    if content is not None
                    for match in matches
                ):
                    ids.append(row_id)

            if "checkbox" in row_content:
                if row_content["checkbox"] in matches:
                    ids.append(row_id)

            if "number" in row_content:
                if row_content["number"] in matches:
                    ids.append(row_id)

            if "select" in row_content and row_content["select"] is not None:
                if row_content["select"]["name"] in matches:
                    ids.append(row_id)

            if "multi_select" in row_content:
                if any(
                    content["name"] == match
                    for content in row_content["multi_select"]
                    if content is not None
                    for match in matches
                ):
                    ids.append(row_id)

            if "date" in row_content:
                if any(
                    value == match
                    for value in (row_content["date"]["start"], row_content["date"]["end"])
                    if value is not None
                    for match in matches
                ):
                    ids.append(row_id)

            if "url" in row_content:
                if row_content["url"] in matches:
                    ids.append(row_id)

            if "email" in row_content:
                if row_content["email"] in matches:
                    ids.append(row_id)

            if "phone_number" in row_content:
                if row_content["phone_number"] in matches:
                    ids.append(row_id)

            if "people" in row_content:
                if any(
                    content["id"] == match
                    for content in row_content["people"]
                    if content is not None
                    for match in matches
                ):
                    ids.append(row_id)

            if "relation" in row_content:
                if any(
                    content["id"] == match
                    for content in row_content["relation"]
                    if content is not None
                    for match in matches
                ):
                    ids.append(row_id)

        return ids

