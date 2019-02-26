# chat-backend
Backend for Android ChatApp - written using Python Django. Repository for Android app: https://github.com/sbearben/ChatApp

### Built With
* [Django](https://www.djangoproject.com/): A high-level Python Web framework
* [Django REST framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs
* [Django Channels](https://channels.readthedocs.io/en/latest/): A project that takes Django and extends its abilities beyond HTTP - WebSockets, chat protocols, IoT protocols, etc.
* [django-rest-auth](https://django-rest-auth.readthedocs.io/en/latest/): A set of REST API endpoints to handle User Registration and Authentication tasks
* [django-friendship](https://github.com/revsys/django-friendship): Django app to manage following and bi-directional friendships
* [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup): Lets you interact with Firebase from privileged environments (used for Firebase Cloud Messaging)

### Usage

Clone the repository and setup your environment:

```
pip install django
pip install djangorestframework
pip install markdown
pip install django-filter
pip install channels
pip install channels_redis
pip install django-rest-auth
pip install django-allauth
pip install django-friendship
pip install firebase-admin
```

You will also need to follow the instructions to [Add the Firebase Admin SDK to Your Server](https://firebase.google.com/docs/admin/setup).
Once you have the JSON file provided by Firebase containing your service account's credentials, add it to the root folder of chat-backend as `chatappAccountKey.json`.

Run the following two commands to start the server and its workers:

```
python manage.py runserver
python manage.py runworker realtime-event-sender
```

### License
    Copyright (C) 2018 Armon Khosravi

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License. 

