use taller1;

CREATE TABLE IF NOT EXISTS `users`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) NOT NULL UNIQUE,
    `gender` char(1) DEFAULT NULL,
    `age` int(11) DEFAULT NULL,
    `country` varchar(255) DEFAULT NULL,
    `password` varchar(255) NOT NULL, 
    `created_at` datetime NOT NULL, 
    `updated_at` datetime NOT NULL, 
    PRIMARY KEY (`id`));


CREATE TABLE IF NOT EXISTS `user_listening_habits`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL UNIQUE,
    `track_id` int(11) DEFAULT NULL,
    `artist_id` int(11) DEFAULT NULL,
    `recomendation_score` decimal(4,4) DEFAULT NULL,
    `created_at` datetime NOT NULL, 
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`track_id`) REFERENCES `tracks`(`id`),
    FOREIGN KEY (`artist_id`) REFERENCES `artists`(`id`));

CREATE TABLE IF NOT EXISTS `tracks`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `music_track_id` varchar(100) DEFAULT NULL,
    `music_track_name` varchar(500) DEFAULT NULL,
    PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `artists`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `music_artist_id` varchar(100) DEFAULT NULL,
    `music_artist_name` varchar(500) DEFAULT NULL,
    PRIMARY KEY (`id`));

ALTER TABLE artists CONVERT TO CHARACTER SET utf8;
ALTER TABLE tracks CONVERT TO CHARACTER SET utf8;
-- show tables;
DROP TABLE IF EXISTS `preferences`;
DROP TABLE IF EXISTS `preferences_artists`;
DROP TABLE IF EXISTS `preferences_tracks`;
CREATE TABLE IF NOT EXISTS `preferences_artists`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `artist_name` varchar(255) DEFAULT NULL,
    `score` int(11) DEFAULT 5,
    `created_at` datetime NOT NULL, 
    PRIMARY KEY (`id`,`user_id` ),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`));

CREATE TABLE IF NOT EXISTS `preferences_tracks`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `track_name` varchar(255) DEFAULT NULL,
    `created_at` datetime NOT NULL, 
    `score` int(11) DEFAULT 5,
    PRIMARY KEY (`id`,`user_id` ),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`));
ALTER TABLE preferences_tracks CONVERT TO CHARACTER SET utf8;
ALTER TABLE preferences_artists CONVERT TO CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS `recomendations_tracks`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `track_name` varchar(255) DEFAULT NULL,
    `recomendation_score` decimal(2,1) DEFAULT NULL,
    `model` varchar(15) DEFAULT 'coseno',
    `tipo_modelo` varchar(15) DEFAULT 'item', 
    `created_at` datetime default NOW(), 
    PRIMARY KEY (`id`,`user_id` ),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`));

CREATE TABLE IF NOT EXISTS `recomendations_artists`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `artist_name` varchar(255) DEFAULT NULL,
    `recomendation_score` decimal(2,1) DEFAULT NULL,
    `model` varchar(15) DEFAULT 'coseno',
    `tipo_modelo` varchar(15) DEFAULT 'item',
    `created_at` datetime default NOW(), 
    PRIMARY KEY (`id`,`user_id` ),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`));

ALTER TABLE recomendations_artists CONVERT TO CHARACTER SET utf8;
ALTER TABLE recomendations_tracks CONVERT TO CHARACTER SET utf8;