SELECT SUBSTRING(recordedattime, 1, 13) time, AVG(delayseconds)
  FROM service_location_details
  GROUP BY time;
