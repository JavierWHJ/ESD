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
    `email` varchar(256) NOT NULL,
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
	('d1', 'doctor1', 'doctor1@gmail.com', 50.00, 'Male', '12345678', '169608', 'Flu'),
    ('d2', 'doctor2', 'doctor2@gmail.com', 150.00, 'Male', '12345678', '238864', 'Flu'),
    ('d3', 'doctor3', 'doctor3@gmail.com', 250.00, 'Female', '12345678', '178903', 'Flu');
    
use bookings;
SET time_zone='+08:00';
insert into bookings (bookingID, doctorID, datestart, dateend, status, price ) values
(1, 'd1', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 50.00),
(2, 'd1', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Unbooked', 50.00),
(3, 'd1', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Unbooked', 50.00),

(4, 'd2', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 150.00),
(5, 'd2', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Unbooked', 150.00),
(6, 'd2', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Unbooked', 150.00),

(7, 'd3', '2020-05-01 08:00:00', '2020-05-01 12:00:00' , 'Unbooked', 250.00),
(8, 'd3', '2020-05-01 12:00:00', '2020-05-01 15:00:00' , 'Unbooked', 250.00),
(9, 'd3', '2020-05-01 15:00:00', '2020-05-01 18:00:00' , 'Unbooked', 250.00),

(10, 'd1', '2020-05-02 08:00:00', '2020-05-02 12:00:00' , 'Unbooked', 50.00),
(11, 'd1', '2020-05-02 12:00:00', '2020-05-02 15:00:00' , 'Unbooked', 50.00),
(12, 'd1', '2020-05-02 15:00:00', '2020-05-02 18:00:00' , 'Unbooked', 50.00),
(13, 'd1', '2020-05-02 18:00:00', '2020-05-02 20:00:00' , 'Unbooked', 50.00),

(14, 'd2', '2020-05-02 08:00:00', '2020-05-02 12:00:00' , 'Unbooked', 150.00),
(15, 'd2', '2020-05-02 12:00:00', '2020-05-02 15:00:00' , 'Unbooked', 150.00),
(16, 'd2', '2020-05-02 15:00:00', '2020-05-02 18:00:00' , 'Unbooked', 150.00),

(17, 'd3', '2020-05-02 08:00:00', '2020-05-02 12:00:00' , 'Unbooked', 250.00),
(18, 'd3', '2020-05-02 12:00:00', '2020-05-02 15:00:00' , 'Unbooked', 250.00),
(19, 'd3', '2020-05-03 15:00:00', '2020-05-03 18:00:00' , 'Unbooked', 250.00),
(20, 'd3', '2020-05-03 15:00:00', '2020-05-03 18:00:00' , 'Unbooked', 250.00),

(21, 'd1', '2020-05-04 08:00:00', '2020-05-04 12:00:00' , 'Unbooked', 50.00),
(22, 'd1', '2020-05-04 12:00:00', '2020-05-04 15:00:00' , 'Unbooked', 50.00),
(23, 'd1', '2020-05-04 15:00:00', '2020-05-04 18:00:00' , 'Unbooked', 50.00),

(24, 'd2', '2020-05-05 08:00:00', '2020-05-05 12:00:00' , 'Unbooked', 150.00),
(25, 'd2', '2020-05-05 12:00:00', '2020-05-05 15:00:00' , 'Unbooked', 150.00),
(26, 'd2', '2020-05-05 15:00:00', '2020-05-05 18:00:00' , 'Unbooked', 150.00),

(27, 'd3', '2020-05-05 08:00:00', '2020-05-05 12:00:00' , 'Unbooked', 250.00),
(28, 'd3', '2020-05-05 12:00:00', '2020-05-05 15:00:00' , 'Unbooked', 250.00),
(29, 'd3', '2020-05-05 15:00:00', '2020-05-05 18:00:00' , 'Unbooked', 250.00)
;


-- use notifications;
-- insert into notifications (nid, userid, message) values (1, 'd1', 'You have a new booking');


use prescriptions;
insert into prescription values
	('1', 'd1', 'c1', 'Panadol, 2 Qty, 5 Days, Morning and Night'),
    ('2', 'd1', 'c1', 'Panana, 1 Qty, 2 Days, Morning and Afternoon'),
    ('3', 'd1', 'c1', 'Apple, 1 Qty, 4 Days, Afternoon and Evening');















    
