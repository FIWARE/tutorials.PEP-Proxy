[![FIWARE Banner](https://fiware.github.io/tutorials.PEP-Proxy/img/fiware.png)](https://www.fiware.org/developers)

[![FIWARE Security](https://img.shields.io/badge/FIWARE-Security-ff7059.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAVCAYAAAC33pUlAAAABHNCSVQICAgIfAhkiAAAA8NJREFUSEuVlUtIFlEUx+eO+j3Uz8wSLLJ3pBiBUljRu1WLCAKXbXpQEUFERSQF0aKVFAUVrSJalNXGgmphFEhQiZEIPQwKLbEUK7VvZrRvbr8zzjfNl4/swplz7rn/8z/33HtmRhn/MWzbXmloHVeG0a+VSmAXorXS+oehVD9+0zDN9mgk8n0sWtYnHo5tT9daH4BsM+THQC8naK02jCZ83/HlKaVSzBey1sm8BP9nnUpdjOfl/Qyzj5ust6cnO5FItJLoJqB6yJ4QuNcjVOohegpihshS4F6S7DTVVlNtFFxzNBa7kcaEwUGcbVnH8xOJD67WG9n1NILuKtOsQG9FngOc+lciic1iQ8uQGhJ1kVAKKXUs60RoQ5km93IfaREvuoFj7PZsy9rGXE9G/NhBsDOJ63Acp1J82eFU7OIVO1OxWGwpSU5hb0GqfMydMHYSdiMVnncNY5Vy3VbwRUEydvEaRxmAOSSqJMlJISTxS9YWTYLcg3B253xsPkc5lXk3XLlwrPLuDPKDqDIutzYaj3eweMkPeCCahO3+fEIF8SfLtg/5oI3Mh0ylKM4YRBaYzuBgPuRnBYD3mmhA1X5Aka8NKl4nNz7BaKTzSgsLCzWbvyo4eK9r15WwLKRAmmCXXDoA1kaG2F4jWFbgkxUnlcrB/xj5iHxFPiBN4JekY4nZ6ccOiQ87hgwhe+TOdogT1nfpgEDTvYAucIwHxBfNyhpGrR+F8x00WD33VCNTOr/Wd+9C51Ben7S0ZJUq3qZJ2OkZz+cL87ZfWuePlwRcHZjeUMxFwTrJZAJfSvyWZc1VgORTY8rBcubetdiOk+CO+jPOcCRTF+oZ0okUIyuQeSNL/lPrulg8flhmJHmE2gBpE9xrJNkwpN4rQIIyujGoELCQz8ggG38iGzjKkXufJ2Klun1iu65bnJub2yut3xbEK3UvsDEInCmvA6YjMeE1bCn8F9JBe1eAnS2JksmkIlEDfi8R46kkEkMWdqOv+AvS9rcp2bvk8OAESvgox7h4aWNMLd32jSMLvuwDAwORSE7Oe3ZRKrFwvYGrPOBJ2nZ20Op/mqKNzgraOTPt6Bnx5citUINIczX/jUw3xGL2+ia8KAvsvp0ePoL5hXkXO5YvQYSFAiqcJX8E/gyX8QUvv8eh9XUq3h7mE9tLJoNKqnhHXmCO+dtJ4ybSkH1jc9XRaHTMz1tATBe2UEkeAdKu/zWIkUbZxD+veLxEQhhUFmbnvOezsJrk+zmqMo6vIL2OXzPvQ8v7dgtpoQnkF/LP8Ruu9zXdJHg4igAAAABJRU5ErkJgggA=)](https://www.fiware.org/developers/catalogue/)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.Time-Series-Data.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/fiware-tutorials/badge/?version=latest)](https://fiware-tutorials.readthedocs.io/en/latest)

This tutorial uses the FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) PEP Proxy combined with **Keyrock** to secure access to endpoints exposed by
FIWARE generic enablers. Users (or other actors) must log-in and use a token to gain access to services. The application
code created in the [previous tutorial](https://github.com/Fiware/tutorials.Securing-Access) is expanded to authenticate
users throughout a distributed system. The design of FIWARE Wilma - a PEP Proxy is discussed, and the parts of the
Keyrock GUI and REST API relevant to authenticating other services are described in detail.

[cUrl](https://ec.haxx.se/) commands are used throughout to access the **Keyrock** and **Wilma** REST APIs - [Postman documentation](http://fiware.github.io/tutorials.PEP-Proxy/) for these calls is also available.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.getpostman.com/collections/66d8ba3abaf7319941b1)


# Contents

- [Securing Microservices with a PEP Proxy](#securing-microservices-with-a-pep-proxy)
  * [Standard Concepts of Identity Management](#standard-concepts-of-identity-management)
  * [:arrow_forward: Video : Introduction to Wilma PEP Proxy](#arrow_forward-video--introduction-to-wilma-pep-proxy)
- [Prerequisites](#prerequisites)
  * [Docker](#docker)
  * [Cygwin](#cygwin)
- [Architecture](#architecture)
- [Start Up](#start-up)
  * [Dramatis Personae](#dramatis-personae)
  * [Logging In to Keyrock using the REST API](#logging-in-to-keyrock-using-the-rest-api)
    + [Create Token with Password](#create-token-with-password)
    + [Get Token Info](#get-token-info)
- [Managing PEP Proxies and IoT Agents](#managing-pep-proxies-and-iot-agents)
  * [:arrow_forward: Video : Wilma PEP Proxy Configuration](#arrow_forward-video--wilma-pep-proxy-configuration)
  * [PEP Proxy CRUD Actions](#pep-proxy-crud-actions)
    + [Create a PEP Proxy](#create-a-pep-proxy)
    + [Read PEP Proxy details](#read-pep-proxy-details)
    + [List PEP Proxies](#list-pep-proxies)
    + [Reset Password of a PEP Proxy](#reset-password-of-a-pep-proxy)
    + [Delete a PEP Proxy](#delete-a-pep-proxy)
  * [IoT Agent CRUD Actions](#iot-agent-crud-actions)
    + [Create an IoT Agent](#create-an-iot-agent)
    + [Read IoT Agent details](#read-iot-agent-details)
    + [List IoT Agents](#list-iot-agents)
    + [Reset Password of an IoT Agent](#reset-password-of-an-iot-agent)
    + [Delete an IoT Agent](#delete-an-iot-agent)
- [Securing the Orion Context Broker](#securing-the-orion-context-broker)
  * [Securing Orion - PEP Proxy Configuration](#securing-orion---pep-proxy-configuration)
  * [Securing Orion - Application Configuration](#securing-orion---tutorial-configuration)
  * [Securing Orion - Start up](#securing-orion---start-up)
    + [:arrow_forward: Video : Wilma PEP Proxy Configuration](#arrow_forward-video--wilma-pep-proxy-configuration-1)
  * [User Logs In to the Application using the REST API](#user-logs-in-to-the-application-using-the-rest-api)
    + [Keyrock - User Obtains an Access Token](#keyrock---user-obtains-an-access-token)
    + [PEP Proxy - Accessing Orion with an Access Token](#pep-proxy---accessing-orion-with-an-access-token)
  * [Securing Orion - Sample Code](#securing-orion---sample-code)
- [Securing an IoT Agent](#securing-an-iot-agent)
  * [Securing an IoT Agent - PEP Proxy Configuration](#securing-an-iot-agent---pep-proxy-configuration)
  * [Securing an IoT Agent - Application Configuration](#securing-an-iot-agent---tutorial-configuration)
  * [Securing IoT Agent - Start up](#securing-iot-agent---start-up)
  * [IoT Sensor Logs In to the Application using the REST API](#iot-sensor-logs-in-to-the-application-using-the-rest-api)
    + [Keyrock - IoT Sensor Obtains an Access Token](#keyrock---iot-sensor-obtains-an-access-token)
    + [PEP Proxy - Accessing IoT Agent with an Access Token](#pep-proxy---accessing-iot-agent-with-an-access-token)
  * [Securing an IoT Agent - Sample Code](#securing-an-iot-agent----sample-code)

# Securing Microservices with a PEP Proxy

> "Oh, it's quite simple. If you are a friend, you speak the password, and the doors will open."
>
>  — Gandalf (The Fellowship of the Ring by J.R.R Tolkien)

The [previous tutorial](https://github.com/Fiware/tutorials.Securing-Access) demonstrated that it is possible to Permit or Deny access
to resources based on an authenticated user identifying themselves within an application.  It was simply a matter of the code following
a different line of execution if the `access_token` was not found (Level 1 - *Authentication Access*), or confirming that a given `access_token`
had appropriate rights (Level  2 - *Basic Authorization*). The same method of securing access can be applied by placing a Policy Enforcement
Point (PEP) in front of other services within a FIWARE-based Smart Solution.

A **PEP Proxy** lies in front of a secured resource  and is an endpoint found at "well-known" public location. It serves
as a gatekeeper for resource access. Users or other actors must supply sufficient information to the **PEP Proxy** to allow their request
to succeed and pass through the **PEP proxy**. The **PEP proxy** then passes the request on to the real location of the
secured resource itself - the actual location of the secured resource is unknown to the outside user - it could be held
in a private network behind the **PEP proxy** or found on a different machine altogether.

FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) is a simple implentation of a **PEP proxy** designed to work with the FIWARE [Keyrock](http://fiware-idm.readthedocs.io/) Generic Enabler. Whenever a user tries to gain access to the resource behind the **PEP proxy**, the
PEP will describe the user's attributes to the Policy Decision Point (PDP), request a security decision, and enforce the decision.
(Permit or Deny). There is mimimal disruption of access for authorized users  - the response received is the same as if they had
accessed the secured service directly. Unauthorized users are simply returned a **401 - Unauthorized** response.


## Standard Concepts of Identity Management

The following common objects are found with the **Keyrock** Identity Management database:

* **User** - Any signed up user able to identify themselves with an eMail and password. Users can be assigned
 rights individually or as a group
* **Application** -  Any securable FIWARE application consisting of a series of microservices
* **Organization** - A group of users who can be assigned a series of rights. Altering the rights of the organization
 effects the access of all users of that organization
* **OrganizationRole** - Users can either be members or admins of an organization - Admins are able to add and remove users
 from their organization, members merely gain the roles and permissions of an organization. This allows each organization
 to be responsible for their members and removes the need for a super-admin to administer all rights
* **Role** - A role is a descriptive bucket for a set of permissions. A role can be assigned to either a single user
 or an organization. A signed-in user gains all the permissions from all of their own roles plus all of the roles associated
 to their organization
* **Permission** - An ability to do something on a resource within the system

Additionally two further non-human application objects can be secured within a FIWARE application:

* **IoTAgent** - a proxy between IoT Sensors and  the Context Broker
* **PEPProxy** - a middleware for use between generic enablers challenging the rights of a user.


 The relationship between the objects can be seen below - the entities marked in red are used directly within this tutorial:

![](https://fiware.github.io/tutorials.PEP-Proxy/img/entities.png)

## :arrow_forward: Video : Introduction to Wilma PEP Proxy

[![](http://img.youtube.com/vi/8tGbUI18udM/0.jpg)](https://www.youtube.com/watch?v=8tGbUI18udM "Introduction")

Click on the image above to see an introductory video


# Prerequisites

## Docker

To keep things simple both components will be run using [Docker](https://www.docker.com). **Docker** is a
container technology which allows to different components isolated into their respective environments.

* To install Docker on Windows follow the instructions [here](https://docs.docker.com/docker-for-windows/)
* To install Docker on Mac follow the instructions [here](https://docs.docker.com/docker-for-mac/)
* To install Docker on Linux follow the instructions [here](https://docs.docker.com/install/)

**Docker Compose** is a tool for defining and running multi-container Docker applications. A
[YAML file](https://raw.githubusercontent.com/Fiware/tutorials.Identity-Management/master/docker-compose.yml) is used
configure the required services for the application. This means all container services can be brought up in a single
command. Docker Compose is installed by default as part of Docker for Windows and  Docker for Mac, however Linux users
will need to follow the instructions found  [here](https://docs.docker.com/compose/install/)

## Cygwin

We will start up our services using a simple bash script. Windows users should download [cygwin](http://www.cygwin.com/) to provide a
command line functionality similar to a Linux distribution on Windows.

# Architecture


This application protects access to the existing Stock Management and Sensors-based application by adding PEP Proxy instances around the services created in previous tutorials and uses data pre-populated into the **MySQL** database used by **Keyrock**. It
will make use of four FIWARE components - the [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/),the [IoT Agent for UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/), the [Keyrock](http://fiware-idm.readthedocs.io/) Generic enabler
and adds one or two instances [Wilma](https://fiware-pep-proxy.rtfd.io/) PEP Proxy dependent upon which interfaces are to be secured.
Usage of the Orion Context Broker is sufficient for an application to qualify as *“Powered by FIWARE”*.

Both the Orion Context Broker and the IoT Agent rely on open source [MongoDB](https://www.mongodb.com/) technology to keep persistence of the information they hold. We will also be using the dummy IoT devices created in the [previous tutorial](https://github.com/Fiware/tutorials.IoT-Sensors/). **Keyrock** uses its own [MySQL](https://www.mysql.com/) database.

Therefore the overall architecture will consist of the following elements:

* The FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) which will receive requests using [NGSI](https://fiware.github.io/specifications/OpenAPI/ngsiv2)
* The FIWARE [IoT Agent for UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/) which will receive southbound requests using [NGSI](https://fiware.github.io/specifications/OpenAPI/ngsiv2) and convert them to  [UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) commands for the devices
* FIWARE [Keyrock](http://fiware-idm.readthedocs.io/) offer a complement Identity Management System including:
    * An OAuth2 authentication system for Applications and Users
    * A website graphical front-end for Identity Management Administration
    * An equivalent REST API for Identity Management via HTTP requests
* FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) is a PEP Proxy securing access to the **Orion** and/or **IoT Agent** microservices
* The underlying [MongoDB](https://www.mongodb.com/) database :
    * Used by the **Orion Context Broker** to hold context data information such as data entities, subscriptions and registrations
    * Used by the **IoT Agent** to hold device information such as device URLs and Keys
* A [MySQL](https://www.mysql.com/) database :
    * Used to persist user identities, applications, roles and permissions
* The **Stock Management Frontend** does the following:
   * Displays store information
   * Shows which products can be bought at each store
   * Allows users to "buy" products and reduce the stock count.
   * Allows authorized users into restricted areas
* A webserver acting as set of [dummy IoT devices](https://github.com/Fiware/tutorials.IoT-Sensors) using the [UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) protocol running over HTTP - access to certain resources is restricted.


Since all interactions between the elements are initiated by HTTP requests, the entities can be containerized and run from exposed ports.

The specific architecture of each section of the tutorial is discussed below.


# Start Up

To start the installation, do the following:

```console
git clone git@github.com:Fiware/tutorials.PEP-Proxy.git
cd tutorials.PEP-Proxy

./services create
```

>**Note** The initial creation of Docker images can take up to three minutes


Thereafter, all services can be initialized from the command line by running the [services](https://github.com/Fiware/tutorials.PEP-PRoxy/blob/master/services) Bash script provided within the repository:

```console
./services <command>
```

Where `<command>` will vary depending upon the exercise we wish to activate.

>:information_source: **Note:** If you want to clean up and start over again you can do so with the following command:
>
>```console
>./services stop
>```
>


## Dramatis Personae

The following people at `test.com` legitimately have accounts within the Application

* Alice, she will be the Administrator of the **Keyrock** Application
* Bob, the Regional Manager of the supermarket chain - he has several store managers under him:
  * Manager1
  * Manager2
* Charlie, the Head of Security of the supermarket chain - he has several store detectives under him:
  * Detective1
  * Detective2

| Name       |eMail                       |Password |
|------------|----------------------------|---------|
| alice      | alice-the-admin@test.com   | `test`  |
| bob        | bob-the-manager@test.com   | `test`  |
| charlie    | charlie-security@test.com  | `test`  |
| manager1   | manager1@test.com          | `test`  |
| manager2   | manager2@test.com          | `test`  |
| detective1 | detective1@test.com        | `test`  |
| detective2 | detective2@test.com        | `test`  |


The following people at `example.com`  have signed up for accounts, but have no reason to be granted access

* Eve - Eve the Eavesdropper
* Mallory - Mallory the malicious attacker
* Rob - Rob the Robber


| Name       |eMail                       |Password |
|------------|----------------------------|---------|
| eve        | eve@example.com            | `test`  |
| mallory    | mallory@example.com        | `test`  |
| rob        | rob@example.com            | `test`  |


Two organizations have also been set up by Alice:

| Name       | Description                         | UUID                                 |
|------------|-------------------------------------|--------------------------------------|
| Security   | Security Group for Store Detectives |`security-team-0000-0000-000000000000`|
| Management | Management Group for Store Managers |`managers-team-0000-0000-000000000000`|

One application, with appropriate roles and permissions has also been created:

| Key           | Value                                  |
|---------------|----------------------------------------|
| Client ID     | `tutorial-dckr-site-0000-xpresswebapp` |
| Client Secret | `tutorial-dckr-site-0000-clientsecret` |
| URL           | `http://localhost:3000`                |
| RedirectURL   | `http://localhost:3000/login`          |


To save time, the data creating users and organizations from the [previous tutorial](https://github.com/Fiware/tutorials.Roles-Permissions) has been downloaded and is automatically persisted to the MySQL
database on start-up so the assigned UUIDs do not change and the data does not need to be entered again.

The **Keyrock** MySQL database deals with all aspects of application security including storing users, password etc; defining access rights and dealing with OAuth2 authorization protocols.
The complete database relationship diagram can be found [here](https://fiware.github.io/tutorials.Securing-Access/img/keyrock-db.png)

To refresh your memory about how to create users and organizations and applications, you can log in at `http://localhost:3005/idm`
using the account `alice-the-admin@test.com` with a password of `test`.

![](https://fiware.github.io/tutorials.PEP-Proxy/img/keyrock-log-in.png)

and look around.


## Logging In to Keyrock using the REST API


Enter a username and password to enter the application. The default super-user has the values `alice-the-admin@test.com` and `test`. The URL `https://localhost:3443/v1/auth/tokens` should also work in a secure system.

### Create Token with Password

The following example logs in using the Admin Super-User:

#### :one: Request:
```console
curl -iX POST \
  'http://localhost:3005/v1/auth/tokens' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "alice-the-admin@test.com",
  "password": "test"
}'
```

### Get Token Info

# Managing PEP Proxies and IoT Agents


## :arrow_forward: Video : Wilma PEP Proxy Configuration

[![](http://img.youtube.com/vi/b4sYU78skrw/0.jpg)](https://www.youtube.com/watch?v=b4sYU78skrw "PEP Proxy Configuration")

Click on the image above to see a video about configuring the Wilma PEP Proxy using the **Keyrock** GUI

## PEP Proxy CRUD Actions

### Create a PEP Proxy
### Read PEP Proxy details
### List PEP Proxies
### Reset Password of a PEP Proxy
### Delete a PEP Proxy


## IoT Agent CRUD Actions

### Create an IoT Agent
### Read IoT Agent details
### List IoT Agents
### Reset Password of an IoT Agent
### Delete an IoT Agent



# Securing the Orion Context Broker

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-orion.png)

## Securing Orion - PEP Proxy Configuration

The `orion-proxy` container is an instance of FIWARE **Wilma** listening on port `1027`, it is configured to forward traffic to
`orion` on port `1026`, which is the default port that the Orion Context Broker is listening to for NGSI Requests.

```yaml
  orion-proxy:
    image: fiware/pep-proxy
    container_name: fiware-orion-proxy
    hostname: orion-proxy
    networks:
      default:
        ipv4_address: 172.18.1.10
    depends_on:
      - keyrock
    ports:
      - "1027:1027"
    expose:
      - "1027"
    environment:
      - PEP_PROXY_APP_HOST=orion
      - PEP_PROXY_APP_PORT=1026
      - PEP_PROXY_PORT=1027
      - PEP_PROXY_IDM_HOST=keyrock
      - PEP_PROXY_HTTPS_ENABLED=false
      - PEP_PROXY_AUTH_ENABLED=false
      - PEP_PROXY_IDM_SSL_ENABLED=false
      - PEP_PROXY_IDM_PORT=3005
      - PEP_PROXY_APP_ID=tutorial-dckr-site-0000-xpresswebapp
      - PEP_PROXY_USERNAME=pep_proxy_00000000-0000-0000-0000-000000000000
      - PEP_PASSWORD=test
      - PEP_PROXY_PDP=idm
      - PEP_PROXY_MAGIC_KEY=1234
```

The `PEP_PROXY_APP_ID` and `PEP_PROXY_USERNAME` would usually be obtained by adding new entries to the application in **Keyrock**,
however, in this tutorial, they have been pre-defined by populating the **MySQL** database with data on start-up.

The `orion-proxy` container is listening on a single port:

* The PEP Proxy Port - `1027` is exposed purely for tutorial access - so that cUrl or Postman can requests directly to the **Wilma** instance
  without being part of the same network.





## Securing Orion - Application Configuration

```yaml
  tutorial-app:
    image: fiware/tutorials.context-provider
    hostname: tutorial-app
    container_name: tutorial-app
    depends_on:
        - orion-proxy
        - iot-agent
        - keyrock
    networks:
      default:
        ipv4_address: 172.18.1.7
        aliases:
          - iot-sensors
    expose:
        - "3000"
        - "3001"
    ports:
        - "3000:3000"
        - "3001:3001"
    environment:
        - "WEB_APP_PORT=3000"
        - "SECURE_ENDPOINTS=true"
        - "CONTEXT_BROKER=http://orion-proxy:1027/v2"
        - "KEYROCK_URL=http://localhost"
        - "KEYROCK_IP_ADDRESS=http://172.18.1.5"
        - "KEYROCK_PORT=3005"
        - "KEYROCK_CLIENT_ID=tutorial-dckr-site-0000-xpresswebapp"
        - "KEYROCK_CLIENT_SECRET=tutorial-dckr-site-0000-clientsecret"
        - "CALLBACK_URL=http://localhost:3000/login"
```
All of the `tutorial` container settings have been described in previous tutorials. One important change is necessary however,
rather than accessing **Orion** directly on the default port `1026` as shown in all previous tutorials, all context broker
traffic is now sent to `orion-proxy` on port `1027`. As a reminder, the relevant settings are detailed below:

| Key |Value|Description|
|-----|-----|-----------|
|WEB_APP_PORT|`3000`|Port used by web-app which displays the login screen & etc.|
|KEYROCK_URL|`http://localhost`| This is URL of the **Keyrock** Web Front-End itself, used for redirection when forwarding users |
|KEYROCK_IP_ADDRESS|`http://172.18.1.5`| This is URL of the **Keyrock** OAuth Communications |
|KEYROCK_PORT|`3005` | This is the port that **Keyrock** is listening on.|
|KEYROCK_CLIENT_ID|`tutorial-dckr-site-0000-xpresswebapp`| The Client ID defined by Keyrock for this application |
|KEYROCK_CLIENT_SECRET|`tutorial-dckr-site-0000-clientsecret`| The Client Secret defined by Keyrock for this application |
|CALLBACK_URL|`http://localhost:3000/login`| The callback URL used by Keyrock when a challenge has succeeded.|

## Securing Orion - Start up

To start the system with a PEP Proxy protecting  access to **Orion**, run the following command:

```console
./services orion
```


### :arrow_forward: Video : Wilma PEP Proxy Configuration

[![](http://img.youtube.com/vi/coxFQEY0_So/0.jpg)](https://www.youtube.com/watch?v=coxFQEY0_So "Securing a REST API")

Click on the image above to see a video about securing a REST API the Wilma PEP Proxy


## User Logs In to the Application using the REST API

### Keyrock - User Obtains an Access Token

User of the application
OAuth Password Flow

### PEP Proxy - Accessing Orion with an Access Token


## Securing Orion - Sample Code




# Securing an IoT Agent

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-iot-agent.png)


## Securing an IoT Agent - PEP Proxy Configuration

The `iot-agent-proxy` container is an instance of FIWARE **Wilma** listening on port `7897`, it is configured to forward traffic to
`iot-agent` on port `7896`, which is the default port that the Ultralight agent is listening to for HTTP Requests.

```yaml
  iot-agent-proxy:
    image: fiware/pep-proxy
    container_name: fiware-iot-agent-proxy
    hostname: iot-agent-proxy
    networks:
      default:
        ipv4_address: 172.18.1.11
    depends_on:
      - keyrock
    ports:
      - "7897:7897"
    expose:
      - "7897"
    environment:
      - PEP_PROXY_APP_HOST=iot-agent
      - PEP_PROXY_APP_PORT=7896
      - PEP_PROXY_PORT=7897
      - PEP_PROXY_IDM_HOST=keyrock
      - PEP_PROXY_HTTPS_ENABLED=false
      - PEP_PROXY_AUTH_ENABLED=false
      - PEP_PROXY_IDM_SSL_ENABLED=false
      - PEP_PROXY_IDM_PORT=3005
      - PEP_PROXY_APP_ID=tutorial-dckr-site-0000-xpresswebapp
      - PEP_PROXY_USERNAME=pep_proxy_00000000-0000-0000-0000-000000000000
      - PEP_PASSWORD=test
      - PEP_PROXY_PDP=idm
      - PEP_PROXY_MAGIC_KEY=1234
```

The `PEP_PROXY_APP_ID` and `PEP_PROXY_USERNAME` would usually be obtained by adding new entries to the application in **Keyrock**,
however, in this tutorial, they have been pre-defined by populating the **MySQL** database with data on start-up.

The `iot-agent-proxy` container is listening on a single port:

* The PEP Proxy Port - `7897` is exposed purely for tutorial access - so that cUrl or Postman can requests directly to this **Wilma** instance
  without being part of the same network.


## Securing an IoT Agent - Application Configuration


```yaml
  tutorial-app:
    image: fiware/tutorials.context-provider
    hostname: tutorial-app
    container_name: tutorial-app
    depends_on:
        - orion-proxy
        - iot-agent-proxy
        - keyrock
    networks:
      default:
        ipv4_address: 172.18.1.7
        aliases:
          - iot-sensors
    expose:
        - "3000"
        - "3001"
    ports:
        - "3000:3000"
        - "3001:3001"
    environment:
        - "IOTA_HTTP_HOST=iot-agent-proxy"
        - "IOTA_HTTP_PORT=7897"
        - "DUMMY_DEVICES_PORT=3001" # Port used by the dummy IOT devices to receive commands
        - "DUMMY_DEVICES_TRANSPORT=HTTP" # Default transport used by dummy Io devices
        - "DUMMY_DEVICES_API_KEY=4jggokgpepnvsb2uv4s40d59ov"
        - "DUMMY_DEVICES_USER=iot_sensor_00000000-0000-0000-0000-000000000000"
        - "DUMMY_DEVICES_PASSWORD=test"
```

The `tutorial` container also hosts the dummy Ultralight sensors. Rather than accessing the **IoT Agent** directly on port `7896` as
shown in all previous tutorials, all traffic is forwarded to `iot-agent-proxy` on port `7897`.


| Key |Value|Description|
|-----|-----|-----------|
|IOTA_HTTP_HOST|`iot-agent-proxy`| The host name of the Wilma PEP Proxy protecting the IoT Agent for UltraLight 2.0 |
|IOTA_HTTP_PORT|`7896` | The port that the Wilma PEP Proxy protecting the IoT Agent is listenting on|
|DUMMY_DEVICES_PORT|`3001`| Port used by the dummy IOT devices to receive commands|
|DUMMY_DEVICES_TRANSPORT|`HTTP`|Default transport used by dummy Io devices|
|DUMMY_DEVICES_API_KEY|`4jggokgpepnvsb2uv4s40d59ov`| Random security key used for UltraLight interactions - ensures the integrity of interactions between the devices and the IoT Agent |
|DUMMY_DEVICES_USER|`iot_sensor_00000000-0000-0000-0000-000000000000` | Username assigned to the device(s) in **Keyrock** |
|DUMMY_DEVICES_PASSWORD|`test` | Password assigned to the device(s) in **Keyrock** |

The `DUMMY_DEVICES_USER` and `DUMMY_DEVICES_PASSWORD` would usually be obtained by adding new entries to the application in **Keyrock**,
however, in this tutorial, they have been pre-defined by populating the **MySQL** database with data on start-up.

## Securing IoT Agent - Start up

To start the system with a PEP Proxies protecting access to both **Orion** and the **IoT Agent** run the following command:

```console
./services iot-agent
```


## IoT Sensor Logs In to the Application using the REST API

### Keyrock - IoT Sensor Obtains an Access Token

User of the application
OAuth Password Flow

### PEP Proxy - Accessing IoT Agent with an Access Token


## Securing an IoT Agent -  Sample Code

---

## License

[MIT](LICENSE) © FIWARE Foundation e.V.












