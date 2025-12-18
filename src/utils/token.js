const jwt = require('jsonwebtoken');
const { jwtSecret } = require('../config/env');

const signToken = (payload) => jwt.sign(payload, jwtSecret, { expiresIn: '7d' });

module.exports = { signToken };
