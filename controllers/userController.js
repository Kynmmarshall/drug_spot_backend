// controllers/userController.js
const pool = require('../db/pool');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET || 'your_jwt_secret';

exports.register = async (req, res) => {
  const { username, email, phone, password, bio, avatar_path, user_type } = req.body;
  if (!username || !email || !password || !user_type) return res.status(400).json({ error: 'Missing fields' });
  try {
    const hash = await bcrypt.hash(password, 10);
    const result = await pool.query(
      'INSERT INTO users (username, email, phone, password_hash, bio, avatar_path, user_type) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id',
      [username, email, phone, hash, bio, avatar_path, user_type]
    );
    res.json({ id: result.rows[0].id });
  } catch (e) {
    res.status(400).json({ error: e.detail || e.message });
  }
};

exports.login = async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'Missing fields' });
  try {
    const result = await pool.query('SELECT * FROM users WHERE username=$1', [username]);
    if (!result.rows.length) return res.status(401).json({ error: 'Invalid credentials' });
    const user = result.rows[0];
    const valid = await bcrypt.compare(password, user.password_hash);
    if (!valid) return res.status(401).json({ error: 'Invalid credentials' });
    const token = jwt.sign({ id: user.id, username: user.username, user_type: user.user_type }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.getProfile = async (req, res) => {
  try {
    const result = await pool.query('SELECT username, email, phone, bio, avatar_path, user_type FROM users WHERE id=$1', [req.user.id]);
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

exports.updateProfile = async (req, res) => {
  const { email, phone, bio, avatar_path } = req.body;
  try {
    await pool.query(
      'UPDATE users SET email=$1, phone=$2, bio=$3, avatar_path=$4 WHERE id=$5',
      [email, phone, bio, avatar_path, req.user.id]
    );
    res.json({ success: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};
