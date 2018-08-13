SELECT date, serviceid, sms, departurestatus, COUNT(*) AS Number
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT MAX(timestamp)
        FROM stop_departures_details sd2
        WHERE sd1.aimeddeparture = sd2.aimeddeparture
            AND sd1.serviceid = sd2.serviceid
	    AND sd1.sms = sd2.sms
            AND sd2.departurestatus IS NOT NULL)
    AND sd1.departurestatus IS NOT NULL
    GROUP BY date, serviceid, sms, departurestatus
    ORDER BY date, serviceid, sms, departurestatus;
