const express = require('express');
const asyncHandler = require('../../middleware/asyncHandler');
const auth = require('../../middleware/auth');
const service = require('./adsService');

const router = express.Router();

router.get(
  '/',
  asyncHandler(async (req, res) => {
    const ads = await service.list();
    return res.json(ads);
  })
);

router.get(
  '/:id',
  asyncHandler(async (req, res) => {
    const ad = await service.getById(Number(req.params.id));
    return res.json(ad);
  })
);

router.post(
  '/',
  auth,
  asyncHandler(async (req, res) => {
    const ad = await service.create(req.user.id, req.body);
    return res.status(201).json(ad);
  })
);

router.put(
  '/:id',
  auth,
  asyncHandler(async (req, res) => {
    const ad = await service.update(req.user.id, Number(req.params.id), req.body);
    return res.json(ad);
  })
);

router.delete(
  '/:id',
  auth,
  asyncHandler(async (req, res) => {
    const result = await service.remove(req.user.id, Number(req.params.id));
    return res.json(result);
  })
);

module.exports = router;
