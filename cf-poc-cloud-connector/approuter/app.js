const http = require('http');
const express = require('express');
const path = require('path');
const app = express();

app.listen(process.env.PORT || 3000, () => {
    console.log('App running on port 3000');
});