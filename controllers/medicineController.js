// controllers/medicineController.js
const pool = require('../db/pool');

exports.getAllMedicines = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM medicines');
    res.json(result.rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.getMedicineById = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM medicines WHERE id=$1', [req.params.id]);
    if (!result.rows.length) return res.status(404).json({ error: 'Not found' });
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.getMedicinesByPharmacy = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM medicines WHERE pharmacy_id=$1', [req.params.id]);
    res.json(result.rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.addMedicine = async (req, res) => {
  if (req.user.user_type !== 'pharmacy') return res.status(403).json({ error: 'Forbidden' });
  const { name, price } = req.body;
  try {
    const pharmacy = await pool.query('SELECT id FROM pharmacies WHERE user_id=$1', [req.user.id]);
    if (!pharmacy.rows.length) return res.status(400).json({ error: 'Pharmacy not found' });
    const pharmacyId = pharmacy.rows[0].id;
    const result = await pool.query(
      'INSERT INTO medicines (name, price, pharmacy_id) VALUES ($1, $2, $3) RETURNING *',
      [name, price, pharmacyId]
    );
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.updateMedicine = async (req, res) => {
  if (req.user.user_type !== 'pharmacy') return res.status(403).json({ error: 'Forbidden' });
  const { name, price } = req.body;
  try {
    const med = await pool.query('SELECT m.id FROM medicines m JOIN pharmacies p ON m.pharmacy_id=p.id WHERE m.id=$1 AND p.user_id=$2', [req.params.id, req.user.id]);
    if (!med.rows.length) return res.status(403).json({ error: 'Forbidden' });
    await pool.query('UPDATE medicines SET name=$1, price=$2 WHERE id=$3', [name, price, req.params.id]);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.deleteMedicine = async (req, res) => {
  if (req.user.user_type !== 'pharmacy') return res.status(403).json({ error: 'Forbidden' });
  try {
    const med = await pool.query('SELECT m.id FROM medicines m JOIN pharmacies p ON m.pharmacy_id=p.id WHERE m.id=$1 AND p.user_id=$2', [req.params.id, req.user.id]);
    if (!med.rows.length) return res.status(403).json({ error: 'Forbidden' });
    await pool.query('DELETE FROM medicines WHERE id=$1', [req.params.id]);
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};
