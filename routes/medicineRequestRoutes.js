// routes/medicineRequestRoutes.js
const express = require('express');
const router = express.Router();
const medicineRequestController = require('../controllers/medicineRequestController');

router.get('/', medicineRequestController.getAllRequests);
router.post('/', medicineRequestController.addRequest);

module.exports = router;
