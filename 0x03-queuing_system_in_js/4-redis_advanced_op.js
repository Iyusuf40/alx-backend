import redis from 'redis';

const client = redis.createClient();

client.on('error', (err) => console.log(`Redis client not connected to the \
server: ${err.message}`));

client.on('ready', () => console.log('Redis client connected to the server'));

const arr = [
  ['Portland', 50],
  ['Seattle', 80],
  ['New York', 20],
  ['Bogota', 20],
  ['Cali', 40],
  ['Paris', 2],
];

for (const [key, val] of arr) {
  client.hset('HolbertonSchools', key, val, redis.print);
}

client.hgetall('HolbertonSchools', (err, data) => {
  if (err) console.log(err.message);
  console.log(data);
});
