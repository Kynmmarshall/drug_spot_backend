// controllers/medicineRequestController.js
const pool = require('../db/pool');

exports.getAllRequests = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM medicine_requests');
    res.json(result.rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.addRequest = async (req, res) => {
  const { username, contact, medicine_name, avatar_path, use_asset } = req.body;
  if (!username || !contact || !medicine_name) return res.status(400).json({ error: 'Missing fields' });
  try {
    const result = await pool.query(
      'INSERT INTO medicine_requests (username, contact, medicine_name, avatar_path, use_asset) VALUES ($1,$2,$3,$4,$5) RETURNING *',
      [username, contact, medicine_name, avatar_path, use_asset || false]
    );
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};
