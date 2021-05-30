global._ = require('lodash');

const vars = {
  tz: 'America/Bogota',
  minPassword: 6,
};
_.forEach(vars, (v, i) => {
  global[i] = v;
});
