DROP TABLE Users CASCADE CONSTRAINTS;
DROP TABLE Movies CASCADE CONSTRAINTS;
DROP TABLE Screens CASCADE CONSTRAINTS;
DROP TABLE Shows CASCADE CONSTRAINTS;
DROP TABLE Seats CASCADE CONSTRAINTS;
DROP TABLE Bookings CASCADE CONSTRAINTS;

CREATE TABLE Users (
    user_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    password VARCHAR2(100) NOT NULL,
    status VARCHAR2(10) CHECK (status IN ('admin', 'customer'))
);

CREATE TABLE Movies (
    movie_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR2(100) NOT NULL,
    duration NUMBER CHECK (duration > 0)
);

CREATE TABLE Screens (
    screen_id NUMBER PRIMARY KEY,
    seat_count NUMBER CHECK (seat_count > 0)
);

CREATE TABLE Shows (
    show_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    movie_id NUMBER REFERENCES Movies(movie_id) ON DELETE CASCADE,
    screen_id NUMBER REFERENCES Screens(screen_id) ON DELETE CASCADE,
    show_time TIMESTAMP,
    UNIQUE(screen_id, show_time)
);

CREATE TABLE Seats (
    seat_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    screen_id NUMBER REFERENCES Screens(screen_id) ON DELETE CASCADE,
    show_id NUMBER REFERENCES Shows(show_id) ON DELETE CASCADE,
    seat_number VARCHAR2(5),
    is_booked CHAR(1) DEFAULT 'N' CHECK (is_booked IN ('Y', 'N')),
    UNIQUE(show_id, seat_number)
);

CREATE TABLE Bookings (
    booking_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id NUMBER REFERENCES Users(user_id) ON DELETE CASCADE,
    show_id NUMBER REFERENCES Shows(show_id) ON DELETE CASCADE,
    screen_id NUMBER REFERENCES Screens(screen_id) ON DELETE CASCADE,
    seat_number VARCHAR2(5),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE OR REPLACE TRIGGER populate_seats_for_new_show
AFTER INSERT ON Shows
FOR EACH ROW
DECLARE
    seat_count NUMBER;
BEGIN
    SELECT s.seat_count INTO seat_count
    FROM Screens s
    WHERE s.screen_id = :NEW.screen_id;

    -- populate the seats for the new show
    FOR i IN 1..seat_count LOOP
        INSERT INTO Seats (screen_id, show_id, seat_number) 
        VALUES (:NEW.screen_id, :NEW.show_id, 'A' || i);
    END LOOP;
END;
/

--checks for shows screening on the same screen
CREATE OR REPLACE TRIGGER check_show_conflict
BEFORE INSERT ON Shows
FOR EACH ROW
DECLARE
    conflict_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO conflict_count
    FROM Shows
    WHERE screen_id = :NEW.screen_id
      AND show_time = :NEW.show_time;

    IF conflict_count > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Conflict: A movie is already scheduled on this screen at this time.');
    END IF;
END;
/


CREATE OR REPLACE PROCEDURE book_seat(
    p_show_id IN NUMBER,
    p_seat_number IN VARCHAR2,
    p_user_id IN NUMBER
) AS
    v_is_booked CHAR(1);
BEGIN
    SELECT is_booked INTO v_is_booked
    FROM Seats
    WHERE show_id = p_show_id AND seat_number = p_seat_number;

    IF v_is_booked = 'Y' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Seat is already booked!');
    END IF;

    UPDATE Seats
    SET is_booked = 'Y'
    WHERE show_id = p_show_id AND seat_number = p_seat_number;

    INSERT INTO Bookings ( user_id,show_id, seat_number)
    VALUES ( p_user_id,p_show_id, p_seat_number);

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE cancel_booking (
    p_user_id NUMBER,
    p_show_id NUMBER,
    p_seat_number VARCHAR2
) AS
BEGIN
    DELETE FROM Bookings
    WHERE user_id = p_user_id
      AND show_id = p_show_id
      AND seat_number = p_seat_number;

    UPDATE Seats
    SET is_booked = 'N'
    WHERE show_id = p_show_id
      AND seat_number = p_seat_number
      AND is_booked = 'Y';

    COMMIT;
END;
/

-- sample data -- MODIFY THE DATES AS THE OLD MOVIES WILL BE AUTOMATICALLY REMOVED FROM THE LIST

INSERT INTO Users (username, password, status) VALUES ('admin_user', 'admin123', 'admin');
INSERT INTO Users (username, password, status) VALUES ('customer1', 'pass123', 'customer');
INSERT INTO Users (username, password, status) VALUES ('customer2', 'pass456', 'customer');

INSERT INTO Movies (title, duration) VALUES ('The Journey', 120);
INSERT INTO Movies (title, duration) VALUES ('Space Adventure', 150);
INSERT INTO Movies (title, duration) VALUES ('Comedy Night', 90);

INSERT INTO Screens (screen_id, seat_count) VALUES (1, 50); 
INSERT INTO Screens (screen_id, seat_count) VALUES (2, 30);  

INSERT INTO Shows (movie_id, screen_id, show_time) 
VALUES (1, 1, TO_TIMESTAMP('2025-11-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));

INSERT INTO Shows (movie_id, screen_id, show_time) 
VALUES (2, 1, TO_TIMESTAMP('2025-11-15 17:00:00', 'YYYY-MM-DD HH24:MI:SS'));

INSERT INTO Shows (movie_id, screen_id, show_time) 
VALUES (3, 2, TO_TIMESTAMP('2025-11-15 17:00:00', 'YYYY-MM-DD HH24:MI:SS'));

INSERT INTO Movies (title, duration) VALUES ('Mama Mia ', 90);

INSERT INTO Shows (movie_id, screen_id, show_time) 
VALUES (4, 1, TO_TIMESTAMP('2025-11-15 20:00:00', 'YYYY-MM-DD HH24:MI:SS'));
commit;



