create table prescription(
    jobID int,
    doctorID int,
    customerID int,
    prescription varchar(500),
    PRIMARY KEY (jobID, doctorID, customerID)
    );
    
