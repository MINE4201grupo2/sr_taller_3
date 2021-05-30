library(dplyr)
library(recommenderlab)
library(magrittr)
library(tidyverse)
library(reshape2)
library(readr)

userid_timestamp_artid_artname_traid_traname <- read_delim("C:/Users/Acer/Downloads/lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv", 
                                                             +     "\t", escape_double = FALSE, col_names = FALSE, 
                                                             +     trim_ws = TRUE)
Artistas<-group_by(userid_timestamp_artid_artname_traid_traname,X1,X4)
ArtistasA<-summarise(Artistas,Plays=n())
ArtistasB<-group_by(ArtistasA,X1)
ArtistasB<-summarise(ArtistasA,max(Plays))
ArtistasC<-left_join(ArtistasA,ArtistasB)
ArtistasC$rating<-round(ArtistasC$Plays*5/ArtistasC$`max(Plays)`,6)
ArtistasC$user_id<-substr(ArtistasC$X1,nchar(ArtistasC$X1)-3,nchar(ArtistasC$X1))
Artistas_Final<-data.frame(user_id=ArtistasC$user_id,artist_name=ArtistasC$X4,rating=ArtistasC$rating)

write_delim(Artistas_Final,"C:/Users/Acer/Documents/Artistas_Final.csv",delim="\t")



Tracks<-group_by(userid_timestamp_artid_artname_traid_traname,X1,X6)
TracksA<-summarise(Tracks,Plays=n())
TracksB<-group_by(TracksA,X1)
TracksB<-summarise(TracksA,max(Plays))
TracksC<-left_join(TracksA,TracksB)
TracksC$rating<-round(TracksC$Plays*5/TracksC$`max(Plays)`,6)
TracksC$user_id<-substr(TracksC$X1,nchar(TracksC$X1)-3,nchar(TracksC$X1))
Tracks_Final<-data.frame(user_id=TracksC$user_id,track_name=TracksC$X6,rating=TracksC$rating)

write_delim(Tracks_Final,"C:/Users/Acer/Documents/Tracks_Final.csv",delim="\t")
