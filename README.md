cnblogs-extractor
=================

This is a script to extract blogs to html from CNBlog's backup file.

## Usage
1. 首先从CNBlog中导出博客备份, 例如导出的文件为example.xml
2. ./cnblogs-extractor -o markdown example.xml，生成octopress使用的markdown文件。不指定-o选项时，默认生成markdown文件。
3. 或者./cnblogs-extractor -o html example.xml，生成html文件。
3. 导出的博客存放在output目录下，每篇博客单独一个html或者markdown文件。
