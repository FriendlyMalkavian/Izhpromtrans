PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT, 
title text NOT NULL, 
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS stations (
StationId integer PRIMARY KEY AUTOINCREMENT, 
StationName text NOT NULL, 
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS certificates (
CertificateId integer PRIMARY KEY AUTOINCREMENT,
RegistrationNumber varchar UNIQUE,
PathLength decimal NOT NULL,
CadastralNumber varchar NOT NULL UNIQUE, 
StationId integerp,
FOREIGN KEY(StationId) REFERENCES stations(StationId)
);

CREATE TABLE IF NOT EXISTS propertyObjects (
ObjectId integer PRIMARY KEY AUTOINCREMENT, 
ObjectName varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS tenants (
TenantId integer PRIMARY KEY AUTOINCREMENT, 
TenantName varchar NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rent (
RentId integer PRIMARY KEY AUTOINCREMENT,
ContractNumber varchar NOT NULL UNIQUE,
RentPricePM decimal NOT NULL,
TenantId integer,
FOREIGN KEY (TenantId) REFERENCES tenants(TenantId) 
);

CREATE TABLE IF NOT EXISTS rentalObjects (
RentId integer,
ObjectId varchar,
FOREIGN KEY (RentId) REFERENCES rent(RentId), 
FOREIGN KEY (ObjectId) REFERENCES propertyObjects(ObjectId)
);

CREATE TABLE IF NOT EXISTS objectsInCertificate (
CertificateId integer, 
ObjectId varchar, 
StationId integer,
FOREIGN KEY (CertificateId) REFERENCES certificates(CertificateId), 
FOREIGN KEY (ObjectId) REFERENCES propertyObjects(ObjectId),
FOREIGN KEY(StationId) REFERENCES stations(StationId)
);