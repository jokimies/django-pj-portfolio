var gulp = require('gulp');
var Server = require('karma').Server;

gulp.task('test', function(done) {
    new Server({
        configFile: __dirname + '/../../../karma.conf.js',
        singleRun: true,
        reporters: ['dots', 'junit', 'coverage'],
        junitReporter: {
            outputDir: '',
            outputFile: 'test-results.xml'
        },
        preprosessors: {
            '**/portfolio/static/js/**/*.js': ['coverage'],
        },
        coverageReporter: {
            type : 'cobertura',
            dir : 'coverage/'
    },

        useBrowserName: false,
        browsers: ['PhantomJS']
    }, done).start();
});

