create schema if not exists prescriptions;
use prescriptions;
create table prescription(
    `bookingID` int NOT NULL, # changed this to bookingID from jobid to be consistent with booking microservice
    `doctorID` varchar(2) NOT NULL,
    `customerID` varchar(2) NOT NULL,
    `prescription` varchar(500) not null,
    PRIMARY KEY (bookingID)
    );

create schema if not exists doctors;
use doctors;
create table doctors (
	# doctor stuff
    `doctorID` varchar(2) NOT NULL,
    `name` varchar(64) NOT NULL,
    `price` decimal(10,2) NOT NULL,
    `sex` varchar(10) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `postalcode` varchar(512) NOT NULL,
    `services` varchar(64) NOT NULL,
    PRIMARY KEY (`doctorID`)
    
);

create schema if not exists customers;
use customers;
create table customers (
	# customers stuff
    `customerID` varchar(2) NOT NULL,
    `name` varchar(64) NOT NULL,
    `email` varchar(256) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `postalcode` varchar(512) NOT NULL,
    PRIMARY KEY (customerID)
);


create schema if not exists admins;
use admins;
create table admins (
    `adminID` varchar(2) NOT NULL,
    `name` varchar(64) NOT NULL,
    `email` varchar(256) NOT NULL,
    PRIMARY KEY (adminID)
);

create schema if not exists bookings;
use bookings;
create table bookings (
	
    `bookingID` int auto_increment NOT NULL,
    `customerID` varchar(2)  null,
    `doctorID` varchar(2) not null,
    `datestart` datetime null,
    `dateend` datetime null,
    `status` varchar(20) not null,
    `price` decimal(10,2) not null,
    `service` varchar(256) null,
    PRIMARY KEY (bookingID)
);

create schema if not exists notifications;
use notifications;

create table notifications (
	`nid` int not null,
    `userid` varchar(2) not null,
    `message` varchar(500) not null,
    PRIMARY KEY (nid)
);

use admins;
insert into admins values ('a1', 'admin', 'admin@gmail.com');

use customers;
insert into customers values 
	('c1', 'customer1', 'customer1@gmail.com', '12345678', '510444'),
    ('c2', 'customer2', 'customer2@gmail.com', '12345678', '118175'),
    ('c3', 'customer3', 'customer3@gmail.com', '12345678', '669562');

use doctors;
insert into doctors values
	('d1', 'doctor1', 50.00, 'Male', '12345678', '169036', 'Flu'),
    ('d2', 'doctor2', 150.00, 'Male', '12345678', '238864', 'Flu'),
    ('d3', 'doctor3', 250.00, 'Female', '12345678', '178903', 'Flu');
    
use bookings;
insert into bookings (bookingID,  customerID, doctorID, datestart, dateend, status, price ) values
(1, 'd1', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 200.00),
(2, 'd1', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Unbooked', 200.00),
(3, 'd1', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Unbooked', 200.00),

(4, 'd2', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 200.00),
(5, 'c2', 'd2', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Booked', 200.00),
(6, 'c3', 'd2', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Booked', 200.00),

(7, 'd3', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 200.00),
(8, 'd3', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Unbooked', 200.00),
(9, 'c3', 'd3', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Booked', 200.00)
;


use notifications;
insert into notifications (nid, userid, message) values (1, 'd1', 'You have a new booking');

















    
