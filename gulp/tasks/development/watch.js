var gulp = require('gulp');
var config = require('../../config').watch;

/**
 * Start browsersync task and then watch files for changes
 */
gulp.task('watch', ['browsersync'], function() {
    gulp.watch(config.less, ['less']);
    gulp.watch(config.html);
});
