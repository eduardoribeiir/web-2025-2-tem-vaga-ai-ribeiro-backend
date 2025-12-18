const { db } = require('../../config/db');
const { HttpError } = require('../../utils/httpError');

const listByUser = async (userId) => {
  const rows = db.prepare(
    `SELECT a.id, a.user_id, a.title, a.description, a.seller, a.location, a.price, a.category, a.images, a.created_at, a.updated_at
     FROM favorites f
     JOIN ads a ON a.id = f.ad_id
     WHERE f.user_id = ?
     ORDER BY f.created_at DESC`
  ).all(userId);
  return rows.map(row => ({
    id: row.id,
    user_id: row.user_id,
    title: row.title,
    description: row.description,
    seller: row.seller,
    location: row.location,
    price: row.price,
    category: row.category,
    images: row.images ? JSON.parse(row.images) : [],
    created_at: row.created_at,
    updated_at: row.updated_at,
    postedBy: row.user_id?.toString() || ''
  }));
};

const toggle = async (userId, adId) => {
  if (!adId) throw new HttpError(400, 'ID inválido');

  const exists = db.prepare('SELECT 1 FROM ads WHERE id = ?').get(adId);
  if (!exists) throw new HttpError(404, 'Anúncio não encontrado');

  const fav = db.prepare('SELECT 1 FROM favorites WHERE user_id = ? AND ad_id = ?').get(userId, adId);
  if (fav) {
    db.prepare('DELETE FROM favorites WHERE user_id = ? AND ad_id = ?').run(userId, adId);
    return { favorite: false };
  }

  db.prepare('INSERT INTO favorites (user_id, ad_id) VALUES (?, ?)').run(userId, adId);
  return { favorite: true };
};

module.exports = { listByUser, toggle };
