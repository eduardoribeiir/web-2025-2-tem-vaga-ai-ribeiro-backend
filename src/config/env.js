require('dotenv').config();
const path = require('path');

module.exports = {
  port: process.env.PORT || 4000,
  jwtSecret: process.env.JWT_SECRET || 'dev-secret',
  dbPath: process.env.DB_PATH || path.join(__dirname, '../../database.sqlite'),
};
