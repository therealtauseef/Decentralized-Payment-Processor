# Decentralized Payment Processor

Welcome to the Decentralized Payment Processor project! This project allows users to send and receive payments using a cryptocurrency with a Flask API backend that interacts with both MongoDB and the XRPL (XRP Ledger).

## Overview

This project consists of a Flask API that handles user accounts, transactions, and integration with the XRPL network for cryptocurrency transactions. Users can register, log in, check their account balance, send payments to others using both MongoDB and the XRPL.

## Prerequisites
Before running the project, make sure you have the following prerequisites installed:
- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-PyMongo
- Flask-Bcrypt
- XRPL Python Library
- MongoDB
- Git (for cloning the project)

## Installation
1. Clone the project from the GitHub repository:
https://github.com/therealtauseef/Decentralized-Payment-Processor

2. Navigate to the project directory:

3. Install the project dependencies using pip:


4. Configure MongoDB:
- Create a MongoDB Atlas account (if you don't have one).
- Replace the MongoDB URI in `config.py` with your MongoDB Atlas URI.

## Running the Flask API

To run the Flask API, use the following command:

##############     python app.py     ####################


The API will start running on `http://127.0.0.1:5000/`.

## API Endpoints

- `/register`: Register a new user.
- `/login`: Log in with your username and password.
- `/balance`: Retrieve your account balance.
- `/send_payment`: Send cryptocurrency to another user.
- `/add_money`: Send cryptocurrency to another user.


## XRPL Integration

This project also supports XRPL integration for cryptocurrency transactions. To send XRP using XRPL, you can use the `/xrpl_send_payment` endpoint.
