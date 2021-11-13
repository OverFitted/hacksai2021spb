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
    res.json(req.files)

    // fs.readFile(request.files[0].path, function (err, data) {
    //     var newPath = __dirname + "/public/img/xspectra/customlogo.png";
    //     fs.writeFile(newPath, data, function (err) {
    //         console.log("Finished writing file..." + err);
    //         response.redirect("back");
    //     });
    // });

    res.status(301).end();
});

module.exports = router;