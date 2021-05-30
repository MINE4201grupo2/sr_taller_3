use taller3;

create INDEX IX_users_user_ID on users(user_id);
create INDEX IX_recomendations_business_user_ID on recomendations_movies(user_id);
create INDEX IX_business_business_ID on movies(movies_id);