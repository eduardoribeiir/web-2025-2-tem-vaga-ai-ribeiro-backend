const { db } = require('../../config/db');
const { HttpError } = require('../../utils/httpError');

const list = async () => {
  const rows = db.prepare("SELECT * FROM ads WHERE status = 'published' ORDER BY created_at DESC").all();
  return rows.map(row => ({
    id: row.id,
    user_id: row.user_id,
    title: row.title,
    description: row.description,
    seller: row.seller,
    location: row.location,
    cep: row.cep,
    price: row.price,
    category: row.category,
    bedrooms: row.bedrooms,
    bathrooms: row.bathrooms,
    rules: row.rules ? JSON.parse(row.rules) : [],
    amenities: row.amenities ? JSON.parse(row.amenities) : [],
    custom_rules: row.custom_rules,
    custom_amenities: row.custom_amenities,
    images: row.images ? JSON.parse(row.images) : [],
    status: row.status,
    created_at: row.created_at,
    updated_at: row.updated_at,
    postedBy: row.user_id?.toString() || ''
  }));
};

const getById = async (id) => {
  if (!id) throw new HttpError(400, 'ID inválido');
  const row = db.prepare('SELECT * FROM ads WHERE id = ?').get(id);
  if (!row) throw new HttpError(404, 'Anúncio não encontrado');
  return {
    id: row.id,
    user_id: row.user_id,
    title: row.title,
    description: row.description,
    seller: row.seller,
    location: row.location,
    cep: row.cep,
    price: row.price,
    category: row.category,
    bedrooms: row.bedrooms,
    bathrooms: row.bathrooms,
    rules: row.rules ? JSON.parse(row.rules) : [],
    amenities: row.amenities ? JSON.parse(row.amenities) : [],
    custom_rules: row.custom_rules,
    custom_amenities: row.custom_amenities,
    images: row.images ? JSON.parse(row.images) : [],
    status: row.status,
    created_at: row.created_at,
    updated_at: row.updated_at,
    postedBy: row.user_id?.toString() || ''
  };
};

const create = async (userId, payload) => {
  const { title, description, seller, location, cep, price, category, bedrooms, bathrooms, rules, amenities, custom_rules, custom_amenities, images, status } = payload;
  if (!title || !description || !seller || !location || !category) {
    throw new HttpError(400, 'Campos obrigatórios: title, description, seller, location, category');
  }
  const parsedPrice = price !== undefined ? Number(price) : null;
  const parsedBedrooms = bedrooms !== undefined ? Number(bedrooms) : null;
  const parsedBathrooms = bathrooms !== undefined ? Number(bathrooms) : null;
  const rulesJson = Array.isArray(rules) ? JSON.stringify(rules) : '[]';
  const amenitiesJson = Array.isArray(amenities) ? JSON.stringify(amenities) : '[]';
  const imgs = Array.isArray(images) ? JSON.stringify(images) : '[]';
  const adStatus = status === 'draft' ? 'draft' : 'published';

  const result = db.prepare(
    `INSERT INTO ads (user_id, title, description, seller, location, cep, price, category, bedrooms, bathrooms, rules, amenities, custom_rules, custom_amenities, images, status)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
     RETURNING *`
  ).get(userId, title, description, seller, location, cep || null, parsedPrice, category, parsedBedrooms, parsedBathrooms, rulesJson, amenitiesJson, custom_rules || null, custom_amenities || null, imgs, adStatus);
  
  return {
    id: result.id,
    user_id: result.user_id,
    title: result.title,
    description: result.description,
    seller: result.seller,
    location: result.location,
    cep: result.cep,
    price: result.price,
    category: result.category,
    bedrooms: result.bedrooms,
    bathrooms: result.bathrooms,
    rules: result.rules ? JSON.parse(result.rules) : [],
    amenities: result.amenities ? JSON.parse(result.amenities) : [],
    custom_rules: result.custom_rules,
    custom_amenities: result.custom_amenities,
    images: result.images ? JSON.parse(result.images) : [],
    status: result.status,
    created_at: result.created_at,
    updated_at: result.updated_at,
    postedBy: userId?.toString() || ''
  };
};

