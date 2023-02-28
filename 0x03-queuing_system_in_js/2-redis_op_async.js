import redis from 'redis';
import util from 'util';

const client = redis.createClient();
client.get = util.promisify(client.get);

client.on('error', (err) => console.log(`Redis client not connected to the \
server: ${err.message}`));

client.on('ready', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
  const data = await client.get(schoolName);
  console.log(data);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
