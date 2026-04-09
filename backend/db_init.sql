
CREATE TABLE if not exists earthquakes (
    id VARCHAR PRIMARY KEY,
    lat float, 
    lon float, 
    magnitude float, 
    time date,
    alert varchar
);

