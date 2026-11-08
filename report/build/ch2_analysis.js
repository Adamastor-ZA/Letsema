'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: '2', title: 'Analysis and insights', dir: path.join(__dirname, 'content', 'ch2'), bookmark: 'ch2' });
