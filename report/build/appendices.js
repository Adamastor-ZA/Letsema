'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: 'A', title: 'Appendices', dir: path.join(__dirname, 'content', 'appendices'), bookmark: 'app' });
