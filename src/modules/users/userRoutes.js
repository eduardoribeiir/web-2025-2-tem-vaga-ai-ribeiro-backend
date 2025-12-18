const express = require('express');
const asyncHandler = require('../../middleware/asyncHandler');
const auth = require('../../middleware/auth');
const adsService = require('../ads/adsService');

const router = express.Router();

router.get(
  '/me/ads',
  auth,
  asyncHandler(async (req, res) => {
    const ads = await adsService.listByUser(req.user.id);
    return res.json(ads);
  })
);

module.exports = router;
