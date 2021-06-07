use taller3;

CREATE TABLE IF NOT EXISTS `users`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` varchar(255) NOT NULL UNIQUE,
    `email` varchar(255) NOT NULL UNIQUE,
    `password` varchar(255) NOT NULL, 
    `created_at` datetime default NOW(), 
    `updated_at` datetime  default NOW(), 
    PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `movies`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `movies_id` varchar(100) DEFAULT NULL,
    `title` varchar(500) DEFAULT NULL,
    `genres` varchar(500) DEFAULT NULL,
    PRIMARY KEY (`id`));

ALTER TABLE movies CONVERT TO CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS `recomendations_movies`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `movie_id` varchar(255) DEFAULT NULL,
    `recomendation_score` decimal(2,1) DEFAULT NULL,
    `model` varchar(15) DEFAULT 'coseno',
    `tipo_modelo` varchar(15) DEFAULT 'item', 
    `created_at` datetime default NOW(), 
    PRIMARY KEY (`id`,`user_id` )
    );

ALTER TABLE recomendations_movies CONVERT TO CHARACTER SET utf8;

DROP TABLE IF EXISTS `preferences`;
CREATE TABLE IF NOT EXISTS `preferences`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `movie_id` varchar(255) DEFAULT NULL,
    `score` int(11) DEFAULT 5,
    `created_at` datetime NOT NULL, 
    PRIMARY KEY (`id`,`user_id` ),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`));