SELECT SUBSTRING(recordedattime, 12, 2) hour, AVG(delayseconds)
  FROM service_location_details
  GROUP BY hour;
