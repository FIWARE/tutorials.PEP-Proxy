[![FIWARE Banner](https://fiware.github.io/tutorials.PEP-Proxy/img/fiware.png)](https://www.fiware.org/developers)

[![FIWARE Security](https://img.shields.io/badge/FIWARE-Security-ff7059.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAVCAYAAAC33pUlAAAABHNCSVQICAgIfAhkiAAAA8NJREFUSEuVlUtIFlEUx+eO+j3Uz8wSLLJ3pBiBUljRu1WLCAKXbXpQEUFERSQF0aKVFAUVrSJalNXGgmphFEhQiZEIPQwKLbEUK7VvZrRvbr8zzjfNl4/swplz7rn/8z/33HtmRhn/MWzbXmloHVeG0a+VSmAXorXS+oehVD9+0zDN9mgk8n0sWtYnHo5tT9daH4BsM+THQC8naK02jCZ83/HlKaVSzBey1sm8BP9nnUpdjOfl/Qyzj5ust6cnO5FItJLoJqB6yJ4QuNcjVOohegpihshS4F6S7DTVVlNtFFxzNBa7kcaEwUGcbVnH8xOJD67WG9n1NILuKtOsQG9FngOc+lciic1iQ8uQGhJ1kVAKKXUs60RoQ5km93IfaREvuoFj7PZsy9rGXE9G/NhBsDOJ63Acp1J82eFU7OIVO1OxWGwpSU5hb0GqfMydMHYSdiMVnncNY5Vy3VbwRUEydvEaRxmAOSSqJMlJISTxS9YWTYLcg3B253xsPkc5lXk3XLlwrPLuDPKDqDIutzYaj3eweMkPeCCahO3+fEIF8SfLtg/5oI3Mh0ylKM4YRBaYzuBgPuRnBYD3mmhA1X5Aka8NKl4nNz7BaKTzSgsLCzWbvyo4eK9r15WwLKRAmmCXXDoA1kaG2F4jWFbgkxUnlcrB/xj5iHxFPiBN4JekY4nZ6ccOiQ87hgwhe+TOdogT1nfpgEDTvYAucIwHxBfNyhpGrR+F8x00WD33VCNTOr/Wd+9C51Ben7S0ZJUq3qZJ2OkZz+cL87ZfWuePlwRcHZjeUMxFwTrJZAJfSvyWZc1VgORTY8rBcubetdiOk+CO+jPOcCRTF+oZ0okUIyuQeSNL/lPrulg8flhmJHmE2gBpE9xrJNkwpN4rQIIyujGoELCQz8ggG38iGzjKkXufJ2Klun1iu65bnJub2yut3xbEK3UvsDEInCmvA6YjMeE1bCn8F9JBe1eAnS2JksmkIlEDfi8R46kkEkMWdqOv+AvS9rcp2bvk8OAESvgox7h4aWNMLd32jSMLvuwDAwORSE7Oe3ZRKrFwvYGrPOBJ2nZ20Op/mqKNzgraOTPt6Bnx5citUINIczX/jUw3xGL2+ia8KAvsvp0ePoL5hXkXO5YvQYSFAiqcJX8E/gyX8QUvv8eh9XUq3h7mE9tLJoNKqnhHXmCO+dtJ4ybSkH1jc9XRaHTMz1tATBe2UEkeAdKu/zWIkUbZxD+veLxEQhhUFmbnvOezsJrk+zmqMo6vIL2OXzPvQ8v7dgtpoQnkF/LP8Ruu9zXdJHg4igAAAABJRU5ErkJgggA=)](https://www.fiware.org/developers/catalogue/)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.Time-Series-Data.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/fiware-tutorials/badge/?version=latest)](https://fiware-tutorials.readthedocs.io/en/latest)

This tutorial uses a PEP Proxy combined with the Keyrock to secure access to endpoints exposed by
FIWARE generic enablers. Users (or other actors) must log-in and use a token to gain access to services. The application
code created in the [previous tutorial](https://github.com/Fiware/tutorials.Securing-Access) is expanded to authenticate
users throughout a distributed system. The design of FIWARE Wilma - a PEP Proxy is discussed, and the parts of the
Keyrock GUI and REST API relevant to authenticating other services are described in detail.

[cUrl](https://ec.haxx.se/) commands are used throughout to access the **Keyrock** and **Wilma** REST APIs - [Postman documentation](http://fiware.github.io/tutorials.PEP-Proxy/) for these calls is also available.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.getpostman.com/collections/66d8ba3abaf7319941b1)


# Contents

TBD

# Securing Microservices with a PEP Proxy

> "Oh, it's quite simple. If you are a friend, you speak the password, and the doors will open."
>
>  — Gandalf (The Fellowship of the Ring by J.R.R Tolkien)





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


This application adds OAuth2-driven security into the existing Stock Management and Sensors-based application
created in [previous tutorials](https://github.com/Fiware/tutorials.IoT-Agent/) by using the data created in the first [security tutorial](https://github.com/Fiware/tutorials.Identity-Management/) and reading it programmatically. It
will make use of three FIWARE components - the [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/),the [IoT Agent for UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/) and integrates the use of the [Keyrock](http://fiware-idm.readthedocs.io/) Generic enabler. Usage of the Orion Context Broker is sufficient for an application to qualify as *“Powered by FIWARE”*.

Both the Orion Context Broker and the IoT Agent rely on open source [MongoDB](https://www.mongodb.com/) technology to keep persistence of the information they hold. We will also be using the dummy IoT devices created in the [previous tutorial](https://github.com/Fiware/tutorials.IoT-Sensors/). **Keyrock** uses its own [MySQL](https://www.mysql.com/) database.

Therefore the overall architecture will consist of the following elements:

* The FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) which will receive requests using [NGSI](https://fiware.github.io/specifications/OpenAPI/ngsiv2)
* The FIWARE [IoT Agent for UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/) which will receive southbound requests using [NGSI](https://fiware.github.io/specifications/OpenAPI/ngsiv2) and convert them to  [UltraLight 2.0](http://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual) commands for the devices
* FIWARE [Keyrock](http://fiware-idm.readthedocs.io/) offer a complement Identity Management System including:
    * An OAuth2 authentication system for Applications and Users
    * A website graphical front-end for Identity Management Administration
    * An equivalent REST API for Identity Management via HTTP requests
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

![](https://fiware.github.io/tutorials.PEP-Proxy/img/architecture.png)

The necessary configuration information for adding security to the **Stock Management Frontend**  can be found in the `tutorial` section of the associated `docker-compose.yml` file - only the relevant variables are shown below:









# Start Up

To start the installation, do the following:

```console
git clone git@github.com:Fiware/tutorials.Securing-Access.git
cd tutorials.Securing-Access

./services create
```

>**Note** The initial creation of Docker images can take up to three minutes


Thereafter, all services can be initialized from the command line by running the [services](https://github.com/Fiware/tutorials.Securing-Access/blob/master/services) Bash script provided within the repository:

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


### Dramatis Personae

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

![](https://fiware.github.io/tutorials.Securing-Access/img/keyrock-log-in.png)

and look around.





---

## License

[MIT](LICENSE) © FIWARE Foundation e.V.












