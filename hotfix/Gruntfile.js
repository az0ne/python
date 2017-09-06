module.exports = function (grunt) {
	grunt.initConfig({  
		pkg: grunt.file.readJSON('package.json'),
 
        /**
         * step 1:
         * 压缩 文件
         */
        uglify: {
			options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %>\n*/\n'//添加banner
            },
            app: {
                files: {
                    // '2016/src/common.js': ['2016/dev/common.js'],
                    // '2016/src/lps4StuQuesAns.js': ['2016/dev/lps4StuQuesAns.js'],
                    // '2016/src/lps4StuQuesAnsdetail.js': ['2016/dev/lps4StuQuesAnsdetail.js'],
                    // '2016/src/newPay.js': ['2016/dev/newPay.js'],
                    // '2016/src/student_info.js': ['2016/dev/student_info.js'],
                    // '2016/src/studyPanel.js': ['2016/dev/studyPanel.js'],
                    // '2016/src/teaOneVOne.js': ['2016/dev/teaOneVOne.js'],
                    // '2016/src/teaOneVOnedetail.js': ['2016/dev/teaOneVOnedetail.js'],
                    // '2016/src/teaOneVOneLine.js': ['2016/dev/teaOneVOneLine.js'],
                    // '2016/src/teaOneVOneList.js': ['2016/dev/teaOneVOneList.js'],
                    // '2016/src/oneToOne.js': ['2016/dev/oneToOne.js'],
                    // '2016/src/otoDetail.js': ['2016/dev/otoDetail.js'],
                    // '2016/src/lps4StuQuesAns_lps3.1.js': ['2016/dev/lps4StuQuesAns_lps3.1.js'],
                    '2016/src/small_course.js': ['2016/dev/small_course.js'],
                    '2016/src/showBigImg.js': ['2016/dev/showBigImg.js'],
                    '2016/lib/video/video_play.js': ['2016/dev/video_play.js'],
                    '2016/src/lessonVideoPlay.js': ['2016/dev/lessonVideoPlay.js'],
                }
            }
        },

        /**
         * step 2:
         * 将这个临时目录删除
         */
        clean: {
            build: ['.build']
        }
	}); 

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-clean');

    // 执行所有插件的任务
    grunt.registerTask('default', ['uglify', 'clean']); 
}