'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    email: DataTypes.STRING,
    gender: DataTypes.STRING,
    age: DataTypes.STRING,
    country: DataTypes.STRING,
    user_email: {type:DataTypes.STRING, unique: true},
    user_password: DataTypes.STRING
  }, {});
  return User;
};