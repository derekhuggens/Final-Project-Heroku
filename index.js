const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const db = require('./queries');
const {spawn} = require('child_process');
const port = 3001;

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

app.get('/', (request, response) => {
    response.json({ info: 'Node.js, Express, and Postgres API' })
  })

// PostgreSQL Database Routes

app.get('/rows', db.getColumns)
app.post('/rows', db.createNewRow)

// Python Script Routes (Decision Tree/Random Forest)

app.get('/rf', (req, res) => {
 
  var dataToSend;
  // spawn new child process to call the python script
  const python = spawn('python', ['ML_Model_Decision_Tree.py']);
  // collect data from script
  python.stdout.on('data', function (data) {
   console.log('Pipe data from python script ...');
   dataToSend = data.toString();
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
  console.log(`child process close all stdio with code ${code}`);
  // send data to browser
  res.send(dataToSend)
  });
  
});

// Python Script Routes (Neural Network)

 app.get('/nn', (req, res) => {
 
  var dataToSend;
  // spawn new child process to call the python script
  const python = spawn('python', ['ML_Model_Neural_Network.py']);
  // collect data from script
  python.stdout.on('data', function (data) {
   console.log('Pipe data from python script ...');
   dataToSend = data.toString();
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
  console.log(`child process close all stdio with code ${code}`);
  // send data to browser
  res.send(dataToSend)
  });
  
 });

// Port Listening

app.listen(port, () => {
console.log(`App running on port ${port}.`)
})