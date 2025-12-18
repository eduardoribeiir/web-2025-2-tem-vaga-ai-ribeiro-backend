const express = require('express');
const authRoutes = require('../modules/auth/authRoutes');
const adsRoutes = require('../modules/ads/adsRoutes');
const favoriteRoutes = require('../modules/favorites/favoriteRoutes');
const userRoutes = require('../modules/users/userRoutes');

const router = express.Router();

router.use('/auth', authRoutes);
router.use('/ads', adsRoutes);
router.use('/favorites', favoriteRoutes);
router.use('/users', userRoutes);

module.exports = router;
