## REST API for fetching text and images from webpage.

### Setup

```
$ docker-compose up --build
```

After laucnch API will be available at http://localhost:8000/api/.

### Endpoints
#### `/api/documents/`
* PUT submit url to get text from the page.
![put_image](postman/document_put_example.png)

* POST get task status.
![post_image](postman/document_post_example.png)

* GET fetch result from submitted task.
![get_image](postman/document_get_example.png)
#### `/api/image/`
* PUT submit url to get images from the page.
![put_image](postman/image_put_example.png)

* POST get task status.
![post_image](postman/image_post_example.png)

* GET fetch downloaded image.
![get_image](postman/image_get_example.png)

