CREATE INDEX index_sdd_serviceid ON stop_departures_details(serviceid);
CREATE INDEX index_sdd_sms ON stop_departures_details(sms);
CREATE INDEX index_sdd_isrealtime ON stop_departures_details(isrealtime);
CREATE INDEX index_sdd_aimeddeparture ON stop_departures_details(aimeddeparture);
CREATE INDEX index_sdd_serviceid_sms_isrealtime_aimeddeparture ON stop_departures_details(serviceid, sms, isrealtime, aimeddeparture);