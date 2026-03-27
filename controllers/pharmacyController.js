// controllers/pharmacyController.js
const pool = require('../db/pool');

exports.getAllPharmacies = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM pharmacies');
    res.json(result.rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.getPharmacyById = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM pharmacies WHERE id=$1', [req.params.id]);
    if (!result.rows.length) return res.status(404).json({ error: 'Not found' });
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};
