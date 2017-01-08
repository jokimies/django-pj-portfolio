var src               = 'app';
var build             = 'build';
var development       = 'build/development';
var production        = 'build/production';
var srcAssets         = 'app/_assets';
var developmentAssets = 'build/assets';
var productionAssets  = 'build/production/assets';
var srcVendors = 'static/assets/vendor/bower_components';
var assets = 'portfolio/static';
const djangoTemplates = 'portfolio/templates';

module.exports = {
    browsersync: {
        development: {
            port: 8001,
            proxy: 'homer:8001',
            files: [
                assets + '/css/*.css',
                assets + '/js/**/*.js',
                djangoTemplates + '/**/*.html',
            ],
            open: false,
        }
    },
    copyfonts: {
        src:  srcVendors + '/**/fonts/*',
        dest: assets + '/fonts'
    },
    less: {
        src: assets + '/less/style.less',
        dest: assets + '/css'
    },
    watch: {
        less: assets + '/less/*',
        html: 'templates/**/*.html'
    }
};
