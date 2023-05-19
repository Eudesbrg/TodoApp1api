
-- clean the database
DROP TABLE IF EXISTS user_role;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS todos;

-- create all table
CREATE TABLE role (
    id INTEGER PRIMARY KEY,
    title VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL
);

CREATE TABLE user_role (
    role_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role (id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT user_rolePK PRIMARY KEY (role_id,user_id)
);

CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- populate all tables with test data
INSERT INTO role (id,title) VALUES (1,"view"),(2,"edit"),(3,"delete"),(4,"create");
INSERT INTO user (email,username) VALUES ("userid1@mail.net","user1"),("userid2@mail.net","user2"),("userid3@mail.net","user3"),("userid4@mail.net","user4"),("userid5@mail.net","user5");
INSERT INTO todos (message,user_id) VALUES ("task 1 of user 1", 1),("task 2 of user 1", 1),("task 3 of user 1", 1),("task 4 of user 1", 1),("task 5 of user 1", 1),
                                            ("task 1 of user 2", 2),("task 2 of user 2", 2),("task 3 of user 2", 2),("task 4 of user 2", 2),("task 5 of user 2", 2),
                                            ("task 1 of user 3", 3),("task 2 of user 3", 3),("task 3 of user 3", 3),("task 4 of user 3", 3),("task 5 of user 3", 3),
                                            ("task 1 of user 4", 4),("task 2 of user 4", 4),("task 3 of user 4", 4),("task 4 of user 4", 4),("task 5 of user 4", 4),
                                            ("task 1 of user 5", 5),("task 2 of user 5", 5),("task 3 of user 5", 5),("task 4 of user 5", 5),("task 5 of user 5", 5);

INSERT INTO user_role (role_id,user_id) VALUES (1,1),(2,1),(3,1),(4,1),
                                                (1,2),
                                                (1,3),(2,3),
                                                (1,4),(2,4),(3,4),
                                                (1,5),(2,5),(3,5),(4,5);