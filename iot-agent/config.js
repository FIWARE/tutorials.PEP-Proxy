var config = {};


config.mqtt = {
    host: 'mosquitto',
    port: 1883,
    qos: 0,
    retain: false
};

config.amqp = {
    host: 'localhost',
    port: 5672,
    // username: 'guest',
    // password: 'guest',
    exchange: 'iota-exchange',
    queue: 'iotaqueue',
    options: {durable: true}
};

config.http = {
    port: 7896
};

config.iota = {

    authentication:  {
        enabled: true,
        type: 'keystone',
        header: 'X-Auth-Token',
        host: '172.18.1.5',
        port: '3005',
        user: 'iot_sensor_00000000-0000-0000-0000-000000000000',
        password: 'test'
    },

    ngsiVersion: 'v2',
    logLevel: 'DEBUG',
    timestamp: true,
    contextBroker: {
        host: 'orion',
        port: '1026'
    },
    server: {
        port: 4041
    },
    deviceRegistry: {
        type: 'mongodb'
    },
    mongodb: {
        host: 'mongo',
        port: '27017',
        db: 'iotagentul'
    },
    types: {},
    service: 'howtoService',
    subservice: '/howto',
    providerUrl: 'http://localhost:4041',
    deviceRegistrationDuration: 'P1M',
    defaultType: 'Thing'
};

config.defaultKey = 'TEF';

module.exports = config;