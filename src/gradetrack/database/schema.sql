DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT NOT NULL,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id       INTEGER NOT NULL,
    group_id      INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles (role_id),
    FOREIGN KEY (group_id) REFERENCES groups (group_id)
);

CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE
);

CREATE TABLE grades (
    grade_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    value      INTEGER NOT NULL,
    grade_date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
);

INSERT INTO roles (role_id, name) VALUES
    (1, 'Администратор'),
    (2, 'Преподаватель'),
    (3, 'Студент');

INSERT INTO groups (group_id, name) VALUES
    (1, '26-ИВТ-1'),
    (2, '26-ИВТ-2');

INSERT INTO subjects (subject_id, name) VALUES
    (1, 'Информатика'),
    (2, 'Математический анализ'),
    (3, 'Программирование на Python');

INSERT INTO users (user_id, full_name, login, password_hash, role_id, group_id) VALUES
    (1, 'Администратор', 'admin', '1a0a027f9afcf59bcc9e9b52c35eb759$f21a994c09dbda3f74d8d1493862d3d5b75890a5acd61db445587830e78d7b04', 1, NULL),
    (2, 'Смирнова Ольга Викторовна', 'teacher', '092889efe99eabc1976162f345ebd71a$20ac049c0577a6ee457b293493df0e49a267dbd1fcf67d2b7b63b6da0126a471', 2, NULL),
    (3, 'Андреев Максим Игоревич', 'andreev', '9a76e15d2bd24d445d340a35c69cddd5$ae71422813a6b398d717678267218171ee0a5fc23d665c5b41a4380483f6db1c', 3, 1),
    (4, 'Борисова Дарья Сергеевна', 'borisova', '3f208006875251e813fe263f6f7bb30f$7aff2c28f316bf40693035c5a1ae3b19c59bb94da1a6024970662f6545f6576c', 3, 1),
    (5, 'Волков Кирилл Андреевич', 'volkov', 'd1e72e2c712d0def9c8b3b56f5f02549$b34b8383b3db39ab580b17199b36f0ddb538e02dcd8783e214c09b120d2346fb', 3, 1),
    (6, 'Григорьева Полина Олеговна', 'grigoreva', '7928932411e358325c7aeee6192955d0$d9e052f22c646d984ef5497e5d5364bd868a3091c0a79dcfe41efa25667e77d0', 3, 2),
    (7, 'Дмитриев Артём Денисович', 'dmitriev', 'f5ecf758d30af3a43e1b94622ee392d5$2b4ebe74528a32bd5a0b8ee69c61920388d0377889a2c39d490749a1490b41d9', 3, 2),
    (8, 'Егорова Софья Максимовна', 'egorova', '90e7437318e7ad280037e2c1dc4f2455$cff58551fd6b53a808201f081fa7dcf6f0597dc3159a0e4c009dd458e530e773', 3, 2);

INSERT INTO grades (student_id, subject_id, value, grade_date) VALUES
    (3, 1, 5, '2026-10-05'),
    (3, 1, 4, '2026-10-12'),
    (3, 2, 4, '2026-10-07'),
    (3, 3, 5, '2026-10-09'),
    (4, 1, 4, '2026-10-05'),
    (4, 2, 3, '2026-10-07'),
    (4, 3, 4, '2026-10-09'),
    (5, 1, 3, '2026-10-05'),
    (5, 2, 2, '2026-10-07'),
    (6, 1, 5, '2026-10-06'),
    (6, 2, 5, '2026-10-08'),
    (6, 3, 4, '2026-10-12'),
    (7, 1, 4, '2026-10-06'),
    (7, 2, 4, '2026-10-08'),
    (8, 1, 3, '2026-10-06'),
    (8, 3, 5, '2026-10-12');
