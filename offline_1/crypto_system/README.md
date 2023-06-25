# Crypto system

## Description
In this crypto system there is a server where all the values of p, g and all user's public key is stored
where 
```
p = a large prime number for the system
g = a primitive root modulo p
user's public key = g^{private key} mod p
```
when a user wants to send a message to another user, he/she will send the message to the server requesting the public key of the receiver. The server will then send the public key of the receiver to the sender. The sender will then encrypt the message using the public key of the receiver and send it to the server. The server will then send the encrypted message to the receiver. The receiver will then decrypt the message using his/her private key and senders public key.

## API Endpoints

List of available endpoints:

| Endpoint | Method | Description | Quick Link |
| --- | --- | --- | --- |
| `/public/get_parameters` | `GET` | Get p and g | [Link](#get-p-and-g) |
| `/unauth/register` | `POST` | Register User | [Link](#register-user) |
| `/users/get_user` | `GET` | Get User | [Link](#get-user) |
| `/users/get_all_users` | `GET` | Get All Users | [Link](#get-all-users) |
| `/users/send_message` | `POST` | Send Message | [Link](#send-message) |
| `/users/get_message` | `GET` | Get Message | [Link](#get-message) |


### Get p and g
---
- Endpoint: <br>
```
/public/get_parameters
```
- Method: <br>
```
GET
```
- Success Response: <br>
```json:
{
    "p": "prime_number",
    "g": "generator",
    "min_len": "minimum private key length",
}
```

### Register User
---
- Endpoint: <br>
```
/unauth/register
```
- Method: <br>
```
POST
```
- Request Body: <br>
```json: 
{
    "username": "user1", 
    "public_key": "public_key"
}
```
- Success Response: <br>
```json:
{
    "message": "User registered successfully"
    "user" : {
        username: "user1",
        public_key: "public_key"
    }
}
```
- Error Response: <br>
```json:
{
    "message": "User already exists"
}
```

### Get User
---
- Endpoint: <br>
```
/users/get_user
```
- Method: <br>
```
GET
```
- Request Body: <br>
```json: 
{
    "username": "user1"
}
```
- Success Response: <br>
```json:
{
    "username": "user1",
    "public_key": "public_key"
}
```
- Error Response: <br>
```json:
{
    "message": "User does not exist"
}
```

### Get All Users
---
- Endpoint: <br>
```
/users/get_all_users
```

- Method: <br>
```
GET
```

- Success Response: <br>
```json:
{
    "users": [
        {
            "username": "user1",
            "public_key": "public_key"
        },
        {
            "username": "user2",
            "public_key": "public_key"
        }
    ]
}
```

### Send Message
---
- Endpoint: <br>
```
/users/send_message
```
- Method: <br>
```
POST
```
- Request Body: <br>
```json: 
{
    "sender": "user1",
    "receiver": "user2",
    "message": "message"
}
```
- Success Response: <br>
```json:
{
    "message": "Message sent successfully"
}
```
- Error Response: <br>
```json:
{
    "message": "User does not exist"
}
```

### Get Message
---
- Endpoint: <br>
```
/users/get_message
```
- Method: <br>
```
GET
```
- Request Body: <br>
```json: 
{
    "username": "user2"
}
```
- Success Response: <br>
```json:
{
    "sender": "user1",
    "message": "message"
}
```
- Error Response: <br>
```json:
{
    "message": "User does not exist"
}
```