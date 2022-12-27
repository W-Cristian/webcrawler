# webcrawler

This project consists on a webcrawler that collects information of project from the [freelance.de](https://www.freelance.de/) page using selenium framework, python and is mounted on a docker container for quick launch.

Once 🌐 Docker Desktop is installed, you can run the command
* docker-compose up --build \
in the root folder which (contains docker-compose.yml)

once the program is running you can make a request by the get method to the endpoint:

* http://localhost:4000/freelancer/<string:search_word>\
or to:

* http://localhost:4000/freelancer
by the post method sending a Json with the following scheme

```json
{
     "user":"user_credentials",
     "pass":"pass_credentials",
     "quantity":"5", -----> optional
     "key":"search_word"
}
```
