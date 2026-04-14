CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE if not exists earthquakes (
    id VARCHAR PRIMARY KEY,
    lat float, 
    lon float, 
    magnitude float, 
    time timestamp,
    alert varchar
);

