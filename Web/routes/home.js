const Router = require('express');
const router = Router();
const fs = require('fs');
const multer  = require('multer')

router.get('', (req, res, _next) => {
    res.status(301);

    res.render('index', {
        title: "Hacks AI - RoadToBananaDevs",
        isHome: true,
    });
});

router.post('', async (req, res, _next) => {
    
});

module.exports = router;