# API Requests

### Upload
With `upload` request you can add new post to the server.  

```
URL:
[POST] <IP>/api/upload

REQUEST BODY of 'form-data' type:
title (string):          The title or headline of the post
description (string):    Description of the post
category (string):       One of the five categories (newcomers, new-projects, tournaments, sport-challenges, other-events)
pictures (files):        One or more images belonging to the post. First will be shown as a thumbnail    
```

### Get
With `get` you can request data of posts from database.  

```
URL:
[GET] <IP>/api/get/<category>
category:   One of the five categories (newcomers, projects, tournaments, sport, other)

RESPONSE of 'JSON' type:
{
    "status": (string),
    "errmsg": (string or empty),
    "error": (string or empty),
    "message": (array of dictionaries)
        [
            {
                "title": (string),
                "description: (string)",
                "uploaded_time": (datetime),
                "images": (array of arrays)
                    [
                        [
                            0: filename (string),
                            1: alternative_text (string),
                            2: max_width (int)
                        ]
                        ...
                    ]
            }
            ...
        ]
    "status_code": (integer)
}
```