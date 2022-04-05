const pw = require("./config");
const Pool = require('pg').Pool
const pool = new Pool({
  user: username_db,
  host: 'localhost',
  database: 'insurance_fraud_db',
  password: password_db,
  port: 5432,
});

const getColumns = (request, response) => {
    pool.query('SELECT insured_sex, age, months_as_customer, incident_state, auto_make, auto_model, policy_deductible FROM insurance_claims', (error, results) => {
      if (error) {
        throw error
      }
      response.status(200).json(results.rows)
    })
  }

const createNewRow = (request, response) => {
    const {insured_sex, age, months_as_customer, incident_state, auto_make, auto_model, policy_deductible } = request.body
  
    pool.query('INSERT INTO insurance_claims (insured_sex, age, months_as_customer, incident_state, auto_make, auto_model, policy_deductible) VALUES ($1, $2, $3, $4, $5, $6, $7)', [insured_sex, age, months_as_customer, incident_state, auto_make, auto_model, policy_deductible], (error, results) => {
      if (error) {
        throw error
      }
      response.status(201).send(`User added: `)
    })
  }



module.exports = {
    getColumns,
    createNewRow,
}