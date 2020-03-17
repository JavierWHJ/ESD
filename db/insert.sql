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



