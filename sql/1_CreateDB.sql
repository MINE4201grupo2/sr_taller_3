-- http://coding-karma.com/2017/08/12/creating-login-registration-using-nodejs-mysql/
create database taller1;
show databases;
use taller1;

CREATE USER 'user_taller1'@'localhost' IDENTIFIED BY 'taller1.';
GRANT ALL PRIVILEGES ON taller1.* TO 'user_taller1'@'localhost';
FLUSH PRIVILEGES;

