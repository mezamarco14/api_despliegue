const { Client } = require('cassandra-driver');
require('dotenv').config();

const client = new Client({
    contactPoints: [process.env.CASSANDRA_HOST],
    localDataCenter: 'datacenter1', // Cambia esto según tu configuración
});

client.connect()
    .then(() => console.log('Conectado a Cassandra'))
    .catch(err => console.error('Error conectando a Cassandra', err));

module.exports = client;
