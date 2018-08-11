BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `service_location_details` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`timestamp`	TEXT NOT NULL,
	`date`	TEXT,
	`LastModified`	TEXT NOT NULL,
	`Code`	TEXT,
	`TrimmedCode`	TEXT,
	`Name`	TEXT,
	`Mode`	TEXT,
	`Link`	TEXT,
	`RecordedAtTime`	TEXT,
	`VehicleRef`	TEXT,
	`ServiceID`	TEXT,
	`HasStarted`	INTEGER,
	`DepartureTime`	TEXT,
	`OriginStopID`	TEXT,
	`OriginStopName`	TEXT,
	`DestinationStopID`	TEXT,
	`DestinationStopName`	TEXT,
	`Direction`	TEXT,
	`Bearing`	TEXT,
	`BehindSchedule`	INTEGER,
	`VehicleFeature`	TEXT,
	`DelaySeconds`	INTEGER,
	`Lat`	NUMERIC,
	`Long`	NUMERIC
);
COMMIT;