const update = async (userId, adId, payload) => {
  if (!adId) throw new HttpError(400, 'ID inválido');
  
  const ad = db.prepare('SELECT * FROM ads WHERE id = ?').get(adId);
  if (!ad) throw new HttpError(404, 'Anúncio não encontrado');
  if (ad.user_id !== userId) throw new HttpError(403, 'Você não tem permissão para editar este anúncio');

  const { title, description, seller, location, cep, price, category, bedrooms, bathrooms, rules, amenities, custom_rules, custom_amenities, images, status } = payload;
  const updatedTitle = title !== undefined ? title : ad.title;
  const updatedDesc = description !== undefined ? description : ad.description;
  const updatedSeller = seller !== undefined ? seller : ad.seller;
  const updatedLocation = location !== undefined ? location : ad.location;
  const updatedCep = cep !== undefined ? cep : ad.cep;
  const updatedPrice = price !== undefined ? Number(price) : ad.price;
  const updatedCategory = category !== undefined ? category : ad.category;
  const updatedBedrooms = bedrooms !== undefined ? Number(bedrooms) : ad.bedrooms;
  const updatedBathrooms = bathrooms !== undefined ? Number(bathrooms) : ad.bathrooms;
  const updatedRules = rules !== undefined ? JSON.stringify(Array.isArray(rules) ? rules : []) : ad.rules;
  const updatedAmenities = amenities !== undefined ? JSON.stringify(Array.isArray(amenities) ? amenities : []) : ad.amenities;
  const updatedCustomRules = custom_rules !== undefined ? custom_rules : ad.custom_rules;
  const updatedCustomAmenities = custom_amenities !== undefined ? custom_amenities : ad.custom_amenities;
  const updatedImages = images !== undefined ? JSON.stringify(Array.isArray(images) ? images : []) : ad.images;
  const updatedStatus = status !== undefined ? status : ad.status;

  const result = db.prepare(
    `UPDATE ads SET title = ?, description = ?, seller = ?, location = ?, cep = ?, price = ?, category = ?, bedrooms = ?, bathrooms = ?, rules = ?, amenities = ?, custom_rules = ?, custom_amenities = ?, images = ?, status = ?, updated_at = CURRENT_TIMESTAMP
     WHERE id = ?
     RETURNING *`
  ).get(updatedTitle, updatedDesc, updatedSeller, updatedLocation, updatedCep, updatedPrice, updatedCategory, updatedBedrooms, updatedBathrooms, updatedRules, updatedAmenities, updatedCustomRules, updatedCustomAmenities, updatedImages, updatedStatus, adId);

  return {
    id: result.id,
    user_id: result.user_id,
    title: result.title,
    description: result.description,
    seller: result.seller,
    location: result.location,
    cep: result.cep,
    price: result.price,
    category: result.category,
    bedrooms: result.bedrooms,
    bathrooms: result.bathrooms,
    rules: result.rules ? JSON.parse(result.rules) : [],
    amenities: result.amenities ? JSON.parse(result.amenities) : [],
    custom_rules: result.custom_rules,
    custom_amenities: result.custom_amenities,
    images: result.images ? JSON.parse(result.images) : [],
    status: result.status,
    created_at: result.created_at,
    updated_at: result.updated_at,
    postedBy: userId?.toString() || ''
  };
};

const remove = async (userId, adId) => {
  if (!adId) throw new HttpError(400, 'ID inválido');
  
  const ad = db.prepare('SELECT * FROM ads WHERE id = ?').get(adId);
  if (!ad) throw new HttpError(404, 'Anúncio não encontrado');
  if (ad.user_id !== userId) throw new HttpError(403, 'Você não tem permissão para deletar este anúncio');

  db.prepare('DELETE FROM ads WHERE id = ?').run(adId);
  return { message: 'Anúncio deletado com sucesso' };
};

const listByUser = async (userId) => {
  const rows = db.prepare('SELECT * FROM ads WHERE user_id = ? ORDER BY created_at DESC').all(userId);
  return rows.map(row => ({
    id: row.id,
    user_id: row.user_id,
    title: row.title,
    description: row.description,
    seller: row.seller,
    location: row.location,
    cep: row.cep,
    price: row.price,
    category: row.category,
    bedrooms: row.bedrooms,
    bathrooms: row.bathrooms,
    rules: row.rules ? JSON.parse(row.rules) : [],
    amenities: row.amenities ? JSON.parse(row.amenities) : [],
    custom_rules: row.custom_rules,
    custom_amenities: row.custom_amenities,
    images: row.images ? JSON.parse(row.images) : [],
    status: row.status,
    created_at: row.created_at,
    updated_at: row.updated_at,
    postedBy: userId?.toString() || ''
  }));
};

module.exports = { list, getById, create, update, remove, listByUser };
