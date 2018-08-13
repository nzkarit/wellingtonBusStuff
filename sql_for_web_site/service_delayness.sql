SELECT date, serviceid, sms AS stop, aimeddeparture, expecteddeparture, TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture) AS delay
	FROM stop_departures_details sd1
	WHERE timestamp =
	    (SELECT MAX(timestamp)
	        FROM stop_departures_details sd2
	        WHERE sd1.aimeddeparture = sd2.aimeddeparture
	            AND sd1.serviceid = sd2.serviceid
	            AND sd1.sms = sd2.sms)
	AND isrealtime    
	AND departurestatus != 'cancelled'
	ORDER BY date, serviceid, sms;
