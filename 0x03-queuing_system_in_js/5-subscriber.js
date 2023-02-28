import redis from 'redis';

const client = redis.createClient();

client.on('error', (err) => console.log(`Redis client not connected to the \
server: ${err.message}`));

client.on('ready', () => console.log('Redis client connected to the server'));

client.subscribe('holberton school channel');

client.on('message', (channel, msg) => {
  console.log(msg);
  if (msg === 'KILL_SERVER') client.unsubscribe();
});
