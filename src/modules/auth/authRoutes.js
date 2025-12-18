const express = require('express');
const asyncHandler = require('../../middleware/asyncHandler');
const service = require('./authService');

const router = express.Router();

router.post(
  '/register',
  asyncHandler(async (req, res) => {
    const { name, email, password } = req.body;
    const result = await service.register({ name, email, password });
    return res.status(201).json(result);
  })
);

router.post(
  '/login',
  asyncHandler(async (req, res) => {
    const { email, password } = req.body;
    const result = await service.login({ email, password });
    return res.json(result);
  })
);

module.exports = router;
