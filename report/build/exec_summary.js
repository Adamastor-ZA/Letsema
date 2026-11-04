'use strict';
const path = require('path');
const { makeChapter } = require('./content_render');
module.exports = makeChapter({ chapter: 'ES', title: 'Executive summary', dir: path.join(__dirname, 'content', 'exec'), bookmark: 'exec' });
