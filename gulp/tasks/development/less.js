var gulp = require('gulp');
//var plumber = require('gulp-plumber');
var browsersync = require('browser-sync');
var less = require('gulp-less');
var gulpFilter = require('gulp-filter');
// var autoprefixer = require('gulp-autoprefixer');
var sourcemaps = require('gulp-sourcemaps');
var config = require('../../config');


gulp.task('less', function () {

    return gulp.src(config.less.src)
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.less.dest));
});
