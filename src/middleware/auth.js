const jwt = require('jsonwebtoken');
const { jwtSecret } = require('../config/env');
const { HttpError } = require('../utils/httpError');

module.exports = (req, res, next) => {
  const header = req.headers.authorization;
  if (!header) return next(new HttpError(401, 'Token ausente'));
  const [, token] = header.split(' ');
  try {
    const payload = jwt.verify(token, jwtSecret);
    req.user = payload;
    return next();
  } catch (err) {
    return next(new HttpError(401, 'Token inválido'));
  }
};
