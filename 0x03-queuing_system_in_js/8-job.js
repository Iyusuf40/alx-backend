export default function createPushNotificationsJobs(jobs, queue) {
  const q = queue;
  if (!(Array.isArray(jobs))) throw new Error('Jobs is not an array');
  for (const data of jobs) {
    const job = q.create('push_notification_code_3', data)
    job.save(function(err) {
      if (err) console.log(`Notification job failed: ${err.message}`);
      console.log(`Notification job created: ${job.id}`);
    });
    job.on('failed', (err) => console.log(`Notification job ${job.id} \
failed: ${err}`));
    job.on('complete', () => console.log(`Notification job ${job.id} completed`));
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  }
}
