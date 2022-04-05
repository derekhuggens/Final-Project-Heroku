-- Create vehicle data table (policy number, vehicle make, vehicle model & vehicle year)
CREATE TABLE vehicle_data (
	policy_number INTEGER,
	auto_make VARCHAR(10),
	auto_model VARCHAR(15),
	auto_year INTEGER,
	PRIMARY KEY (policy_number)
);

--Create insurance claims table w/o vehicle make, vehicle model & vehicle year)
CREATE TABLE insurance_data (
	months_as_customer INTEGER,
	age INTEGER,
	policy_number INTEGER,
	policy_bind_date DATE,
	policy_state VARCHAR(2),
	policy_csl VARCHAR(10),
	policy_deductible INTEGER,
	policy_annual_premium DECIMAL,
	umbrella_limit INTEGER,
	insured_zip INTEGER,
	insured_sex VARCHAR(6),
	insured_education_level VARCHAR(15),
	insured_occupation VARCHAR(25),
	insured_hobbies VARCHAR(15),
	insured_relationship VARCHAR(15),
	capital_gains INTEGER,
	capital_loss INTEGER,
	incident_date DATE,
	incident_type VARCHAR(25),
	collision_type VARCHAR(20),
	incident_severity VARCHAR(20),
	authorities_contacted VARCHAR(10),
	incident_state VARCHAR(2),
	incident_city VARCHAR(15),
	incident_location VARCHAR(25),
	incident_hour_of_the_day INTEGER,
	number_of_vehicles_involved INTEGER,
	property_damage VARCHAR(3),
	bodily_injuries INTEGER,
	witnesses INTEGER,
	police_report_available VARCHAR(3),
	total_claim_amount INTEGER,
	injury_claim INTEGER,
	property_claim INTEGER,
	vehicle_claim INTEGER,
	fraud_reported VARCHAR(1),
FOREIGN KEY (policy_number) REFERENCES vehicle_data (policy_number),
	PRIMARY KEY (policy_number)
);

-- Join vehicle_data and insurance_data into insuracne_claims table
SELECT * FROM vehicle_data
JOIN insurance_data ON vehicle_data.policy_number = insurance_data.policy_number;


CREATE TABLE insurance_claims (
 	months_as_customer INTEGER,
 	age INTEGER,
 	policy_number INTEGER,
 	policy_bind_date DATE,
 	policy_state VARCHAR(2),
 	policy_csl VARCHAR(10),
 	policy_deductible INTEGER,
 	policy_annual_premium DECIMAL,
 	umbrella_limit INTEGER,
 	insured_zip INTEGER,
 	insured_sex VARCHAR(6),
 	insured_education_level VARCHAR(15),
 	insured_occupation VARCHAR(25),
 	insured_hobbies VARCHAR(15),
 	insured_relationship VARCHAR(15),
 	capital_gains INTEGER,
 	capital_loss INTEGER,
 	incident_date DATE,
 	incident_type VARCHAR(25),
 	collision_type VARCHAR(20),
 	incident_severity VARCHAR(20),
 	authorities_contacted VARCHAR(10),
 	incident_state VARCHAR(2),
 	incident_city VARCHAR(15),
 	incident_location VARCHAR(25),
 	incident_hour_of_the_day INTEGER,
 	number_of_vehicles_involved INTEGER,
 	property_damage VARCHAR(3),
 	bodily_injuries INTEGER,
 	witnesses INTEGER,
 	police_report_available VARCHAR(3),
 	total_claim_amount INTEGER,
 	injury_claim INTEGER,
 	property_claim INTEGER,
 	vehicle_claim INTEGER,
 	auto_make VARCHAR(10),
 	auto_model VARCHAR(15),
 	auto_year INTEGER,
 	fraud_reported VARCHAR(1)
 );

-- Use to clear insurance_claims table
DROP TABLE insurance_claims;

SELECT * FROM vehicle_data;
SELECT * from insurance_data;
SELECT * FROM insurance_claims;