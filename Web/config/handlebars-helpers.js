module.exports = {
    ifDark: function(options){
        console.log(options);
    },
    getArr: function(array, options){
        result = JSON.stringify(array);
        return result;
    },
    ifeq: function (a, b, options) {
        if (a === b) {
            return options.fn(this);
        }
        return options.inverse(this);
    },
    var: function (name, value, options) {
        options.data.root[name] = value;
    },
    ifnot: function (a, options) {
        if (!a) {
            return options.fn(this);
        }
        return options.inverse(this);
    },
    getMax: function (dict, _options) {
        var arr = [];

        for (var k in dict.math) {
            arr.push(dict.math[k].finalScore);
        }

        return Math.max.apply(null, arr);
    },
    compare: function (lvalue, rvalue, options) {
        if (lvalue >= 10) {
            lvalue = lvalue % 10;
        }

        if (arguments.length < 3)
            throw new Error("Handlebars Helper 'compare' needs 2 parameters");

        let operator = options.hash.operator || "==";

        let operators = {
            '==': function (l, r) {
                return l == r;
            },
            '===': function (l, r) {
                return l === r;
            },
            '!=': function (l, r) {
                return l != r;
            },
            '<': function (l, r) {
                return l < r;
            },
            '>': function (l, r) {
                return l > r;
            },
            '<=': function (l, r) {
                return l <= r;
            },
            '>=': function (l, r) {
                return l >= r;
            },
            'typeof': function (l, r) {
                return typeof l == r;
            },
            '%': function (l, r) {
                return l % r === 0;
            }
        }

        if (!operators[operator])
            throw new Error("Handlerbars Helper 'compare' doesn't know the operator " + operator);

        let result = operators[operator](lvalue, rvalue);

        if (result) {
            return options.fn(this);
        } else {
            return options.inverse(this);
        }

    },
    comp: function (lvalue, rvalue, options) {
        if (arguments.length < 3)
            throw new Error("Handlebars Helper 'compare' needs 2 parameters");
        if (typeof rvalue !== "string") {
            rvalue = lvalue;
        }

        let operator = options.hash.operator || "==";

        let operators = {
            '==': function (l, r) {
                return l == r;
            },
            '===': function (l, r) {
                return l === r;
            },
            '!=': function (l, r) {
                return l != r;
            },
            '<': function (l, r) {
                return l < r;
            },
            '>': function (l, r) {
                return l > r;
            },
            '<=': function (l, r) {
                return l <= r;
            },
            '>=': function (l, r) {
                return l >= r;
            },
            'typeof': function (l, r) {
                return typeof l == r;
            },
            '%': function (l, r) {
                return l % r === 0;
            }
        }

        if (!operators[operator])
            throw new Error("Handlerbars Helper 'compare' doesn't know the operator " + operator);

        let result = operators[operator](lvalue, rvalue);

        if (result) {
            return options.fn(this);
        } else {
            return options.inverse(this);
        }
    },
    getFromArr: function (array, index, options) {
        if (index > 0){
            return array[index];
        } else {
            return array[array.length + index];
        }
    },
    inc: function(value, offset, options)
    {
        return parseInt(value) + parseInt(offset);
    },
    dec: function(value, offset, options)
    {
        return parseInt(value) - parseInt(offset);
    },
    times: function (n, block, options) {
        var accum = '';
        for (var i = 0; i < n; ++i)
            accum += block.fn(i);
        return accum;
    },
    cl: function (str, options) {
        return console.log(str);
    }
}