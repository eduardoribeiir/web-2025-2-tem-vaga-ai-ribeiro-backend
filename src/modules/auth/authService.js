const bcrypt = require('bcryptjs');
const { db } = require('../../config/db');
const { signToken } = require('../../utils/token');
const { HttpError } = require('../../utils/httpError');

const register = async ({ name, email, password }) => {
  if (!email || !password) throw new HttpError(400, 'Email e senha são obrigatórios');

  const exists = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
  if (exists) throw new HttpError(409, 'Email já cadastrado');

  const password_hash = await bcrypt.hash(password, 10);
  const result = db.prepare(
    'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?) RETURNING id, name, email, created_at'
  ).get(name || null, email, password_hash);
  
  const token = signToken({ id: result.id, email: result.email });
  return { user: result, token };
};

const login = async ({ email, password }) => {
  if (!email || !password) throw new HttpError(400, 'Email e senha são obrigatórios');

  const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email);
  if (!user) throw new HttpError(401, 'Credenciais inválidas');

  const ok = await bcrypt.compare(password, user.password_hash);
  if (!ok) throw new HttpError(401, 'Credenciais inválidas');

  const token = signToken({ id: user.id, email: user.email });
  return { user: { id: user.id, name: user.name, email: user.email }, token };
};

module.exports = { register, login };
