import redis, { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => console.log(`Redis client not connected to the \
server: ${err.message}`));

client.on('ready', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, data) => {
    if (err) console.log(err.message);
    console.log(data);
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
