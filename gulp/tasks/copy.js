var gulp   = require('gulp');
var config = require('../config').copyfonts;
var flatten = require('gulp-flatten');

gulp.task('copy:fonts', function () {
    return gulp.src(config.src)
        .pipe(flatten())
        .pipe(gulp.dest(config.dest));
});
