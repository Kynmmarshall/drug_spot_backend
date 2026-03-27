// routes/medicineRoutes.js
const express = require('express');
const router = express.Router();
const authenticate = require('../middleware/authenticate');
const medicineController = require('../controllers/medicineController');

router.get('/', medicineController.getAllMedicines);
router.get('/:id', medicineController.getMedicineById);
router.get('/pharmacy/:id', medicineController.getMedicinesByPharmacy);
router.post('/', authenticate, medicineController.addMedicine);
router.put('/:id', authenticate, medicineController.updateMedicine);
router.delete('/:id', authenticate, medicineController.deleteMedicine);

module.exports = router;
