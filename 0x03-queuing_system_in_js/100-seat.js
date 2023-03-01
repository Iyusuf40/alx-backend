import redis from 'redis';
import util from 'util';
import express from 'express';
import kue from 'kue';

const redisClient = redis.createClient();
redisClient.get = util.promisify(redisClient.get);

let reservationEnabled = false;

const q = kue.createQueue();

redisClient.on('error', (err) => {
  console.log(`Error from redis client${err.message}`);
});

function reserveSeat(number) {
  redisClient.set('available_seats', number, (err) => {
    if (err) return console.log(`could not set avaialable_seats: ${err.message}`);
    console.log(`available_seats set to: ${number}`);
    if (number) reservationEnabled = true;
    return null;
  });
}

redisClient.on('ready', () => reserveSeat(50));

async function getCurrentAvailableSeats() {
  const availSeats = await redisClient.get('available_seats');
  return availSeats;
}

function processQ(q) {
  q.process('reserve_seat', (job, done) => {
    getCurrentAvailableSeats()
      .then((availSeats) => {
        if (availSeats > 1) {
          reserveSeat(availSeats - 1);
          done();
          return;
        }
        const newAvailSeats = availSeats - 1;
        if (newAvailSeats === 0) {
          reserveSeat(newAvailSeats);
          reservationEnabled = false;
          done();
          return;
        }
        reservationEnabled = false;
        if (newAvailSeats < 0) {
          done(new Error('Not enough seats available'));
        }
        reserveSeat(0);
        done();
      });
  });
}

const app = express();
app.use(express.json());

app.get('/available_seats', (req, res) => {
  getCurrentAvailableSeats()
    .then((num) => res.send({ numberOfAvailableSeats: num }));
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.send({ status: 'Reservation are blocked' });
  }
  const job = q.create('reserve_seat');
  job.save((err) => {
    if (err) {
      return res.send({ status: 'Reservation failed' });
    }
    return null;
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (err) => console.log(`Seat reservation job ${job.id} \
failed: ${err}`));
  return res.send({ status: 'Reservation in process' });
});

app.get('/process', (req, res) => {
  processQ(q);
  return res.send({ status: 'Queue processing' });
});

app.post('/create_seats', (req, res) => {
  const numberOfSeatsToCreate = Number(req.body.number_of_seats);
  if (!numberOfSeatsToCreate) {
    return res.send({ status: 'failed' });
  }
  reserveSeat(numberOfSeatsToCreate);
  return res.send({ status: `${numberOfSeatsToCreate} seats created` });
});

app.listen(1245, () => {
  console.log('read to serve, port 1245');
});
