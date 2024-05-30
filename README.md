[![FIWARE Banner](https://fiware.github.io/tutorials.PEP-Proxy/img/fiware.png)](https://www.fiware.org/developers)

[![FIWARE Security](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/security.svg)](https://github.com/FIWARE/catalogue/blob/master/security/README.md)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.PEP-Proxy.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/tag-fiware-orange.svg?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/fiware)

This tutorial uses the FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) PEP Proxy combined with **Keyrock** to secure
access to endpoints exposed by FIWARE generic enablers. Users (or other actors) must log-in and use a token to gain
access to services. The application code created in the
[previous tutorial](https://github.com/FIWARE/tutorials.Securing-Access) is expanded to authenticate users throughout a
distributed system. The design of FIWARE Wilma - a PEP Proxy is discussed, and the parts of the Keyrock GUI and REST API
relevant to authenticating other services are described in detail.

[cUrl](https://ec.haxx.se/) commands are used throughout to access the **Keyrock** and **Wilma** REST APIs -
[Postman documentation](https://www.postman.com/downloads/) for these calls is also available.

# Start-Up

## NGSI-v2 Smart Supermarket

**NGSI-v2** offers JSON based interoperability used in individual Smart Systems. To run this tutorial with **NGSI-v2**, use the `NGSI-v2` branch.

```console
git clone https://github.com/FIWARE/tutorials.PEP-Proxy.git
cd tutorials.PEP-Proxy
git checkout NGSI-v2

./services create
./services start
```

| [![NGSI v2](https://img.shields.io/badge/NGSI-v2-5dc0cf.svg)](https://fiware-ges.github.io/orion/api/v2/stable/) | :books: [Documentation](https://github.com/FIWARE/tutorials.PEP-Proxy/tree/NGSI-v2) |  | <img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/postman.svg" height="15" width="15"> [Postman Collection](https://fiware.github.io/tutorials.PEP-Proxy/) |
| --- | --- | --- |


<!--
## NGSI-LD Smart Farm

**NGSI-LD** offers JSON-LD based interoperability used for Federations and Data Spaces. To run this tutorial with **NGSI-LD**, use the `NGSI-LD` branch.

```console
git clone https://github.com/FIWARE/tutorials.PEP-Proxy.git
cd tutorials.PEP-Proxy
git checkout NGSI-LD

./services create
./services start
```

| [![NGSI LD](https://img.shields.io/badge/NGSI-LD-d6604d.svg)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/gs_cim009v010801p.pdf) | :books: [Documentation](https://github.com/FIWARE/tutorials.PEP-Proxy/tree/NGSI-LD) | <img  src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/postman.svg" height="15" width="15"> [Postman Collection](https://fiware.github.io/tutorials.PEP-Proxy/ngsi-ld.html) |
| --- | --- | --- |

-->

---

## License

[MIT](LICENSE) © 2018-2024 FIWARE Foundation e.V.
