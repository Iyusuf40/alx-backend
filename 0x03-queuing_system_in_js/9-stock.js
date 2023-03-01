import redis from 'redis';
import util from 'util';
import express from 'express';

const redisClient = redis.createClient();
redisClient.hget = util.promisify(redisClient.hget);

redisClient.on('error', (err) => {
  console.log(`Error from redis client${err.message}`);
});

const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

function getItemById(id) {
  return listProducts.find((itm) => itm.Id === id);
}

function transformListProducts(listProducts) {
  const list = [];
  for (const item of listProducts) {
    const transformedItem = {};
    for (const key in item) {
      switch (key) {
        case 'Id':
          transformedItem.itemId = item.Id;
          break;
        case 'name':
          transformedItem.itemName = item.name;
          break;
        case 'price':
          transformedItem.price = item.price;
          break;
        case 'stock':
          transformedItem.initialAvailableQuantity = item.stock;
          break;
      }
    }
    list.push(transformedItem);
  }
  return list;
}

function reserveStockById(itemId, stock) {
  redisClient.hset('stock', itemId.toString(), stock, (err, resp) => {
    if (err) return console.log(`error while stting stock ${err.message}`);
    console.log(`item with id ${itemId} current stock set to ${stock}`);
  });
}

async function getCurrentReservedStockById(itemId) {
  const stock = await redisClient.hget('stock', itemId.toString());
  return Number(stock);
}

const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  res.send(['hello from server']);
});

app.get('/list_products', (req, res) => {
  res.send(transformListProducts(listProducts));
});

app.get('/list_products/:itemId', (req, res) => {
  const id = Number(req.params.itemId);
  const item = getItemById(id);
  if (!item) {
    res.status(404).send({ status: 'Product not found' });
    return;
  }
  res.send(transformListProducts([item]));
});

app.get('/reserve_product/:itemId', (req, res) => {
  const id = Number(req.params.itemId);
  const item = getItemById(id);
  if (!item) {
    res.status(404).send({ status: 'Product not found' });
    return;
  }
  if (!item.stock) {
    res.send({ status: 'Not enough stock available', itemId: id });
  } else {
    reserveStockById(id, 1);
    res.send({ status: 'Reservation confirmed', itemId: id });
  }
  /* getCurrentReservedStockById(id)
  .then((stock) => {
    if (!stock) {
      res.send({"status": "Not enough stock available","itemId": id})
    } else {
      reserveStockById(id, 1)
      res.send({"status": "Reservation confirmed", "itemId": id})
    }
  }) */
});

app.listen(1245, () => {
  console.log('read to serve, port 1245');
});
