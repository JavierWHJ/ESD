create schema if not exists prescriptions;
use prescriptions;
create table prescription(
    bookingID int, # changed this to bookingID from jobid to be consistent with booking microservice
    doctorID int,
    customerID int,
    prescription varchar(500),
    PRIMARY KEY (bookingID, doctorID, customerID)
    );


# incomplete pls finish, remove this line when done    
create schema if not exists doctors;
use doctors;
create table doctors (
	# doctor stuff
    doctorID int auto_increment not null,
    isadmin boolean not null default false,
	PRIMARY KEY (doctorID)
);

# incomplete pls finish, remove this line when done   
create schema if not exists customers;
use customers;
create table customers (
	# customers stuff
    customerID int auto_increment not null,
    isadmin boolean not null default false,
    PRIMARY KEY (customerID)
);


create schema if not exists admins;
use admins;
create table admins (
	# bookings stuff
    adminID int auto_increment not null,
     isadmin boolean not null default true,
     PRIMARY KEY (adminID)
);

# incomplete pls finish, remove this line when done   
create schema if not exists bookings;
use bookings;
create table bookings (
	# bookings stuff
    bookingID int auto_increment not null,
    PRIMARY KEY (bookingID)
);









    
