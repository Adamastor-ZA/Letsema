'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: '4', title: 'Execution plan', dir: path.join(__dirname, 'content', 'ch4'), bookmark: 'ch4' });
