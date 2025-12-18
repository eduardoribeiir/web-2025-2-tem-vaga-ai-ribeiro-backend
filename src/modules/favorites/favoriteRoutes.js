const express = require('express');
const asyncHandler = require('../../middleware/asyncHandler');
const auth = require('../../middleware/auth');
const service = require('./favoriteService');

const router = express.Router();

router.get(
  '/',
  auth,
  asyncHandler(async (req, res) => {
    const list = await service.listByUser(req.user.id);
    return res.json(list);
  })
);

router.post(
  '/:adId/toggle',
  auth,
  asyncHandler(async (req, res) => {
    const result = await service.toggle(req.user.id, Number(req.params.adId));
    return res.json(result);
  })
);

module.exports = router;
