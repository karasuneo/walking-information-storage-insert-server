\c indoor_location_estimation;

CREATE TABLE particles (
    id VARCHAR(26) PRIMARY KEY,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    direction INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    walking_sample_id VARCHAR(26) REFERENCES walking_samples(id)
);

CREATE TABLE estimated_positions (
    id VARCHAR(26) PRIMARY KEY,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    direction INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    walking_sample_id VARCHAR(26) UNIQUE REFERENCES walking_samples(id)
);
