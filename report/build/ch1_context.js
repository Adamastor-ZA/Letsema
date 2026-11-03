'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: '1', title: 'Context', dir: path.join(__dirname, 'content', 'ch1'), bookmark: 'ch1' });
