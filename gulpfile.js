// Assuming you already have NodeJS, npm and gulp installed
// and followed instructions at:
// https://www.browsersync.io/docs/gulp/
//
// save this file at <<DJANGO PROJECT ROOT>>
// on your terminal:
// $ cd <<DJANGO PROJECT ROOT>>
// $ gulp

// this will open a browser window with your project
// and reload it whenever a file with the extensions scss,css,html,py,js
// is changed

var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var cache = require('gulp-cache');

// This task can be called from the command line with  `gulp dj-runserver`
gulp.task('dj-runserver', function () {
    const spawn = require('child_process').spawn;
    return spawn('python', ['./manage.py', 'runserver'])
        .stderr.on('data', (data) => {
            console.log(`${data}`);
        });
});


// Clear cache
gulp.task('clearCache', function (done) {
    return cache.clearAll(done);
});


function reload(done) {
    // browserSync.reload();
    browserSync.stream({once: true})
    done();
}


// Tell gulp to executed 'styles' when sass files change, and execute
// a browser reload when any file changes.
gulp.task('watch', function () {
    browserSync.init({
        notify: true,
        proxy: "localhost:8000",
    });

    gulp.watch(['./**/*.{scss,css,html,py,js}'], gulp.series('clearCache', reload));
});

