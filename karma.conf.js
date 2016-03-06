// Karma configuration
// Generated on Mon Jan 25 2016 18:13:57 GMT+0200 (EET)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine-jquery', 'jasmine'],


    // list of files / patterns to load in the browser
    files: [
        'bower_components/angular/angular.js',
        'bower_components/angular-mocks/angular-mocks.js',
        'bower_components/angular-resource/angular-resource.js',
        'bower_components/angular-toArrayFilter/toArrayFilter.js',
        'bower_components/angular-animate/angular-animate.min.js',
        'bower_components/moment/min/moment.min.js',
        'node_modules/jasmine-jquery/lib/jasmine-jquery.js',
        /* need to  ensure module definitions (in *.module.js files are
           loaded first */
        'portfolio/static/js/portfolio/portfolio2.module.js',
        'portfolio/static/js/portfolio/account_summary.module.js',
        'portfolio/static/js/portfolio/**/*.module.js',
        'portfolio/static/js/portfolio/**/*.js',
        'portfolio/static/js/portfolio/*.js',
        'portfolio/static/tests/**/*.spec.js',
        'portfolio/static/vendor/**/*.js',
        // fixtures
        {pattern: 'portfolio/static/tests/mock/*.json', watched: true, served: true, included: false}
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
        //'**/portfolio/static/js/**/*.js': 'coverage',
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress', 'coverage'],

    coverageReporter: {
        type : 'html',
        dir : 'coverage/'
    },

    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false,

    // Concurrency level
    // how many browser should be started simultaneous
    concurrency: Infinity
  })
}
