'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: '5', title: 'Monitoring and evaluation framework', dir: path.join(__dirname, 'content', 'ch5'), bookmark: 'ch5' });
