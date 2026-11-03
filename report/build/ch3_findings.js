'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: '3', title: 'Findings and recommendations', dir: path.join(__dirname, 'content', 'ch3'), bookmark: 'ch3' });
