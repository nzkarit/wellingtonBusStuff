SELECT
  stop5000.hour,
  Delay7041,
  Delay7083,
  Delay7224,
  Delay7217,
  Delay5000,
  Delay5008,
  Delay5010,
  Delay5015,
  Delay5319,
  Delay5322,
  Delay5327,
  Delay5331
FROM
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5000
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
    AND
    sd1.isrealtime
    AND
    departurestatus != 'cancelled'
    AND
    sms = 5000
    AND
    serviceid = '2'
  GROUP BY hour) stop5000,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5008
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
    AND
    sd1.isrealtime
    AND
    departurestatus != 'cancelled'
    AND
    sms = 5008
    AND
    serviceid = '2'
  GROUP BY hour) stop5008,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5010
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5010
      AND
      serviceid = '2'
  GROUP BY hour) stop5010,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5015
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5015
      AND
      serviceid = '2'
  GROUP BY hour) stop5015,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5319
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5319
      AND
      serviceid = '2'
  GROUP BY hour) stop5319,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5322
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5322
      AND
      serviceid = '2'
  GROUP BY hour) stop5322,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5327
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5327
      AND
      serviceid = '2'
  GROUP BY hour) stop5327,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay5331
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 5331
      AND
      serviceid = '2'
  GROUP BY hour) stop5331,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay7041
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 7041
      AND
      serviceid = '2'
  GROUP BY hour) stop7041,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay7083
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 7083
      AND
      serviceid = '2'
  GROUP BY hour) stop7083,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay7224
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 7224
      AND
      serviceid = '2'
  GROUP BY hour) stop7224,
  (SELECT
    SUBSTRING(timestamp, 12, 2) as hour,
    AVG(TIMESTAMPDIFF(SECOND, aimeddeparture, expecteddeparture)) AS Delay7217
  FROM stop_departures_details sd1
  WHERE timestamp =
    (SELECT
      MAX(timestamp)
    FROM stop_departures_details sd2
    WHERE
      sd1.aimeddeparture = sd2.aimeddeparture
      AND
      sd1.serviceid = sd2.serviceid
      AND
      sd1.sms = sd2.sms
      AND
      sd2.isrealtime)
      AND
      sd1.isrealtime
      AND
      departurestatus != 'cancelled'
      AND
      sms = 7217
      AND
      serviceid = '2'
  GROUP BY hour) stop7217
WHERE
  stop5000.hour = stop5008.hour
  AND
  stop5000.hour = stop5010.hour
  AND
  stop5000.hour = stop5015.hour
  AND
  stop5000.hour = stop5319.hour
  AND
  stop5000.hour = stop5322.hour
  AND
  stop5000.hour = stop5327.hour
  AND
  stop5000.hour = stop5331.hour
  AND
  stop5000.hour = stop7041.hour
  AND
  stop5000.hour = stop7083.hour
  AND
  stop5000.hour = stop7224.hour
  AND
  stop5000.hour = stop7217.hour
ORDER BY hour;
