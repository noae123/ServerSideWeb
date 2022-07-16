create table users
(
    id       int(255) auto_increment not null,
    fname    varchar(255) not null,
    lname    varchar(255) not null,
    email    varchar(255) not null,
    password varchar(255) not null,
    primary key (email),
    constraint unique_email
        unique (email),
    constraint unique_id
        unique (id)
);

INSERT INTO ex4.users (id, fname, lname, email, password) VALUES (1, 'maya', 'assulyn', 'pedacop128@mahazai.com', '1234');
INSERT INTO ex4.users (id, fname, lname, email, password) VALUES (2, 'noa', 'elharar', 'pongau@24hinbox.com', '1234');
INSERT INTO ex4.users (id, fname, lname, email, password) VALUES (3, 'benny', 'xar', 'progport@bomukic.com', '1234');
INSERT INTO ex4.users (id, fname, lname, email, password) VALUES (4, 'shelly', 'shabty', 'w5ui8@bitcoinandmetals.com', '1234');
INSERT INTO ex4.users (id, fname, lname, email, password) VALUES (5, 'jj', 'shefi', 'elsukov5@uhpanel.com', '1234');
