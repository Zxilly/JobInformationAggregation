module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],

    chainWebpack(config) {
        // set whitespace
        config.module
            .rule("vue")
            .use("vue-loader")
            .loader("vue-loader")
            .tap(options => {
                options.compilerOptions.whitespace = 'preserve';
                return options;
            })
            .end();
    }
}

