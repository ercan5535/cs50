-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE description LIKE "%cs50%"
--295 | 2021 | 7 | 28 | Humphrey Street |
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

SELECT * FROM interviews WHERE day = 28 AND month = 7 and year = 2021 AND transcript LIKE "%Bakery%";
--id | name | year | month | day | transcript
--161 | Ruth | 2021 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--162 | Eugene | 2021 | 7 | 28 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
--163 | Raymond | 2021 | 7 | 28 | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


--The caller(phone number) who calls on that date and talked less than a minute
SELECT caller FROM phone_calls
    WHERE day = 28 AND month = 7 AND year = 2021 AND duration < 60

--The accounts number which withdraw at that date on the Leggett Street
SELECT account_number FROM atm_transactions
    WHERE day = 28 AND month = 7 and year = 2021 AND
    transaction_type = "withdraw" AND atm_location LIKE "%Leggett%"

--The license plates which are moved around bakery within ten minutes and its activity exit
SELECT license_plate FROM bakery_security_logs
    WHERE day = 28 AND month = 7 AND year = 2021 AND hour = 10
    AND minute >= 15 AND minute <= 25 AND activity = "exit";

-- Passport numbers who has flight for tomorrow earliest flight
SELECT passport_number FROM passengers
    WHERE passengers.flight_id = (
        SELECT flights.id from flights
        JOIN airports ON flights.origin_airport_id = airports.id
        WHERE flights.day = 29 AND flights.month = 7 AND flights.year = 2021
        AND airports.full_name LIKE "%Fiftyville%"
        ORDER BY hour, minute LIMIT 1)


-- Query for all evidance at once
SELECT DISTINCT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE people.phone_number IN
    (SELECT caller FROM phone_calls
    WHERE day = 28 AND month = 7 AND year = 2021 AND duration < 60)
AND
people.license_plate IN
    (SELECT license_plate FROM bakery_security_logs
    WHERE day = 28 AND month = 7 AND year = 2021 AND hour = 10
    AND minute >= 15 AND minute <= 25 AND activity = "exit")
AND
bank_accounts.account_number IN
    (SELECT account_number FROM atm_transactions
    WHERE day = 28 AND month = 7 and year = 2021 AND
    transaction_type = "withdraw" AND atm_location LIKE "%Leggett%")
AND
people.passport_number IN
    (SELECT passport_number FROM passengers
    WHERE passengers.flight_id = (
        SELECT flights.id from flights
        JOIN airports ON flights.origin_airport_id = airports.id
        WHERE flights.day = 29 AND flights.month = 7 AND flights.year = 2021
        AND airports.full_name LIKE "%Fiftyville%"
        ORDER BY hour, minute LIMIT 1));
-- Thief is Bruce!


-- To find where he is going, check destination of earliest flight from Fiftyville
SELECT city FROM airports
WHERE id = (SELECT destination_airport_id from flights
        JOIN airports ON flights.origin_airport_id = airports.id
        WHERE flights.day = 29 AND flights.month = 7 AND flights.year = 2021
        AND airports.full_name LIKE "%Fiftyville%"
        ORDER BY hour, minute LIMIT 1);
-- It is New York City!

-- To find accomplice, check Bruce called who?
SELECT DISTINCT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE day = 28 AND month = 7 AND year = 2021 AND duration < 60
    AND caller = (
        SELECT phone_number FROM people
        WHERE name = "Bruce"));
-- Accomplice is Robin!

