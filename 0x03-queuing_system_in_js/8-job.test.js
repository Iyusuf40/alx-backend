import kue from 'kue';
import assert from 'assert';
import createPushNotificationsJobs from './8-job';

const q = kue.createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account',
  },
];

before(() => {
  q.testMode.enter();
});

afterEach(() => {
  q.testMode.clear();
});

after(() => {
  q.testMode.clear();
  q.testMode.exit();
});

describe('test for createPushNotificationsJobs function', () => {
  it('should create 2 jobs successfully', () => {
    createPushNotificationsJobs(jobs, q);
    assert.equal(q.testMode.jobs.length, 2);
    assert.deepEqual(q.testMode.jobs[0].data, jobs[0]);
  });
  it('should throw Jobs is not an array error', () => {
    const err = () => createPushNotificationsJobs('stringsEveryWhere', q);
    assert.throws(err, new Error('Jobs is not an array'));
  });
});
