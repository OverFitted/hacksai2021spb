const Router = require('express');
const router = Router();
const fs = require('fs');
const multer = require('multer')

router.get('', (req, res, _next) => {
    res.status(301);

    res.render('index', {
        title: "Hacks AI - RoadToBananaDevs",
        isHome: true,
    });
});

router.post('/', multer({dest: 'data/'}).any(), async (req, res, next) => {
    console.log(req.files);

    res.json(301)
    res.status(301).end();
});

module.exports = router;