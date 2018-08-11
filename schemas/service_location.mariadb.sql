START TRANSACTION;
CREATE TABLE service_location_details (
  `id` BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
  `date`	DATE NOT NULL,
  `timestamp`	TIMESTAMP NOT NULL,
  `LastModified` TIMESTAMP,
  `Code` TEXT ,
  `TrimmedCode` TEXT ,
  `Name` TEXT ,
  `Mode` TEXT ,
  `Link` TEXT ,
  `RecordedAtTime` TIMESTAMP,
  `VehicleRef` SMALLINT,
  `ServiceID` SMALLINT,
  `HasStarted` BOOLEAN,
  `DepartureTime` TIMESTAMP,
  `OriginStopID` SMALLINT,
  `OriginStopName` TEXT,
  `DestinationStopID` SMALLINT,
  `DestinationStopName` TEXT,
  `Direction` TEXT,
  `Bearing` SMALLINT,
  `BehindSchedule` BOOLEAN,
  `VehicleFeature` TEXT ,
  `DelaySeconds` INTEGER ,
  `Latitude`  FLOAT,
  `Longitude` FLOAT
) ENGINE=InnoDB;
COMMIT;
