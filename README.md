# Query-Enabled Annotation Framework for Text Processing

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Running the LanguageTool Server](#running-the-languagetool-server)
- [Running the Flask Application](#running-the-flask-application)
- [Usage](#usage)
  - [Profile](#profile)
  - [Chats](#chats)
  - [Search](#search)
  - [Konkordanz](#konkordanz)
  - [Annotation](#annotation)
  - [Metrics](#metrics)
  - [Settings](#settings)



## About
This project provides a lightweight framework for the automatic and manual annotation of text data, with a focus on instant messaging corpora (e.g., WhatsApp).  
It integrates **[spaCy](https://spacy.io/)** for linguistic annotation, **[LanguageTool](https://languagetool.org/)** for error detection, and a **[Flask](https://flask.palletsprojects.com/) web interface** for exploration.  
Unlike standalone NLP tools, the framework includes a **query-enabled design** that allows researchers to filter, analyze, and retrieve text and annotations efficiently.

---

## Features

- **Automatic annotation**  
  - Part-of-speech, morphology, syntax (via spaCy)  
  - Error detection (via LanguageTool)  

- **Manual annotation**  
  - Researchers can refine or correct automatic annotations  
  - Supports scope, reason, and comments  

- **Query-enabled interface**  
  - Retrieve all messages with errors  
  - Filter by author  
  - Count emoji or punctuation usage  
  - SQL-like queries without requiring deep SQL knowledge  

- **Performance optimizations**  
  - In-memory caching for faster repeated queries  
  - Parallel processing for annotation tasks  

- **Lightweight deployment**  
  - SQLite backend (no separate DB server required)  
  - Flask-based UI
 
- **Offline operation**  
  - All annotation and querying is done locally  
  - No internet connection or external APIs required  
  - Suitable for sensitive or private data (e.g., chat corpora)

---

## Installation

Install `virtualenv`

    pip3 install virtualenv

Create environment called `venv`

    python3 -m venv venv

Activate the environment:

    # Windows
    ./venv/Scripts/activate

    # Linux
    source ./venv/bin/activate

Install python libs

    pip install -r requirements.txt

## Requirements

- **Java 17** is required to run the LanguageTool server. LanguageTool analyses the errors from the inputed text and annotates them. 

## Running the LanguageTool Server

This project uses **LanguageTool version 6.6**.

LanguageTool can be downloaded from the official website:  
[https://languagetool.org/download/](https://languagetool.org/download/)

After downloading and extracting the archive, navigate into the extracted directory:

```bash
cd LanguageTool-6.6
```
After downloading the `languagetool-server.jar`, you can start the server with:

```bash
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081
```

## Running the Flask Application

In the main project directory, start the Flask application by running:

    python runFlask.py

Once the server is running, open your browser and go to:
http://localhost:5000

You will be automatically redirected to the `/profile` route, which acts as the entry point to this application.

## Usage

Once the Flask app is running, the navigation bar contains the following views:

### Profile (`/profile`)
Displays profile information for imported authors. Lets you import chats and select an author.

### Chats (`/chat`)
Shows the imported chats from the perspective of the selected author.

### Search (`/search`)
Provides a simple search to find substrings in messages. You can choose the author whose messages you want to search.

### Konkordanz (`/konkordanz`)
Lets you create complex search queries and view the results in a concordance view.

### Annotation (`/annotation`)
Enables adding or updating annotations for selected messages.

### Metrics (`/metrics`)
Displays basic author metrics such as emoji usage and error rate. These can be shown relative to every 100 words or per message.

### Settings (`/settings`)
Currently in development. In the future, this will allow customization of font and color.





