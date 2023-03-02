const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'myproject';

let db = null
let flag = false
let globalClient = null;

// Use connect method to connect to the server

MongoClient.connect(url, {useUnifiedTopology: true}, function(err, client) {
  if (err) return console.log(`Could not connect: ${err}`)

  globalClient = client;

  flag = true
});

async function closeClient() {
  if (globalClient) return globalClient.close()
  throw new Error('client doesnt exist');
}

async function connectToMongo() {
  let timer = 0
  while (flag === false) {
    if (timer > 1500) throw new Error('taking too long to connect')
    const res = await wait()
    timer += 30
  }
  console.log('connection established')
  // console.log(db)

  // closeClient()
  return (db)
}

function wait() {
  return new Promise((res) => setTimeout(() => res('waiting'), 30))
}

async function getDb(dbName) {
  await connectToMongo()
  db = globalClient.db(dbName);
  return db
}

getDb('hello')
.then((db) => {
  console.log(db)
  closeClient()
})
