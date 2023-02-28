import kue from 'kue';

const q = kue.createQueue();

const qdata = {
  phoneNumber: '01-1111-95-443',
  message: 'this data is common to all queus',
};

const job = q.create('push_notification_code', qdata).save((err) => {
  if (err) console.log('Notification job failed');
  console.log(`Notification job created: ${job.id}`);
});

job.on('complete', () => console.log('Notification job completed'));
