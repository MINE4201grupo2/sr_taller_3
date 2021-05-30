module.exports = (app) => {
  const { lstatSync, readdirSync } = require('fs');
  const { join } = require('path');

  const isDirectory = (source) => lstatSync(source).isDirectory();

  const getDirectories = (source) => readdirSync(source).map((name) => join(source, name)).filter(isDirectory);
  _.forEach(getDirectories(__dirname), (d) => {
    // eslint-disable-next-line import/no-dynamic-require
    require(d)(app);
  });

  const w = _.random(10000);
  app.get('/status', (req, res) => {
    const memory = process.memoryUsage();
    res.send({
      w,
      v: config.v,
      rss: memory.rss / 1048576,
      heapTotal: memory.heapTotal / 1048576,
      heapUsed: memory.heapUsed / 1048576
    });
  });
};
