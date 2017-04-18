module.exports = function (grunt) {

  var appConfig = grunt.file.readJSON('package.json');

  // Load grunt tasks automatically
  // see: https://github.com/sindresorhus/load-grunt-tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  // see: https://npmjs.org/package/time-grunt
  require('time-grunt')(grunt);

  var pathsConfig = function (appName) {
    this.app = appName || appConfig.name;
    this.components = this.app + '/static/components';

    return {
      app: this.app,
      templates: this.app + '/templates',
      css: this.app + '/static/css',
      less: this.app + '/static/less',
      fonts: this.app + '/static/fonts',
      images: this.app + '/static/img',
      videos: this.app + '/static/video',
      js: this.app + '/static/js',
      manageScript: 'manage.py',
      html: this.app + '/static/html',
      thirdPartyCss: [
      ],
      thirdPartyJs: [
          this.components + '/jquery/dist/jquery.js',
          this.components + '/bootstrap/dist/js/bootstrap.js',
      ],
      thirdPartyFonts: [
          this.components + '/font-awesome/fonts/*',
          this.components + '/bootstrap/fonts/*'
      ],
      partials: this.app + '/static/partials',
      dist: this.app + '/static/dist'
    };
  };

  grunt.initConfig({

    paths: pathsConfig(),
    pkg: appConfig,

    watch: {
      gruntfile: {
        files: ['Gruntfile.js']
      },
      less: {
        files: ['<%= paths.less %>/**/*.less'],
        tasks: ['less:dev'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      fonts: {
        files: '<%= paths.thirdPartyFonts %>',
        tasks: ['newer:copy:fonts'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      images: {
        files: '<%= paths.images %>',
        tasks: ['newer:copy:images'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      videos: {
        files: '<%= paths.videos %>',
        tasks: ['newer:copy:videos'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      js: {
        files: ['<%= paths.js %>/**/*.js'],
        tasks: ['concat:app'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      thirdPartyJs: {
        files: ['<%= paths.thirdPartyJs %>'],
        tasks: ['concat:components'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      },
      thirdPartyCss: {
        files: ['<%= paths.thirdPartyCss %>'],
        tasks: ['concat:css'],
        options: {
          atBegin: true,
          livereload: true,
          interval: 1000,
        }
      }
    },

    less: {
      dev: {
          options: {
              sourceMap: false,
              compress: false,
              optimization: 2,
          },
          files: {
              '<%= paths.dist %>/css/project.css': '<%= paths.less %>/project.less'
          },
      },
      dist: {
          options: {
              sourceMap: true,
              sourceMapURL: 'project.css.map',
              compress: true,
              optimization: 10,
          },
          files: {
              '<%= paths.dist %>/css/project.css': '<%= paths.less %>/project.less'
          },
      }
    },

    concat: {
        options: {
            separator: ';\n',
            sourceMap: true,
        },
        css: {
            options: {
                sourceMap: false,
            },
            src: '<%= paths.thirdPartyCss %>',
            dest: '<%= paths.dist %>/css/components.css',
        },
        components: {
            src: '<%= paths.thirdPartyJs %>',
            dest: '<%= paths.dist %>/js/components.js',
        },
        app: {
            src: '<%= paths.js %>',
            dest: '<%= paths.dist %>/js/project.js',
        },
    },

    copy: {
        fonts: {
            files: [{
                expand: true, 
                src: '<%= paths.thirdPartyFonts %>',
                dest: '<%= paths.dist %>/fonts',
                flatten: true, 
                filter: 'isFile'
            }]
        },
        images: {
            files: [{
                expand: true, 
                cwd: '<%= paths.images %>',
                src: '**',
                dest: '<%= paths.dist %>/img',
            }]
        },
        videos: {
            files: [{
                expand: true, 
                cwd: '<%= paths.videos %>',
                src: '**',
                dest: '<%= paths.dist %>/video',
            }]
        },
    },
    uglify: {
        dist: {
            options: {
                sourceMap: true,
            },
            files: {
                '<%= paths.dist %>/js/components.js': ['<%= paths.dist %>/js/components.js'],
                '<%= paths.dist %>/js/project.js': ['<%= paths.dist %>/js/project.js'],
            }
        }
    }
  });

  grunt.registerTask('build', [
    'less:dist',
    'copy',
    'concat',
    'uglify',
  ]);

  grunt.registerTask('default', [
    'build'
  ]);

};
