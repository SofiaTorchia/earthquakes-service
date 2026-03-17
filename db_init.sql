CREATE TABLE if not exists users (
    id SERIAL PRIMARY KEY, 
    user_name varchar, 
    user_surname varchar, 
    user_phone varchar, 
    user_address varchar
);

INSERT INTO users (id, user_name, user_surname, user_phone, user_address)
VALUES
    (1, 'John', 'Doe', '1234567890', '123 Main Street'),
    (2, 'GG', 'Project', '887733402', 'Via Tonale 331'),
    (3, 'Fabio', 'Nonso', '23643724184', 'Via Degli Spiriti 5'),
    (4, 'Alfreda', 'Gianni', '842936428', 'Via Vai 55'),
    (5, 'Mala', 'Grotta', '330022485', 'Via di Mala Grotta 29'),
    (6, 'Fede', 'Rica', '297518471', 'Via Costa Rica 86')
on conflict (id) do update set
    user_name = excluded.user_name,
    user_surname = excluded.user_surname,
    user_phone = excluded.user_phone,
    user_address = excluded.user_address;


