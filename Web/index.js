const express = require('express');
const morgan = require('morgan');
const exphbs = require('express-handlebars');
const cookieParser = require('cookie-parser');
const app = express();

const hbs = exphbs.create({
    defaultLayout: 'main',
    extname: 'hbs',
    helpers: require('./config/handlebars-helpers')
});

app.engine('hbs', hbs.engine);
app.set('view engine', 'hbs');
app.set('views', 'Views');

app.use(express.json({extended: false}));
app.use(express.urlencoded({extended: true}));
app.use(cookieParser())
app.use(express.static('public'));
app.use(morgan('dev'))

app.use('/', require('./routes/home'));
app.use('/result/', require('./routes/result'));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server running at port: ${PORT}`);
});
