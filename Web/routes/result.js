const Router = require('express');
const router = Router();
const fs = require('fs');
const {spawn} = require('child_process');

router.get('', (req, res, _next) => {
    res.status(301);

    // redir to success (preloader)
    // write to json and csv
    let id = req.query.id

    const python = spawn('python', ['D:/Doc/Projects/HacksAI2021SPB/Web/routes/script1.py']);

    python.stdout.on('data', (data) => {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();

        let companydata = dataToSend.split("\r\n");
        console.log(companydata)

        company = {
            name: "Сбербанк",
            city: "Москва",
            site: "https://sberbank.ru",
            organization: "СберМегаМаркет",
            phone: "+7 (495) 457 57-35",
            desc: "Маркетплейс, принадлежащий Сбербанку. Платформа электронной коммерции, ассортимент которой включает товары продавцов в различных категориях. У пользователя есть возможность сравнить товары по цене, характеристикам, условиям доставки и самостоятельно выбрать продавца. Позиции от разных продавцов собираются в один заказ. Система доставки, оплаты, возврата общая для всех",
            organization_site: "https://goods.ru",
            sum_score: 28,
            runet_devepment_score: 5,
            pr_score: 2,
            projects_score: 4,
            gr_score: 3,
            tech_score: 5,
            social_score: 4,
            people_score: 5,
            nomination: "Экономика и Бизнес"
        }

        res.render('result', {
            title: "Hacks AI - RoadToBananaDevs",
            isHome: true,
            company
        });
    });
});

module.exports = router;