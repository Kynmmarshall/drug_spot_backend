// drug_spot_backend/index.js
// Node.js Express backend for Drug Spot


const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const userRoutes = require('./routes/userRoutes');
const pharmacyRoutes = require('./routes/pharmacyRoutes');
const medicineRoutes = require('./routes/medicineRoutes');
const medicineRequestRoutes = require('./routes/medicineRequestRoutes');

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(bodyParser.json());

app.use('/api', userRoutes);
app.use('/api/pharmacies', pharmacyRoutes);
app.use('/api/medicines', medicineRoutes);
app.use('/api/medicine_requests', medicineRequestRoutes);

app.listen(port, () => {
  console.log(`Drug Spot backend listening on port ${port}`);
});
