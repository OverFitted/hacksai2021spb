const Router = require('express');
const router = Router();
const fs = require('fs');

router.get('', (req, res, _next) => {
    res.status(301);

    res.render('result', {
        title: "Hacks AI - RoadToBananaDevs",
        isHome: true,
    });
});

module.exports = router;