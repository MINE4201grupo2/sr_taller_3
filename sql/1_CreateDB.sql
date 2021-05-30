-- http://coding-karma.com/2017/08/12/creating-login-registration-using-nodejs-mysql/
create database taller3;
show databases;
use taller3;

CREATE USER 'user_taller3'@'localhost' IDENTIFIED BY 'taller3.';
GRANT ALL PRIVILEGES ON taller3.* TO 'user_taller3'@'localhost';
FLUSH PRIVILEGES;

