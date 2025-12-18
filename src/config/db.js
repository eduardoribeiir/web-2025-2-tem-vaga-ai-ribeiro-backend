const Database = require('better-sqlite3');
const { dbPath } = require('./env');

const db = new Database(dbPath);
db.pragma('journal_mode = WAL');

const migrate = () => {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      description TEXT NOT NULL,
      seller TEXT NOT NULL,
      location TEXT NOT NULL,
      cep TEXT,
      price REAL,
      category TEXT NOT NULL,
      bedrooms INTEGER,
      bathrooms INTEGER,
      rules TEXT,
      amenities TEXT,
      custom_rules TEXT,
      custom_amenities TEXT,
      images TEXT,
      status TEXT DEFAULT 'published',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS favorites (
      user_id INTEGER NOT NULL,
      ad_id INTEGER NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (user_id, ad_id),
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
      FOREIGN KEY (ad_id) REFERENCES ads(id) ON DELETE CASCADE
    );
  `);
};

module.exports = { db, migrate };
