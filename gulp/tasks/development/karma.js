var gulp = require('gulp');
var Server = require('karma').Server;

gulp.task('test', function(done) {
    new Server({
        configFile: __dirname + '/../../../karma.conf.js',
        singleRun: true,
        reporters: ['dots', 'junit'],
        junitReporter: {
            outputDir: '',
            outputFile: 'test-results.xml'
        },
        useBrowserName: false,
        browsers: ['PhantomJS']
    }, done).start();
});

