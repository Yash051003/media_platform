# Media Platform Backend

Hey there! Welcome to the Media Platform project. This is a secure and robust backend built with FastAPI that allows an admin to upload media files (like videos and audio) and generate temporary, secure links for streaming them.

It's a complete little ecosystem, with a database to keep track of everything, a modern API to handle all the logic, and a simple frontend to interact with it all.

###  Features

* **Secure Authentication:** Sign up and log in using JWT (JSON Web Tokens) to ensure only authorized admins can access the dashboard.
* **Media Uploads:** A simple interface to upload video and audio files.
* **Database Integration:** Uses PostgreSQL (running in Docker) to store information about users and media assets.
* **Secure Streaming Links:** Generate unique, token-based URLs for media files that automatically expire after 10 minutes.
* **Interactive API Docs:** Thanks to FastAPI, you get a beautiful, interactive API documentation page right out of the box.
* **Simple Frontend:** Includes pages for signup, login, and a main dashboard, all built with Tailwind CSS.

###  Tech Stack

* **Backend:** Python with **FastAPI**
* **Database:** **PostgreSQL** (managed with **Docker Compose**)
* **Data Validation:** **Pydantic**
* **Authentication:** **JWT** with `python-jose` and `passlib`
* **Database ORM:** **SQLAlchemy**
* **Frontend:** Plain HTML, CSS (**Tailwind CSS**), and JavaScript

###  Getting Started: How to Run Locally

Ready to get this running on your machine? Just follow these steps.

#### Prerequisites

Make sure you have these installed first:

* **Git:** To clone the project.
* **Docker** and **Docker Compose:** To run the PostgreSQL database.
* **Python 3.8+** and a package manager like `pip`.

#### Step 1: Clone the Repository

First, get the code onto your machine.

```bash
git clone <Repo Url (This one) >
cd media_platform
```

#### Step 2: Set up database credentials
* Find the **.env**  file in the project and add
```bash
DATABASE_URL="postgresql://dev_user:dev_password123@localhost:5432/media_platform_dev"
SECRET_KEY="a_very_long_and_secure_random_string_of_characters"
```
#### Step 3: Start the Database with Docker
The docker-compose.yml file has all the instructions to set up and run your PostgreSQL database in a container.

```bash
docker-compose up -d
```

#### Step 4: Set Up the Python Environment

*Create the Virtual env

```bash
python -m venv venv
```

*Activate it 
```bash
venv/Scripts/Activate
```

*Install all the required packages
```bash
pip install -r requirements.txt
```
#### Step 5: Run the Application

*Run the command in the root Dir 
```bash
uvicorn app.main:app --reload
```

#### Step 5: Extra Things :
*Before Starting up the Database , Make sure you have the Postgreasql image installed in your local network
*Example env file is also included in the project , I have pushed the .gitignore file too 
