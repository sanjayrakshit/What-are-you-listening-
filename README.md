# What have you been listening?

The sole purpose of this project is to explore the world of APIs and some database. What other way to achieve that
except making a project.

So, in this project I've used Spotify's Web API and MongoDB

Let's talk about the required credentials. Spotify provides 3 different ways to give you access. We are not going to go
into the details. You can find more [here](https://developer.spotify.com/documentation/general/guides/authorization/).

For our use case we would require the **_CLIENT ID_** & **_CLIENT SECRET_**. More on
this [here](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)

After you've found your **client id** and **client secret** save it in a json file like this:

```json
{
  "client_id": <your-client-id>,
  "client_secret": <your-client-secret>
}
```

Now, let's set up MongoDB. For this, you can use the free version of the cloud storage option. There is a nice course by
MongoDB on the basics. You can find it [here](https://university.mongodb.com/courses/M001/about). This course will guide
you on how to set everything up. Note down the connection url with the username and password. It would look something
like this.

``mongodb+srv://<USERNAME>:<PASSWORD>@spotify-cluster.lixsh.mongodb.net/admin``
Change this link inside the `connect()` of [db_utils.py](./db_utils.py)

Now you need to save your username and password in a json file like this:

```json
{
  "username": <your-username>,
  "password": <your-password>
}
```

You can also change the database name and collection name inside `runner()` of [data_feed.py](./data_feed.py).

Look for these lines:

```python
mongo.set_database('spotify_data')
mongo.set_collection('featured_playlist')
```

All you need to do now is call the runner() from somewhere or the [main.py](./main.py)

Below is the docstring of the runner() to help you out

```text
Runner method which handles all the flow
:param spotify_credentials_path: Credentials of spotify
:param db_credentials_path: Credentials of mongo db
:param start_date: "From date" to start fetching
:param stop_date: "To date" to stop fetching at
:param delta: Time difference gap
:param batch_size: batch_size/interval at which you would want to push to eliminate too frequent write operations
:return: None
```
